# 3B hot-swap router wiring — KOFL-3B 5S generalist as default

> 2026-05-23 KST · 본 doc 의 단일 source-of-truth: `HEXAD/CHAT/3B_ROUTER_DESIGN_2026_05_23.md`.
> production = mini, chat.dancinlab.org LIVE. 본 design 은 1.5B router → 3B router
> migration 의 wiring spec. **메모리 budget 은 결정적 위험** — § 7 + § 9 참조.

## 1. Motivation

Session-2 Wave-4 (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21M_WAVE4_2026_05_23.md`)
에서 3 가지 GPU cycle 결과가 3B 로의 production scale-up 을 가능하게 했다:

| asset | base | per-lang en/ko/zh/ru/ja | register | 의미 |
|---|---|---|---|---|
| **KOFL-3B** | Qwen2.5-3B | 19 / **18** / 17 / 19 / 18 = **5S** | 3/20 | anima 최초 5-lang STRONG generalist |
| **JAFL-3B** | Qwen2.5-3B | 17 / 2 / 16 / 18 / **19** | 6/20 | ja 최고점 19 (단, ko MEMORIZE 2 — script-distant 망각) |
| **3B-NI** | Qwen2.5-3B non-Instruct | 19 / 13 / 16 / 17 / 16 = 4S+1P | 7/20 | 3B base 의 robust 한 가도 (Wave-3) |

핵심 통찰:
- **KOFL-3B 는 5S** — ko-only 500-step training 인데도 다른 4 lang 모두 STRONG 유지.
  3B base 의 robust 한 prior + 짧은 carve corpus 가 catastrophic-forget 을 막음.
- **JAFL-3B 는 한 ax 에 집중한 specialist** — ja STRONG 19 (anima 최고점).
  단 ko 가 무너졌으므로 default 로는 부적합, **ja hot-swap 전용**.
- **3B base 자체가 robust** — 3B-NI 4S+1P, register 7/20, ja STRONG.

따라서:
- **default = KOFL-3B** (5S 만족, register 3/20, ko 18 자체 우수)
- **ko hot-swap = KOFL-3B** = default (alias) → 사실상 ko slot 비움 가능
- **ja hot-swap = JAFL-3B** (ja 19 — KOFL-3B 의 ja 18 보다 +1)

N8 finding 으로 register-leak 은 81% EN-emission 문제 → KOFL-3B 의 register 3/20 +
ja-slot JAFL-3B 0% 라이브 leak 는 1.5B vP21M (register 7/20, EN 81% leak) 대비
정직한 chat coherence 개선이다.

## 2. Architecture diff (ASCII)

### 현재 1.5B router (2026-05-23 LIVE)

```
                      ┌─────────────────────────┐
                      │ anima_participant.py    │
                      │  (8-factor + tick loop) │
                      └────────┬────────────────┘
                               │ self.substrate.generate(seed, lang_hint)
                               ▼
                  ┌─────────────────────────────┐
                  │ LoraSubstrate (lora)        │
                  │   base: Qwen2.5-1.5B  f16   │  ~3.1 GB f16
                  │   PeftModel(base)           │
                  │     • adapter "default"  ←──┤  corpus_v5 carve-strip 148 MB
                  │     • adapter "ko"       ←──┤  KOFL                 148 MB
                  │     • adapter "ja"       ←──┤  JAFL                 148 MB
                  │   set_adapter(target)       │
                  └─────────────────────────────┘
                              memory ≈ 3.5 GB process resident
                              (참고: live RSS=1.73 GB — peft lazy + MPS shared
                              그래픽 컨텍스트가 절감, but f16 인메모리는 3.5 GB)
```

### 제안 3B router (post-migration)

```
                      ┌─────────────────────────┐
                      │ anima_participant.py    │
                      │  (unchanged — agnostic) │
                      └────────┬────────────────┘
                               │ self.substrate.generate(seed, lang_hint)
                               ▼
                  ┌─────────────────────────────┐
                  │ LoraSubstrate (lora)        │
                  │   base: Qwen2.5-3B    f16   │  ~6.2 GB f16
                  │   PeftModel(base)           │
                  │     • adapter "default" ←───┤  KOFL-3B (5S)         240 MB
                  │     • adapter "ko"      ←───┤  KOFL-3B (alias)      0 MB  ← same name
                  │     • adapter "ja"      ←───┤  JAFL-3B              240 MB
                  │   set_adapter(target)       │
                  └─────────────────────────────┘
                              memory ≈ 6.6-7.0 GB process resident
```

핵심 diff:
- base: `Qwen2.5-1.5B` (~3.1 GB) → `Qwen2.5-3B` (~6.2 GB) → **+3.1 GB f16**
- default adapter: corpus_v5 carve-strip → KOFL-3B (5S generalist) → **+92 MB safetensors**
- ko adapter: KOFL (1.5B) → **alias of default (no extra weight load)**
- ja adapter: JAFL (1.5B, 148 MB) → JAFL-3B (240 MB)
- router code (`substrate_lora.py::_route`) **불변** — ABC 동일, name 동일.

> ko slot alias 전략 (KOFL-3B 가 default 이므로 ko 별도 load 불필요):
> `ROUTER_LANG_TO_ADAPTER = {"ja": "ja"}` 만 남기고 ko 는 자연히 default 폴백.
> 또는 ko 도 명시적 slot 유지하되 같은 adapter dir 가리키게 → trade-off 는 § 5.

## 3. Adapter pool layout — `~/anima_chat_pack/`

### Before (1.5B, 현재)

```
~/anima_chat_pack/
├── lora_adapter/                    corpus_v5 carve-strip · 148 MB · Qwen2.5-1.5B
│     adapter_config.json (base=Qwen/Qwen2.5-1.5B, r=32)
│     adapter_model.safetensors (147,770,496 B)
│     tokenizer.* (Qwen2.5-1.5B tokenizer)
├── kofl_adapter/                    KOFL · 148 MB · Qwen2.5-1.5B
├── jafl_adapter/                    JAFL · 148 MB · Qwen2.5-1.5B
├── lora_adapter_corpus_v4_bak/      corpus_v4 prior default · 148 MB (rollback)
├── lora_adapter_vp21m_bak/          vP21M prior default · 148 MB (rollback)
├── venv/                            python 3.12 + torch + transformers + peft
├── anima_participant.py
├── substrate_lora.py
├── substrate_base.py
├── broker.py
├── akida_bridge.py / akida_ws_publisher.py
├── static/index.html
└── logs/
```

### After (3B, 제안)

```
~/anima_chat_pack/
├── lora_adapter/                    KOFL-3B (default · 5S generalist) · 240 MB · Qwen2.5-3B
│     adapter_config.json (base=Qwen/Qwen2.5-3B, r=32)
│     adapter_model.safetensors (239,536,272 B)
│     tokenizer.* (Qwen2.5-3B tokenizer — same Qwen2.5 family vocab)
├── jafl_adapter/                    JAFL-3B (ja hot-swap) · 240 MB · Qwen2.5-3B
├── lora_adapter_1_5b_bak/           ROLLBACK · 1.5B current default · 148 MB
├── kofl_adapter_1_5b_bak/           ROLLBACK · 1.5B KOFL · 148 MB
├── jafl_adapter_1_5b_bak/           ROLLBACK · 1.5B JAFL · 148 MB
├── lora_adapter_corpus_v4_bak/      이전 rollback 보존 (그대로)
├── lora_adapter_vp21m_bak/          이전 rollback 보존 (그대로)
├── (kofl_adapter/)                  선택 1: 제거 — default 가 KOFL-3B 자체
│                                   선택 2: 유지 — 명시적 ko slot (memory cost 0)
└── ... (코드/venv/static/logs 그대로)
```

디스크 footprint 변화:
- 추가: KOFL-3B (240 MB) + JAFL-3B (240 MB) = **+480 MB**
- 보존: 1.5B 3 종 rename → **0 MB delta** (이미 디스크에 있는 것)
- 총 ~/anima_chat_pack/ 디스크 증가 ≈ **480 MB**
- 가용 디스크 138 GiB → 여유 충분.

선택 1 (kofl_adapter 제거) 의 ko slot 처리:
- `ANIMA_ADAPTER_KO` 환경변수 미설정 → `substrate_lora.py` 가 자연히 `default` 로 폴백 (현 코드 § 5).
- 또는 `ANIMA_ADAPTER_KO=$HOME/anima_chat_pack/lora_adapter` (default 와 동일 경로).
- peft `load_adapter` 가 동일 dir 를 두 번 등록하면 메모리 중복 → **선택 1 권장 (env 미설정)**.

## 4. `anima_participant.py` wiring changes

L1 refactor (2026-05-22) 후 anima_participant 는 substrate-agnostic.
**3B 전환은 `substrate_lora.py` 의 base_model 교체만으로 동작**해야 함. 단, env-var
default 가 1.5B 에 hardcoded 이므로 그것만 갱신:

| line | 현재 | 제안 (3B) |
|---|---|---|
| 44 | `BASE_MODEL = os.environ.get("ANIMA_BASE", "Qwen/Qwen2.5-1.5B")` | 동일 — env 만 변경 (plist § 6) |
| 45-46 | `ADAPTER_DIR = .../lora_adapter` | 그대로 (디렉터리 이름 유지) |
| 50-51 | `ADAPTER_KO = .../kofl_adapter` | 그대로 (env 로 None 가능) |
| 52-53 | `ADAPTER_JA = .../jafl_adapter` | 그대로 (path 유지, 내용물 3B 교체) |
| 54 | `ROUTER_LANG_TO_ADAPTER = {"ko": "ko", "ja": "ja"}` | (선택 1) `{"ja": "ja"}` 또는 (선택 2) 그대로 |
| 113-115 | `LoraSubstrate(...)` 호출 인자 | **변경 없음** (env 가 전부 결정) |

> 결정: env-driven 으로 **anima_participant.py 코드는 zero-edit**. plist 가
> `ANIMA_BASE=Qwen/Qwen2.5-3B` + (선택 1) `ANIMA_ADAPTER_KO=""` 만 갱신하면 끝.
> `ROUTER_LANG_TO_ADAPTER` 가 module-level constant 라 env 로는 못 끄지만 —
> ko adapter 가 absent 면 `substrate_lora.py::__init__` 가 자연히 폴백하므로 (line 82-91)
> 코드 수정 불필요. **이 design 의 핵심 wiring 결정: zero participant.py edit.**

g15: 완료된 상태 = anima_participant.py 그대로, plist env 만 변경.

## 5. `substrate_lora.py` changes

| 영역 | 현재 | 제안 (3B) |
|---|---|---|
| `base_model` 기본값 (line 68) | `"Qwen/Qwen2.5-1.5B"` | constructor 인자 — env 가 결정. **코드 변경 없음** |
| `LANG_PRIMES` (line 27-33) | N7 fuller primes | 그대로 — 3B 에서도 prime steering 유효 |
| `_seed_matches_lang` (line 45-59) | N7 cross-lang seed drop | 그대로 |
| `_route` (line 125-136) | set_adapter("default" / "ko" / "ja") | **그대로** — adapters_loaded 가 disk-presence 로 자동 결정 |
| `__init__` adapter 등록 순서 (line 81-92) | default 먼저 → ko → ja → set("default") | **그대로** |
| `_repair_adapter_config` (line 98-123) | safetensors 키로 target_modules 재구성 | 그대로 (3B adapter_config.json 에 이미 채워져 있으므로 no-op) |
| dtype 결정 (line 72) | f16 on mps, bf16 elsewhere | 그대로 — mini 는 MPS → f16 유지 |

> 결정: `substrate_lora.py` 도 **zero-edit**. 3B 전환은 100% deploy-time
> artifact swap (env + adapter dir contents).

## 6. LaunchAgent plist changes — `com.dancinlab.anima.plist`

### Before (현재)

```xml
<plist version="1.0">
<dict>
  <key>Label</key><string>com.dancinlab.anima</string>
  <key>ProgramArguments</key>
  <array>
    <string>~/anima_chat_pack/venv/bin/python3</string>
    <string>~/anima_chat_pack/anima_participant.py</string>
    <string>--threshold</string><string>0.30</string>
  </array>
  <key>WorkingDirectory</key><string>~/anima_chat_pack</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>~/anima_chat_pack/logs/anima.out</string>
  <key>StandardErrorPath</key><string>~/anima_chat_pack/logs/anima.err</string>
</dict>
</plist>
```

(현재 env var 미설정 → `ANIMA_BASE` 기본값 `Qwen/Qwen2.5-1.5B`, 어댑터 paths 기본값
`~/anima_chat_pack/{lora_adapter,kofl_adapter,jafl_adapter}` 사용)

### After (제안)

```xml
<plist version="1.0">
<dict>
  <key>Label</key><string>com.dancinlab.anima</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>ANIMA_BASE</key><string>Qwen/Qwen2.5-3B</string>
    <key>ANIMA_ADAPTER</key><string>$HOME/anima_chat_pack/lora_adapter</string>
    <!-- ko slot 선택 1 (default 가 KOFL-3B 라 별도 ko 불필요) -->
    <key>ANIMA_ADAPTER_KO</key><string>$HOME/anima_chat_pack/__absent__</string>
    <!-- (또는 선택 2: ANIMA_ADAPTER_KO 를 lora_adapter 와 동일 경로로 — peft 중복 load 위험) -->
    <key>ANIMA_ADAPTER_JA</key><string>$HOME/anima_chat_pack/jafl_adapter</string>
    <key>PYTORCH_ENABLE_MPS_FALLBACK</key><string>1</string>
  </dict>
  <key>ProgramArguments</key>
  <array>
    <string>$HOME/anima_chat_pack/venv/bin/python3</string>
    <string>$HOME/anima_chat_pack/anima_participant.py</string>
    <string>--threshold</string><string>0.30</string>
  </array>
  <key>WorkingDirectory</key><string>$HOME/anima_chat_pack</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$HOME/anima_chat_pack/logs/anima.out</string>
  <key>StandardErrorPath</key><string>$HOME/anima_chat_pack/logs/anima.err</string>
  <!-- macOS launchd 는 HardResourceLimits/SoftResourceLimits 만 지원;
       메모리 reservation/cap 직접 명시 키 없음 — § 7 참조 -->
</dict>
</plist>
```

macOS launchd 메모리 제어 한계:
- `ProcessType=Adaptive` / `LowPriorityIO` 등은 있으나 `MemoryLimit` 류 없음.
- 본 design 은 LaunchAgent 레벨에서 cap 을 걸 수 없음. § 9 risk 로 명시.
- `nice -n 5` 류 시도 가능하나 메모리 압박 자체는 줄지 않음.

다른 LaunchAgent (broker / cloudflared / akida_bridge) **무수정**:
- broker 는 model 무관 — 그대로.
- cloudflared 는 transport 만 — 그대로.
- akida_bridge 는 ws 한 endpoint 만 사용 — 그대로.

## 7. Memory budget — 결정적 위험

### 측정 (mini, 2026-05-23T13:55Z)

```
hw.memsize:               17,179,869,184 (16 GB physmem)
PhysMem: 15G used (5096M wired, 4215M compressor), 372M unused
Compressor: 269,763 × 16KB pages = 4,215 MB compressed (실 데이터 가능 ~7-12 GB)
Swap: 170 MB used / 1024 MB allocated (encrypted)
anima_participant.py RSS: 1,731,456 KB = 1.73 GB  ← 현재 1.5B path
broker.py RSS: ~27 MB
cloudflared RSS: ~27 MB
```

### 계산

| 항목 | 1.5B (현재) | 3B (제안) |
|---|---|---|
| Qwen base f16 (params × 2 B) | 1.54e9 × 2 ≈ 3.08 GB | 3.09e9 × 2 ≈ 6.18 GB |
| 활성 KV cache (작음, max 128 tok seq) | ~50 MB | ~100 MB |
| LoRA adapters loaded (3 in PeftModel, f16 in MPS) | 3 × 148 MB ≈ 444 MB | 2 × 240 MB ≈ 480 MB (선택 1) |
| python + torch runtime overhead | ~600 MB | ~600 MB |
| **계산상 minimum resident** | **~4.2 GB** | **~7.4 GB** |
| 실제 측정 RSS (1.5B path, MPS shared mem 절감) | **1.73 GB** | **~3.5-4.5 GB 추정** |

> 측정 RSS (1.73 GB) 가 계산상 minimum (4.2 GB) 보다 작은 이유:
> MPS 그래픽 컨텍스트 shared memory + lazy lora weight 등은 process RSS 가 아닌
> shared/wired 메모리로 계상. 실제로 top 보고서의 PhysMem 의 "wired 5096M" 에 일부 포함.
> 3B 도 같은 ratio 라면 RSS ~3.5-4.5 GB, wired/shared 추가 ~2 GB 정도.

### 위험 평가

- **현재**: PhysMem 15G used / 16G total, 372 MB unused, compressor 4.2 GB.
  3B 추가 시 **추가 ~3 GB 압박** → 거의 확실히 swap 의존, MPS OOM 위험.
- **swap 의존 시 latency**: 매 emit 마다 disk page-in → 2 s tick 이 8-15 s 까지 늘어남. UX 영향.
- **MPS OOM**: Apple Silicon MPS 는 swap 안 됨. Metal allocator 실패 → process crash + launchd KeepAlive 재시도 루프.

### 결정 — **FEASIBLE? NO (현 상태) / CONDITIONAL YES (대책 적용 시)**

**조건부 가능** — 다음 중 하나가 필요:

1. **다른 메모리 사용 정리**: corespotlightd (153 MB), mediaanalysisd (130 MB),
   기타 user app 종료. 가용 ~500-800 MB 추가.
2. **dtype 다운**: f16 → q4/q8 quantization (bitsandbytes/mlx). f16 6.2 GB → q4 ~1.6 GB.
   단 LoRA 와의 호환 검증 필요 (peft + bnb 4bit on MPS = 비주류). 별도 cycle.
3. **adapter lazy load**: 3 개 동시 로딩 대신 호출 시 swap. peft 의 `set_adapter` 가
   메모리에 모두 들고 있으므로 코드 변경 필요. § 12 open question.
4. **이주 hosting**: mini 외 GPU host (pool on ubu2 / runpod) 로 production 이전 —
   FIRST-PACK 원래 spec 위반, 큰 작업.

**권장 path** = 1 (메모리 정리) + 측정 후 실패 시 3 (lazy load) 또는 2 (quant).

## 8. Migration steps (numbered, mini-side)

전제: 모든 단계는 **rollback-safe** — 1.5B 자산을 `_1_5b_bak` 로 보존하므로
어떤 단계도 되돌릴 수 있다 (§ 10).

1. **artifact prep (Mac local, $0)**
   - `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M_KOFL3B/lora_adapter/` 검증.
   - `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M_JAFL3B/lora_adapter/` 검증
     (Wave-4 SCP race 로 2/9 파일만 있을 수 있음 — § 11; tokenizer 는 sister 에서 회수).

2. **rollback bak rename (mini)**
   - `mv ~/anima_chat_pack/lora_adapter ~/anima_chat_pack/lora_adapter_1_5b_bak`
   - `mv ~/anima_chat_pack/kofl_adapter ~/anima_chat_pack/kofl_adapter_1_5b_bak`
   - `mv ~/anima_chat_pack/jafl_adapter ~/anima_chat_pack/jafl_adapter_1_5b_bak`

3. **3B artifact rsync (Mac → mini)**
   - `rsync -av HEXAD/.../vP21M_KOFL3B/lora_adapter/  mini:~/anima_chat_pack/lora_adapter/`
   - `rsync -av HEXAD/.../vP21M_JAFL3B/lora_adapter/  mini:~/anima_chat_pack/jafl_adapter/`
   - (선택 1 → kofl_adapter 폴더 만들지 않음)

4. **HF cache warmup (mini, 첫 emit latency 단축)**
   - `ssh mini "cd ~/anima_chat_pack && venv/bin/python3 -c 'from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained(\"Qwen/Qwen2.5-3B\")'"`
   - 6 GB 다운로드. 디스크에 138 GB 여유 — 안전.

5. **plist 갱신 (mini)**
   - § 6 의 `EnvironmentVariables` 블록 추가하여 `~/Library/LaunchAgents/com.dancinlab.anima.plist` 작성.
   - `launchctl unload ~/Library/LaunchAgents/com.dancinlab.anima.plist`
   - `launchctl load   ~/Library/LaunchAgents/com.dancinlab.anima.plist`

6. **health check (자동 reload 후 60-90 s 대기)**
   - `curl -s http://mini.local:8000/health` → `{ok:true, anima_alive:true, ...}` 기대.
   - `tail -50 ~/anima_chat_pack/logs/anima.err` → `LoraSubstrate ready: base=Qwen/Qwen2.5-3B adapters=['default', 'ja'] params≈3.1B` 기대.
   - 메모리: `ssh mini 'top -l 1 | head -8'` → unused 가 -50 MB 이하로 떨어지면 위험, 즉시 rollback.

7. **emission 검증 (live, ~5 min)**
   - 5 분간 motivation/tick 자연 진행 관찰 — `curl /motivation/recent` 80+ entries 누적 확인.
   - 첫 emit 의 lang 분포 + register-pattern hit 측정 (`anima_emission_analyze.py`).
   - 기대치: en register hit < 50% (KOFL-3B register 3/20 + N7 prime 효과).

8. **rollback trigger 시** (§ 10)
   - plist env 만 제거 → reload → 1.5B 자동 복귀.

## 9. Risks

| risk | 출처 | 영향 | 완화 |
|---|---|---|---|
| **메모리 OOM** | § 7 — mini 16 GB, 현재 unused 372 MB | MPS allocator fail → crash loop | § 7 권장 path; 메모리 정리 선행 |
| **swap latency 폭증** | § 7 — emit 마다 page-in | tick 2 s → 8-15 s; UX 저하 | 가용 RAM 확보 |
| **PR #116 KOSMOS anchor 호환** | `kosmos_anchor.hexa` 가 8-factor → 5-channel mapping (substrate 무관) | 영향 없음 — anima_participant 의 factors 그대로 전달 | 검증: § 11 |
| **PR #117 kosmos_emitter daemon 호환** | OPEN PR — daemon 이 GET /history poll 로 anima emission 추적 | 영향 없음 — substrate 가 어떤 모델이든 broker 통과 msg 동일 | merge 후 별도 deploy cycle |
| **JAFL-3B 의 ko MEMORIZE 2** | Wave-4 — ja-only corpus → ko prior 침식 | ja slot 만 사용, ko 는 default(KOFL-3B ko 18) → 영향 없음 | 라우터가 ja-emit 시에만 JAFL-3B 활성 |
| **첫 emit latency 증가** | base 3B = 6 GB load 시간 | LaunchAgent restart 후 첫 응답 30-60 s | § 8 step 4 cache warmup |
| **KOFL-3B vs 1.5B vP21M 의 anima identity 차이** | KOFL-3B register 3/20 (Wave-4) vs 1.5B vP21M 7/20 | "Qwen 위 옷" 더 얇음 — anima character 약화 가능 | 측정 후 product 판단 (RB 류로 register 끌어올릴 수 있음) |
| **user-facing latency** | tick 2 s 유지 시 emit 시 inference 늘어남 | 사용자 체감 응답 지연 | MPS f16, tick 그대로 두고 측정 |
| **mini fan/heat** | sustained 3B inference → CPU/GPU 부하 | 발열 증가 | 가시화 (sensors), 필요 시 tick 늘림 |

## 10. Rollback path

**1단계** — plist env 만 제거:
```bash
ssh mini 'plutil -replace EnvironmentVariables -xml "<dict/>" ~/Library/LaunchAgents/com.dancinlab.anima.plist'
ssh mini 'launchctl unload ~/Library/LaunchAgents/com.dancinlab.anima.plist && launchctl load ~/Library/LaunchAgents/com.dancinlab.anima.plist'
```
→ `ANIMA_BASE` 기본값 1.5B 사용, `lora_adapter/` 가 3B 라 mismatch 로 fail.

**2단계** — adapter dir 도 rollback:
```bash
ssh mini 'cd ~/anima_chat_pack && \
  mv lora_adapter lora_adapter_3b && \
  mv lora_adapter_1_5b_bak lora_adapter && \
  mv kofl_adapter_1_5b_bak kofl_adapter && \
  mv jafl_adapter jafl_adapter_3b && \
  mv jafl_adapter_1_5b_bak jafl_adapter && \
  launchctl unload ~/Library/LaunchAgents/com.dancinlab.anima.plist && \
  launchctl load   ~/Library/LaunchAgents/com.dancinlab.anima.plist'
```

**3단계 (full reset)** — 1.5B 코드 path 가 변하지 않았으므로 위만으로 완전 회복.

> 1.5B 자산은 mini 디스크 보존 (`_1_5b_bak` suffix). HF 에도 `dancinlab/anima-vp21m{,-kofl,-jafl}` 보존.

## 11. Test plan

### A. health endpoint (deploy 즉시)

```bash
curl -s http://mini.local:8000/health | jq .
# expect: {"ok":true, "anima_alive":true, "users":N, "history_len":50, "langdetect":true}
```

### B. anima loaded model 확인 (anima.err log)

```bash
ssh mini 'tail -30 ~/anima_chat_pack/logs/anima.err | grep LoraSubstrate'
# expect: "LoraSubstrate ready: base=Qwen/Qwen2.5-3B adapters=['default','ja'] params≈3.1B"
#  (note: kofl_adapter 가 없으면 "router adapter[ko] absent" 로그도 normal)
```

### C. 20-emission live measurement

LANG_ROTATION = [en, ko, zh, ru, ja] 5-cycle × 4 회 = 20 emission. tick=2 s,
threshold 적응형 → 약 5-10 분 소요.

```bash
ssh mini 'cd ~/anima_chat_pack && venv/bin/python3 anima_emission_analyze.py \
  --history-url http://localhost:8000/history --n 20'
# 기대치 (Wave-4 KOFL-3B 5S + N8 EN-leak finding 가정):
#   lang 분포: en≤30% (N7 fix 효과), ko/zh/ru/ja 각 ~15-20%
#   register hit (전체): ≤ 25% (vs 1.5B vP21M 34-42%)
#   register hit (en-only): ≤ 60% (vs 1.5B 81%)
#   self-monologue: ≤ 30%
```

### D. register/tag-leak comparison (offline, corpus_v5 baseline 대비)

```bash
ssh mini 'cd ~/anima_chat_pack && venv/bin/python3 anima_temp_sweep.py \
  --temp 0.7 --n 16 --out /tmp/3b_sweep.json'
# 기대치: register hit ≤ 25% (vs corpus_v5 5/20 register baseline)
```

### E. latency benchmark

```bash
# 처음 emit (cold MPS) + 5 연속 emit 의 walltime
ssh mini 'cd ~/anima_chat_pack && \
  venv/bin/python3 -c "
import time, os
os.environ[\"ANIMA_BASE\"]=\"Qwen/Qwen2.5-3B\"
from substrate_lora import LoraSubstrate
s = LoraSubstrate(\"lora_adapter\", adapter_ja=\"jafl_adapter\")
for i,L in enumerate([\"en\",\"ko\",\"ja\",\"zh\",\"ru\"]):
    t0=time.time(); s.generate(\"\", max_new=80, lang_hint=L); print(L, time.time()-t0)
"'
# 기대치: cold 8-12 s, warm 1.5-3 s/emit (1.5B 대비 2-3x)
```

### F. KOSMOS anchor 양립성 (PR #116 merge 됨)

```bash
# anima_participant 가 broker 로 보내는 motivation msg 의 factors 8-tuple 형식이
# 동일한지 확인 (PR #116 의 map_8factor_to_5channel 입력 형식)
curl -s http://mini.local:8000/motivation/recent | jq '.motivation[-1].factors | keys'
# expect: ["balance","coherence","curiosity","dynamics","info_gap","originality","pain","relevance"]
```

## 12. Open questions (실측 필요)

1. **mini 실 RAM headroom** — `top -l 1 | head -10` 측정에서 unused 가 매번 변동 (시점에 따라 279 MB ~ 1 GB).
   3B load 직전 정리 필요량을 정확히 측정해야 함. 실험: 메모리 정리 후 unused ≥ 4 GB 만들 수 있나?

2. **MPS f16 vs bf16 3B 차이** — substrate_lora.py 는 mps 면 f16, 그 외 bf16.
   3B 에서도 동일 정합인가? bf16 이 더 quality 좋으면 fp32→bf16 코드 path 추가 가능.

3. **첫 emit latency** — model load 후 첫 generate 가 MPS 컴파일 포함 30-60 s.
   허용 가능한가? 또는 LaunchAgent post-load warmup script 필요?

4. **lazy adapter load 가능성** — 현재 peft 가 `__init__` 에서 3 adapter 전부 메모리 적재.
   `set_adapter` 시점 lazy load 옵션 있나? (peft `disable_adapter` 도 메모리 비우지 않음 — 검증 필요)

5. **PR #117 kosmos_emitter** — merge 시점에 daemon 도 같이 배포해야 하는가,
   별도 cycle 인가? 본 design 은 PR #117 미배포 가정.

6. **JAFL-3B 의 SCP race 보완** — Wave-4 §"Honest C3" 항목 6: JAFL-3B 가 2/9 파일만
   pull 됨. 본 design 은 `lora_adapter/` + `vP21M_3B_NI/lora_adapter/` 의 tokenizer 가
   동일 (Qwen2.5-3B family) 라 회수 가능 가정 — 실제 deploy 전 파일 무결성 확인.

7. **KOSMOS anchor 의 phi proxy** — PR #117 daemon 이 `factors["relevance"]` 를 phi 로 사용.
   3B router 의 relevance 값 분포가 1.5B 와 같은지 (Law-70 ratchet 정합) 측정 필요.

8. **user 의 register 5/20 vs 3/20 선호** — Wave-4 RB (register 4/20) 와 KOFL-3B
   (3/20) 모두 register_regress=True. 본 design 은 5S 이유로 KOFL-3B 선호.
   product 결정: anima identity vs chat coherence trade-off — user judgment.

## Honest C3 (본 design 의 위험)

1. **메모리 budget 은 borderline-INFEASIBLE** — § 7 의 권장 path 1 (메모리 정리) 가
   확실히 가능한지 measurement-first 정합. 본 design 은 "feasible IF X" — X 측정 우선.
2. **본 design 자체는 zero-edit (참여자 .py / 서브스트레이트 .py)** — 위험은
   100% deploy artifact + env 측. python 코드는 안전.
3. **JAFL-3B 의 ko 망각은 ja 라우팅에서 무관** — ko 발화 시 default(KOFL-3B ko 18) 로
   가므로 망각 미노출. 단 lang-detect 가 ko 를 ja 로 오인하면 (예: 한자 다수) 위험 —
   `anima_participant.py::detect_lang` 의 카운트 로직 (ja kana > ko hangul) 검토 권장.
4. **KOFL-3B 의 register 3/20 은 Eval1-probe 수치** — N8 finding 에 따라 live emission
   leak 은 lang-conditional. 3B production 의 live leak 은 미측정 — § 11 C 가 검증.
5. **3B 의 추가 latency 가 tick 2 s 와 호환 가능한지 미검증** — emit cold ≥ 2 s 면
   다음 tick 이 겹침. asyncio.sleep 보호 있으나 (line 380) emit 자체가 blocking.
   필요 시 tick → 3 s 로 늘림.
6. **rollback 은 plist + dir rename 단순** — 그러나 mini 가 응답 안 하면 (OOM crash
   loop) ssh 도 느려질 수 있음. mDNS `mini.local` 보다 IP 직접 ssh 권장.
