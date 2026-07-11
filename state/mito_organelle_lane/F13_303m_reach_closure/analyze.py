#!/usr/bin/env python3
"""H_9285 2차 분석 — run.py 가 남긴 per-item×per-arm 값에서 (추가 계산 0):
  (A) 사전등록 V-gate 판정 (headline detector liveness · 처치채널 가시성)
  (B) POST-HOC: '살아있는' 하위 detector(근접-cue 소비 branch m_B_conj, c0에서 t=+4.4)
      위에서 arm 들이 무엇이라도 움직이는가 — dead-detector 로 KILL 을 찍지 않기 위한 정보 회수.
모든 비교 = control 별 paired-t (blocked-CRN, n=20). max(controls) 금지."""
import json, math
import numpy as np

R = json.load(open("result.json"))
IT, NB = R["items"], R["n_blocks"]
ARMS = ["c0", "c1_k1", "c1_k2", "EXP", "c2_shuf", "SHOCK"]


def blk(arm, f):
    return np.array([np.mean([r["arm"][arm][f] for r in IT if r["block"] == b])
                     for b in range(NB)])


def paired(a, b):
    d = a - b
    sem = d.std(ddof=1) / math.sqrt(len(d))
    t = float(d.mean() / sem) if sem > 0 else 0.0
    from math import erf
    return {"delta": float(d.mean()), "sem": float(sem), "t": t,
            "p": float(2 * (1 - 0.5 * (1 + erf(abs(t) / math.sqrt(2))))),
            "ci95": [float(d.mean() - 2.093 * sem), float(d.mean() + 2.093 * sem)]}


out = {"headline_prereg": "m_conj = min(m_A_conj, m_B_conj)  (held-out 2-cue 결합 마진)"}

# ── (A) V-gates on the pre-registered headline ──
c0c = blk("c0", "m_conj")
out["vgate"] = {
    "V_liveness_single_cue_ceiling": {
        "ceiling_min(sA,sB)": paired(blk("c0", "ceiling"), np.zeros(NB)),
        "sA_distal_cue_alone": paired(blk("c0", "s_A"), np.zeros(NB)),
        "sB_proximal_cue_alone": paired(blk("c0", "s_B"), np.zeros(NB)),
        "verdict": "FAIL — headline 의 두 branch 중 distal(A) branch 가 CONTROL 조건에서 이미 죽음"},
    "V_channel_visibility_on_headline": {
        "SHOCK_vs_c0": paired(blk("SHOCK", "m_conj"), c0c),
        "k1_vs_c0": paired(blk("c1_k1", "m_conj"), c0c),
        "verdict": "FAIL — router mixing 을 완전 파괴(SHOCK=균등)해도 headline 이 안 움직임"},
}

# ── (B) POST-HOC: live sub-detector (proximal branch) ──
live = {}
lb = blk("c0", "m_B_conj")
live["c0_level"] = paired(lb, np.zeros(NB))
for a in ARMS:
    if a == "c0":
        continue
    live[a + "_vs_c0"] = paired(blk(a, "m_B_conj"), lb)
# pooled-mean control (금지: max(controls))
pool = np.mean([blk(c, "m_B_conj") for c in ["c0", "c1_k1", "c1_k2", "c2_shuf"]], axis=0)
live["EXP_vs_pooled_controls"] = paired(blk("EXP", "m_B_conj"), pool)
sd = float((blk("EXP", "m_B_conj") - lb).std(ddof=1))
live["MDE_alpha05_n20"] = 2.093 * sd / math.sqrt(NB)
live["dynamic_range_c0_level"] = float(lb.mean())
live["mde_ok_vs_c0_level"] = bool(live["MDE_alpha05_n20"] < abs(lb.mean()))
out["posthoc_live_branch_m_B_conj"] = live

# ── arm table on both ──
out["arm_table"] = {a: {"m_conj": float(blk(a, "m_conj").mean()),
                        "m_conj_sem": float(blk(a, "m_conj").std(ddof=1) / math.sqrt(NB)),
                        "m_B_conj_live": float(blk(a, "m_B_conj").mean()),
                        "m_B_conj_sem": float(blk(a, "m_B_conj").std(ddof=1) / math.sqrt(NB)),
                        "m_A_conj_distal": float(blk(a, "m_A_conj").mean()),
                        "dacc": float(blk(a, "dacc").mean())} for a in ARMS}
out["prereg_paired"] = R["paired_vs_controls"]
out["mde_prereg"] = R["mde"]
out["info_channel"] = R["info_channel"]
out["theta"] = R["theta"]
out["c1_best_constant"] = R["c1_best_constant"]
json.dump(out, open("analysis.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
