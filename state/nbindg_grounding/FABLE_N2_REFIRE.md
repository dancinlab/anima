## 결론 먼저

**추천 = (E) 변형: 지금은 아무것도 재발사하지 않는다.** N2는 이미 이 프로토콜이 낼 수 있는 최대 verdict를 냈다 — **NAT-CRACK 🟢는 seed 7 하나만으로 이미 REFUTED**(아래 3번), seed-11 arm은 INVALID(단 라벨은 "under-exposed"가 아니라 **install-fragile**로 정정), GROUNDING-🧱은 DIRECTIONAL로 남긴다. 남은 지출은 $0 진단 2개 + shuffle 착지 대기(3h)뿐이고, 벽을 TERMINAL로 만드는 유일한 경로는 seed 보충이 아니라 **새 사전등록(N3, TOST 포함)**이다.

핵심 재프레임: 질문이 "2-seed 요건을 어떻게 회복하나"인데, **회복할 필요가 없다.** 2-seed 요건이 보호하는 것은 양성 주장(NAT-CRACK)인데, 그 주장은 conjunctive bar(양 seed 모두 Δ≥0.20)라서 **유효한 seed 하나가 bar 아래면 그걸로 죽는다.** seed 7은 모든 유효성 게이트를 통과하고 bar 아래(Δ=−0.023)에 착지했다. seed 11이 0.99를 찍고 돌아와도 NAT-CRACK은 못 산다. seed 11 재발사는 양성 verdict에 아무 정보도 더하지 않는다.

---

## 1. 진단: 0.950 vs 0.725

**최적화 분산(seed-fragile installation)이다. 노출 부족이 아니다** — 그리고 이건 이 데이터만으로 이미 강하게 구분된다. 노출 바이트·T·f_grid가 동일한데 Δ=0.225 갈렸다는 것 자체가 "exposure가 marginal해서 둘 다 bar 근처에서 흔들린다"는 under-exposure 예측과 모순된다(under-exposure면 두 seed가 bar 주변에 몰려야지, 하나가 0.95로 여유 통과하면 안 된다). 게이트 (b) T×f_grid ≥ 1.25×E*가 빌드에서 이미 확인됐다는 사실도 같은 방향이다.

**스펙의 결함은 게이트가 아니라 라벨이다.** 게이트 (a)는 올바른 manipulation check다(설치 안 된 모델로 transfer를 측정하면 안 됨). 그러나 게이트 실패에 "under-exposed"라는 특정 인과 진단을 이름으로 박아놨고, 데이터가 그 진단을 반증했다. 카드에 "install-fail INVALID(원인 미확정: 최적화 분산 우세)"로 정정 기록해라 — bar·detector를 건드리지 않으므로 tune-to-green이 아니라 measurement-frame 정정이다.

**확정하는 싼 관측** ($0, 학습 불필요): seed 11의 중간 ckpt(있으면) 또는 train log의 grid-row loss 궤적. T 끝에서 **plateau면 최적화 분산 확정**(더 굴려도 안 됨 → T 상향 remedy 근거 소멸), **아직 하강 중이면 진짜 under-trained**(그때만 T 상향이 원리적 remedy가 됨 — 단 새 prereg로). 추가로 seed 11 seen 오류가 특정 atom/극성 클래스에 몰리는지 보면 basin 효과인지도 판별된다.

## 2. remedy 옵션 판정

- **(A) T 1.5× 재발사 — 기각.** 두 겹으로 무효: (i) 게이트 실패를 관측한 *후에* 실패한 arm만 T를 올리는 것은 게이트 통과까지 굴리는 remedy-shopping이고, 위 진단이 "plateau"로 나오면 인과적으로도 틀린 처방이다. (ii) 더 치명적으로, main-s11만 157k면 base_only/shuffle(105k)과 노출이 어긋나 Δ 비교 자체가 깨진다. T를 올리려면 4-arm 전부 재발사 = 새 prereg = 4×13.3h. 그런데 양성 verdict가 이미 죽어 있으므로 살 이유가 없다.
- **(B) 동일 T 재발사 — 기각.** 결정론적이면 비트 동일 낭비(13.3h). 비결정론적이면 "seed 11"이라 부르는 새 draw를 뽑는 것 = 은폐된 seed swap. 둘 다 나쁘다.
- **(C) 새 seed 추가 — 금지 항목 그 자체.** 게이트 실패를 본 뒤 통과할 때까지 seed를 뽑는 것은 제약에 명시된 사후 seed swap이다. (참고로 미래 설계 교훈: seed 정책은 "설치 게이트 통과 seed 2개까지, 최대 K개 발사, **발사한 전 seed 보고**"로 사전에 박으면 이 상황이 합법이 된다 — N3에 넣을 것.)
- **(D) 5-seed 분포 측정 — 정의상 새 prereg(N3)다**, bar를 seed-level 통계로 재정의하는 순간. 합법이지만 **정보가치가 낮다**: 3×13.3h를 태워 얻는 것은 "설치 fragility의 분산"인데, 살아있는 질문은 설치가 아니라 **접지**다(flip0 < 0.50). 설치된 seed 7이 이미 접지 실패를 보여주고 있는데 설치 분산을 정밀 측정하는 건 floor의 오차막대를 재는 일이다.
- **(E) — 채택**, 단 "verdict를 벌 수 없다"가 아니라 "**이 prereg가 낼 수 있는 verdict는 이미 나왔다**"로. licensing: NAT-CRACK REFUTED(이 설계점 한정: 이 corpus×T×grid) · s11 INVALID(install-fragile) · GROUNDING-🧱 DIRECTIONAL. 못 하는 것: 벽 TERMINAL 선언 — 그리고 이건 seed가 부족해서만이 아니다. **N2의 verdict grid는 threshold식(Δ<0.20)이지 등가검정이 아니므로, seed 11이 완벽히 통과했어도 소유자 정책(음성 종결 = 사전등록 TOST)상 substrate-level 벽은 N2 구조 안에서 애초에 cement 불가였다.** 벽을 벌려면 어차피 N3다.

