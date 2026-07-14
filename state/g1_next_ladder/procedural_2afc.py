"""H_9308 · PROCEDURAL-2AFC — is polarity present in the PROCEDURAL layer at all?

Frame (Fable, substrate-first). The dissociation has a name: **blindsight**. The model acts on
polarity (SEEN D-acc 0.9625) but no readout point exposes it (H_9307: 54 combos, positive control
tops out at 0.750 < 0.85). That is procedural (implicit) memory without declarative (explicit)
access — a blindsight patient points correctly but cannot report.

Read-side probes cannot decide M1(the variable was never written) vs M2(written, generation-only):
both predict probe silence. And GEN-DIR is dead on arrival — it is A1's alias (same generation
direction, same minimal pair, same repairs), and A1 failed its own positive control at 3.4σ power
(sign-acc 0.554). So we must ask the PROCEDURAL layer directly: **forced choice.**

KEY FACT (source-checked, cli/evaluate.py:1352 + 1394): `--xbind` already computes exactly this.
    MARGIN = teacher-forced NLL(counterfactual) − NLL(gold)
A positive margin means the model, forced to bet between "긍정." and "부정.", bets on gold. That IS
the behavioural 2AFC. It sidesteps every killer that murders the NLL-on-atom probes: no byte-locality
problem (we score the ANSWER, not the atom), no SOV word-order problem (the answer follows the
context naturally, as in training), no carrier contamination (gold and counterfactual share the
identical seed prefix — the paired difference cancels it).

We do not need a new fire. The numbers are already on disk.

Frozen gate (Fable's mandate — a probe that fails its own positive control decides nothing):
    PC  : SEEN atoms (the ones the model demonstrably masters) must light up — frac(margin>0) high,
          z large. If PC is at chance, the INSTRUMENT is dead and the held-out number is void.
    TEST: held-out atoms. Read ONLY if PC passes.

Verdict:
    PC lights ∧ held-out ≈ chance  -> polarity is absent from the procedural layer too, for
        held-out atoms. Not "we cannot read it" — the model does not BET on it. This is the first
        evidence that survives the read-side graveyard, and it points at M1 (nothing was written),
        not M2 (written but inverted).
    PC lights ∧ held-out > chance  -> procedural polarity EXISTS but is declaratively inaccessible
        = pure blindsight -> the wall is ACCESS, not GROUNDING -> route to the L5 hippocampal store.
    PC at chance                   -> instrument dead, verdict VOID.
"""

import json
import math
import os
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = os.path.expanduser("~/anima-weights/c34")
ARMS = ("main_s7", "main_s11", "shufGT", "N2rep")
MAINS = ("main_s7", "main_s11")

BAR_PC = 0.85          # positive control: SEEN frac(margin>0) must clear this
Z_CRIT = 1.96          # two-sided .05 for the held-out chance test


def load(name):
    p = os.path.join(KEEP, name)
    return json.load(open(p)) if os.path.exists(p) else None


def binom(ms):
    """frac(margin>0), n, z against the 0.5 null, median margin."""
    n = len(ms)
    if not n:
        return float("nan"), 0, float("nan"), float("nan")
    pos = sum(1 for x in ms if x > 0)
    frac = pos / n
    se = math.sqrt(0.25 / n)
    return frac, n, (frac - 0.5) / se, st.median(ms)


