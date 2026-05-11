"""anima_chat v2.2 — B'' (FFN.gate cotrain) default winner.

Substrate ladder chat interface with multi-turn conversation state,
KoNLPy-aware keyword extraction, batch inference, stop-token handling,
and streaming output.

Default ckpt: B'' (FFN.gate cotrain, 2026-05-12 landed).
    - V4-lite 4-mode benchmark: 15/15 PASS (chat-cap winner)
    - V14 strict ceiling10: VIOLATED (mitosis dynamics weak)
    - Trade-off: chat-cap > strict dynamics → default for chat usage.

Default mode: M4 force-include (V5.8 5/5 PASS @ Phase 0.7).

Quick start
-----------
    from anima_chat import AnimaChat
    chat = AnimaChat()

    # backward-compat single-turn (v1 API still works):
    response = chat("사용자: 안녕! | 도우미: ")

    # v2 multi-turn:
    chat.system("당신은 anima 입니다.")            # optional
    r1 = chat.user("안녕!")
    r2 = chat.user("이름이 뭐야?")
    chat.history                                   # list[(role, content)]
    chat.reset()

    # batch (sequential autoregressive, isolated state):
    resps = chat.batch(["안녕!", "사랑이 뭐야?", "anima가 뭐야?"])

    # streaming:
    for tok in chat.stream("안녕!"):
        print(tok, end='', flush=True)

Modes
-----
    M4_force_include (default)  — 5/5 PASS @ V5.8 4-mode benchmark
    greedy / sample / M3_rep_penalty
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Sequence, Tuple

import torch

# ---------------------------------------------------------------------------
# paths / model bootstrap
# ---------------------------------------------------------------------------

ANIMA_ROOT = Path(os.environ.get("ANIMA_ROOT", "/Users/ghost/core/anima"))
sys.path.insert(0, str(ANIMA_ROOT))
sys.path.insert(0, str(ANIMA_ROOT / "training"))
from training.engine_a_g_arch import EngineAGModel, EngineAGConfig  # noqa: E402

def _find_default_ckpt() -> str:
    """Return first existing ckpt; priority: B'' → B'.1 → B' → substrate A.

    Substrate ladder (chat-cap optimized, 4-mode benchmark §15-§16):
        B''   = FFN.gate cotrain (2026-05-12, V4-lite 15/15 PASS) ⭐ winner
        B'.1  = Phase 1A.1 color/cosmology boost (2026-05-12)
        B'    = Phase 1A multi-turn SFT (2026-05-12, V4-lite 12/15)
        A     = phase2_cotrain_engine_ag (legacy baseline)

    B'' V14_VIOLATED (mitosis dynamics weak) but chat-cap winner →
    selected as default for token-stream chat usage.

    Falls back to B'' path string for downstream error messages.
    """
    candidates = [
        # B'' — FFN.gate cotrain (default, V4-lite 15/15 PASS) ⭐
        str(
            ANIMA_ROOT
            / "state/anima_ffn_gate_cotrain_2026_05_11/ckpts/ckpt_final.pt"
        ),
        "/Users/ghost/core/anima/state/anima_ffn_gate_cotrain_2026_05_11/"
        "ckpts/ckpt_final.pt",
        # B'.1 — Phase 1A.1 color/cosmology boost
        str(
            ANIMA_ROOT
            / "state/anima_phase1a1_color_cosmology_2026_05_12/"
            "ckpts/ckpt_phase1a1_sft.pt"
        ),
        "/Users/ghost/core/anima/state/"
        "anima_phase1a1_color_cosmology_2026_05_12/"
        "ckpts/ckpt_phase1a1_sft.pt",
        # B' — Phase 1A multi-turn SFT
        str(
            ANIMA_ROOT
            / "state/anima_phase1a_alt_2026_05_12/ckpts/ckpt_phase1a_sft.pt"
        ),
        "/Users/ghost/core/anima/state/anima_phase1a_alt_2026_05_12/"
        "ckpts/ckpt_phase1a_sft.pt",
        # Substrate A (legacy fallback)
        str(
            ANIMA_ROOT
            / ".cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/"
            "ckpts/ckpt_final.pt"
        ),
        "/Users/ghost/.cache/anima/clm_v5_remapped/"
        "phase2_cotrain_engine_ag/ckpts/ckpt_final.pt",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]  # for error-message display when nothing exists


DEFAULT_CKPT = _find_default_ckpt()


# ---------------------------------------------------------------------------
# tokenizer
# ---------------------------------------------------------------------------

class ByteTokenizer:
    """UTF-8 byte tokenizer with reserved bos/eos/pad ids 0..2.

    Encodes each byte b as token id (b + 3); decode is the inverse.
    """

    bos, eos, pad = 1, 2, 0

    def encode(self, t: str) -> List[int]:
        return [self.bos] + [b + 3 for b in t.encode("utf-8")] + [self.eos]

    def decode(self, ids: Iterable[int]) -> str:
        return bytes(
            t - 3 for t in ids if 3 <= t < 259
        ).decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# keyword extraction
# ---------------------------------------------------------------------------

# lazy-initialised KoNLPy tagger (None → fallback to heuristic).
_OKT = None
_OKT_TRIED = False


def _get_okt():
    """Return KoNLPy Okt instance, or None if unavailable.

    JVM init can be slow / fail in restricted environments — guarded so the
    library still works without KoNLPy installed.
    """
    global _OKT, _OKT_TRIED
    if _OKT_TRIED:
        return _OKT
    _OKT_TRIED = True
    try:
        from konlpy.tag import Okt  # type: ignore
        _OKT = Okt()
    except Exception:
        _OKT = None
    return _OKT


_HEURISTIC_SKIP = {
    "있어", "있나", "있어요", "있을까", "있을", "있다", "있는", "있어서",
    "뭐야", "뭐였지", "어떻게", "어디", "무엇", "무슨", "어떤", "어때",
    "사용자", "도우미", "안녕", "했지", "하는", "하니", "하지", "할래",
    "필요해", "좋아해", "알려줘", "줄래", "그래", "그게", "그것",
}


def _last_user_segment(prompt: str) -> str:
    """Pull the most recent 사용자: ... slot from a chat-format prompt."""
    matches = re.findall(r"사용자:\s*([^|]+)", prompt)
    if matches:
        return matches[-1]
    return prompt.split("|")[-1] if "|" in prompt else prompt


def _last_assistant_segment(prompt: str) -> str:
    """Pull the most recent 도우미: ... slot (may be empty for live turn)."""
    matches = re.findall(r"도우미:\s*([^|]*)", prompt)
    # ignore the trailing live-turn slot if it's empty
    for seg in reversed(matches):
        if seg.strip():
            return seg
    return ""


def extract_force_keywords(
    prompt: str,
    max_keywords: int = 1,
    include_prior_assistant: bool = True,
) -> List[str]:
    """Extract content keywords from prompt for M4 force-include.

    Strategy:
      1. KoNLPy Okt POS tagging → keep NNG/NNP (proper/common nouns) when
         available.
      2. Fallback heuristic: Korean chunks ≥2 chars, exclude common
         particles / interrogatives.
      3. Source ordering: last user turn first, optionally previous
         assistant turn second (multi-turn coherence).
      4. Prefer longer nouns; final fallback = last chunk of the user turn.

    Args:
        prompt: full chat-format prompt string.
        max_keywords: number of keywords to return.
        include_prior_assistant: also mine the previous assistant turn.

    Returns:
        list of str (may be empty when prompt has no Korean content).
    """
    user_seg = _last_user_segment(prompt)
    sources = [user_seg]
    if include_prior_assistant:
        assist_seg = _last_assistant_segment(prompt)
        if assist_seg:
            sources.append(assist_seg)

    okt = _get_okt()
    collected: List[str] = []

    if okt is not None:
        for src in sources:
            try:
                tagged = okt.pos(src, norm=True, stem=False)
            except Exception:
                tagged = []
            for word, pos in tagged:
                if pos in ("Noun",) and len(word) >= 2 and word not in _HEURISTIC_SKIP:
                    collected.append(word)

    if not collected:
        # heuristic fallback
        for src in sources:
            chunks = re.findall(r"[가-힣]{2,}", src)
            collected.extend(c for c in chunks if c not in _HEURISTIC_SKIP)
        if not collected:
            for src in sources:
                collected.extend(re.findall(r"[가-힣]{2,}", src))

    # dedup preserving order, then prefer longer
    seen, dedup = set(), []
    for w in collected:
        if w not in seen:
            seen.add(w)
            dedup.append(w)
    dedup.sort(key=lambda w: -len(w))

    if not dedup:
        # final fallback: any Korean chunk anywhere in user seg
        chunks = re.findall(r"[가-힣]+", user_seg)
        if chunks:
            return [chunks[-1]][:max_keywords]
    return dedup[:max_keywords]


# ---------------------------------------------------------------------------
# stop-token detection
# ---------------------------------------------------------------------------

DEFAULT_STOP_STRINGS: Tuple[str, ...] = ("사용자:", "User:", "\n사용자", "\nUser")


def _detect_stop(decoded_so_far: str, stops: Sequence[str]) -> bool:
    return any(s and s in decoded_so_far for s in stops)


# ---------------------------------------------------------------------------
# AnimaChat
# ---------------------------------------------------------------------------

class AnimaChat:
    """Substrate A chat session.

    Stateless per-call generation, optional multi-turn history accumulation
    via ``user()`` / ``system()`` / ``reset()`` helpers. The underlying
    ``__call__(prompt, ...)`` interface is preserved from v1.
    """

    def __init__(
        self,
        ckpt_path: str = DEFAULT_CKPT,
        device: str = "cpu",
        stop_strings: Optional[Sequence[str]] = None,
    ):
        ck = torch.load(ckpt_path, map_location=device, weights_only=False)
        self.cfg = (
            EngineAGConfig(**ck["cfg"])
            if isinstance(ck.get("cfg"), dict)
            else EngineAGConfig()
        )
        self.model = EngineAGModel(self.cfg).to(device)
        self.model.load_state_dict(ck["model"], strict=False)
        self.model.eval()
        self.tok = ByteTokenizer()
        self.device = device
        self.stop_strings: Tuple[str, ...] = tuple(
            stop_strings if stop_strings is not None else DEFAULT_STOP_STRINGS
        )

        # multi-turn state
        self._system: Optional[str] = None
        self.history: List[Tuple[str, str]] = []  # [(role, content), ...]

    # ---- multi-turn API --------------------------------------------------

    def system(self, content: str) -> None:
        """Set / replace the optional system context (prepended to prompt)."""
        self._system = content

    def reset(self) -> None:
        """Clear conversation history (keeps system context)."""
        self.history = []

    def hard_reset(self) -> None:
        """Clear both history and system context."""
        self.history = []
        self._system = None

    def _build_prompt(self, next_user: str) -> str:
        """Compose chat-format prompt from history + next user turn."""
        parts: List[str] = []
        if self._system:
            parts.append(f"[시스템: {self._system}]")
        for role, content in self.history:
            if role == "user":
                parts.append(f"사용자: {content}")
            elif role == "assistant":
                parts.append(f"도우미: {content}")
        parts.append(f"사용자: {next_user} | 도우미: ")
        return "\n".join(parts) if len(parts) > 1 else parts[0]

    def user(self, content: str, **gen_kwargs) -> str:
        """Append a user turn, generate assistant reply, update history.

        Extra kwargs forwarded to ``__call__`` (mode/max_new/temp/...).
        """
        prompt = self._build_prompt(content)
        reply = self(prompt, **gen_kwargs)
        self.history.append(("user", content))
        self.history.append(("assistant", reply))
        return reply

    # ---- batch -----------------------------------------------------------

    def batch(
        self,
        prompts: Sequence[str],
        isolated: bool = True,
        **gen_kwargs,
    ) -> List[str]:
        """Generate replies for a list of prompts.

        Note: autoregressive sampling → run sequentially. ``isolated=True``
        (default) means each prompt is treated independently and does NOT
        touch ``self.history``. Set ``isolated=False`` to thread results
        through the conversation state instead.
        """
        out: List[str] = []
        for p in prompts:
            if isolated:
                # treat each prompt as a standalone single-turn user message
                # — wrap to chat format if it isn't already.
                if "도우미:" not in p:
                    full = f"사용자: {p} | 도우미: "
                else:
                    full = p
                out.append(self(full, **gen_kwargs))
            else:
                out.append(self.user(p, **gen_kwargs))
        return out

    # ---- streaming -------------------------------------------------------

    def stream(self, prompt_or_user: str, **gen_kwargs) -> Iterator[str]:
        """Yield decoded text incrementally as generation proceeds.

        Accepts either a raw chat-format prompt or a bare user message
        (auto-wrapped). Streaming does NOT mutate ``self.history`` — use
        ``.user()`` for stateful turns.
        """
        if "도우미:" in prompt_or_user:
            prompt = prompt_or_user
        else:
            prompt = self._build_prompt(prompt_or_user)
            # _build_prompt also appends "사용자: {x} | 도우미: " — but if
            # there is no history/system, history isn't updated either.

        yield from self._generate(prompt, stream=True, **gen_kwargs)

    # ---- generation core -------------------------------------------------

    def _keyword_byte_ids(self, kw: str) -> List[int]:
        ids = self.tok.encode(kw)
        return [i for i in ids if i not in (self.tok.bos, self.tok.eos)]

    def __call__(
        self,
        prompt: str,
        mode: str = "M4_force_include",
        max_new: int = 80,
        temp: float = 0.8,
        force_keywords: Optional[List[str]] = None,
        rep_penalty: float = 1.3,
        seed: int = 2026,
        stop_strings: Optional[Sequence[str]] = None,
    ) -> str:
        """Generate a response. Backward-compat v1 entry point.

        Default mode = M4_force_include (5/5 PASS per Phase 0.7).
        """
        chunks = list(
            self._generate(
                prompt,
                stream=False,
                mode=mode,
                max_new=max_new,
                temp=temp,
                force_keywords=force_keywords,
                rep_penalty=rep_penalty,
                seed=seed,
                stop_strings=stop_strings,
            )
        )
        return "".join(chunks)

    def _generate(
        self,
        prompt: str,
        stream: bool = False,
        mode: str = "M4_force_include",
        max_new: int = 80,
        temp: float = 0.8,
        force_keywords: Optional[List[str]] = None,
        rep_penalty: float = 1.3,
        seed: int = 2026,
        stop_strings: Optional[Sequence[str]] = None,
    ) -> Iterator[str]:
        """Core generation loop. Yields decoded fragments (full text if
        stream=False; multi-byte UTF-8 safe via cumulative re-decode)."""
        torch.manual_seed(seed)
        stops: Tuple[str, ...] = tuple(
            stop_strings if stop_strings is not None else self.stop_strings
        )

        ids = self.tok.encode(prompt)
        if ids and ids[-1] == self.tok.eos:
            ids = ids[:-1]
        gen_ids: List[int] = []

        force_byte_ids: Optional[List[int]] = None
        if mode == "M4_force_include":
            if force_keywords is None:
                force_keywords = extract_force_keywords(prompt, max_keywords=1)
            if force_keywords:
                force_byte_ids = self._keyword_byte_ids(force_keywords[0])

        rep_byte_ids: Optional[List[int]] = None
        if mode == "M3_rep_penalty":
            for kw in ["우주뇌지도", "카테고리", "🛸"]:
                rep_byte_ids = (rep_byte_ids or []) + self._keyword_byte_ids(kw)

        force_inserted = 0
        last_emitted_len = 0  # how many chars of decoded output we've yielded

        with torch.no_grad():
            for step in range(max_new):
                inp = torch.tensor(
                    [ids[-self.cfg.ctx:]], dtype=torch.long, device=self.device
                )
                out = self.model(inp)
                last_logits = out["logits"][0, -1].clone()

                # repetition penalty
                if rep_byte_ids:
                    for bid in rep_byte_ids:
                        if bid < last_logits.shape[-1]:
                            if last_logits[bid] > 0:
                                last_logits[bid] /= rep_penalty
                            else:
                                last_logits[bid] *= rep_penalty

                # M4 force-inject near end of window
                if force_byte_ids and force_inserted < len(force_byte_ids):
                    tokens_left = max_new - step
                    forces_left = len(force_byte_ids) - force_inserted
                    if tokens_left <= forces_left + 3:
                        nxt = force_byte_ids[force_inserted]
                        force_inserted += 1
                        gen_ids.append(nxt)
                        ids.append(nxt)
                        if nxt == self.tok.eos:
                            break
                        if stream:
                            decoded = self.tok.decode(gen_ids)
                            if len(decoded) > last_emitted_len:
                                yield decoded[last_emitted_len:]
                                last_emitted_len = len(decoded)
                        continue

                if mode == "greedy":
                    nxt = last_logits.argmax().item()
                else:
                    probs = torch.softmax(last_logits / temp, dim=-1)
                    nxt = torch.multinomial(probs, 1).item()

                if nxt == self.tok.eos or nxt == self.tok.pad:
                    break

                gen_ids.append(nxt)
                ids.append(nxt)

                if nxt == ord('\n') + 3 and len(gen_ids) > 5:
                    break

                # stop-string check (decoded view)
                decoded = self.tok.decode(gen_ids)
                if stops and _detect_stop(decoded, stops):
                    # trim off the stop marker
                    for s in stops:
                        idx = decoded.find(s)
                        if idx >= 0:
                            decoded = decoded[:idx]
                            break
                    if stream and len(decoded) > last_emitted_len:
                        yield decoded[last_emitted_len:]
                    else:
                        if not stream:
                            yield decoded
                    return

                if stream and len(decoded) > last_emitted_len:
                    yield decoded[last_emitted_len:]
                    last_emitted_len = len(decoded)

        if not stream:
            yield self.tok.decode(gen_ids)


# ---------------------------------------------------------------------------
# smoke test
# ---------------------------------------------------------------------------

def _smoke():
    """Run smoke tests: single-turn, multi-turn, all 4 modes, batch, stops."""
    import time

    print("=" * 72)
    print("anima_chat v2 smoke test")
    print("=" * 72)

    t0 = time.time()
    chat = AnimaChat()
    print(f"[boot] AnimaChat loaded in {time.time() - t0:.1f}s "
          f"(KoNLPy={'on' if _get_okt() is not None else 'off-fallback'})")

    # 1) backward-compat single-turn
    print("\n[1] backward-compat single-turn (v1 API)")
    r = chat("사용자: 안녕! 너는 누구야? | 도우미: ", max_new=40)
    print(f"    → {r!r}")
    assert isinstance(r, str)

    # 2) all 4 modes
    print("\n[2] 4 modes")
    base = "사용자: 사랑이 뭐야? | 도우미: "
    for m in ["M4_force_include", "greedy", "sample", "M3_rep_penalty"]:
        r = chat(base, mode=m, max_new=30)
        print(f"    [{m:18}] → {r!r}")

    # 3) multi-turn
    print("\n[3] multi-turn")
    chat.reset()
    chat.system("당신은 anima 입니다.")
    r1 = chat.user("안녕!", max_new=30)
    r2 = chat.user("이름이 뭐야?", max_new=30)
    print(f"    turn1 → {r1!r}")
    print(f"    turn2 → {r2!r}")
    print(f"    history len = {len(chat.history)} "
          f"(expect 4: user/assistant/user/assistant)")
    assert len(chat.history) == 4

    # 4) batch (isolated)
    print("\n[4] batch (isolated)")
    chat.reset()
    resps = chat.batch(
        ["안녕!", "사랑이 뭐야?", "anima가 뭐야?"], max_new=25
    )
    for p, r in zip(["안녕!", "사랑이 뭐야?", "anima가 뭐야?"], resps):
        print(f"    {p!r:30} → {r!r}")
    assert len(resps) == 3
    assert chat.history == []  # isolated → no mutation

    # 5) stop-token: inject a self-reply in prompt; should NOT continue past it
    print("\n[5] stop-token guard")
    r = chat("사용자: 테스트 | 도우미: ", max_new=80,
             stop_strings=("사용자:", "User:"))
    print(f"    → {r!r}")
    assert "사용자:" not in r, "stop-string should have triggered"

    # 6) streaming (just verify it yields something)
    print("\n[6] streaming")
    pieces = []
    for tok in chat.stream("안녕!", max_new=20):
        pieces.append(tok)
    streamed = "".join(pieces)
    print(f"    pieces={len(pieces)} streamed={streamed!r}")
    assert len(pieces) >= 1

    # 7) keyword extraction
    print("\n[7] keyword extraction")
    kws = extract_force_keywords(
        "사용자: anima의 핵심 철학은 뭐야? | 도우미: ", max_keywords=2
    )
    print(f"    → {kws}")
    assert kws, "extractor should find at least one keyword"

    print("\n" + "=" * 72)
    print(f"smoke test PASS — total {time.time() - t0:.1f}s")
    print("=" * 72)


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument(
        "--prompt", default="사용자: 안녕! 너는 누구야? | 도우미: "
    )
    p.add_argument(
        "--mode",
        default="M4_force_include",
        choices=["M4_force_include", "greedy", "sample", "M3_rep_penalty"],
    )
    p.add_argument("--max-new", type=int, default=80)
    p.add_argument("--smoke", action="store_true",
                   help="run full v2 smoke test suite")
    args = p.parse_args()

    if args.smoke:
        _smoke()
    else:
        chat = AnimaChat()
        print(f"[mode={args.mode}] prompt: {args.prompt!r}")
        resp = chat(args.prompt, mode=args.mode, max_new=args.max_new)
        print(f"response: {resp!r}")