## 3. seed 7 하나가 licensing하는 최대 주장

비대칭이 핵심이다: **한 seed로 벽은 선언 못 하지만, 한 유효 seed로 "양 seed 필수" conjunctive 양성 주장은 반증할 수 있다.** 둘은 동시에 정직하다.

**말할 수 있는 것** (TERMINAL, 이 prereg 범위 내):
> "grid에 설치된 XOR 극성 연산자(seen 0.950)는 이 corpus·T·설계점에서 자연-접지 held-out 원자로 transfer 신호를 내지 못했다(D-acc 0.477, flip0 0.402). NAT-CRACK은 이 설계점에서 반증. flip 분해상 실패 지점은 연산자(flip1 0.552)가 아니라 **극성 접지 liveness(flip0 < chance)** — GROUNDING 방향, DIRECTIONAL."

**말할 수 없는 것**: "303M substrate는 자연분포 극성 접지가 불가능하다"(벽·천장 주장 — 2-seed + 사전등록 TOST 필요) · MODEL-🧱 vs FORMAT-🧱 확정(shuffle 착지 전) · 이 corpus/objective 밖으로의 일반화(`a_scale_honest_scope`).

## 4. flip0 < 0.50 — 우연 이하는 무지가 아니다, 그런데 해석이 갈린다

우연-이하는 두 기제가 내는데 GROUNDING-🧱에 대한 함의가 **정반대**라 반드시 갈라야 한다:

- **(i) 상수-방출 + 클래스 불균형**: 모델이 P_nat에서 atom과 무관하게 한 극성 어휘를 거의 항상 방출하면, flip0 acc ≈ 그 극성의 base rate(<0.5 가능), flip1 acc ≈ 1 − flip0. **seed 7이 정확히 이 서명을 보인다: 0.402 + 0.552 = 0.954 ≈ 1.** 이 경우 flip0<0.5는 오배정이 아니라 marginal artifact이고, "atom별 신호가 전무해서 marginal로 후퇴했다"는 뜻 → **GROUNDING-🧱을 강화**한다(접지가 아예 설치 안 됨).
- **(ii) 체계적 반전 접지**: 접지가 설치됐는데 부호가 뒤집힘. 이것도 flip0+flip1≈1을 내지만(연산자가 작동하면), 극단적 ε/1−ε 형태여야 하고, **atom별 정확도가 0/1 근처 bimodal**이어야 한다. 이 경우 접지 채널은 살아있고 문제는 부호/라벨 정렬 → GROUNDING-🧱을 **약화**하고 라벨-채널(V3류) 조사를 요구한다.

**가르는 진단은 $0이고 이미 있는 eval 출력에서 나온다**: (1) arm별 응답 marginal — main-s7이 P_nat에서 한 극성을 ~90%+ 방출하면 (i) 확정. (2) atom↔응답 상호정보/atom별 정확도 분포 — 응답이 atom에 따라 변하지 않으면 (i), bimodal이면 (ii). 새 학습 0, 몇 분짜리 로그 분석이다.

---

## 실행 순서 (전부 $0)

1. **지금**: seed-11 grid-loss 궤적(plateau vs 하강) + seed-7 P_nat 응답 marginal/atom-MI 분석 — 위 1·4번 확정.
2. **3h 후**: shuffle_grid 착지 → verdict grid의 FORMAT vs MODEL 분기 완결.
3. **기록**: N2 종결 = NAT-CRACK REFUTED(설계점) · s11 INVALID(라벨 정정: install-fragile) · GROUNDING-🧱 DIRECTIONAL. 카드에 "under-exposed" 라벨 반증 명기.
4. **reopen 경로(N3, 별도 사전등록·필요시 spend-go)**: 표적은 seed 수가 아니라 **접지 채널**(held-out 극성을 접지시키는 데이터/objective). N3에 미리 박을 것 — TOST Δ_eq·N_REQ 사전 고정, seed 정책("설치-게이트 통과 2 seed까지 최대 K발, 전 seed 보고") 사전 고정, 게이트 라벨은 인과 중립("install-fail")로.

한 줄 요약: **seed 11을 살리려는 모든 경로는 이미 죽은 양성 verdict를 위한 지출이고, 살아있는 음성 verdict는 이 prereg 구조로는 어차피 TERMINAL이 될 수 없다. N2가 준 것을 정확한 scope로 기록하고, compute는 접지 채널을 겨눈 N3에 써라.**