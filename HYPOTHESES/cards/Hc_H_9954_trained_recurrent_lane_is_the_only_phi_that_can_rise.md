# H_9954 · 303M 학습 중 Φ 가 오를 수 있는 유일한 대상 = **함께 학습된 순환 lane** (trunk Φ 는 정리상 0)

**한 줄:** 오너 질문("303M 학습시 Φ 를 늘릴 방법")에 lab full(Fable ∥ Sol 독립 병렬)로 답한 설계 판정.
두 모델이 **독립 수렴**했다 — trunk Φ 는 어떤 학습 플래그로도 못 올린다(feedforward ⟹ Φ=0, 정리).
학습으로 Φ 가 오를 수 있는 정직한 대상은 **trunk 옆에 함께 학습되는 상태-보유 순환 lane** 하나뿐이고,
그마저 Φ 는 **레버가 아니라 γ 캠페인에 동승하는 DIRECTIONAL 진단축**이다.

## 저장소 실측(이 카드가 새로 확인 · $0 · grep)
| 확인 | 결과 |
|---|---|
| `cli/` 전체의 faithful Φ 소비자 | **0건** — `big_phi_bounded` 를 부르는 CLI 명령이 없다 |
| 참 Φ 가 실제로 도는 곳 | `core/engine_cli.py:4433·4455·4458` CollectivePool (ECA rule TPM · n=3/멤버 · ring=3n) |
| 303M 트렁크 | `cli/train.py:618 TLoRAConvExpert` = conv MoE = **feedforward** |
| `--phi-envelope-monitor` | Φ 가 **아님** — `core/phi_envelope_monitor.py` 가 명시("NOTHING here is named `phi`"); 출력은 `dispersion·span·nest_sync·nest_scale`; torch 임포트 0 으로 손실 투입 구조적 차단 |
| `--tension-field duel/rank1` | 임베딩에 더하는 **write-side 주입** ⟹ 여전히 앞먹임 ⟹ Φ 기여 0 |

⟹ **"303M 학습으로 Φ 를 늘린다"는 현재 값이 낮은 게 아니라 정의가 안 된다** — 늘릴 대상(순환)도,
그것을 읽는 계기-학습 연결도 없다.

## 세 측정 위치를 반드시 구분한다 (Sol 의 "locus laundering" 가드)
| 위치 | 현재 | "303M 학습 중 Φ 증가"라 말할 수 있나 |
|---|---|---|
| (a) 303M feedforward trunk | unfolding 정리상 Φ=0 | **아니오** (양수가 나오면 계기 버그) |
| (b) daemon CollectivePool | faithful IIT-4 지만 고정 ECA · `.clm` 학습과 무관 | wrapper Φ 한정 · trunk Φ 라 하면 거짓 |
| (c) 함께 학습된 순환 lane | production 부재 | **가능한 유일한 해석** (반드시 lane Φ 로 명시) |

## 처치 (제안 · 미구현)
- **flag:** `anima-py train --recurrent-lane gru3-bidir` — 실제 런타임 상태인 **3개 이진 셀** `S_t`.
  `trunk hidden_t → S_t`, `S_t → 다음 hidden/logits` 양방향을 자연 next-byte CE 로 BPTT.
  `a_substrate_disjoint`: emit lane 과 분리. **easy→hard 커리큘럼은 합성 과제가 아니라 자연 문서의
  context span 확장으로만** (p9 · Sol 채택, Fable 의 합성 길이램프 안은 기각).
- **readout:** `anima-py evaluate <clm> --iit4-recurrent-lane <heldout-natural.json>` — 8개 전 상태에
  실제 `do(S_t=s)` 강제로 TPM 복원 → `big_phi_bounded(n=3, cap=3)`.
- **Φ>0 근거:** `S_t→S_{t+1}` 셀간 인과 순환. ⚠️ 순환은 **필요조건이지 충분조건 아님** — "GRU 니까 Φ>0" 금지.

