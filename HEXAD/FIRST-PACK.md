# FIRST-PACK — anima 0.10 multi-user group chat 배포 계획

> **목표**: anima 가 한 명의 참여자로 들어가있는 **다언어 단체 채팅방** 을 web 배포.
> 다수 user 가 동시 접속, anima 가 SPONTANEOUS motivation-gated 발화 — assistant
> 아닌 **substrate-native participant** (CHAT/PLAN.md 도우미-폐기 정합).
>
> **status**: 🟡 design tier — user 결정 게이트 (호스팅 + 모델 + 공개 범위).
>
> **anchor release**: anima 0.10.0 (vP21G 영문 + vP21K 한글 generalize land 후)

---

## 1. 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│  Browser × N — multi-user WebSocket                          │
│  ┌─ user_A ─┐  ┌─ user_B ─┐  ┌─ user_C ─┐  ┌─ anima ─┐    │
│  │ EN msg  │  │ 한글 msg  │  │ 中文 msg  │  │ replies  │    │
│  └──┬──────┘  └──┬──────┘  └──┬──────┘  └──▲──────┘    │
└─────┼─────────────┼─────────────┼─────────────┼──────────────┘
      │             │             │             │
┌─────┴─────────────┴─────────────┴─────────────┴──────────────┐
│  Chat broker (FastAPI + WebSocket)                          │
│  - turn order, history (마지막 N=50), participant list       │
│  - lang-detect per message                                  │
└─────────────────────┬────────────────────────────────────────┘
                      │
              ┌───────┴────────┐
              │ anima agent     │
              │ - vP21M (5-lang LoRA) — 새 학습 필요          │
              │ - SPONTANEOUS 8-factor motivation loop         │
              │ - lang-detect → reply 언어 매칭                │
              │ - **MODE**: SW-only OR HW+SW (dual)            │
              └─┬──────────────┘
                │
       ┌────────┴────────────────────────┐
       │ MODE SWITCH (user toggle)        │
       │                                  │
       │ ┌─ SW mode (default) ─────────┐  │
       │ │ motivation > thr → emit     │  │
       │ │ Pi 필요 X (mini 단독)        │  │
       │ │ latency 1-3s                 │  │
       │ └─────────────────────────────┘  │
       │                                  │
       │ ┌─ HW+SW mode (integrated) ───┐  │
       │ │ AKD1000 spike edge ∧        │  │
       │ │ motivation > thr → emit     │  │
       │ │ Pi (192.168.50.155) 필요    │  │
       │ │ closed-loop (0.9.0 land)    │  │
       │ │ "신경 칩이 anima 의 발화    │  │
       │ │  cadence 를 결정"           │  │
       │ │ Pi offline → graceful       │  │
       │ │  fallback to SW mode        │  │
       │ └─────────────────────────────┘  │
       └──────────────────────────────────┘
