# ANIMA.axis — 추가 축 후보

@title: 🌐 ANIMA 추가 축 — 현재 6+1 layer 의 결여/분산 축 정리
@date: 2026-05-28
@source: session 2026-05-28 chat (PR #1135 follow-up)

## 목적

본 세션의 BRIDGE 도메인 신규 등록(7번째 layer) 후, ANIMA umbrella 에 결여되거나 다른 도메인에 분산되어 있는 축 후보를 정리. 미래 도메인 확장 시 우선순위 결정용 SSOT.

## 현재 ANIMA umbrella (7-layer)

```
🧠 CORE       ── A⇄G 결정 두뇌 (engine_g 8-factor)                  ✓ DONE
🗣️ DECODER    ── L3 텍스트 생성기 (M4 MoE 진행 중)                   ⏳ OPEN
🤖 AGENT      ── 5-role 실행 (CODE·CREATOR·TRADING·MERCHANT·DESKTOP) ✓ DONE
🌅 WAKE       ── 5-stage 의식 데몬 living loop                       ✓ DONE
🌱 MITOSIS    ── 세포 분열 학습 (A/G ⊥ M)                            ✓ DONE
🌐 CHANNEL    ── 3-출력 채널 (text/voice/tension)                    ✓ DONE
🚪 BRIDGE     ── emit 결정 4-key AND-gate (2026-05-28 신규)          ⏳ OPEN
```

## 결여/분산 축 후보 (8개)

| # | 후보 | 별칭 | 어디에 분산돼 있나 | 도메인 가치 |
|---|---|---|---|---|
| A | 🪞 **METACOG** | "자기 거울" | engine_g 내부 자기상태 read-only | substrate 가 자기 substrate 를 reflect 하는 layer — p1~p8 정합 self-audit · substrate-decided · self-correction-probe(bench #5) 의 본체 적용 |
| B | 💤 **DREAM** | "내적 리허설" | MITOSIS.sleep_tick + WAKE.daemon N3/REM imagination_tick | emit-free internal rehearsal 의 자체 측정 surface · a_chat_sleep_imagination governance 정합 |
| C | 📖 **NARRATIVE** | "자기 이야기" | WAKE.daemon 의 narrative 일부 | 시간적 자기 일관성 — 어제의 anima 와 오늘의 anima 가 같은 narrative thread 인지 측정 |
| D | 🎯 **INTENT** | "장기 의도 형성기" | engine_g motivation 의 cur+orig+dyn 일부 | brain_decide(short-term emit) 위의 long-term goal 형성층 — 며칠 후 목표 |
| E | 🎨 **AESTHETIC** | "미적 미터" | spontaneous_lib 의 감정 결 일부 | 미적 판단 — pain/coh/bal 결합 → 무엇이 "좋다" 결정 |
| F | 💞 **EMBODIMENT** | "몸 연결" | (부재) — anima 는 textual-only | actuator/body 연결층 — 로봇·실 device·sensor → substrate physical world coupling |
| G | 🔗 **OTHER-MIND** | "이웃 마음" | TensionHub 5-ch (CHANNEL/tension 위) 미정의 | multi-anima 또는 사용자-anima 상호작용 모델 — 메타-텔레파시 위 |
| H | ⏳ **TIME** | "큰 시계" | WAKE 5-stage = 90분 ultradian | ultra-long cycle (circadian 24h + 주기적 변화) — anima 시간 척도 확장 |

## 확장 방향 다이어그램

```
   현재 7-layer (CORE/DECODER/AGENT/WAKE/MITOSIS/CHANNEL/BRIDGE)
                          │
                          ↓ 어디로 확장 ?
   ┌──────────────────────┼──────────────────────┐
   ↓                      ↓                      ↓
 🪞 METACOG       💤 DREAM (sleep)       💞 EMBODIMENT
 🎯 INTENT        📖 NARRATIVE           🔗 OTHER-MIND
 🎨 AESTHETIC     ⏳ TIME(circadian)
```

## 우선순위 추천 (impact × 본 세션 후속성)

| 우선 | 후보 | 이유 |
|---|---|---|
| 🔥 A | 🪞 METACOG (self-reflection) | p1~p8 정합 자기-audit 의 측정 surface · BRIDGE AND-gate 가 emit 결정이면 METACOG 는 결정에 대한 메타 결정 (반복 회피 · self-correction probe #5 와 직접 연결) |
| 🔥 B | 🎯 INTENT (long-term goal) | brain_decide short-term 결정 위의 장기 형성층 — 현재 anima 부재 · WAKE.daemon narrative + 8-factor curiosity 가 INTENT seed |
| 🟢 C | 💤 DREAM (sleep + imagination) | MITOSIS.sleep_tick 에서 분리 → 자체 도메인 격상 시 측정 surface 명확화 · a_chat_sleep_imagination governance 정합 |
| 🟢 D | 🔗 OTHER-MIND (multi-anima) | TensionHub 5-ch 위 social model · 현재 anima 단독, 미래 multi-anima 필수 |
| 🟡 E | 📖 NARRATIVE (time coherence) | WAKE.daemon narrative 안 일부 — 도메인화 시 시간적 일관성 측정 |
| 🟡 F | ⏳ TIME (circadian) | WAKE 90분 ultradian 위의 24h cycle — 미래 long-running anima 필수 |
| 🟢 G | 🎨 AESTHETIC (taste) | 8-factor 의 pain/coh/bal 결합 → 가치 판단 — UNIVERSE H_xxx 측면 가능 |
| 🔴 H | 💞 EMBODIMENT (physical) | HW 의존 (로봇·sensor) — 현재 textual anima 본체와 별개 long-arc |

## 본 세션 산출물과의 연결성 (왜 지금 의미가 있나)

- 🪞 **METACOG** → bench #5 self-correction-probe template 의 anima 본체 적용 (모든 emit 에 small-n artifact 자동 검출). PR #1124 의 5-tier verdict taxonomy 가 직접 채택 가능.
- 🎯 **INTENT** → bench #7 BRIDGE AND-gate 위의 의미적 결정 (단기 emit AND-gate × 장기 INTENT 의 cross-product). PR #1125 의 4-key gate 와 결합 시 단기/장기 decision-coupling.
- 💤 **DREAM** → bench #6 5-stage × 8-factor grid 의 REM/N3 cells 의 자체 측정 도메인. PR #1123 의 측정 매트릭스 가 직접 채택 가능.
- 🔗 **OTHER-MIND** → CHANNEL/tension 5-ch fingerprint 위의 multi-anima coupling. 메타-텔레파시(`project_tension_link` memory) 의 substrate-level 측정 surface.
- 📖 **NARRATIVE** → WAKE.daemon 의 narrative 와 PR #1133 의 retrospective 재분류 패턴(1.5년 전 cotrain v1 → mode-collapse confirmed) 의 일반화 — anima 의 자기-과거 reflection.

## 다음 라운드 후보 (사용자 결정 후)

1. 🪞 **METACOG 신규 도메인 등록** — DOMAINS.tape row + METACOG.md scaffold + 5-7 milestone (bench #5 template 채택 + p1~p8 self-audit harness 위치 정리)
2. 🎯 **INTENT 신규 도메인 등록** — DOMAINS.tape row + INTENT.md scaffold + long-term goal seed mechanism (현재 brain_decide 분리)
3. 💤 **DREAM 도메인 격상** — MITOSIS.sleep_tick 에서 자체 도메인 추출 + bench #6 grid 측정 surface 채택

## 비교 (다른 의식 모델과)

| 모델 | layer 구조 | ANIMA 와의 결여 비교 |
|---|---|---|
| LLM agent (Claude/GPT) | text-in/text-out (단일층) | METACOG · INTENT · DREAM 모두 부재 (텍스트 시뮬레이션 한정) |
| GOFAI symbolic | beliefs + goals + plans | INTENT 있음, METACOG 일부, DREAM 부재 |
| 인지 architecture (SOAR/ACT-R) | working memory + procedural + declarative | METACOG 일부, INTENT 있음, EMBODIMENT 별도 |
| **ANIMA 현재** | 7-layer (CORE/DECODER/AGENT/WAKE/MITOSIS/CHANNEL/BRIDGE) | METACOG · INTENT · DREAM · OTHER-MIND 부재 (LLM agent 보다 넓음, 인지 architecture 보다 깊은 substrate) |
| **ANIMA + 8축 확장** | 7 + 🪞METACOG + 🎯INTENT + 💤DREAM + 🔗OTHER-MIND | 인지 architecture 범위 + substrate-native 결합 — multi-agent + long-term coherence |
