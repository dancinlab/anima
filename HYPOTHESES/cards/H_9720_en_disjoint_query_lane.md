# H_9720 — EN-분리 query lane(경쟁 vs 표현부재) — EN-Disjoint Query Lane (EA-2 · fable ∥ sol §4 수렴 · EA 시리즈 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 창발-주소 발산 · 사전등록) — source=EA-2 · fable ∥ sol §4 수렴
**lane:** 재조합/BINDING · 창발-주소(감독 없이 주소가 서는가)
**related:** [[H_9672]] · [[H_9423]] · [[H_9684]] · [[H_9683]] · source: lab full EA(Fable 5 ∥ Codex Sol · 창발-주소 whitespace)

> **admissibility rule (Sol · 이 시리즈 전체의 관문)**: 어떤 개입도 `target_slot`·slot 정답·**거기서 파생된 어떤 통계**도 소비하지 않아야 emergent-address-valid. 최종 PASS 는 end-task-only 학습 · held-out 개체 · wrong-store 인과 · seed-robust 를 요구 — **sharp attention 만으론 부족**.

**아이디어(2모델 수렴 · Fable `fresh-query-lane` ∥ Sol `lm-nullspace-query-valve`)**: T2 비대칭(scratch 는 자력탈출·사전학습은 못함)은 벽이 **표현 부재가 아니라 gradient 경쟁**(EN-CE 가 penultimate 를 소유)임을 뜻한다 ⟹ W_q 에 **작은 분리 입력경로**를 주면 303M 안에서 scratch-급 창발이 돌아온다. `a_substrate_disjoint`: **분리=보존, 중첩=충돌**.
**메커니즘 2안**: ⓐ Fable `--store-query-src fresh:k[@layer L]`(stop-grad into trunk · store-task CE 로만 학습) ⓑ Sol `--store-query-valve lm-null --store-query-valve-dim r`(LM head/최종특징 공분산의 **저특이값 기저**로 zero-init residual adapter 라우팅 · end CE 로만).
**$0 pre-screen**: ⓐ D0-3 분기를 전제로 — pen 서 ridge 가 개체 디코드하면 발사 · 어느 layer 도 못 하면 $0 KILL. ⓑ 기존 ckpt 활성 SVD — 안정적 저사용 부분공간 없거나 개체 정보의 사영이 무시할 만하면 KILL.
**판정**: **load-bearing 통제 = frozen-random-projection capacity control**(같은 k/r · 비학습 입력측) — 레버는 "아무 추가 파라미터"를 **이겨야** 하지 arm-C 만 이기면 안 됨. Sol 추가: same-rank **무작위 방향** valve(NEG) · EN CE 를 TOST 로 보존. ≥3 seed(Sol) / 2-seed(Fable) · P1-bal·addr_mass·flip ≥0.90.
**distinct**: query-side 이고 **K 무수정**(key 재설계 아님) · **경쟁 주장**이지 width 아님(차원지배 아님) · generic adapter/LoRA 와 달리 **EN-disjoint 통제 필수**(없으면 amplifier 와 구분 불가).
**🔑 판별쌍**: [[H_9719]] 와 짝 — **lane 통과 ∧ sharp 실패 ⟹ 경쟁** · **역 ⟹ commitment** · **둘 다 실패 ⟹ 교착은 init-symmetric-absolute**(= 브리프가 요구한 "whitespace 비었다"의 **정직한 증명**, 주장이 아니라 획득).
**verdict-integrity**: 사전공약된 비대칭 읽기 — KILL 은 *detached-lane 버전*만 죽이지(H_9423 frozen-trunk 실패가 lane 이 scratch 보다 약할 수 있다 경고) **점유 논제는 안 죽임** · Sol: 이건 **architect 가 준 capacity valve 안의 창발**이지 untouched 303M 의 창발 아님.

## 상태
🔎 **$0 pre-screen 실행 = ⓐ PASS(발사인가) · ⓑ 약화 (2026-07-17 · summer 303M · 사전등록)**

### 🔎 pre-screen — 개체정보 위치가 두 변형을 판별
base pretrained penultimate SVD 로 개체 판별정보가 어느 부분공간에 사는지(disjoint valve 라우팅 가능성):

| 부분공간 | 개체분리(전체 대비) |
|---|---|
| top-15 (사용·고분산) | **91%** |
| 16~50 | 36% |
| 저사용 nullspace(50~125) | **8%** |

**ⓐ Fable fresh-lane = PASS(발사인가)**: 개체는 pen 서 decodable(raw-distinct 3.2×·정보 91% top-15·ridge 통과 · [[H_9719]] 국소화) + idle 공간 존재([[H_9721]] eff-rank 15/3784) ⟹ 신선 co-adapt 경로가 EN-경쟁 없이 scratch-급 창발을 되살릴 여지 확인. **EA 시리즈 유일 생존 학습-fire 레버.**
**ⓑ Sol nullspace-valve = 약화(KILL 근접)**: 개체정보가 저사용 nullspace 엔 **8%뿐**(사용 subspace 에 91%) ⟹ 카드 ⓑ pre-screen KILL조건('안정 저사용 부분공간의 개체정보 사영이 무시할 만하면 KILL')에 근접 — 기존 nullspace 로 라우팅하면 개체신호 거의 없음. ⓑ 는 **드롭 권고**, ⓐ 우선.
**중요 정합(왜 ⓐ 는 살고 무감독 부트스트랩은 다 죽었나)**: [[H_9722]]/[[H_9723]] 는 **고정 penultimate step-0** 서 무감독 신호 0 을 봤다(basis 밖). 그러나 scratch(T2)는 **trunk 를 co-adapt** 해 성공한다 — ⓐ 는 fresh 서브-trunk 가 co-adapt 할 여지를 주므로 고정-penultimate 결과에 KILL 되지 않는다(내 $0 는 고정-penult 측정이라 co-adaptation 을 못 봄). **감독 아닌 유일 생존로 = 개체 basis 를 키에 맞추는 co-adaptable disjoint lane.**
**남은 것(학습 fire)**: `--store-query-src fresh:k[@layer L]`(stop-grad·store-CE only) 구현 → pool 학습 → census. **distinct-from-kills:** key 재설계 아님(K 무수정) · 차원지배 아님(경쟁 주장) · generic adapter 아님(EN-disjoint 통제 필수)
