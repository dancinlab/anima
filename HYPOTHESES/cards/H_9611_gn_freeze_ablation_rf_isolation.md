# H_9611 — GN-freeze 절제 = RF-격리 — GN-Freeze Ablation · RF Isolation (fable R3-A1 · R3 · 🟢 EXECUTED · GN-bus 인과확증 + RF=35 방전)

**status:** 🟢 EXECUTED (engine-native aiden CPU · $0 · 계기 PASS + 본실험 INERT) — source=fable R3-A1
**lane:** BINDING / GroupNorm 전역 bus 채널 (R3 신규 whitespace)
**related:** [[H_9560]] · [[H_9359]] · [[H_9304]] · [[H_9267]] · source: lab full R3 (fable R3-A1)

**아이디어(FIRE-FIRST · 모든 것의 게이트)**: GN μ/σ² 를 상수로 clamp 하면 trunk 가 **엄격히 RF-local** 이 된다. 기존 cement 된 재조합 수치가 전부 불변이면 GN bus 는 아무것도 안 실었고 beyond-RF 는 *스칼라 경로*가 아니라 **경로 자체 없음**으로 격상.
**메커니즘**: `anima-py evaluate <clm> --gn-freeze`(신규 flag · μ/σ²←고정상수 · affine γ/β 무수정). H_9359/H_9304/H_9267 채점셋 재생.
**$0 pre-screen(프리스크린의 프리스크린)**: `--dump-hidden` 한 prefix 로 frozen vs live GN 간 ‖Δh‖≠0 확인 — 0 이면 flag 무력=INSTRUMENT-DEAD 중단.
**판정표**: C1 **양성통제**=live-GN baseline 이 cement 된 수치를 byte-identical 재현(실패=계기死·verdict 없음) · C2 shuffled-far-context. **PASS-inert**: 전 Δ 가 det-noise 내 ⟹ bus 는 readout-무관 ⟹ "beyond-RF 아키텍처 부재"를 **no channel** 로 격상 ∧ [[H_9562]] outside-RF arm 이 **유효 null 이 됨**. **PASS-live**: Δ 존재 ⟹ **모든 far-context verdict 가 GN-confounded** → [[H_9612]] 발화.
**distinct**: 가장 가까운 kill="floor 가 long-range bus 증명"(死). 이건 **역**: bus 를 이용 안 하고 **삭제**해 load-bearing 이었나 시험. RF 무수정이라 H_1584(깊이) 아님.
**verdict-integrity**: inert ⇏ "GN 무용"(정규화자다 · *cross-position 정보*만 inert). 동결상수는 train-set 통계서 **사전등록**, 스윕 금지(스윕=tune-to-green).

## 🟢 실행 결과 (aiden · clm303_clean L4 · CPU-pinned bit-exact · $0 · 2026-07-16)
계기 `anima-py evaluate --dump-hidden --gn-freeze <ref>`(v0.15.15 구현 · v0.15.16 allowlist fix · GN 사이트 5곳=trunk×4+norm_out 전부 pin · ref=58B filler 사전등록·스윕 0).

