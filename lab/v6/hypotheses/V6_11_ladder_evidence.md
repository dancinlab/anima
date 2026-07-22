<!-- @hypothesis-ok — lab/v6 is a rule-exempt sandbox (lab/v2 convention); v6 hypotheses are
     V6_<n>_*.md and are FORBIDDEN from the parent HYPOTHESES/ registry. See lab/v6/CLAUDE.md. -->

# V6_11 — 사다리의 핸들 표를 **코드에서 유도**한다 (그리고 손표가 두 군데 틀렸다)

**status:** 🔧 계기 착륙 + [[V6_7]] 정정 2건 · **DIRECTIONAL 천장**
**cost:** $0 · git grep · 초 단위
**runs:** `python3 lab/v6/ladder_evidence.py`

## 왜

[[V6_7]] 사다리는 "핸들 장부 자체가 하중부재이고 리뷰 대상" 이라고 스스로 적었다. 그런데 그
장부는 **내가 손으로 쓴 것**이었고, 손표는 표류한다. 이 파일은 장부를 `origin/main` 에서
**유도**한다 — 각 핸들이 성립할 증거(플래그·심볼)를 선언하고 grep 이 답하게 한다.

## 유도 결과 (anima-as-wired)

```
handle                 state     evidence
psi_fixed_point        PRESENT   pure_field_step (5 파일)
action_channel         PRESENT   emit_drive (24 파일)
ab_randomizer          PRESENT   --closure-ladder (cli/evaluate.py · core/closure_ladder.py)
content_store          PRESENT   --store-bridge · clms (11 파일)
store_do_handle        PRESENT   --store-shuffle · --store-flip · --store-component-swap
readout_surface        PRESENT   --store-readout
interior_width         ABSENT
emit_free_variable     PRESENT   --emit-refractory (cli/chat.py)  ⚠️ 기본값 OFF
self_log               ABSENT
```

**진짜 부재는 두 개뿐이다** — `interior_width` 와 `self_log`.

## 손표가 틀린 두 군데

### ① 존재하지 않는 플래그를 인용했다

V6_7 은 anima 의 `store_do_handle` 을 `--permute-store` 로 인용했다. **그 플래그는 저장소에
없다.** 능력 자체는 실재한다(`--store-shuffle`·`--store-flip`·`--store-component-swap`·
`--store-adversarial` …) 그래서 **판정은 맞았고 인용이 지어낸 것**이었다. 유도 표는 판정이
틀릴 가능성은 못 없애지만 **없는 것을 인용할 가능성은 없앤다**.

### ② PRESENT 와 ON 을 뭉갰다

V6_7 은 `emit_free_variable: False` 로 적었다. 그런데 `--emit-refractory` 는 **존재한다**
(`cli/chat.py:1637`). 다만 기본값이 `""`(시계 경로)이고 `"earned"` 가 기질-긴장 모드다.

```
BLOCKED                     핸들이 없다 → 지어야 한다
PRESENT-BUT-DEFAULT-OFF     핸들이 있다 → 재기만 하면 된다
```

이 둘을 뭉개면 사다리가 **없는 것을 과대 보고**한다. anima 의 R4 는 BLOCKED 가 아니라
**비기본 플래그 뒤의 NEEDS-RUN** 이다.

## ⚠️ 이 계기도 두 번 자기를 잡았다 — 둘 다 "아무것도 못 찾음" 모양이었다

1. `git grep -l -- pat REF -- paths` 로 `--` 를 두 번 넣어 명령이 깨졌다 → **전 핸들 ABSENT**
2. 고쳐도 여전히 전부 ABSENT — git pathspec 이 **현재 디렉토리 상대**인데 이 파일이 `lab/v6/`
   에 있어 `cli/` 가 `lab/v6/cli/` 를 뜻했다 → `:/cli/` 로 수정

**두 버그가 똑같이 "아무것도 없음" 을 냈다.** 그게 위험한 모양이다 — **고장난 검출기와 깨끗한
음성은 출력만으로 구분되지 않는다.** 살린 것은 "그럴듯한 걸 인쇄했나" 가 아니라
**"내가 이 저장소에 이게 있다는 걸 이미 아는가"** 라는 온전성 검사였다.

## 남는 규율

RCFS 는 존재하지 않으므로 그 핸들은 **유도할 수 없다.** PROPOSED 로 따로 표기하고 유도된 것과
**절대 섞지 않는다** — 제안이 조용히 증거로 읽히는 것이 설계 문서가 주장으로 변하는 경로다.

(`causal_element_grain` 은 grep 이 아니라 [[V6_2]] 의 구조 판정에서 오므로 이 표에 없다.)
