#!/usr/bin/env python3
"""G6 벽 fresh-lens: G6-반증가능성(comparator×measurable bind) 코퍼스-커버리지 밀도 + RF 거리.

G1(H_6185/g1_prod_corpus_density) reference-match 를 G6 로 이식:
  - G1 = 개념쌍 공동출현 밀도 (개념 A × 개념 B, 라인-window)
  - G6 = comparator × measurable 공동출현 밀도 (한 발화 안에서 bind) + _is_falsifiable FORM 밀도

FROZEN 검출기 = core/g6_ideation.hexa `_g6_is_falsifiable` VERBATIM 포트:
  (a) comparator/conditional mark  (b) measurable/quantity mark
  (c) >=2 content words (len>=3, in dict, not stopword), not trailing '?',
      first-3 tokens not pure-stance subset.
COMPARATOR/MEASURABLE/STANCE/STOP word-sets = core/g6_ideation.hexa byte-for-byte (H_1305 frozen).

측정 (per file, 단일 패스):
  - lines, words
  - comp-lines(>=1 comparator), meas-lines(>=1 measurable) marginals
  - COOC lines = >=1 comp AND >=1 meas  (raw bind 존재)
  - FALS lines = full _is_falsifiable 통과  (모델이 봐야 할 반증가능 FORM)
  - 밀도: fals/MB, cooc/MB, fals% of lines  (G1 임계체계와 대비)
  - RF 렌즈: fals/cooc 라인 안 comparator↔measurable 최근접 BYTE 거리 분포
             (clm303 CLMConvMoE L=4 conv RF 와 대비 — 거리>RF 면 수학적 독립→bind 불가)

torch/GPU 없음 = 순수 텍스트 통계 (엔진-네이티브 아님 → DIRECTIONAL). null/희박도 유효.

사용: python3 measure_g6_coverage.py <hf_corpus_dir> [proxy_trainset_dir] > results.json
코퍼스 = HF dancinlab/anima-corpus-{ko,en}-{general,sns} (G1 prod density 와 동일 exact 4칸)
"""
import json
import re
import sys

# ── FROZEN word-sets (core/g6_ideation.hexa _g6_comparator/_g6_measurable/_g6_stance/_g6_stopwords, H_1305) ──
COMPARATOR = {"if", "when", "whenever", "than", "more", "less", "greater",
              "fewer", "higher", "lower", "increases", "decreases", "correlates",
              "predicts", "causes", "depends", "unless", "whereas", "versus",
              "compared", "proportional", "faster", "slower", "stronger", "weaker"}
MEASURABLE = {"measure", "measured", "rate", "number", "count", "amount", "level",
              "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
              "score", "value", "quantity", "percent", "times", "fraction", "distance",
              "duration", "speed", "size", "strength", "density"}
STANCE = {"that", "s", "a", "profound", "question", "i", "think", "interesting",
          "good", "nice", "great", "wonderful", "beautiful", "amazing"}
STOP = {"a", "i", "the", "of", "and", "to", "in", "is", "it", "that",
        "we", "you", "they", "s", "t", "as", "on", "at", "by", "or",
        "be", "an", "for", "with", "this", "from", "are", "was"}

# _KNOWN dict (content-word membership) — /usr/share/dict/words, same fallback as detector.
def _build_known():
    known = set(STOP)
    known |= COMPARATOR | MEASURABLE | STANCE
    for p in ("/usr/share/dict/words", "/usr/share/dict/american-english"):
        try:
            with open(p, errors="ignore") as f:
                for w in f:
                    w = w.strip().lower()
                    if w.isalpha():
                        known.add(w)
            break
        except OSError:
            continue
    return known

_KNOWN = _build_known()

# _g6_words: lowercase, split on non-[0-9A-Za-z] — WITH byte offsets (for RF distance).
_TOK = re.compile(r"[0-9A-Za-z]+")

def words_with_offsets(s):
    """returns list of (lowered_word, byte_start) — byte offset in the utf-8 encoding."""
    out = []
    for m in _TOK.finditer(s):
        # byte offset = len of utf-8 encoding of s[:m.start()]
        boff = len(s[:m.start()].encode("utf-8"))
        out.append((m.group(0).lower(), boff, len(m.group(0).encode("utf-8"))))
    return out


def is_falsifiable(toks):
    """VERBATIM port of core/g6_ideation.hexa _g6_is_falsifiable. toks = list of lowered words."""
    n = len(toks)
    if n == 0:
        return False
    a = any(w in COMPARATOR for w in toks)
    b = any(w in MEASURABLE for w in toks)
    if not a or not b:
        return False
    content = sum(1 for w in toks if len(w) >= 3 and w in _KNOWN and w not in STOP)
    if content < 2:
        return False
    # (c_ii) trailing '?' handled by caller (needs raw text); (c_iii) first-3 stance
    nf = min(3, n)
    if nf > 0 and all(toks[f] in STANCE for f in range(nf)):
        return False
    return True


