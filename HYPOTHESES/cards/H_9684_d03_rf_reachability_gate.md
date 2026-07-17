# H_9684 — D0-3 앞 RF-도달성 게이트 — D0-3 RF-Reachability Gate (교차-lane · $0 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · $0 · 발사 전 게이트 · 사전등록) — source=교차-lane(H_9560/H_9611 census → H_9672 D0-3)
**lane:** 재조합/BINDING · 주소경로 (frontier g1-interface-addressable-wall)
**related:** [[H_9672]] (D0-3 를 NEXT 로 지목했으나 T3 가 앞질러 미착륙) · [[H_9611]] (RF=35 engine-measured · GN 전역 bus 인과확증) · [[H_9560]] (beyond-RF = 순열불변 O(L)-스칼라 GN bus 뿐) · [[H_9423]] (Stage1.5 주소학습 격리)

## 제안 — D0-3 은 읽기 전에 **거리**부터 재야 한다

[[H_9672]] 의 D0 절이 지목한 **D0-3**(frozen py303 pen-dump → ridge → K[entity] top-1 = "(3) 트렁크 미인코딩" 판별)은 아직 미착륙이고, **2-seed 정정**(주소벽은 robust 돌파 · **값읽기 seed-취약** seed-7 ORACLE 0.99 vs seed-11 0.50 · TERMINAL 부정) 이후 오히려 **더 load-bearing** 해졌다 — 그 카드 자신의 판정표가 이렇게 쓴다:
> **"D0-3 FAIL ∧ T3 성공 = addr gradient 가 트렁크를 구부려 인코딩 생성"**(retention 이 비용 채점)

**그런데 D0-3 을 그렇게 읽으려면 먼저 두 가지를 배제해야 한다.**

### 함정 ① 자명-디코드 (읽는 위치)
개체 nonce 가 문맥에 **그대로 있으면** *그 개체 자신의 위치*에서 선형탐침은 **자명하게** 성공한다(바이트가 거기 있다). D0-3 이 물어야 하는 건 **질의/판독 위치**(주소가 계산되는 지점)의 penultimate 다. 어느 위치를 덤프하나가 verdict 를 가른다.

### 함정 ② 🔑 RF 도달불가 (이 카드의 핵심)
[[H_9611]] 이 engine-measured 로 확정: 이 arch 의 **RF = 35 byte**(D=34 비영 · **D=36 정확히 0**) · 그 너머로 판독점에 닿는 **유일 경로 = GroupNorm 전역 bus**(순열불변 O(L)≈10 스칼라 · **content-addressed 불가** · 동결 시 beyond-RF 영향 **정확히 0** 으로 인과확증).
⟹ **개체↔질의 byte 거리 D 가 35 를 넘으면, 질의 위치의 penultimate 는 개체 정체성을 담을 수 없다 — BY CONSTRUCTION.**

```
  개체 ─── D bytes ─── 질의(주소 계산 지점)
   D ≤ 35 : 국소 conv 가 나름     → penultimate 에 있을 수 있음 → D0-3 이 유의미
   D > 35 : GN bus 뿐(주소불가)   → 담을 수 없음 → D0-3 은 자동 FAIL
```
**⟹ 그 경우 D0-3 FAIL 은 "트렁크가 안 했다"가 아니라 "못 한다"이고, "addr gradient 가 트렁크를 구부렸다"는 해석도 틀린다 — 닿지 못하는 것은 구부릴 수 없다.** (⚠️ KO 는 **3 B/char** 라 RF=35B ≈ **11 한글자**뿐 — `a_korean_byte_budget` 이 여기서도 배수로 작동. 합성 CVCVC nonce = 9 B/개체.)

## 사전등록 게이트 (D0-3 발사 **전** · $0 · 모델 불요 · 순수 산술)

1. **거리 census**: storebind 매니페스트에서 각 항목의 **개체 마지막 byte ↔ 질의/판독 위치** byte 거리 D 를 산출(우측정렬 `win` 기준 · 계기가 실제 덤프할 위치와 동일 정의).
2. **판정**:
   - **D ≤ 35 가 대다수** ⟹ D0-3 유의미 → 발사. FAIL 이면 진짜 "미인코딩"(구부림 해석 가능).
   - **D > 35 가 대다수** ⟹ **D0-3 은 발사 무의미**(자동 FAIL 예정) → 먼저 **질의 위치를 개체 RF 안으로** 재설계하거나, 판독점을 개체 근처로 옮겨야 한다. 이 경우 "트렁크 미인코딩(3)" 가설은 **미검 상태로 남고**, T3 의 성공은 **CLMS 가 store 를 통해 개체를 나르기 때문**이지 트렁크가 구부러져서가 아니다(store 는 RF 를 우회하는 별도 경로).
   - **혼재** ⟹ D 로 층화해 D0-3 을 나눠 읽는다(D≤35 층만 "미인코딩" 판독 유효).
3. **양성통제**: D≤5 인 항목(개체가 질의 바로 앞)은 D0-3 이 **반드시 통과**해야 — 안 되면 탐침/덤프 위치가 계기死(음성 읽기 금지 · [[positive-control-before-reading-a-negative]]).

## verdict-integrity (over-claim 선차단)
- 이 카드는 **D0-3 의 결과를 예측하지 않는다** — **읽는 법**을 사전등록할 뿐이다. 거리 census 는 $0 산술이고 D0-3 자체는 별도.
- RF=35 는 clm303_clean/natem 계열 **L4 arch** 에서 engine-measured 다([[H_9611]]). **py303_full 의 L 이 다르면 RF 도 다르다** — census 전에 그 ckpt 헤더로 RF 를 재산출할 것(H_9564 의 closed-form: embed_conv 2 + trunk Σ(K−1)·min(2^i,cap) + expert_conv 2 + 1).
- store 경로(CLMS)는 **RF 를 우회**한다 — 이 게이트는 **트렁크 자력 인코딩**(D0-3 의 대상)에만 적용되지 T3 의 store-경유 성공엔 적용 안 됨.

## 상태
🔵 PROPOSED — 미실행 사전등록($0 · 모델 불요). **distinct-from-kills**: 기존 RF 카드(H_9559/9564/9560/9611)는 RF 를 *측정*했고, 이 카드는 그 측정을 **다른 lane 의 미착륙 진단(D0-3)에 게이트로 적용**한다 = 새 대상. H_9672 D0-3 의 중복이 아니라 **그 발사 전 필수 선행**.