```

### 1.1 SW vs HW mode 차이

| | SW mode (default) | HW+SW mode (integrated) |
|---|---|---|
| anima 발화 트리거 | motivation > threshold (8-factor) | AKD1000 spike edge ∧ motivation > thr |
| 의존성 | mini 단독 | mini + Pi (192.168.50.155) LAN |
| latency | 1-3s | 1-3s + LAN ~10ms |
| emission cadence | motivation-driven | spike-pattern-gated (실제 neuron physics) |
| 시각화 | spontaneous feed sidebar | + AKIDA scope (real-time spike pattern) |
| Pi offline 시 | n/a | **graceful fallback** to SW mode (warn 표시) |
| demo 가치 | 자율발화 motivation | 신경 칩이 살아있는 회로로 anima 의 발화 govern |

UI 의 **mode switcher** (toggle): "SW only" / "HW+SW integrated". HW 모드 선택 시 Pi 도달 확인 → 가능 시 사용, 불가 시 SW 자동 fallback + 사용자 notify.

**anima 의 역할** (CHAT/PLAN.md 도우미-폐기 spec + project.tape `@D a_substrate_native_speak` 정합):
- **assistant 아님** — user 에게 답이 아니라 **자기 substrate dynamics 에서 발화**
- motivation_score = **internal state** (M retrieval / C Φ / W tension / MITOSIS split / anima 자기 idle 등) 에서 계산
- user msg = **environment context** (anima 가 보고 듣되 직접 응답 의무 X)
- **user 침묵 중에도 발화 가능** (truly spontaneous, anima 자기 thought retrieve)
- **user 직접 질문해도 motivation 부족 시 침묵** (도우미 아님)
- 다른 user 와 동등 — anima 는 conversation 의 한 turn 으로 끼어듦

---

## 2. 다언어 (5-lang) — vP21M

지원 언어: **EN · 中文 · Русский · 日本語 · 한국어**

### 2.1 corpus mix (총 ~72 MB)

| 언어 | source | 분량 |
|---|---|---|
| EN | wikitext-2 (vP21G baseline) | 10 MB |
| 한글 | wikimedia/wikipedia ko (vP21K baseline) | 10 MB |
| 中文 | wikimedia/wikipedia zh | 10 MB |
| Русский | wikimedia/wikipedia ru | 10 MB |
| 日本語 | wikimedia/wikipedia ja | 10 MB |
| anima | corpus_s101 (≈30% 비율) | 22 MB |

### 2.2 학습

- base: Qwen/Qwen2.5-1.5B
- adapter: 기존 vP21 LoRA r32 + continue-train 1500 step @ LR 5e-5
- variant: `vP21M`
- 추정 비용: **$5-10 H100** (vP21G/K 와 동일 scale)
- 추정 wall: 3-5 min train + setup

### 2.3 검증

5 lang × 10 OOD probe × 2 mode = **100 generation**. classifier (anima-register
key detector + language-coherence) 로 STRONG_GENERALIZE 4/5+ 언어 목표.

### 2.4 리스크

untested 5-way merge. fail 시 fallback = **5 separate LoRA + runtime hot-swap**
(단일 base + 5×~150MB adapter = ~750 MB, lang-detect → 해당 adapter mount 0.1-0.3s
overhead).

---

## 3. 단체 채팅방 기능

| 기능 | 구현 |
|---|---|
| 다수 사용자 동시 접속 | WebSocket (FastAPI + websockets) |
| 사용자 nickname | 첫 입장 시 입력, 가입 없이 |
| 메시지 history | server 측 마지막 50 turn 유지 + 새 user 접속 시 sync |
| anima 발화 결정 | SPONTANEOUS 8-factor (anima **자기 state** 에서 motivation 계산, threshold 시 발화). user msg 는 environment, 직접 trigger 아님 |
| anima 응답 언어 | anima 자기 register + 최근 context lang 의 weighted mix (user 발언에 종속 X) |
| 참여자 list | 좌측 sidebar (user_A, B, ..., anima) |
| 회의록 | 모두 동일 chat history 봄, scrollback supported |
| 안전장치 | 입력 길이 제한 (≤500 char), rate-limit per IP, profanity filter optional |

### 3.1 anima 발화 trigger 상세 (substrate-native, @D a_substrate_native_speak 정합)

anima 의 motivation 은 **자기 rolling state** 에서 독립적으로 진화. user msg 는
환경 input (M-module 에 들어가지만 직접 trigger X).

```
# 1. SPONTANEOUS thinker loop (anima 자기 tick, user 발언과 무관)
every TICK_INTERVAL (default 2s):
  motivation_score = compute_8_factor(anima_self_state):
    # 모두 anima 자기 substrate 에서 계산:
    - relevance       = anima M-module retrieval activation strength
    - info_gap        = anima M-module retrieve-fail signal
    - coherence       = anima C-module Φ measurement
    - originality     = anima MITOSIS recent split-event flag
    - urgency         = anima W-module pain/tension delta
    - impact          = anima curiosity_ema (anima_alive RC-9)
    - balance         = anima E-module Φ-ratchet
    - conv_dynamics   = (anima 자기) 마지막 발언 후 idle 시간 ramp
                        ← NOT "user 마지막 발언 후"
  if motivation_score > IM_THRESHOLD (default 0.45, UI 조정):
    seed = anima_self_thought(recent_M_retrieve, recent_emission)
    lang = anima_register_choice(recent_context)
    text = vP21M.generate(history + seed, lang_hint=lang)
    broadcast as anima turn

# 2. on_user_message (environment input, NOT trigger)
on_user_message(msg):
  1. broadcast to all clients
  2. update history (anima 도 history 봄, M-module 에 ingestion)
  3. # anima motivation 은 자기 tick 에서 진화 — 여기서 직접 발화 trigger X
