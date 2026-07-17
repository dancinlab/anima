# H_9695 — R3 교량절단: read→mouth 배선만 격리 (write 전에 · 계기)

**status:** 🔵 PRE-REG (lab full · **Sol 2위** · Fable 미제시 = NOVEL) · not-terminal · **주장 상한 = "READ→MOUTH REACHABLE", G6 verdict 아님**
**lane:** G6/ρ·fan · 배선 계기 **related:** [[H_9672]] · [[H_9696]] (본체) · [[H_9693]]

## 물음 (Sol 의 핵심 통찰)

**write+read 를 한 번에 넣으면 실패 위치를 모른다.** 먼저 evaluator 가 동일 G6 frame 에서 concept pair·관계를 store 에 넣되(**frame-oracle**), `"=> "` 없이 **매 생성 위치에서 CLMS 활성화** — 이는 완성된 G6 해법이 아니라 **"작동하는 lookup 이 mouth logits 에 들어가면 생성이 실제로 변하는가"를 격리**하는 실험.

## 조작

`anima-py evaluate <clm> --g6 --g6-store frame-oracle --store-query every-token --store-fuse nonlinear-full-vocab --gen 40` · 대조: `--g6-store off | --g6-store-key-scramble | --g6-store-value-scramble | --g6-store-role-scramble`.

## 게이트

- 동일 seed 서 **store off ↔ intact 생성이 ≥2/3 seed 달라져야** 함.
- intact 의 `fals_bound` 가 scramble 3종 최대치보다 **seed 평균 ≥1.0 idea 높아야**.
- **key/value/role scramble 모두 collapse 필수** — 하나만 무너지면 단순 lexical bias 가능성 잔존.
- `--g6-store off` = base ckpt 와 **byte-identical seal**.

## ⚠️ kill-list 접촉 (Sol 명시)

**evaluator 가 frame→store 변환을 하므로 #1(스캐폴드)과 접촉한다.** ⟹ **이 arm 의 G6 GREEN 은 절대 verdict 가 될 수 없다.** 허용 주장은 오직 **"read→mouth 배선이 살아있다/죽었다"** 뿐. #7 회피=동적 주소+GELU 융합.

## 최대위험

**oracle frame parser 자체가 필요한 결합을 미리 수행**하는 것(가장 쉬운 오도). 이 실험은 [[H_9696]] 의 비싼 write/read 구현 **전에 쓰는 배선 계기로만** 살아있다.

## falsify
🟢 READ→MOUTH REACHABLE(배선 살아있음 → H_9696 진행 정당) | 🧱 store 주입해도 생성 불변 = 배선 死(H_9696 발사 금지·재진단).

## source
lab full Sol 2위(NOVEL · Fable 미제시) · 단계적 사망지점 격리.
