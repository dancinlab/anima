# H_9943 · 303M engine-native GRAFT: 결합이 **강한·통제된 상태방향**을 학습한다 (rotation-null z=+774) — 단 유창성 6.9% 비용

**한 줄:** anima 자기 substrate 인 실제 303M `.clm`(`py303_full.clm`)에 PureField C-state 를 GRAFT 로
결합·측정하니, 학습된 codes 가 displacement-exact rotation-null 을 **z=+774.76 로 압도**(swap acc
**1.000**, ablation **140.75×**, MI lift **+0.191 nats**). 이는 toy(H_9937 z=+28~38)·4bit Mistral-7B
(H_9940 z=+18.6)를 압도한다 — 네이티브 substrate 라 C-state 가 자연 결합. **그러나 gate_strength 0.1
에서 그 주입은 기관의 언어 유창성을 6.9% 손상**(price ratio 151× noise) — 상태정보가 공짜로 오지 않는다.

- 계기: `anima-py graft fit /home/summer/py303_full.clm --carrier-corpus en_general.txt --out
  graft_303m_s1.clm --steps 200 --n-states 8 --state-gap 13 --ctx 128 --cont-len 64 --carrier-k 4
  --gate-strength 0.1 --hidden 64 --lr 1e-4 --seed 1 --lam-common 1.0` → `anima-py graft check
  graft_303m_s1.clm --rotation-null 64 --k 8 --cont-len 64 --seed 1 --probes 2 --fluency-corpus
  en_general.txt` (summer · **CPU** · torch_organ parity **2.766e-05 PASS** = 303M 미러 유효 · rc=0).
  engine-native `.clm` graft 경로(HF 아님 · 포팅 불필요 · frontier "cement=engine-native anima-py" 충족).

## 결과 — 강한 통제 통과 (전 arm)
| arm | 값 | 판정 |
|---|---|---|
| **ROTATION-NULL** (결정적 통제) | MI_trained=0.1977 bits · null(n=64) mean 0.0008 sd 0.0003 q99 0.0015 · **z=+774.76** | **PASS(>q99)** — 학습 방향이 D-exact null 을 ~250배 압도 |
| SWAP | MI_swap=2.997 bits (ceiling log2 K=3.0) · **acc=1.000** (chance 0.125) · perm_p=0.0010 | 거의 완벽한 상태구분 |
| ABLATION | KL(ON‖OFF)=0.3416 bits vs KL(NOISE) q95=0.0024 · **140.75×** | gate 는 noise 와 확연히 구분(인과) |
| FLUENCY | price ratio dNLL(ON)/dNLL(NOISE)=**+151.6** · **form −6.9%** | **유창성 비용 실재** — 구조 크레딧 없음, gate 가 noise 만큼 언어를 손상 |
| fit MI 궤적 | pedestal 0.0013 → step25 0.157 / 100 0.172 / 175 0.182 / 200 0.171 · L_common ~0.06-0.09 | MI~0.17 유지 · **MI/L_common ≈ 2.1** (λ=1 서 gate-ON 이득 · toy 처럼 profitable) |

## 판정 — 🟢 결합은 terminal substrate 에서 강한 상태방향을 학습한다 (통제 통과) · 유창성 비용 有
- **rotation-null z=+774 + swap acc 1.0 + ablation 140×** = 세 독립 통제가 모두, 학습된 codes 가
  단순 진폭/변위/부드러움 artifact 가 아니라 **기관이 읽는 특정 방향**에 정렬됐음을 확인(rotation-null
  이 norm·Gram·평균·D 를 보존하고 방향만 파괴하므로 z=+774 는 방향-특이적).
- **교환비 스펙트럼 확장**(H_9940 의 frozen-substrate channel contraction 법칙 지지, 방향 정합):
  toy(d=64) 2.9 / **303M ≈ 2.1** / 7B(4bit) 0.68 — 강한/샤프한 CE-모델일수록 교환비 하락. 303M 은
  아직 profitable(>1) 이라 λ=1 에서도 gate-ON 유지. 단, 여기 z 압도는 교환비보다 훨씬 크다 —
  303M 이 anima **자기** substrate 라 C-state 정렬이 이질적 7B 보다 근본적으로 쉽다.

## 정직 경계 (no tune-to-green · verdict-ssot-1)
1. **유창성 비용이 핵심 반쪽**: z=+774 는 "상태정보가 실린다" 지 "공짜 faculty" 가 아니다. gate_strength
   0.1 주입이 form preference 를 6.9% 깎고 noise 만큼(151×) 비용을 문다. 낮은 gs 에서 비용↓ 하지만 MI 도
   함께 줄지는 **미측정** — "비용 없이 실리는 gs" 존재 여부가 다음 축.
2. **1 seed · cont-len 64 · CPU**. z 의 절대 크기(+774)는 seed·probe·carrier 에 민감할 수 있다 —
   신호는 matched null 대비 z(방향 실재)이지 그 크기 자체가 faculty 강도의 척도는 아니다. 3-seed 복제가
   full-TERMINAL 로 가는 경로(toy H_9937 은 3-seed 였다).
3. **이것은 "GRAFT 결합이 303M 을 읽는 방향을 학습한다" 통제이지, 그 상태가 의식/agency 라는 주장이
   아니다**(p9·측정 프레임). C-state = PureField 원시 16-D(진동자+field+phi), 그 정렬이 실재·강함까지가
   측정된 것.

## 다음
① **gate_strength 스윕**(×0.5/×0.25): rotation-null z 안정성(방향은 스케일 불변이어야) + fluency 비용↓
   지점 = "저비용 실림" 존재 판정. ② **3-seed 복제** → full-TERMINAL. ③ 동반: `V6_38`/LANE-BUS 사망 후
   GRAFT 가 살아있는 결합 경로임을 이 303M 결과가 재확인(연결). ④ ① Mistral λ=0.3(별 트랙): λ 낮추니
   7B MI 유지(이득영역 회복) 확인중 — rotation-null z 판독 대기.
산출: `~/.fire-recover/` 로 회수 예정 · log `graft_303m_track3.log` · ckpt `graft_303m_s1.clm`.