def main():
    man = load("n2_eval_manifest.json")
    if not man:
        raise SystemExit("[PENDING] n2_eval_manifest.json 없음")
    held = man["heldout"]

    print("=" * 80)
    print("H_9308 PROCEDURAL-2AFC — 절차층에 극성이 있는가 (강제선택 베팅)")
    print("  margin = teacher-forced NLL(counterfactual) − NLL(gold)  [cli/evaluate.py:1394]")
    print("  = 모델이 '긍정.' vs '부정.' 사이에서 강제로 베팅한 결과 = 행동 2AFC")
    print("  귀무: frac(margin>0) = 0.5 (gold 를 더 선호하지 않음)")
    print("=" * 80)

    # ---- positive control: SEEN atoms (the model demonstrably masters these)
    print(f"\n[PC 양성대조] SEEN 원자 — 계기가 켜지는가 (bar frac ≥ {BAR_PC})")
    pc = {}
    for t in ARMS:
        ev = load(f"eval_seen_c34_{t}.json")
        if not ev:
            print(f"  {t:9s} (SEEN eval 없음)")
            continue
        d = ev["splits"]["heldout"]
        frac, n, z, md = binom([r["margin"] for r in d["rows"]])
        pc[t] = frac
        print(f"  {t:9s} D-acc={d['summary']['d_acc']:.4f} · frac(margin>0)={frac:.4f} "
              f"(n={n} · z={z:+.2f}) · median={md:+.3f}  {'PASS' if frac >= BAR_PC else 'FAIL'}")
    pc_ok = all(pc.get(t, 0) >= BAR_PC for t in MAINS)
    print(f"  => 계기 {'유효 (PC PASS)' if pc_ok else '死 (PC FAIL) — held-out 판정 무효'}")

    # ---- test: held-out atoms
    print(f"\n[TEST] held-out 원자 — 절차층에 극성이 있는가")
    test = {}
    for t in ARMS:
        ev = load(f"eval_c34_{t}.json")
        if not ev:
            continue
        rows = ev["splits"]["heldout"]["rows"]
        if len(rows) != len(held):
            raise SystemExit(f"[FAIL] rows={len(rows)} vs manifest={len(held)} — 정렬 불가")
        all_m = [r["margin"] for r in rows]
        f0_m = [r["margin"] for r, m in zip(rows, held) if m["flip"] == 0]
        fa, na, za, mda = binom(all_m)
        f0, n0, z0, md0 = binom(f0_m)
        test[t] = (fa, za, f0, z0)
        print(f"  {t:9s} 전체 frac={fa:.4f} (n={na} · z={za:+.2f} · med {mda:+.3f})  |  "
              f"flip0 frac={f0:.4f} (n={n0} · z={z0:+.2f} · med {md0:+.3f})")

    # ---- verdict
    print("\n" + "=" * 80)
    if not pc_ok:
        v = ("⛔ INSTRUMENT-DEAD — 양성대조가 서지 않는다. held-out 판정 무효(VOID). "
             "이 계기로는 어떤 결론도 licensing 불가.")
    else:
        chance = all(abs(test[t][1]) < Z_CRIT for t in MAINS if t in test)
        if chance:
            v = ("🧱 PROCEDURAL-ABSENT — 계기는 살아있는데(SEEN z≫0) held-out 은 정확히 우연이다. "
                 "모델은 held-out 극성에 **베팅조차 하지 않는다** ⟹ '못 읽는 것'이 아니라 "
                 "**절차층에도 없다**. read-side 무덤을 통과한 첫 증거이며 **M1(안 썼다)** 을 가리킨다 "
                 "— M2(썼는데 역방향)가 아니다. M2 라면 강제선택에서 gold 쪽으로 기울어야 한다. "
                 "⟹ O 채널(확정-금지 objective)의 전제('틀린 좌항을 예방/교정')는 M1-strict 하에서 "
                 "발사 전 사망 · 남는 것은 **A 채널(접지를 외부 선언저장소로 이관)** 뿐.")
        else:
            v = ("🟢 PROCEDURAL-PRESENT (blindsight 확정) — held-out 절차층에 극성이 **있다**"
                 "(강제선택에서 gold 쪽 유의 편향). 단지 선언적으로 읽히지 않을 뿐 ⟹ 벽은 "
                 "**GROUNDING 이 아니라 ACCESS** ⟹ L5 해마 explicit-store 라우팅이 직격 처방.")
    print("VERDICT:", v)
    print("=" * 80)

    out = {"hypothesis": "H_9308", "bar_pc": BAR_PC,
           "pc_seen_frac": pc, "test_heldout": {k: {"frac_all": v[0], "z_all": v[1],
                                                    "frac_flip0": v[2], "z_flip0": v[3]}
                                                for k, v in test.items()},
           "pc_ok": pc_ok, "verdict": v}
    with open(os.path.join(HERE, "PROCEDURAL_2AFC.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("→ PROCEDURAL_2AFC.json")


if __name__ == "__main__":
    main()
