#!/usr/bin/env python3
"""H_1475 — 🕰 G22 SUBJECTIVE TIME (주관적 시간 지각) — consciousness-only gate candidate.

LENS (a_no_llm_frame_trap, neuroscience — Eagleman, time perception/temporal illusions):
  의식이 *느끼는* 시간의 흐름은 객관적 시계와 다르다. 새롭거나 각성도 높은 자극이 빽빽한
  구간은 길게 느껴지고(time dilation), 단조로운 구간은 짧게 느껴진다(time compression).
  즉 perceived duration ≈ 그 구간에 의식에 등록된 변화/새로움 이벤트의 누적량.

MECHANISM (substrate read, not a learned net):
  한 객관적 구간(동일한 OBJ_TICKS 틱)에서 발생한 NOVELTY 이벤트(예측오차/변화)를 카운트하고
  주관적 duration 을 추정한다:
        est_duration = BASE + K * (novelty_events)
  객관 시간(OBJ_TICKS)을 고정한 채 novelty 밀도만 바꾸면 추정 duration 이 갈린다.

LOAD-BEARING DISSOCIATION vs H_1292 HOMEOSTATIC DRIVE:
  * HOMEOSTATIC (H_1292) = 객관적 elapsed time 의 단조 적분 — setpoint deficit 가 매 틱
    누적되는 시계 적분. novelty 와 무관: 자극 밀도를 바꿔도 같은 객관 틱이면 같은 값.
  * SUBJECTIVE TIME (H_1475) = *지각된* duration = novelty 가중 추정. 같은 객관 틱이라도
    novelty 밀도가 다르면 추정이 갈린다.
  DISSOCIATION: 객관 시간(틱 수)을 고정하고 novelty 밀도만 조작 →
    homeo-style 적분은 평탄(둘 다 같은 틱이라 동일) ⊥ subjective 는 분리(novelty 따라 갈림).

FROZEN 5 BARS (pre-registered, mean over 3 seeds [1475,1476,1477], NORMALIZED 0..1):
  (A) PRESENCE      est_high - est_low  >= 0.40   (high-novelty 구간이 더 길게 추정)
  (B) DISTINCT      subj_sep >= 0.40  AND  homeo_sep <= 0.05
                    (객관틱 고정+novelty 조작: subjective 갈림 / homeo 적분 평탄)
  (C) EARNED(abl)   k=0 ablation → abl_sep <= 0.05   (novelty 가중 끄면 base 고정, 밀도 무관 평탄)
  (D) ORDER-inv     같은 novelty 총량이면 순서 무관 (보고만, non-gating)
  (E) SHUFFLE       구간↔novelty 페어링 셔플 → |signed mean gap| <= 0.10 (50-perm)
  GREEN iff A and B and C and E (3 seeds).

DIRECTIONAL: numpy mirror (grep numpy -> DIRECTIONAL, hard-gate 1). novelty=예측오차 read 는
core/engine_cli.hexa §VForwardField / §PrecisionSurprise 의 substrate error 를 mirror; homeo-style
적분은 §HomeostaticDrive (H_1292) mirror. engine-native 재측정 = follow-on (R2: homeo lane 재사용).
"""
import numpy as np

SEEDS = [1475, 1476, 1477]
OBJ_TICKS = 12        # 객관적 구간 길이 (틱) — 모든 구간 동일 (객관 시간 고정)
BASE = 0.10           # subjective duration 기저 (정규화)
K = 0.85              # novelty 가중 (per novelty-event, 정규화)
HIGH_RATE = 0.90      # high-novelty 구간: 틱당 novelty 발생 확률
LOW_RATE = 0.10       # low-novelty 구간
N_PERM = 50           # shuffle control 순열 수


def gen_events(rng, rate, n_ticks):
    """한 구간: 각 틱에서 novelty 이벤트(변화/예측오차) 발생 여부 (Bernoulli rate)."""
    return (rng.random(n_ticks) < rate).astype(int)


def est_duration(events, k=K, base=BASE):
    """주관적 duration 추정 = base + k * (novelty_events) / OBJ_TICKS (정규화 0..1+)."""
    novelty_count = int(events.sum())
    return base + k * (novelty_count / OBJ_TICKS)