**① 계기 프리스크린 PASS**(Fable 의 "프리스크린의 프리스크린"): live vs frozen ‖Δh‖_last = **36.8 / 14.7** ≫ 1e-6 ⟹ flag 가 실제로 GN 을 바꾼다(INERT=계기死 아님). ⚠️ 첫 실행은 `unknown flag` 로 거부 — 파싱만 넣고 `_KNOWN_FLAGS` 미등록(#3829 수정). **계기가 자기 결함을 verdict 전에 드러냄**(positive-control-before-reading-a-negative).

**② 본실험 — byte-flip@D 의 ‖Δh_last‖ (live vs frozen)**:

| D | live | frozen | 판독 |
|---|---|---|---|
| 1 | 24.054 | **24.058** | RF 내 **생존**(내장 양성통제 C1 통과 — 동결이 전부를 날리지 않음) |
| 8 | 1.529 | 1.532 | 생존 |
| 12→34 | 0.85→0.49 | 0.75→**0.006** | 매끄러운 감쇠 = 진짜 RF 경계 |
| **36·40·44·48·56** | 0.485·0.475·0.462·0.443·0.337 | **0.000e+00 (전부)** | ✅ **floor 정확히 붕괴** |

**⟹ 3중 확정:**
- **✅ GN-bus 인과확증**: beyond-RF 영향이 GN 동결로 **정확히 0** 소멸 ⟹ [[H_9560]] 의 acausality *추론*이 **인과 개입**으로 격상. floor 는 100% GroupNorm bus.
- **✅ 양성통제 통과**: RF 내(D=1) 24.054→24.058 생존 ⟹ 동결은 전역 통계만 죽이고 국소 conv 경로 무손상(Fable C1 요구 충족).
- **✅ RF=35 engine-measured 방전**: D=34 서 0.006(비영)·**D=36 서 정확히 0** ⟹ closed-form 파싱(embed_conv 2 + trunk dils(1,2,4,8)→30 + expert_conv 2 + 1 = **35**)과 **정확 일치**. Fable 이 "미검 mirror-claim"(#3800 verdict-integrity ①)이라 지목한 RF 수치가 **이제 engine-measured**.

**Fable A1 판정표 → PASS-inert 가지**(beyond-RF Δ 가 det-noise 아니라 **정확히 0**): "beyond-RF 아키텍처 부재"를 **no channel at all** 로 격상 ∧ **[[H_9562]] 의 outside D≥64 통제 arm blocker 해소** — live GN 하에선 0.44 floor 로 오염되지만 `--gn-freeze` 로 발사하면 수학적으로 깨끗한 null.

**⚠️ 정직한 scope**: 이건 **hidden-influence 채널**의 인과 격리지 **cement 된 verdict 재생이 아니다**(Fable A1 의 원 arm = H_9359/H_9304/H_9267 채점셋 재생 → `--gn-freeze` 를 `--xbind` 에 배선해야 = 미실행). 따라서 [[H_9612]](GN confound verdict 감사)는 **아직 DOA 아님** — bus 가 hidden 을 움직인 건 확증됐고, 그게 *cement 된 수치*를 움직였나는 별도 측정. inert 는 "beyond-RF hidden 경로 없음"이지 "그 bus 가 아무 verdict 도 안 건드렸다"가 아니다.
**scope**: clm303_clean(L4·E3) 1 ckpt · CPU · D≤56(win=64) · DIRECTIONAL(engine-native but 1-model).
**NEXT**: `--gn-freeze` 를 `--xbind` 에 배선 → H_9359/9304/9267 재생(A1 원 arm) · [[H_9613]] 순열불변 falsifier · [[H_9562]] 를 `--gn-freeze` 로 발사(깨끗한 outside null).

## 🎯 A1 원 arm 완료 — GN bus 는 SCORE 를 움직인다 (PASS-**live**, inert 아님 · 2026-07-16)
`--gn-freeze` 를 `--xbind` 에 배선(#3831 v0.15.17) 후 실행. cement 셋 manifest 가 없어(aiden 부재·state/ 가드) **더 직접적으로** A1 의 원 질문을 물었다 — "bus 가 SCORE 를 움직이나": arm 간 **beyond-RF(>35B) 문맥만** 다르고 near+query 는 **동일**한 2AFC manifest.

| arm | live \|Δmargin\| | frozen |
|---|---|---|
| **FAR** (beyond-RF>35 만 상이) | **1.477 nats** | **0.000000e+00** |
| NEAR (within-RF 만 상이 · **양성통제**) | 4.765 | **6.570**(살아있음 ✅) |

- **양성통제 PASS**: near 가 live·frozen 둘 다 margin 이동 ⟹ 계기가 score 를 읽고 있고 동결이 국소경로를 안 죽임.
- **✅ A1 답 = PASS-live**: beyond-RF 문맥이 margin 을 **1.48 nats** 이동(near 효과의 ~31% — 작지 않음) · 동결 시 **정확히 0** ⟹ 그 이동은 **100% GN bus** 경유.
- ⟹ **Fable A1 판정표의 PASS-live 가지 발화**("any Δ ⟹ far-context verdict 는 GN-confounded → A2 발화") ⟹ **[[H_9612]] 는 DOA 아님 · LIVE**(앞선 내 inert 예상은 hidden-채널 결과의 과잉 일반화였다 — hidden 이 0 인 건 *동결 하*이고, **live 에선 bus 가 score 까지 닿는다**).

**⚠️ 과대해석 차단(정직한 scope)**: 이건 bus 가 score 를 **움직일 수 있다**는 능력 확증이지 **특정 cement verdict 가 오염됐다**는 게 아니다 — 오염은 **arm 들이 beyond-RF 에서 서로 다를 때만** 물린다(문맥이 arm 간 동일하면 bus 기여가 두 arm 에 똑같이 실려 **대비에서 상쇄**). 잘 설계된 매니페스트 다수는 문맥을 arm 간 고정하므로 무사할 수 있다. **어느 verdict 가 실제로 물렸나 = [[H_9612]] 의 per-manifest 감사**(arm 간 beyond-RF 차이 유무 조사)가 할 일이고, 이 실험은 그 감사에 **쓸 크기(1.48 nats)와 절제 도구**를 줬다.
**scope**: clm303_clean 1 ckpt · CPU · T=64/RF=35 · 합성 2AFC(cement 셋 자체 재생 아님) · DIRECTIONAL.

## 상태
🟢 EXECUTED (DIRECTIONAL·1 ckpt) — 계기 PASS + hidden-채널 인과격리(frozen beyond-RF=정확히 0·RF=35 방전) + **A1 원 arm 완료=PASS-live**(bus 가 SCORE 를 1.48nats 움직임·frozen 0·양성통제 통과) ⟹ H_9612 LIVE. **distinct-from-kills:** 'floor=long-range bus' kill 의 역 — bus 를 삭제해 load-bearing 검정. RF 무수정(H_1584 깊이 아님).
