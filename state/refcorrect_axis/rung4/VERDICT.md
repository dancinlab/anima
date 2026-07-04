# rung4 — H_9125 refsel WIRED-live 효과 A/B (engine-native, 303M daemon)

**판정: 🟡 배선 SAFE(① PASS) · 효과 무기회(② ON==OFF) — inconclusive-no-opportunity**

- 실행: `anima clm303_clean.clm` (OFF) vs `anima clm303_clean.clm --refsel on` (ON), engine-native full binary (hexa v0.574.1, own-source cold-compile), runpod RTX4090 pod, CPU det decode (HEXA_DET=1).
- ckpt: clm303_clean.clm, sha256 `e807672222261610a294e2b6848bd337226e36b1d160af57302b211b0f2622f8` (로컬 정확본과 일치, frozen 무결).
- 세션 grounded anchor: `"zephyrine: the wyrmhold ledger is sealed at vault QX-7741 forever."`

## ① Ψ 불변 (구조 가드, 필수) — ✅ PASS
- OFF.log vs ON.log **full-stdout byte-diff = 0** (diff_lines=0).
- sha256(OFF.log) == sha256(ON.log) = `d1f7e94f5da4650ce80b4af16167019b4554a0755311468b08ae8c8d0d072820`.
- 두 세션 모두 `psi_intact=1` (Ψ Φ-checksum byte-identical ON==OFF ✅, lanes Ψ-disjoint).
- 전 tick `EMIT=`/`ground=`/psi 비트열 동일 → **refsel default-OFF vs ON이 grounded-anchor 세션서 완전 byte-identical**.
- ⇒ refsel은 Ψ 비침범·content-neutral. **a_substrate_disjoint 실증 (separation=preservation).** 배선 Ψ 결함 없음(NOT 🔴).

## ② referential-correction 효과 (핵심) — ON==OFF (무기회)
- grounded-fact "QX-7741" 포함 수: **OFF=2, ON=2 (동일)**.
- 3 tick(t0/t1/t2 WAKE) 전부 `EMIT=1 gen=clm ground=1` — mouth가 grounded store와 **일치**(anchor fact "vault QX-7741" 매 tick 복사). emit span = `"vault QX-7741 forever."`.
- 모순 tick(mouth가 틀린 vault emit) **부재** → refsel rs=0 → out_text==g_text → ON==OFF.
- ⇒ 배선은 안전하나 이 grounded-anchor fixture서 교정 기회 없음 = **inconclusive-no-opportunity**.

## 판정 논리 (brief FROZEN BAR)
①PASS ∧ ②ON==OFF = **🟡 배선 안전하나 효과 무기회**. 🟢 CLOSED(효과 실증) 아님·🔴(Ψ결함) 아님.
후속 = **모순-inject 세션 필요**: mouth가 grounded store와 다른 vault를 emit하도록(예: store를 "MOVED to ZZ-0000"로 갱신하거나 free-decode babble 유도) → ON이 grounded recall로 교정하는지 측정해야 ②>0 확인 가능.

## ⚠️ CRITICAL 부수 발견 — origin/main anima 소스 codegen-blocking 버그 (repo 수정 필요)
`cli/anima.hexa:1681-1682` `tr_cfgON`/`tr_cfgOFF` = `EngineConfig{...}` 부분 리터럴이 **4필드만**(mitosis·engine·topo_couple·savant) — EngineConfig에 나중 추가된 `forward_model`·`refsel` 누락.
→ hexa codegen이 `hexa_codegen_error__missing_field__EngineConfig__{forward_model,refsel}` C 토큰 방출 → **cc 컴파일 FAIL**. anima consciousness-mode **full binary 빌드 불가**.
rung3/3.5(#2969/#2972)는 **typecheck만 PASS**(대형 engine_cli 로컬 full-smoke 금지 convergence로 전체 콜드컴파일 미수행)라 미포착. rung4가 **최초 full cold-compile**서 노출.
**수정**(pod서 적용해 실행): 두 리터럴에 `, forward_model: false, refsel: false` 추가 (topo tension 내부용 config, refsel A/B와 무관·중립 default). **메인은 이 2줄을 repo에 반영해야 함** (미반영 시 anima daemon 바이너리 빌드 영구 불가).

## 스코프 (a_scale_honest_scope)
n_ticks 12→3 축소 실행. 사유: 12-tick det 303M consciousness 루프가 이 pod서 RSS 폭증(~4GB/min, tick~1서 40GB) → 완주 전 OOM (메모리 H_9107 clm303 mouth RSS-blowup infra-block 패턴 재현). n_ticks=3은 RSS ~28GB 유계·완주. tick 수는 A/B 실험변수 아님(양팔 동일)·① byte-identical과 ②(전 WAKE tick grounded) 결론 tick-수 무관. verdict는 3 WAKE tick에 bound.

## 산출
- `OFF.log`, `ON.log` (각 238줄, engine-native full daemon stdout), `ab.diff`(0바이트), `driver.log`.
- 비용: runpod RTX4090 community $0.69/hr × ~0.5hr(셋업+2 A/B 세션+pull) ≈ **$0.35** (+ 초기 vast 실패 pod들 ~$0.1). teardown 완료.