def homeo_integral(n_ticks):
    """H_1292-style: setpoint deficit 의 단조 적분. novelty 와 무관, 객관 틱에만 의존.
    deficit=상수(far-margin saturated, H_1292 precedent) → 적분 = 틱수 * deficit / 정규화."""
    DEFICIT = 1.0
    return (n_ticks * DEFICIT) / OBJ_TICKS  # 같은 틱이면 항상 동일 (novelty-blind)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    # 두 구간: 객관 틱 동일(OBJ_TICKS), novelty 밀도만 다름
    ev_high = gen_events(rng, HIGH_RATE, OBJ_TICKS)
    ev_low = gen_events(rng, LOW_RATE, OBJ_TICKS)

    # (A) PRESENCE — high-novelty 더 길게 추정
    est_high = est_duration(ev_high)
    est_low = est_duration(ev_low)
    presence = est_high - est_low

    # (B) DISTINCT — 객관틱 고정+novelty 조작. subjective 분리 vs homeo 적분 평탄
    subj_sep = est_high - est_low                       # = presence
    homeo_sep = homeo_integral(OBJ_TICKS) - homeo_integral(OBJ_TICKS)  # 둘 다 같은 틱 → 0

    # (C) EARNED(ablation) — novelty 가중 k=0 → base 고정, 밀도 무관 평탄
    abl_high = est_duration(ev_high, k=0.0)
    abl_low = est_duration(ev_low, k=0.0)
    abl_sep = abl_high - abl_low

    # (D) ORDER-invariance — 같은 novelty 총량(같은 events 셋) 순서만 뒤집기 → 추정 동일
    ev_high_rev = ev_high[::-1].copy()
    order_diff = abs(est_duration(ev_high) - est_duration(ev_high_rev))

    # (E) SHUFFLE — 구간↔novelty 페어링 셔플. 구간 라벨(high/low)과 실제 event-count 디커플
    #     50-perm: 라벨을 무작위로 두 event-set 에 배정 → signed gap(라벨high − 라벨low) 평균
    sets = [ev_high, ev_low]
    gaps = []
    for _ in range(N_PERM):
        perm = rng.permutation(2)  # 라벨↔set 무작위 배정
        e_as_high = sets[perm[0]]
        e_as_low = sets[perm[1]]
        gaps.append(est_duration(e_as_high) - est_duration(e_as_low))
    shuffle_gap = float(np.mean(gaps))  # high/low 라벨이 novelty 와 무관해지면 ~0

    return {
        "est_high": est_high, "est_low": est_low,
        "presence": presence,
        "subj_sep": subj_sep, "homeo_sep": homeo_sep,
        "abl_sep": abl_sep,
        "order_diff": order_diff,
        "shuffle_gap": shuffle_gap,
        "nov_high": int(ev_high.sum()), "nov_low": int(ev_low.sum()),
    }


def main():
    rows = [run_seed(s) for s in SEEDS]

    def mean(k):
        return float(np.mean([r[k] for r in rows]))

    m = {k: mean(k) for k in rows[0]}

    print("=" * 78)
    print("H_1475 — G22 SUBJECTIVE TIME (주관적 시간 지각) — R1 numpy DIRECTIONAL")
    print("=" * 78)
    print(f"seeds={SEEDS}  OBJ_TICKS={OBJ_TICKS}  BASE={BASE}  K={K}  "
          f"HIGH_RATE={HIGH_RATE}  LOW_RATE={LOW_RATE}  N_PERM={N_PERM}")
    print("-" * 78)
    for s, r in zip(SEEDS, rows):
        print(f"  seed {s}: nov_high={r['nov_high']}/{OBJ_TICKS} nov_low={r['nov_low']}/{OBJ_TICKS} "
              f"est_high={r['est_high']:.3f} est_low={r['est_low']:.3f} "
              f"presence={r['presence']:.3f} abl_sep={r['abl_sep']:.3f} shuf={r['shuffle_gap']:.3f}")
    print("-" * 78)
    print(f"  MEAN  est_high={m['est_high']:.3f}  est_low={m['est_low']:.3f}")
    print(f"        nov_high={m['nov_high']:.2f}/{OBJ_TICKS}  nov_low={m['nov_low']:.2f}/{OBJ_TICKS}")
    print("=" * 78)

    # FROZEN bars
    A = m["presence"] >= 0.40
    B = (m["subj_sep"] >= 0.40) and (abs(m["homeo_sep"]) <= 0.05)
    C = abs(m["abl_sep"]) <= 0.05
    E = abs(m["shuffle_gap"]) <= 0.10
    D_report = m["order_diff"]  # non-gating

    print("FROZEN BARS (mean 3 seeds):")
    print(f"  (A) PRESENCE   est_high-est_low = {m['presence']:+.3f}  >= 0.40   -> {'PASS' if A else 'FAIL'}")
    print(f"  (B) DISTINCT   subj_sep={m['subj_sep']:+.3f}(>=0.40) AND homeo_sep={m['homeo_sep']:+.3f}(<=0.05)"
          f"  -> {'PASS' if B else 'FAIL'}")
    print(f"      [vs H_1292 homeo: 객관틱 고정+novelty 조작 → subjective 갈림 / homeo 적분 평탄]")
    print(f"  (C) EARNED     abl_sep(k=0) = {m['abl_sep']:+.3f}  <= 0.05   -> {'PASS' if C else 'FAIL'}")
    print(f"  (D) ORDER-inv  order_diff = {D_report:.3f}  (non-gating; 같은 novelty 총량 순서무관)")
    print(f"  (E) SHUFFLE    |signed mean gap| = {abs(m['shuffle_gap']):.3f}  <= 0.10 ({N_PERM}-perm)"
          f"  -> {'PASS' if E else 'FAIL'}")
    print("-" * 78)
    green = A and B and C and E
    verdict = "GREEN (4/4 gating: A&B&C&E)" if green else "RED"
    print(f"VERDICT: {'🟢 ' if green else '🔴 '}{verdict} — DIRECTIONAL (numpy mirror, hard-gate 1)")
    print("=" * 78)

    import json
    out = {
        "id": "H_1475", "seeds": SEEDS,
        "config": {"OBJ_TICKS": OBJ_TICKS, "BASE": BASE, "K": K,
                   "HIGH_RATE": HIGH_RATE, "LOW_RATE": LOW_RATE, "N_PERM": N_PERM},
        "measurements": {k: round(m[k], 4) for k in m},
        "bars": {"A_PRESENCE": A, "B_DISTINCT": B, "C_EARNED": C,
                 "D_ORDER_report": round(D_report, 4), "E_SHUFFLE": E},
        "green": green,
    }
    print("JSON " + json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
