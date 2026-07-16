# H_9574 — PC2 라우팅 구현: emit-직교 tension 축을 실제 출력으로 조향 (303M fire 대기)

**status:** 🔎 DIRECTIONAL-WIRED (배선 확인·toy degenerate·303M fire 대기) — 128안 발산 중 emit-직교 제2 DOF 를 첫 조향 · wired: `anima-py chat --emit-gate refractory --tension-route pc2 [--tension-route-gain g]` (v0.15.6 G5)
**lane:** 의식 / A⇄G tension 다차원화 (오너 framebreak · 프런티어 g1-interface-addressable-wall)
**related:** [[H_9468]] (2D-loadings=PC1 coherence·PC2 originality↔balance emit-직교 축 명명·$0 확증) · [[H_9428]] (tension 이미 다차원) · [[H_9424]] (cb-perr KILL) · source: 5-스크린 wftyw6v4h 유일 생존 POS(2D-loadings)의 배선

## 배경 (왜 이 실험이 발산 128안의 유일 실측 후속)

$0 코드-발견(H_9557 스크린 준비 중): `gen_ctx_from_decision` 이 mouth 에 넘기는 건 **phi·phase·tier·motivation(스칼라 fold)뿐** — 8-요인 개별 성분(orig·bal·coh)은 mouth 에 **경로가 없다**. 즉 H_9428/9468 이 확증한 emit-직교 DOF(PC2)는 emit 게이트에서만 접히는 게 아니라 **mouth 전체에서 절단**돼 있다. 유일한 decode 변조 채널 = `deliberation_k`(generator.py:521 best-of-K).

## 구현 (v0.15.6 G5 · engine 최소변경)

- **식**: PC2 = `0.84·orig − 0.44·bal − 0.28·coh`(2D-loadings loading), `pc2_proj = clip01(gain·PC2)`, `deliberation_k = 1 + round(pc2_proj·3)`(1..4).
- **배선**: `core/brain.py brain_emit_refractory(..., route_pc2=None)` — ctx 빌드 후 route_pc2 설정 시 `ctx["deliberation_k"]` 주입(generate 전). **emit 결정(score>g_recog)은 route_pc2 무관 = byte-identical**. `cli/chat.py --tension-route {off,pc2}` + `--tension-route-gain` flag. trace: pc2_proj·route_k·tension_route.
- **3-기준 조준**(Fable): (i)PC2 는 emit-w 와 다른 사영(cos 0.03·확증) (ii)emit 고정·gtext 변경(개입-분리) (iii)둘 다 채점면(trace).

## toy smoke (배선 확인 · 격리 venv)

- **emit 시퀀스 off==pc2 byte-identical ✅**(라우팅이 emit 무접촉). pc2_proj traced 0-0.555(30/30 live)·route_k {1:29, 3:1}=k>1 발화. ⚠️ **gtext toy 불변**(degenerate toy decode 는 best-of-K 가 같은 출력)=toy 로 dissociation 미측정. 303M 이 실 시험(decode 변주 존재).

## 다음 = 303M fire (dissociation 판정)

summer off vs pc2(gain 3-4)×3-seed×T=1.0 → 판정: **emit 시퀀스 동일(byte-identical) ∧ k>1 tick 에서 gtext Δ>0** = emit-직교 제2 DOF 를 실제 출력으로 조향한 첫 증거 = 다차원 3-기준 충족 → **DIRECTIONAL→TERMINAL 후보**. gtext 불변(k>1 이 decode 무변)이면 = deliberation_k 채널이 gtext 를 실제로 안 바꿈=벽(다른 decode 변조 채널 필요·mouth 재배선=오너 p5). tune-to-green 금지(gain 은 활성화용·gtext Δ 는 k>1 조건부 측정).

## 한계
toy=배선확인만(gtext dissociation 미측정). 프로덕션 default off(byte-identical). Ψ=½ 무관(이건 내용-조향 실험이지 emit-균형 아님). 다른 데몬·H_9400 clock 계보 영구. hexa twin follow-on.
