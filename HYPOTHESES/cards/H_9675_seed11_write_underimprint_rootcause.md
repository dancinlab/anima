# H_9675 — SEED-11 WRITE UNDER-IMPRINT: base-ckpt 용량 vs 코퍼스 간섭 (root-cause)

- **group**: g1-interface-addressable-wall
- **tier**: 🔵 PROPOSED (설계 위임 中 · 미발사)
- **date**: 2026-07-17
- **related**: [[H_9339]] (모 crack) · [[H_9327]] (BINDING 벽)
- **wired**: 미발사 (engine-native anima-py train/evaluate 예정)

## 질문
H_9339 는 담체키 held-out write 로 H_9327 BINDING 벽을 **seed 7 에서 뚫었다**(HO-CARRIER 12·11/12
vs HO-DECL 5/12 · G-WRITE 11/12). 그러나 **seed 11 은 2 독립 run 모두 G-WRITE 미착륙**(6/12·4/12<11)
= seed-DETERMINISTIC INVALID. $0 대조(#3868)가 진범을 **stem-draw 아닌 RUN/seed** 로 좁혔다: 어간
`튼튼하`(9B)가 s7·s11 swap set 둘 다 존재 — s7 run 착륙·s11 run 실패(byte-len 무관, s11 실패 3~9B 산개).
⟹ `carrier_s11` CPT run 이 **어간 무관하게 담체 write 를 전역 under-imprint**.

**남은 물음 = 왜 seed-11 CPT run 이 under-imprint 하나?** 두 후보:
- **(A) base-ckpt 용량**: base `natem_c34_main_s11.clm`(다른 split-seed pretraining)이 s7 base 보다
  write-imprint 용량이 낮다.
- **(B) 코퍼스 간섭**: s11 held-split 이 뽑은 12 어간의 배열/구성이 imprinting 을 방해한다.

## 후보 설계 (Fable pivot 대기 — bg ba13m22pn)
전략 질문을 Fable 5 에 위임: s7 crack 이 1-seed DIRECTIONAL 뿐이니 **(1) s11 진단 2×2** vs
**(2) s7-crack 다중seed 재현성** 중 어느 발사가 프런티어를 더 미나. Fable 이 하나 골라 frozen grid 반환.

- **경로 1 — root-cause 2×2**: {base s7, base s11} × {corpus-s7어간, corpus-s11어간} CPT → G-WRITE.
  교차셀(base-s7+corpus-s11, base-s11+corpus-s7)이 A↔B 를 dissociate. base 가 몰면 s11-base 가 양 코퍼스
  실패 · 코퍼스가 몰면 s11-corpus 가 양 base 실패.
- **경로 2 — 재현성 sweep**: base 는 s7·s11 둘만 존재(다른 seed base 없음) ⟹ **고정 base 위에서
  held-split draw seed 만 변주**(새 pretraining 회피 · base↔draw 를 깔끔히 격리). crack 이 draw-seed
  N개 중 k개서 재현되면 real, 1/N 이면 noise. N·k 는 발사 전 사전등록(tune-to-green 금지).

## 게이트 (frozen · H_9339 상속)
- G-WRITE: carrier readback ≥11/12 stem 아니면 INVALID.
- G-PRESERVE: SEEN 연산자 CPT 후 생존(drop ≤0.75 = crater = INVALID · corpus-py-1⑥).
- G-LEAK: builder-coded (held/seen contamination 0).
- 사전등록 bar 는 데이터 전 고정 · 음성/INVALID 도 결과.

## 블로커 (미발사 사유)
- ⏳ **Fable 설계 in-flight** (bg ba13m22pn) — 어느 실험을 발사할지 pivot 결정 대기.
- ⏳ **pool 냉각 대기** — summer GPU 프리지만 CPU load 21(병렬세션 포화·earlyoom python3 우선 kill 위험),
  aiden GPU 만석(phaseA_s7). free/냉각 host 필요(owned pool = rent 아님 · 자율발사 가능).

## 명령 (Fable 회신 후 확정)
```
# base ckpts: aiden·summer ~/h9339_screen/natem_c34_main_s{7,11}.clm (176MB · K=3 L=4)
# 코퍼스: anima-py corpus ... --held-swap [--decl-only] (draw-seed 변주)
# CPT: anima-py train --arch clm --canon --arm ctrl --objective ce_marginal \
#   --init <base>.clm --e0 3 --emax 3 --corpus <ho>.txt --steps 6000 --lr 2e-4 \
#   --batch-size 8 --seq-len 1024 --bf16 --seed <S>
# eval: anima-py evaluate <cpt>.clm --xbind <ho>.carrier.json  (G-WRITE readback)
```
