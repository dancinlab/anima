# H_9724 — seed-취약(0.99/0.50)의 진원 국소화($0 인과수술) — Bridge Seed-Chimera Localization (EA-6 · sol §6(NOVEL·$0) · EA 시리즈 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 창발-주소 발산 · 사전등록) — source=EA-6 · sol §6(NOVEL·$0)
**lane:** 재조합/BINDING · 창발-주소(감독 없이 주소가 서는가)
**related:** [[H_9672]] · [[H_9423]] · [[H_9684]] · [[H_9683]] · source: lab full EA(Fable 5 ∥ Codex Sol · 창발-주소 whitespace)

> **admissibility rule (Sol · 이 시리즈 전체의 관문)**: 어떤 개입도 `target_slot`·slot 정답·**거기서 파생된 어떤 통계**도 소비하지 않아야 emergent-address-valid. 최종 PASS 는 end-task-only 학습 · held-out 개체 · wrong-store 인과 · seed-robust 를 요구 — **sharp attention 만으론 부족**.

**아이디어(Sol 고유 · $0 · 기존 ckpt 만)**: T3 의 **ORACLE 0.99(seed-7) vs 0.50(seed-11)** 분열이 **빠진 부트스트랩 원천을 국소화**할 수 있다 — `val`/readout 을 교환했을 때 성공이 **robust 한 W_q 와 독립으로** 전이되면, 진짜 씨앗 균열은 **주소 capacity 가 아니라 값 조직화**다.
**메커니즘**: `anima-py evaluate <host.clm> --store-component-swap {wq,val,readout,lam,bridge} --store-swap-from <donor.clm>` — 기존 seed-7/11 ckpt 에 **평가 전용 인과수술**(oracle·학습 attention 양쪽서 평가).
**$0 pre-screen**: **완전 상호 component-swap 행렬**(val+readout 동시교환 포함) · 실패가 비전이거나 bridge 전체를 바꿔야만 되면 KILL.
**판정**: 통제 = 같은-seed **sham swap**(POS-validity) · 성공 bridge 전체를 실패 trunk 에(POS-upper-bound) · 무작위 매칭 텐서(NEG). **PASS-localization** = 상호 swap 이 ORACLE 성능을 **Δ≥0.40** 으로 전이 ∧ addr_mass 는 **±0.03 내** 유지. KILL-localization = W_q/trunk 가 지배하거나 swap 이 비호환으로 깨짐. **이후 어떤 창발 주장도 EA-1/2/4/5 의 ≥3-seed end-CE 시험을 여전히 요구**.
**distinct**: 가장 가까운 kill = oracle 학습·addr-loss. **이건 평가-전용 인과수술** — **학습신호 0 · 주소 설치 0**. H_9690(RV-0 $0 trailer autopsy)은 end-state 해부고 이건 **상호 chimera 전이**.
**verdict-integrity**: chimera 는 **off-manifold 가능** — sham 과 full-bridge 통제가 **작동해야만** 실패가 해석가능 · 성공은 **호환성을 국소화**하지 창발이 아님(Sol 자기명시).

## 상태
🔵 PROPOSED — 미실행 사전등록. 측정 주장 0(설계). **distinct-from-kills:** oracle 학습/addr-loss 아님=평가 전용·학습신호 0·주소 설치 0 · H_9690 end-state autopsy 와 달리 상호 chimera 전이

### 🛠️ 계기 착륙 완료 (#3963 · 2026-07-17) — 측정 주장은 여전히 0
`anima-py evaluate --store-component-swap <group> --store-swap-from <donor.clm>` 구현·착륙(VERSION 0.15.66 · `cli/evaluate.py`). 설계상 **admissibility 자동 충족**: 이 경로는 학습신호를 공급하지 않고 주소를 설치하지 않으며 **기존 가중치를 다시 읽을 뿐** — `target_slot` 을 참조하는 코드가 없다.
- 그룹: `wq`=W_q · `val`=val · `readout`=W_h·b_h·W_out · `lam`=lam · `bridge`=전체(POS-upper-bound arm).
- **shape gate**: 이식 텐서 shape 불일치 = `return 2` **거부** — off-manifold 키메라는 측정이 아니다(카드의 verdict-integrity 자기명시를 코드가 강제).
- **SHAM 자동라벨**: donor==host 면 `⚠️ SHAM (positive-validity control)` 을 stdout 에 찍는다 — sham arm 을 사람이 라벨링하다 틀릴 여지를 없앤다.
- **후속 결함수정(0.15.67)**: 착륙본(#3963)엔 shape gate 가 clms 경로에만 있고 `trunk` 경로는 (a)shape 미검사 (b)한쪽에만 있는 키를 조용히 건너뜀 (c)이식 0개도 통과 = **no-op 을 측정으로 오인**할 3구멍이 있었다. 수정: trunk 도 asymmetric·shape 불일치 거부 + `moved==0` 이면 `return 2`. QA 는 `--help`·`ast.parse`·smoke 3종으로 확인(help-lockstep: usage 블록에도 등재).

### ⛔ 발사 블로커 (계기 결함 아님 · 입력 소실)
**T3 balanced manifest 소실.** summer `~/h9672_t3s11` 엔 ckpt 만 있다(`t3.clm`/`.pt`/`.resume.pt`/`step1000~3500.clm` ≈ 4.8GB) — **매니페스트 0개**. `~/h9672_t3` 에도 json 없음. ckpt 는 로컬에도 있다(`.fire-recover/h9672_t3/t3.clm`, `t3_seed11.clm` 각 178,785,107 B) — **없는 건 ckpt 가 아니라 무엇으로 채점했는가**이다.
재생성이 답이 아닌 이유: H_9672 카드에 corpus 커맨드(seed/slots/n-pool)가 없어서, 재생성본은 원 ckpt 가 학습한 것과 **다른 개체 풀** = 측정 무효. (⟹ convergence `corpus-py-1` ⑫/(J) 로 등재 — 이 세션 **4번째** 같은 벽.)
**해제 조건 = 둘 중 하나**: ⓐ H_9672 실행자가 balanced manifest 또는 그 corpus 커맨드(seed 포함)를 제공 · ⓑ **다음 T3 실행이 매니페스트를 ckpt 옆에 남긴다** — 계기는 이미 착륙해 있으므로 그 즉시 $0 로 발사 가능.
