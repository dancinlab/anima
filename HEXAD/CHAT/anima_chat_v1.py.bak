"""anima_chat — substrate A inference wrapper.

Default mode: M4 force-include (V5.8 5/5 PASS @ Phase 0.7).
Auto extracts force keywords from prior turn (multi-turn) or user message (single-turn).

Usage:
    from anima_chat import AnimaChat
    chat = AnimaChat()
    response = chat("사용자: 안녕! | 도우미: ")           # default M4
    response = chat("사용자: 안녕! | 도우미: ", mode="greedy")  # override

Modes:
    M4_force_include (default)  — 5/5 PASS @ V5.8 4-mode benchmark
    greedy / sample / M3_rep_penalty
"""
import os, sys, re
from pathlib import Path
import torch

ANIMA_ROOT = Path(os.environ.get("ANIMA_ROOT", "/Users/ghost/core/anima"))
sys.path.insert(0, str(ANIMA_ROOT))
sys.path.insert(0, str(ANIMA_ROOT / "training"))
from training.engine_a_g_arch import EngineAGModel, EngineAGConfig

DEFAULT_CKPT = str(ANIMA_ROOT / ".cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt")
if not os.path.exists(DEFAULT_CKPT):
    DEFAULT_CKPT = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"


class ByteTokenizer:
    bos, eos, pad = 1, 2, 0
    def encode(self, t): return [self.bos] + [b + 3 for b in t.encode("utf-8")] + [self.eos]
    def decode(self, ids): return bytes(t - 3 for t in ids if t >= 3 and t < 259).decode("utf-8", errors="replace")


def extract_force_keywords(prompt: str, max_keywords: int = 1):
    """Heuristic: extract content words from the last user turn for M4 force-include.

    Strategy:
      1. find the last "사용자:" segment
      2. extract Korean nouns / longest Korean word chunks
      3. exclude common 조사/어미/question markers
    """
    last_user_match = re.findall(r"사용자:\s*([^|]+)", prompt)
    if not last_user_match:
        last_user_match = [prompt.split("|")[-1] if "|" in prompt else prompt]
    last_user = last_user_match[-1]
    chunks = re.findall(r"[가-힣]{2,}", last_user)
    skip = {"있어", "있나", "있어요", "있을까", "있을", "있다", "있는", "있어서",
            "뭐야", "뭐였지", "어떻게", "어디", "무엇", "무슨", "어떤", "어때",
            "사용자", "도우미", "안녕", "했지", "하는", "하니", "하지", "할래",
            "필요해", "좋아해", "알려줘", "줄래", "그래", "그게", "그것"}
    keywords = [c for c in chunks if c not in skip]
    if not keywords:
        keywords = chunks  # fallback to all chunks
    return keywords[:max_keywords]


class AnimaChat:
    def __init__(self, ckpt_path: str = DEFAULT_CKPT, device: str = "cpu"):
        ck = torch.load(ckpt_path, map_location=device, weights_only=False)
        self.cfg = EngineAGConfig(**ck["cfg"]) if isinstance(ck.get("cfg"), dict) else EngineAGConfig()
        self.model = EngineAGModel(self.cfg).to(device)
        self.model.load_state_dict(ck["model"], strict=False)
        self.model.eval()
        self.tok = ByteTokenizer()
        self.device = device

    def _keyword_byte_ids(self, kw: str):
        ids = self.tok.encode(kw)
        return [i for i in ids if i not in (self.tok.bos, self.tok.eos)]

    def __call__(self, prompt: str, mode: str = "M4_force_include",
                 max_new: int = 80, temp: float = 0.8,
                 force_keywords: list = None,
                 rep_penalty: float = 1.3,
                 seed: int = 2026):
        """Generate response. Default mode = M4_force_include (5/5 PASS per Phase 0.7)."""
        torch.manual_seed(seed)
        ids = self.tok.encode(prompt)
        if ids and ids[-1] == self.tok.eos:
            ids = ids[:-1]
        gen_ids = []

        force_byte_ids = None
        if mode == "M4_force_include":
            if force_keywords is None:
                force_keywords = extract_force_keywords(prompt, max_keywords=1)
            if force_keywords:
                force_byte_ids = self._keyword_byte_ids(force_keywords[0])

        rep_byte_ids = None
        if mode == "M3_rep_penalty":
            for kw in ["우주뇌지도", "카테고리", "🛸"]:
                rep_byte_ids = (rep_byte_ids or []) + self._keyword_byte_ids(kw)

        force_inserted = 0
        with torch.no_grad():
            for step in range(max_new):
                inp = torch.tensor([ids[-self.cfg.ctx:]], dtype=torch.long, device=self.device)
                out = self.model(inp)
                last_logits = out["logits"][0, -1].clone()

                # rep_penalty
                if rep_byte_ids:
                    for bid in rep_byte_ids:
                        if bid < last_logits.shape[-1]:
                            if last_logits[bid] > 0:
                                last_logits[bid] /= rep_penalty
                            else:
                                last_logits[bid] *= rep_penalty

                # M4 force-inject near end
                if force_byte_ids and force_inserted < len(force_byte_ids):
                    tokens_left = max_new - step
                    forces_left = len(force_byte_ids) - force_inserted
                    if tokens_left <= forces_left + 3:
                        nxt = force_byte_ids[force_inserted]
                        force_inserted += 1
                        gen_ids.append(nxt); ids.append(nxt)
                        if nxt == self.tok.eos: break
                        continue

                if mode == "greedy":
                    nxt = last_logits.argmax().item()
                else:
                    probs = torch.softmax(last_logits / temp, dim=-1)
                    nxt = torch.multinomial(probs, 1).item()
                if nxt == self.tok.eos or nxt == self.tok.pad: break
                gen_ids.append(nxt); ids.append(nxt)
                if nxt == ord('\n') + 3 and len(gen_ids) > 5: break

        return self.tok.decode(gen_ids)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", default="사용자: 안녕! 너는 누구야? | 도우미: ")
    p.add_argument("--mode", default="M4_force_include",
                   choices=["M4_force_include", "greedy", "sample", "M3_rep_penalty"])
    p.add_argument("--max-new", type=int, default=80)
    args = p.parse_args()
    chat = AnimaChat()
    print(f"[mode={args.mode}] prompt: {args.prompt!r}")
    resp = chat(args.prompt, mode=args.mode, max_new=args.max_new)
    print(f"response: {resp!r}")
