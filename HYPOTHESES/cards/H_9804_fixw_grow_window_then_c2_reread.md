# H_9804 — FIX-W GROW-WINDOW 선배선 → 배선된 store-bridge로 C2 bar 재판독 (계기벽 제거가 선행조건)

**tier:** 🔵 PROPOSED · DESIGN-ONLY (lab-full R11 divergence · DIRECTIONAL · NOT a verdict)
**group:** R11-instrument-prerequisite
**source:** lab full 2026-07-19 Fable A1 + 세션 저장소 실측 교정(H_6189 미배선 확인)
**wired:** no
**verdict:** PENDING (설계만 · 측정 0 · cement 는 engine-native `anima-py` 로만)

## claim
H_6189가 byte-math로 확정한 CLM-mouth 측정벽(T=24 우측정렬 decode 창 ⟹ composed seed 가시창이 single seed 창과 byte-identical ⟹ composed_distinct>max_single 이 모델 무관하게 물리적 불가)이 아직 미배선(core/·cli/ 에 T_win·clm_decode_topk_sampled_ranged 부재, 2026-07-20 grep 실측). ⟹ Fix-W(T_win=min(len(seed)+gen,512) ranged decode + echo-guard) 배선 후에야 H_9775 로 배선된 pairodd store-bridge 가 실제 C2 bar 를 움직이는지 판독 가능. Fix-W 전 CLM C2 판독은 전부 WINDOW-BOUND capability-INCONCLUSIVE.

## instrument
core/decode 에 ranged decode 신설(선례 bytegpt_decode_argmax_ranged) + `anima-py evaluate --grow-window` + echo-guard(seed 그대로 되뱉기=false-GREEN 차단). 판독=`--c2 --store-fuse {pairodd,none} --store-readout vocab`.

## controls (사전등록)
echo-guard(seed echo 비율 상한·false-GREEN 차단) · --store-fuse none 대조 · value-permute(H_9775 인증 통제) · ByteGPT mouth 교차판독(창 정합 mouth=$0 즉시 사전판독) · bar FROZEN(H_1129/H_1137 VERBATIM 무이동)

## falsify
Fix-W 후에도 composed_distinct(bridge-on) − (bridge-off) 가 0 이고 ByteGPT mouth 도 동일 ⟹ 다리가 생성경로엔 도달 못함(routing 벽 잔존). bridge-on < bridge-off ⟹ 간섭=substrate-preservation 자료(H_9798 로).

## cost
Fix-W 배선 $0(코드) + toy e2e 1회 + eval $0–5(pool)

## 정직 caveat (c9)
이 카드는 **방향성 설계**이지 검증된 결과가 아니다. lab-full 발산 산출 = DIRECTIONAL, 절대 verdict 아님
(`a_lab_full_diverge`). frozen bar 사후 이동 금지(tune-to-green 금지 · p7). 발사 전 **toy e2e 1회**
(exit 0 + 산출물 + 통제) 필수 — 한 번도 실행 안 된 계기는 버그 여럿 겹쳐 숨긴다
(`instrument-never-run-hides-multiple-bugs`). 음성도 결과다.

## related
H_6189 · H_9775 · H_9720 · H_9798
