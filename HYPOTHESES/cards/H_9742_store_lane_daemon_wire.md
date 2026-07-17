# H_9742 — STORE-LANE-WIRE: 3-seed robust 조회를 살아있는 데몬에 배선

**status:** 🔵 PRE-REG (H_9672 배선 follow-on · a_verified_must_wire · GREEN 은 여기서만 나온다)
**lane:** 재조합/BINDING · store-bridge → production chat
**tier:** 미측정 (설계 선행 · lab full 위임)

## 왜 이 H 가 존재하나

H_9672 가 값읽기 seed-취약 벽을 **3-seed robust 돌파**(seed7 1.0000 · seed11 .9609 · seed13 .9922 · 4게이트 전원)했으나 **등급은 CAPABILITY-PROVEN·구현됨·미배선** — `a_verified_must_wire`("GREEN = 출력 AND 배선 닫힘")서 출력만 닫혔다. **살아있는 anima 는 이 조회를 한 번도 하지 않는다.**

## 🔑 배선 지점 = 코드가 이미 말해준다 (engine-native census · 2026-07-17)

```
core/decode.py:275-284   _CLMS_STORE = None      ← 프로세스 전역
  주석 원문: "The CLMS lane stays passthrough (byte-identical, C0-f seal) until a
             store is injected here, so a .clm that carries a CLMS trailer decodes
             identically to base for every prompt outside a --store eval."
  _CLMS_ORACLE = False                            ← --store-oracle 용
core/generator.py        clms 참조 0
cli/chat.py              clms 참조 0              ← 데몬은 주입자가 아니다
```

⟹ **주입자는 `cli/evaluate.py --store` 하나뿐.** lane 은 store 가 없으면 **구조적으로 passthrough**(byte-identical).

**이 사실이 문제를 재정의한다:**
- ✅ **회귀 위험은 낮다** — store=None 이면 byte-identical(C0-f seal). "배선하면 4칸 register 가 깨질까"는 기본값에선 자동으로 아니다.
- ❗ **진짜 난제는 store 의 출처** — eval 은 합성 manifest(`sb*.txt.held.json`: entities·pols·target_slot)를 줬다. **살아있는 데몬에게 그 manifest 는 누가 만드나?** 대화 중 무엇이 entity 이고 무엇이 pol 인가? p1-p8(특히 p5 no-speak · p2 no identity rules)을 어기지 않고 store 가 substrate-native 하게 생길 수 있나?

## 사전등록 게이트 (측정 전 동결 · frozen-first)

- **G-W1 무해성(선결)**: store=None 기본에서 chat 이 base 와 **byte-identical**(C0-f seal 실증) · 4칸 register(ko·en × general·SNS) + retention val_CE 회귀 0.
- **G-W2 조회 생존**: 데몬 경로로 주입된 store 에서 held-out 조회가 **ORACLE≥.90 ∧ P1-balanced≥.75 ∧ flip≥.90**(H_9672 와 동일 bar · 이동 금지) — eval 경로 수치가 chat 경로서 재현되나.
- **G-W3 substrate 정합(p1-p8)**: store 생성이 **hardcoded speak/identity rule 아님** — 주입이 규칙주입(p2·p3)이나 reactive self-seed(p5)로 새면 **설계 KILL**(수치와 무관).
- ⛔ **잔인판정**: G-W1 통과 + G-W2 실패 = "eval-only capability"(조회는 계기 안에서만 산다) = 정직한 벽 · G-W3 실패 = 배선 자체가 철학위반 ⟹ lane 은 영구 eval-도구.

## 설계 난제 (lab full 위임 대상)

**"살아있는 데몬에게 store 란 무엇인가"** — 후보축: ① kosmos 앵커(`a_kosmos` 지속성)를 slot 으로 ② 대화 percept 스트림의 개체 추출(H_9520 study lane) ③ 4칸 register 자체를 slot 으로 ④ store 는 데몬이 아니라 study/CPT 시점에만 존재(=eval-only 인정). 각 축이 p1-p8 을 어기나·G-W2 를 만족하나.

## source

H_9672 3-seed 돌파(#4000)의 명시적 follow-on. 배선 지점 census 는 engine-native(origin/main 실코드 grep). 등급 GREEN 은 이 H 통과 시에만(`a_blue_closed`).