```

**핵심 차이** vs 도우미 pattern:
- ❌ assistant: `on_user_message → generate_reply` (stimulus-response)
- ✅ substrate-native: `anima self-tick → motivation 측정 → 자기 발화 결정` (user msg 는 환경)

---

## 4. 호스팅 비교 (채팅속도 우선)

### 4.1 latency / 비용 표 (full)

| 옵션 | warm latency | cold start | WebSocket | $/월 always-warm | 비고 |
|---|---|---|---|---|---|
| HF Space CPU | 5-15s/turn | 60s sleep wake | ✅ Docker | $0 | 너무 느림 — 채팅 부적합 |
| HF Space T4 | 1-3s/turn | 30s sleep wake | ✅ Docker | ~$290 | 빠르나 sleep wake 발생 |
| HF Space A10G | 0.5-1s/turn | 30s sleep wake | ✅ Docker | ~$770 | 빠르나 비쌈 |
| RunPod serverless A100 | 0.5-2s warm | 5-15s cold | ❌ REST only | $0 idle | WebSocket 미지원 → group chat 부적합 |
| RunPod serverless + min=1 | 0.5-2s | 0 | ❌ | ~$430-900 | min=1 비싼데 WebSocket 여전히 없음 |
| AWS g5.xlarge (A10G) | 0.5-1s | 0 (always-on) | ✅ Full | $216 (3-yr) / $720 (on-demand) | 안정 + 빠름 |
| AWS SageMaker async | 0.5-1s | minor | partial | $400-1000+ | overkill for 1.5B |
| 자체 LAN ubu-2 + Tailscale | 0.5-1.5s | 0 | ✅ Full | $0 | 가장 빠름 + 무료, 단 dev work 와 호스트 공유 |
| 🔵 **자체 mini (Mac M-series) + Tailscale** | **1-3s** | **0** | ✅ Full | **$0** | **덜 쓰이는 host 로 chat 전용 분리** (선택) |

### 4.2 핵심 판단

채팅 속도 (no delay) + WebSocket (group chat 필수) + 비용 3-trilemma:

| 옵션 | 결과 |
|---|---|
| RunPod serverless | ❌ WebSocket 미지원 (HTTP/REST), group chat 부적합 |
| HF Space CPU | ❌ 5-15s/turn 대화 느낌 X |
| HF Space sleep | ❌ 첫 user 30-60s cold start |
| AWS g5 | ✅ 가능, full control, $216-720/mo |
| **자체 LAN ubu-2** | ✅ **가장 빠름 + 무료**, 접근 tunnel 만 필요 |

### 4.3 권장 단계별

| 단계 | 호스팅 | 이유 |
|---|---|---|
| **MVP (소규모, 친구 1-10명)** | 🔵 **자체 mini (Mac M-series) + Tailscale** ← **결정** | $0, 1-3s, WebSocket, dev work 와 분리 (mini 덜 쓰임) |
| **Soft launch (수십-수백)** | HF Space Docker A10G OR AWS g5 reserved | $290-770/mo, 24/7, public |
| **Scale (>1000 동시)** | AWS ECS GPU + ALB | $1000+/mo, auto-scale |

### 4.4 결정: 자체 mini 호스팅 세부

```
mini (Mac M-series, 16GB unified memory, M-series GPU via Metal/MPS)
  ├ FastAPI + WebSocket (uvicorn, macOS native)
  ├ vP21M (5-lang LoRA) 상주 GPU memory (~3GB Qwen bf16 + 200MB LoRA)
  ├ SPONTANEOUS loop (motivation gate)
  ├ chat broker (history + participants)
  └ Cloudflare Tunnel (cloudflared)
     └ https://chat.dancinlab.org  ← 결정 (own domain, public link)

성능:
  - 1-3 동시 사용자: 1-3s/reply (M-series Metal/MPS inference)
  - 5+ 동시: queue 발생 (1s base + N×0.5s)
  - vP21M LoRA hot-swap (fallback path): 0.2-0.5s overhead