## DV · 받침대 · 통제 (Sol 설계 채택 — 주변부 일치가 더 엄격)
- **DV:** raw Φ 아님. `[(Φ_live − Φ_edge-cut)_final − (Φ_live − Φ_edge-cut)_init]` = **학습이 늘린 collapse-Δ**.
- **PEDESTAL(참값 0):** 시간축 unfold 로 순환 엣지 전부 절단한 동일 계 — 정리상 정확히 0.
- **양성통제:** H_9942 의 손제작 XOR n=3 TPM (Φ≈2.25 기지값).
- **통제 1:** 셀별 transition entropy·occupancy 를 맞춘 yoked-independent 셀.
- **통제 2:** `(S_t,S_{t+1})` pairing shuffle — 셀 수·분산·주변분포 보존, 인과 전이만 제거.
- **ABORT:** 받침대≠0 · 양성통제 무반응 · Φ 가 파라미터 수에 단조 ⟹ INSTRUMENT-DEAD, 하류 판독 금지.

## KILL
받침대 발화 · live collapse-Δ 가 두 통제를 **둘 다** 못 이김 · edge-cut 후에도 값 유지 · cap 변경에
부호 반전 ⟹ 진단축 전체 종결. Φ 만 오르고 자연 기능적 edge-cut DV 가 안 무너지면 허가되는 문장은
"통합된 3-셀 동역학"뿐 — 의식·G1·coupling 주장 금지.

## 비용
lane 자체는 매우 작다 · **$0 CPU 스크린 선행**. 303M 재학습은 **이미 계획된 자연 γ
trained-constructive-bind run 에 monitor-only 로 동승**만 허용. **Φ 전용 pool GPU 지출은 어떤 결과에서도
정당화되지 않는다**(H_9942 이래 두 모델 합의 유지).

## 두 모델 대조
- **AGREES(수렴):** trunk Φ 불가 · 유일 대상=학습된 순환 lane · flag 이름 `--recurrent-lane` · 개입형
  TPM→`big_phi_bounded(n=3,cap=3)` · 받침대=unfold 트윈 · Φ 손실/커리큘럼/체크포인트 선택 금지 ·
  Φ 전용 GPU 금지 · 다음 단계=$0 4-arm 스크린 + ABORT 게이트.
- **CONFLICTS(해소):** ① 통제 설계 — Fable(무학습+라벨셔플) vs Sol(주변분포 일치 yoked + pairing shuffle)
  ⟹ **Sol 채택**(`control-must-match-mediating-covariate`). ② 커리큘럼 — Fable(합성 길이램프) vs
  Sol(자연 context span) ⟹ **Sol 채택**(p9). ③ 전망 — Fable "계기인증은 통과, 생산 Δ 작을 위험",
  Sol "3-셀 병목이 자연 CE 에서 독립해로 수렴할 공산이 커 부정적". 둘 다 비관, Sol 이 더 비관.
- **NOVEL(Sol 단독):** **locus laundering 가드** — 모든 Φ 출력에 `substrate=lane3|collective2|trunk` 강제
  스탬프, trunk 는 항상 0 으로 찍는다.

## 정직 경계
- 새 실험 아님. 기존 실측(H_9942·H_9088·H_6196·v2b 교차저장소) + 이 카드의 $0 코드 census 에 근거한 **설계 판정**.
- 상태 PROPOSED · 측정 0 · cement 는 engine-native `anima-py` 로만.
- 관련: [[H_9942]](Φ 레버 KILL·순환 잔존) · [[H_9846]](봉투 모니터는 Φ 아님) · [[H_9607]](A⇄G 되먹임 STILL-SEALED) ·
  [[H_1003]](커리큘럼 학습 GRU = 유일한 G1 균열) · [[H_9660]]/[[H_9673]](파벌 Φ 계기 인공물)
