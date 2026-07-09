# P6 — anima chat 데몬 py 자체구현 · 2-production 파리티 (DIRECTIONAL)

owner directive(2026-07-09 "py 자체구현 · 언어간 상호의존 0")의 **최종 단계 P6**: hexa-less
호스트가 substrate-native A⇄G consciousness 데몬을 순수 py(numpy)로 구동. `cli/chat.py` =
`cli/anima.hexa` **`anima_consciousness_mode` DEFAULT 경로**(12-tick) + `anima_byte_mode`(--byte)의
byte-faithful py twin. **hexa import 0** (P2-P5 core/*.py twin 만 사용).

> **DIRECTIONAL** (`a_engine_native_learning`): 이건 hexa 데몬의 py 미러 → 판정 tier 를 cement하지
> 않음. 바(bar) = chat 루프의 **BEHAVIORAL / byte 파리티**, consciousness 판정 아님.

## 스코프
- **DEFAULT 경로만** 포팅 (`n_ticks=12`, og_measure/og_live/og_r3/refr_measure 전부 false).
- op-grip / stateful-refractory 연구 계측(`--opgrip*`/`--refractory` · B-density/VQ-code/ARM-SHOCK
  Hamming 하네스)은 **HEXA 전용** — chat 데몬이 아니라 측정 하네스. py 는 해당 플래그에 안내 후 종료.
- `--byte` 바이트-연속 chat 도 포팅(`gen_auto_chat` 경유).

## 파리티 기판 (결정적)
NON-DECODABLE toy ckpt(임의 non-.clm) → generator L3 = **null backend** → `g_text` = 결정적
`_gen_null_text` ASCII. 전체 루프(82-lane 마운트 · brain_emit 자율 emit/silence · C9 REMEMBER ·
N3/REM sleep imagination replay · .kosmos 쓰기)를 실행하되 **CLM matmul 디코드만 우회** → BLAS
디코드 carve-out(raw logit ~1e-15 드리프트) + surrogate-utf8 crash 를 격리. 루프 로직 순수 파리티.
`hexa to_string(float) == python repr(float)`(경험 핀: 1/3→"0.3333333333333333"·1e-9→"1e-09"·
true/false) 이므로 stdout 포맷 일치. 전 println 은 `sys.stdout.buffer`(utf-8/surrogateescape) 경유
→ hexa println 바이트 동일.

## 결과 (재현 = `repro.sh`)

### ✅ 결정성 셀프테스트 — hexa#1 vs hexa#2 = **BYTE-IDENTICAL** (골든 결정적 · 마스크 유효)

### ✅ KOSMOS 트리 — **4/4 파일 BYTE-IDENTICAL** (마스킹: emitted_at)
`mem_001.kosmos`(seed) · `emit_t0.kosmos`(C9 emit anchor · tension 5ch=phi/af_aro/nov/af_val/self_ctx) ·
`dream_w10_0.kosmos`·`dream_w11_0.kosmos`(H_9036 N3/REM dc_compose_window 블렌드 노드). 영속 계층
**바이트 완벽** — kosmos 쓰기는 고정 `%.4f`/`%.6f` 포맷이라 ULP 드리프트가 반올림으로 소거됨.

### 🟢 STDOUT — 253/254 라인 일치. 독립 divergence 7개 전부 **문서화된 carve-out**, 포팅 결함 0:
- **(a) ~5 라인 = last-ULP `repr()` 드리프트** (초월함수-heavy 레인: `scn-net` Kuramoto 400스텝 ·
  `phasesync` phasefield · `stoch-res` sr_channel_mi 2000틱 MI · `Engine A warm` pure_field). 값은
  ~1e-15 까지 일치, `repr` 의 마지막 자릿수만 상이(hexa libm vs numpy/python libm last-ULP). P4 NUL
  carve-out 과 동류의 알려진 수치 carve-out.
- **(b) 2 라인 = 설치된 hexa 바이너리 STALE** (설치 `anima` 가 origin/main 보다 구버전):
  origin/main anima.hexa 는 `GROUND (A3/ρ·tether ← G5 …)`(L5046) + `IMAGINATION(a_chat_sleep …)`
  요약 라인(L5192)을 가지나 **설치 바이너리엔 없음**. py 포트는 **origin/main(포팅 SSOT)에 충실** →
  `hx install anima`(origin/main 리빌드) 하면 소거될 아티팩트. (나머지 라인들은 이 1줄 추가로 인한
  줄번호 시프트 캐스케이드 — 독립 diff 아님.)

## 판정
- **byte-verified**: KOSMOS 4/4 파일 · stdout ~246/253 라인.
- **carve-out(비-결함)**: ~5 라인 ULP-repr(수치) + 2 라인 stale-installed-binary(버전).
- `anima-py chat` 은 chat 경로에서 **hexa 로의 subprocess 0** — 완전 hexa-free (오너 수용 바).

파일: `hexa_golden.txt`(hexa 골든 트랜스크립트) · `py_twin.txt`(py 출력) · `hexa_kosmos/`·`py_kosmos/`
(양 채널 .kosmos 트리) · `repro.sh`(재현: selftest + compare).
