# CLM BRIDGE distill — transfer arm (MITOSIS-ARRAY SECONDARY)

> P0 §11.4/§11.6 (BRIDGE) · `CLM.breakthrough.mining.md` BRIDGE(depleted-both) · F-CLM-BRIDGE-XFER (H_853)

MITOSIS-ARRAY 의 **두 번째 arm**. DISSOLVE(PR2/PR3)가 scale 축을 expert-COUNT 로
**reframe** 한다면, BRIDGE 는 **측정-rung ⊥ 배포-rung** 의 간극(a_scale_honest_scope)을
**knowledge distillation 으로 건넌다**(@L8).

```
   TEACHER (유효 측정 scale)            STUDENT (chip-fit 배포 scale)
   ┌──────────────────────┐            ┌──────────────────────┐
   │ E=32 · d=128          │  ── KD ──▶ │ E=8 · d=64            │
   │ dispatch-entropy z 측정 │   soft-    │ 각 expert ≤ AKD1000   │
   │ (monopoly-escape)     │   target   │ (1.2M nodes) chip-fit │
   └──────────────────────┘            └──────────────────────┘
        z_teacher                            z_student
                    transfer Δ = z_student − z_teacher
              → escape 가 distill 후 생존하는가?
```

## 파일

| 파일 | 역할 |
|---|---|
| `distill_array.py` | teacher/student array builder + Hinton KD loss + dispatch-entropy z 측정 (payload) |
| `run_bridge_transfer.py` | teacher train → KD distill → transfer Δ 측정 runner (smoke + fire 페이로드) |
| `distill_array.hexa` | hexa-native thin driver (d5 1순위 · @L4) |
| `run.sh` | `smoke`($0 local) / `fire`(GPU pod) 글루 |

## 실행

```bash
./run.sh smoke            # $0 local CPU toy distill — plumbing 검증 (toy != scale, H_666)
./run.sh fire   ubu-1     # GPU pod 유효-scale teacher distill — cost-bearing
```

## falsifier F-CLM-BRIDGE-XFER (frozen · @L8)

```
PASS (transfer 생존) iff
   z_student 와 z_teacher SAME SIGN (escape 방향 보존) AND
   |z_student − z_teacher| ≤ XFER_TOL (transfer Δ bounded) AND
   student chip-fit
FAIL (closed-negative) otherwise — 정직 보고 (g63, p7, a_paper_negative_ok)
```

KD = Hinton: `L = (1−α)·CE(student, target) + α·T²·KL(softmax(student/T) ‖ softmax(teacher/T))`.

verdict 영속: `.verdicts/clm-mitosis-array/bridge_transfer_*.txt` (PR5).

## 정직 (p7)

- 추론은 **AKIDA-int4-only 불변**(P0 d4) — distillation 은 GPU/CPU pretrain 만.
- toy scale(toy 2-lane corpus · d≤128)은 intuition(H_666). 유효-scale teacher 는 GPU fire.
- a_scale_honest_scope: 측정 rung(teacher) ⊥ 배포 rung(student chip-fit) — BRIDGE 는 그 사이 transfer 보장을 측정.