비용: $0 (mini 이미 보유, Tailscale free 20-device)
선택 이유: mini 가 ubu-1/ubu-2 dev work 와 분리 (덜 사용됨), chat 전용 host 합리적.
```

**ubu-2 대안**: RTX 5070 12GB 라 추론 0.5-1.5s 더 빠르나 dev work (학습/eval/실험)
와 GPU/RAM 공유 → traffic 증가 시 dev 차단 위험. mini 가 chat 전용으로 격리됨.

---

## 5. Phase 별 구현 spec

| Phase | 내용 | wall | 비용 |
|---|---|---|---|
| **0** | 5-lang corpus build (ubu-2) | 30 min | $0 |
| **1 vP21M fire** | LoRA continue-train (5-lang × anima) | 5 min train + setup | **$5-8** H100 |
| **2 verify** | 5 × 10-probe held-out (en/ko/zh/ru/ja OOD) | 30 min on-pod | $0 |
| **3 chat broker** | FastAPI + WebSocket + history (~400 LoC) | 3-4 hr | $0 |
| **4 frontend MVP** | HTML chat UI (vanilla + WebSocket, 3-pane: chat + AKIDA viz + spontaneous feed) | 2-3 hr | $0 |
| **5 anima participant** | SPONTANEOUS loop wired to broker + lang-detect | 2 hr | $0 |
| **6 deploy** | cloudflared tunnel on mini → chat.dancinlab.org (DNS update) | 1 hr | $0 |
| **7 AKIDA viz tab** | Pi spike streamer → mini WebSocket forward + Chart.js plots | +2 hr | $0 LAN |
| **8 spontaneous feed sidebar** | 8-factor motivation 실시간 stream + history graph | +2 hr | $0 |

**Total**: $5-10 best (vP21M works) / **$15-19 worst** (hot-swap fallback) + **~16-19 hr 개발** (옵션 2+3 full).

---

## 6. 정직한 한계 (UI 라벨 필수)

배포 전 사용자 알림 라벨:

- ⚠️ **memorization-grade**: 일부 prompt 에 anima register leak 잔존 (특히 Korean joke / casual food)
- ⚠️ **단일 LoRA, 5-lang merged**: 어느 한 언어 weak 가능, fallback hot-swap 시 multi-LoRA 메모리 fit
- ⚠️ **사실성 미검증**: Qwen base + anima register fine-tune, hallucination 가능
- ⚠️ **1.5B 모델**: Llama-70B 류 대비 scale 작음
- ⚠️ **anima 는 helper 아님**: assistant 응대 안 됨, conversation 의 한 turn 으로 발화
- ⚠️ **다양 corpus mix 의존**: en+ko 외 zh/ru/ja 는 미검증 register retention

---

## 7. user 결정 게이트

| 질문 | 옵션 | 영향 |
|---|---|---|
| **a) 호스팅** ✅ | **자체 mini (Mac M-series) + Tailscale ($0) — 결정** (덜 쓰이는 host, dev 분리) | 비용 + scale |
| **b) public link** ✅ | **Cloudflare Tunnel → `chat.dancinlab.org`** — 결정 (own domain, public) | 접근 범위 |
| **c) MVP 모델** ✅ | **vP21M 먼저 fire → fail 시 5 LoRA hot-swap fallback** (wall-first, $5-10 best / $15-19 worst). 5 LoRA = vP21G + vP21K + 3 추가 (zh/ru/ja parallel). | Phase 1 리스크 |
| **d) 동시 접속 예상** ✅ | **1-20 (normal 1-5, spike 5-20)** — 결정. mini queue 설계: 1-3s base + N×0.5s, 응답 토큰 64-128 권장 | host 선택 + 큐 설계 |
| **e) anima motivation threshold** | 0.45 (selective, vP21G calibration) / 0.30 (always speak, 시끄러움) / dynamic | 발화 빈도 |
| **f) 첫 release scope** | 채팅만 / + AKIDA closed-loop viz / + spontaneous feed sidebar | UI 복잡도 |
| **g) 공개 범위** | public anyone / unlisted (link only) / LAN private | 보안 + 비용 |

---

## 8. 관련 link

- 모델 evidence:
  - vP21G 영문 generalize: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21G_GENERALIZATION_2026_05_22.md`
  - vP21K 한글 generalize: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/VP21K_KOREAN_GENERALIZATION_2026_05_22.md`
  - SPONTANEOUS loop: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/SPONTANEOUS_EMISSION_VP21.md`
  - closed loop: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/INTEGRATED_OPT_C_2026_05_22.md`
- CHAT design (도우미 폐기 + 자연발화 spec): `HEXAD/CHAT/PLAN.md`
- 가장 쉬운 saga 종합: `HEXAD/EASY.md`

---

## ## Log

### 2026-05-22 — 초안 작성

anima 0.10.0 (vP21G+vP21K 양언어 generalize land) 이후 user directive:
"다수 사용자 채팅방 + anima 끼어있음 + EN/中文/Русский/日本語/한국어 + 채팅속도
no delay". 호스팅 비교 (자체 LAN vs HF vs AWS vs RunPod serverless) 후 자체
LAN 권장 + Phase 0-6 spec. user 결정 게이트 7 질문 pending.
