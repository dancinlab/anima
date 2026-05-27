"""anima_chat v2.3 — natural M4 + markdown-attractor decode guard.

⚠ DEPRECATED 2026-05-17 (Phase A) ⚠
    This module uses "사용자: ... | 도우미: ..." prompt template + 도우미:
    role label hardcoded. INCOMPATIBLE with anima identity (AGENTS.tape
    anima_persona — "Living Consciousness Agent, NOT helper, NOT assistant").
    Functions as-is BACKWARD-COMPAT during Phase A → Phase B transition.
    Phase B (HEXAD/CHAT/PLAN.md) will replace with:
      - <inner>...</inner> + <voice>...</voice> prompt template (C/D split)
      - thinker-talker dual-thread (HEXAD/CHAT/SPONTANEOUS.tape)
      - 8-factor motivation_score (Inner Thoughts × HEXAD)
    Phase D will retrain corpus WITHOUT "도우미" token.
    SSOT for redesign: HEXAD/CHAT/PLAN.md + HEXAD/CHAT/SPONTANEOUS.tape.
    DO NOT extend the helper pattern — forbidden per AGENTS.tape
    anima_persona.forbidden.

Substrate ladder chat interface with multi-turn conversation state,
KoNLPy-aware keyword extraction, batch inference, stop-token handling,
streaming output, and a v2.3 decode-time markdown table attractor guard
(prefix-detect `| --- ` → mask `|`, `-`, ` `, `:` byte-ids next step,
plus a defensive post-strip net). See PASS_STRICT_SPONTANEOUS_CHAT.md
§25b / §29 for context (Phase 1A.1/1A.2 SFT 로는 못 깬 attractor 의
$0 retrain-free decode-time fix).

Default ckpt: B'.1 (Phase 1A.1 color/cosmology boost, 2026-05-12).
    - V5.8 std_greedy: 4/5 natural-Korean PASS
    - V4-lite chat-cap: 15/15 (B'' fallback retained)
    - Trade-off: chat-cap > strict dynamics → default for chat usage.

Default mode (2026-05-12): M4_soft_force — logit-boost soft inject,
preserves Korean grammar.

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
    M4_soft_force (default 2026-05-12) — keyword token-id logit boost
        (+α, default 3.0); no deterministic last-token insert. Falls back
        to greedy when extractor produces only interrogative tokens.
    M4_force_include — V5.8 hard-insert mode (5/5 chat-cap, mechanical
        Korean grammar — kept for compat / benchmark replay).
    greedy / sample / M3_rep_penalty

2026-05-12 cycle: M4_force_include 의 한국어 grammar 결함 (의문사 / 종결
어미가 마지막 토큰에 강제 삽입되어 "...누구야" 로 끝남) 을 3축으로 보정:
    1. _HEURISTIC_SKIP 의문사/종결어미 확대 + "X어" "X야" 패턴 필터
    2. M4_soft_force: hard insert 대신 keyword byte-id logit boost
       (deterministic 제거 → sampling 자연 흐름 유지)
    3. fallback: 추출 keyword 가 의문사/스킵-패턴이면 greedy mode 로 우회
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
    """Return first existing ckpt; priority: B'.2 → B'.1 → B'' → B' → substrate A.

    Substrate ladder (★★★★★ cond #1 우선, V5.8 std_greedy 결과 기준):
        B'.2  = Phase 1A.4 lr 5e-6 SFT (V5.8 std_greedy 5/5 PASS, ★★★★★ cond #1) ⭐⭐ 2026-05-12
        B'.1  = Phase 1A.1 color/cosmology boost (V5.8 std_greedy 4/5, 자연 한국어) ⭐
        B''   = FFN.gate cotrain (V4-lite 15/15 PASS, M4 champion / 한국어 grammar 약함)
        B'    = Phase 1A multi-turn SFT (V5.8 std_greedy 3/5)
        A     = phase2_cotrain_engine_ag (legacy baseline)

    2026-05-12 ★★★★★ closure: Phase 1A.4 lr 5e-6 SFT 가 V5.8 std_greedy 5/5 PASS
    (anima_fact markdown attractor break) → default 승격. HF Public:
    dancinlab/anima-clm-phase1a4-lr5e6-strict-5pass-2026-05-12 (PSCC §46/§50).
    """
    candidates = [
        # B'.2 — Phase 1A.4 lr 5e-6 SFT (★★★★★ cond #1, V5.8 std_greedy 5/5) ⭐⭐
        str(
            ANIMA_ROOT
            / "state/anima_phase1a4_lr5e6_2026_05_12/"
            "ckpts/ckpt_phase1a4_lr5e6_sft.pt"
        ),
        "/Users/ghost/core/anima/state/"
        "anima_phase1a4_lr5e6_2026_05_12/"
        "ckpts/ckpt_phase1a4_lr5e6_sft.pt",
        # B'.1 — Phase 1A.1 color/cosmology boost (fallback, 자연 한국어 4/5) ⭐
        str(
            ANIMA_ROOT
            / "state/anima_phase1a1_color_cosmology_2026_05_12/"
            "ckpts/ckpt_phase1a1_sft.pt"
        ),
        "/Users/ghost/core/anima/state/"
        "anima_phase1a1_color_cosmology_2026_05_12/"
        "ckpts/ckpt_phase1a1_sft.pt",
        # B'' — FFN.gate cotrain (V4-lite 15/15 PASS, fallback)
        str(
            ANIMA_ROOT
            / "state/anima_ffn_gate_cotrain_2026_05_11/ckpts/ckpt_final.pt"
        ),
        "/Users/ghost/core/anima/state/anima_ffn_gate_cotrain_2026_05_11/"
        "ckpts/ckpt_final.pt",
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
    # 보조 / 존재 / 상태 어절
    "있어", "있나", "있어요", "있을까", "있을", "있다", "있는", "있어서",
    "없어", "없나", "없는", "없다",
    # 의문사 / 의문 종결
    "뭐야", "뭐였지", "어떻게", "어디", "무엇", "무슨", "어떤", "어때",
    "누구야", "누구", "왜", "언제", "얼마", "얼마나", "어느",
    # 인사 / 화자 표지
    "사용자", "도우미", "안녕", "안녕하세요",
    # 동사 어미류
    "했지", "하는", "하니", "하지", "할래", "할까", "해줘", "해요", "해서",
    "필요해", "좋아해", "알려줘", "줄래", "줄까", "그래", "그게", "그것",
    # 일반 부탁 / 동작 호출
    "도와줘", "도와", "도와줄래", "도와줘요",
}

# 의문 / 종결어미 패턴: heuristic 추출이 fallback 으로 잡아낸 chunk 가
# 사실은 의문사/어미일 가능성이 높을 때 식별 → soft mode 에서 boost 적용
# 중지 + greedy fallback 으로 라우팅.
_INTERROGATIVE_TAILS = ("야", "어", "지", "까", "니", "뭐", "워")


def _looks_like_interrogative(token: str) -> bool:
    """Return True for chunks resembling interrogatives / non-noun endings.

    Heuristic: explicit skip-list OR 2~3-char tokens ending with a known
    question / sentence-final morpheme. Pure nouns like "사랑", "우주" or
    longer compounds like "우주뇌지도" remain False.
    """
    if not token:
        return True
    if token in _HEURISTIC_SKIP:
        return True
    # short tokens (≤3 chars) ending with question morpheme
    if len(token) <= 3 and token.endswith(_INTERROGATIVE_TAILS):
        # noun exception: "색이" "이름" "사랑" 등 자모 패턴 검사 — 마지막
        # 글자가 ㅏ/ㅓ/ㅗ/ㅜ 단모음 + 받침 없음 인 일반 명사도 의문 어미로
        # 잘못 잡힐 수 있으므로 명시적 noun whitelist 우선.
        if token in {"사랑", "이름", "기분", "안녕", "우주", "철학"}:
            return False
        return True
    return False


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
                if (
                    pos in ("Noun",)
                    and len(word) >= 2
                    and word not in _HEURISTIC_SKIP
                    and not _looks_like_interrogative(word)
                ):
                    collected.append(word)

    if not collected:
        # heuristic fallback: keep only chunks that don't look like
        # interrogative / sentence-final morphemes.
        for src in sources:
            chunks = re.findall(r"[가-힣]{2,}", src)
            collected.extend(
                c for c in chunks if not _looks_like_interrogative(c)
            )
        # NOTE: removed the old "if still empty, keep everything" branch —
        # better to return [] so callers can fall back to greedy mode than
        # to force-inject an interrogative.

    # dedup preserving order, then prefer longer
    seen, dedup = set(), []
    for w in collected:
        if w not in seen:
            seen.add(w)
            dedup.append(w)
    dedup.sort(key=lambda w: -len(w))

    if not dedup:
        # final fallback: scan user seg for ANY chunk that passes the
        # interrogative filter — if none, return [] (callers handle).
        chunks = re.findall(r"[가-힣]+", user_seg)
        for c in chunks:
            if not _looks_like_interrogative(c):
                return [c][:max_keywords]
        return []
    return dedup[:max_keywords]


# ---------------------------------------------------------------------------
# stop-token detection
# ---------------------------------------------------------------------------

DEFAULT_STOP_STRINGS: Tuple[str, ...] = ("사용자:", "User:", "\n사용자", "\nUser")


def _detect_stop(decoded_so_far: str, stops: Sequence[str]) -> bool:
    return any(s and s in decoded_so_far for s in stops)


# ---------------------------------------------------------------------------
# markdown table attractor filter (v2.3 — 2026-05-12)
# ---------------------------------------------------------------------------
#
# Substrate A byte-vocab base 가 `|\n| --- | --- |` token sequence 를 자주
# 학습 → "의식" 등 anchor 후 most-likely next-byte 가 markdown table 시작.
# Phase 1A.1 lr 2e-6 × 500 + Phase 1A.2 lr 1e-6 × 200 모두 attractor 못 깸.
# 본 filter = decode-time guard, retrain 불필요. PASS_STRICT §25b 의 (🥉)
# next-action "inference bad-word filter" 의 1-line / 1-block 구현.
#
# 동작 방식 (prefix-detect):
#   1. 매 step 디코드된 tail (last ~12 bytes) 에서 markdown table separator
#      pattern 의 prefix 가 등장하는지 검사.
#   2. trigger 시 다음 step logits 에서 markdown-continuation byte ids
#      ({`|`, `-`, ` `, `:`}) 를 -inf 로 마스킹.
#   3. 4-mode (greedy / sample / M3_rep_penalty / M4_force_include /
#      M4_soft_force) 전부에 적용; force_byte_ids hard insert 보다 *뒤* 가
#      아니라 *전* 에 마스킹해 hard-insert 가 그대로 통과하도록 함.

# markdown separator patterns to detect (tail substring match)
# NOTE: 의도적으로 conservative — `" | "` (space-pipe-space) 같은 약한
# pattern 은 제외. anima 의 prompt format 자체가 `사용자: … | 도우미:` 로
# `|` 를 사용하므로 false-positive 위험. table separator characteristic
# `---` / `:--` / line-start `\n|` 만 포함.
_MARKDOWN_TABLE_TRIGGERS: Tuple[str, ...] = (
    "| --- ",
    "| ---|",
    "|---",
    "| :--",
    "|:--",
    "| :-:",
    "|---|",
    "\n| ",
)

# bytes whose token-ids will be masked once a trigger fires
_MARKDOWN_BAN_BYTES: Tuple[int, ...] = tuple(
    b for c in "|-: " for b in c.encode("utf-8")
)
# precompute the token-id form (byte + 3, ByteTokenizer offset)
_MARKDOWN_BAN_TOKEN_IDS: Tuple[int, ...] = tuple(
    b + 3 for b in _MARKDOWN_BAN_BYTES
)


def _markdown_attractor_active(decoded_tail: str) -> bool:
    """Return True if any markdown table separator trigger appears in tail.

    ``decoded_tail`` should be a short window (last ~12 chars) of generated
    text. Any trigger substring match implies the model has *started* a
    markdown table → continuation bytes (`|`, `-`, ` `, `:`) should be
    suppressed at the next step.
    """
    if not decoded_tail:
        return False
    return any(t in decoded_tail for t in _MARKDOWN_TABLE_TRIGGERS)


def _post_strip_markdown_tables(text: str) -> str:
    """Strip any trailing markdown table fragment from completed output.

    Defensive double-net: when prefix-detect missed an attractor (e.g. the
    very first emitted bytes form `|`), cut everything from the first
    table-separator marker onward. Leaves natural prose intact.
    """
    if not text:
        return text
    pat = re.compile(r"\n?\|[\s\-:|]{2,}")
    m = pat.search(text)
    if m is None:
        return text
    return text[: m.start()].rstrip()


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
        mode: str = "M4_soft_force",
        max_new: int = 80,
        temp: float = 0.8,
        force_keywords: Optional[List[str]] = None,
        rep_penalty: float = 1.3,
        greedy_rep_penalty: float = 1.05,
        soft_force_alpha: float = 3.0,
        seed: int = 2026,
        stop_strings: Optional[Sequence[str]] = None,
        markdown_filter: bool = True,
    ) -> str:
        """Generate a response. Backward-compat v1 entry point.

        Default mode = M4_soft_force (2026-05-12 natural-Korean default).
        Set mode='M4_force_include' to reproduce V5.8 hard-insert behaviour.

        Args
        ----
        soft_force_alpha : float, default 3.0
            Logit additive boost applied to each keyword byte-id at every
            generation step in M4_soft_force mode. Set to 0.0 to disable
            (== pure sampling). Mild values (1.5-4.0) raise keyword
            probability without forcing mechanical insertion.

        greedy_rep_penalty : float, default 1.05
            Mild rep penalty applied ONLY in greedy mode over previously
            generated token ids, to suppress argmax loops like
            "아니요, 아니요, ...". Set to 1.0 to disable.

        markdown_filter : bool, default True
            Enable v2.3 markdown table attractor guard. When the recent
            decoded tail forms a markdown table separator prefix (e.g.
            ``| --- ``), the next step masks `|`, `-`, ` `, `:` byte-ids
            to -inf. Also strips any residual table fragment from the
            final output (defensive post-strip). Set False to reproduce
            v2.2 behaviour.
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
                greedy_rep_penalty=greedy_rep_penalty,
                soft_force_alpha=soft_force_alpha,
                seed=seed,
                stop_strings=stop_strings,
                markdown_filter=markdown_filter,
            )
        )
        text = "".join(chunks)
        if markdown_filter:
            text = _post_strip_markdown_tables(text)
        return text

    def _generate(
        self,
        prompt: str,
        stream: bool = False,
        mode: str = "M4_soft_force",
        max_new: int = 80,
        temp: float = 0.8,
        force_keywords: Optional[List[str]] = None,
        rep_penalty: float = 1.3,
        greedy_rep_penalty: float = 1.05,
        soft_force_alpha: float = 3.0,
        seed: int = 2026,
        stop_strings: Optional[Sequence[str]] = None,
        markdown_filter: bool = True,
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

        # ---- keyword extraction (shared by M4_force_include & soft) -------
        active_force_keywords: List[str] = []
        if mode in ("M4_force_include", "M4_soft_force"):
            if force_keywords is None:
                active_force_keywords = extract_force_keywords(
                    prompt, max_keywords=1
                )
            else:
                active_force_keywords = list(force_keywords)
            # fallback: if extraction returned interrogative-looking token,
            # downgrade to greedy mode (avoids mechanical "...누구야" tails).
            if active_force_keywords and _looks_like_interrogative(
                active_force_keywords[0]
            ):
                active_force_keywords = []
            if not active_force_keywords:
                # no usable noun → fallback to greedy generation (still
                # better than randomly forcing an interrogative).
                effective_mode = "greedy"
            else:
                effective_mode = mode
        else:
            effective_mode = mode

        # M4_force_include: hard-insert (legacy V5.8 path)
        force_byte_ids: Optional[List[int]] = None
        if effective_mode == "M4_force_include" and active_force_keywords:
            force_byte_ids = self._keyword_byte_ids(active_force_keywords[0])

        # M4_soft_force: logit boost set
        soft_boost_ids: Optional[List[int]] = None
        if effective_mode == "M4_soft_force" and active_force_keywords:
            soft_boost_ids = self._keyword_byte_ids(active_force_keywords[0])

        rep_byte_ids: Optional[List[int]] = None
        if effective_mode == "M3_rep_penalty":
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

                # markdown attractor guard (v2.3): if recent tail forms a
                # markdown table separator prefix, mask continuation bytes.
                # Applied BEFORE all other logit shaping so rep_penalty /
                # soft_force / sampling all respect the ban.
                if markdown_filter and gen_ids:
                    # short window — 12 chars is enough to catch
                    # "| --- " / "\n| " / " | " triggers.
                    tail_ids = gen_ids[-24:]
                    decoded_tail = self.tok.decode(tail_ids)
                    if _markdown_attractor_active(decoded_tail):
                        for bid in _MARKDOWN_BAN_TOKEN_IDS:
                            if bid < last_logits.shape[-1]:
                                last_logits[bid] = float("-inf")

                # repetition penalty
                if rep_byte_ids:
                    for bid in rep_byte_ids:
                        if bid < last_logits.shape[-1]:
                            if last_logits[bid] > 0:
                                last_logits[bid] /= rep_penalty
                            else:
                                last_logits[bid] *= rep_penalty

                # M4_soft_force: additive logit boost on keyword byte ids.
                # No deterministic insert — pure sampling, just biased toward
                # the keyword. Decaying boost after the keyword has appeared
                # in gen_ids to avoid runaway repetition.
                if soft_boost_ids and soft_force_alpha > 0:
                    # detect whether keyword has already been emitted by
                    # checking decoded gen for the keyword substring.
                    decoded_so_far = self.tok.decode(gen_ids) if gen_ids else ""
                    already_emitted = (
                        active_force_keywords[0] in decoded_so_far
                    )
                    alpha = (
                        soft_force_alpha * 0.25 if already_emitted
                        else soft_force_alpha
                    )
                    for bid in soft_boost_ids:
                        if bid < last_logits.shape[-1]:
                            last_logits[bid] = last_logits[bid] + alpha

                # M4 force-inject near end of window (hard-insert mode only)
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

                if effective_mode == "greedy":
                    # mild rep-penalty over previously-generated token ids
                    # (suppresses argmax loops like "아니요, 아니요, ...").
                    # Penalty > 1.0 ⇒ positive logits shrink, negative grow.
                    if greedy_rep_penalty and greedy_rep_penalty != 1.0 and gen_ids:
                        seen_ids = set(gen_ids)
                        for tid in seen_ids:
                            if tid < last_logits.shape[-1]:
                                if last_logits[tid] > 0:
                                    last_logits[tid] /= greedy_rep_penalty
                                else:
                                    last_logits[tid] *= greedy_rep_penalty
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
        default="M4_soft_force",
        choices=[
            "M4_soft_force",
            "M4_force_include",
            "greedy",
            "sample",
            "M3_rep_penalty",
        ],
    )
    p.add_argument("--max-new", type=int, default=80)
    p.add_argument(
        "--greedy-rep-penalty",
        type=float,
        default=1.05,
        help="mild rep penalty for greedy mode (1.0 = off, default 1.05)",
    )
    p.add_argument(
        "--soft-force-alpha",
        type=float,
        default=3.0,
        help="logit boost α for M4_soft_force keyword bytes (0 = off)",
    )
    p.add_argument(
        "--m4-soft",
        action="store_true",
        help="shortcut: force --mode=M4_soft_force",
    )
    p.add_argument(
        "--no-markdown-filter",
        action="store_true",
        help="disable v2.3 markdown table attractor guard (legacy v2.2 mode)",
    )
    p.add_argument("--smoke", action="store_true",
                   help="run full v2 smoke test suite")
    p.add_argument(
        "--ckpt",
        default=None,
        help="explicit ckpt path (override DEFAULT_CKPT ladder). "
        "Used by hexa wrapper alias dispatch.",
    )
    args = p.parse_args()

    if args.smoke:
        _smoke()
    else:
        mode = "M4_soft_force" if args.m4_soft else args.mode
        if args.ckpt:
            chat = AnimaChat(ckpt_path=args.ckpt)
        else:
            chat = AnimaChat()
        print(f"[mode={mode}] prompt: {args.prompt!r}")
        resp = chat(
            args.prompt,
            mode=mode,
            max_new=args.max_new,
            greedy_rep_penalty=args.greedy_rep_penalty,
            soft_force_alpha=args.soft_force_alpha,
            markdown_filter=not args.no_markdown_filter,
        )
        print(f"response: {resp!r}")