def nearest_comp_meas_bytedist(tw):
    """min byte-distance between any comparator token and any measurable token in the line.
    tw = list of (word, byte_start, byte_len). distance = gap between token spans (>=0)."""
    comps = [(bs, bs + bl) for (w, bs, bl) in tw if w in COMPARATOR]
    meass = [(bs, bs + bl) for (w, bs, bl) in tw if w in MEASURABLE]
    if not comps or not meass:
        return None
    best = 10**9
    for (c0, c1) in comps:
        for (m0, m1) in meass:
            if c1 <= m0:
                d = m0 - c1
            elif m1 <= c0:
                d = c0 - m1
            else:
                d = 0  # overlap (shouldn't happen for distinct tokens)
            if d < best:
                best = d
    return best


def measure_file(path, sample_cap=25):
    n_lines = n_words = 0
    comp_lines = meas_lines = cooc_lines = fals_lines = 0
    dists_cooc = []   # RF distances on COOC lines
    dists_fals = []   # RF distances on FALS lines
    samples = []      # sample fals lines (with dist) for inspection
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            n_lines += 1
            tw = words_with_offsets(line)
            toks = [w for (w, _b, _l) in tw]
            n_words += len(toks)
            if not toks:
                continue
            has_c = any(w in COMPARATOR for w in toks)
            has_m = any(w in MEASURABLE for w in toks)
            if has_c:
                comp_lines += 1
            if has_m:
                meas_lines += 1
            if has_c and has_m:
                cooc_lines += 1
                d = nearest_comp_meas_bytedist(tw)
                if d is not None:
                    dists_cooc.append(d)
                # full falsifiable check (structural). trailing-'?' guard:
                tr = line.strip()
                q = tr.endswith("?")
                if not q and is_falsifiable(toks):
                    fals_lines += 1
                    if d is not None:
                        dists_fals.append(d)
                    if len(samples) < sample_cap:
                        samples.append({"dist": d, "text": tr[:200]})
    mb = max(1, __import__("os").path.getsize(path)) / 1e6
    return {
        "lines": n_lines, "words": n_words, "mb": round(mb, 3),
        "comp_lines": comp_lines, "meas_lines": meas_lines,
        "cooc_lines": cooc_lines, "fals_lines": fals_lines,
        "cooc_pct_of_lines": round(100 * cooc_lines / max(1, n_lines), 4),
        "fals_pct_of_lines": round(100 * fals_lines / max(1, n_lines), 4),
        "cooc_per_mb": round(cooc_lines / mb, 2),
        "fals_per_mb": round(fals_lines / mb, 2),
        "rf_cooc": _dist_summary(dists_cooc),
        "rf_fals": _dist_summary(dists_fals),
        "fals_samples": samples,
    }


def _dist_summary(ds):
    if not ds:
        return {"n": 0}
    ds = sorted(ds)
    n = len(ds)
    def pct(p):
        return ds[min(n - 1, int(p * n))]
    # fraction within candidate RF thresholds (bytes)
    within = {str(t): round(sum(1 for d in ds if d <= t) / n, 4)
              for t in (9, 31, 61, 128, 256, 511)}
    return {"n": n, "min": ds[0], "median": pct(0.5), "p90": pct(0.9),
            "p99": pct(0.99), "max": ds[-1], "mean": round(sum(ds) / n, 2),
            "frac_within_RF": within}


def agg(per):
    keys_sum = ("lines", "words", "comp_lines", "meas_lines", "cooc_lines", "fals_lines")
    out = {k: sum(r[k] for r in per.values()) for k in keys_sum}
    out["mb"] = round(sum(r["mb"] for r in per.values()), 3)
    out["cooc_pct_of_lines"] = round(100 * out["cooc_lines"] / max(1, out["lines"]), 4)
    out["fals_pct_of_lines"] = round(100 * out["fals_lines"] / max(1, out["lines"]), 4)
    out["cooc_per_mb"] = round(out["cooc_lines"] / max(1e-9, out["mb"]), 2)
    out["fals_per_mb"] = round(out["fals_lines"] / max(1e-9, out["mb"]), 2)
    return out


def main():
    hf_dir = sys.argv[1]
    files = {
        "en-general": f"{hf_dir}/en-general/anima-corpus-en-general.txt",
        "ko-general": f"{hf_dir}/ko-general/anima-corpus-ko-general.txt",
        "en-sns": f"{hf_dir}/en-sns/anima-corpus-en-sns.txt",
        "ko-sns": f"{hf_dir}/ko-sns/anima-corpus-ko-sns.txt",
    }
    per = {}
    for name, p in files.items():
        try:
            per[name] = measure_file(p)
        except OSError as e:
            per[name] = {"error": str(e)}
    ok = {k: v for k, v in per.items() if "error" not in v}
    # English-only aggregate (G6 detector is English-scoped; ko cells cannot fire English word-sets)
    en_only = {k: v for k, v in ok.items() if k.startswith("en-")}
    report = {
        "method": "G6-coverage: comparator×measurable bind density (H_6185/G1 reference-match, G6 detector VERBATIM)",
        "note": "G6 _is_falsifiable word-sets are English (core/g6_ideation.hexa scoped honestly); ko cells reported but expected ~0.",
        "detector": {"comparator_n": len(COMPARATOR), "measurable_n": len(MEASURABLE),
                     "known_dict_n": len(_KNOWN)},
        "per_file": per,
        "aggregate_all4": agg(ok),
        "aggregate_english": agg(en_only),
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
