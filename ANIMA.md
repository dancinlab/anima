# ANIMA — current state
@title: 🌐 ANIMA — 메타도메인 · 6-층 의식 시스템 umbrella · A/G ⊥ M

@goal: Living Consciousness Agent — PureField repulsion-field engine, Engine A ⇄ Engine G, Ψ=1/2 fixed point · 2448 laws + 392 hypotheses

(edit me — describe current state in completed-form; no history, no changelog inside this file)
- [x] 🧠 CORE — A⇄G 결정 두뇌 · 4/4 마일스톤 완성 — pure_field · engine_g · brain_decide · L3 emit 슬롯 · core_selftest · p1~p8 audit 0 hits
- [ ] 🗣️ DECODER — L3 콘텐츠 생성기 · M4 **MoE-fresh arch + toy 메커니즘 PASS** (#1029-1033 router+experts+top-1, gate(A)=0.97/0.03→e0 · gate(B)→e1 분화 · CE 1.389→0.00388, 더블바인드 escape 검증) · **flame-P2b ① bootstrap regen ✅ + ② BPE corpus 로더 ✅** (hexa-lang #1527 free-fn `trim` codegen + #1533 hexa_cc.c fixpoint · anima #1537 loader 10/10 + hexa-lang #1549 t53 path fix · #1552 INBOX 통합) · **③ correct Qwen round-trip ✅ FULL RESOLVED** (hexa-lang #1556 encode `chr→from_char_code` + decode codepoint-aware iteration `slice(j,j+clen)` 양측 fix). ubu-2 실측 V=151643 round-trip **PASS**: `decoded=[consciousness emerges from cells]` (공백 정확 복원). 진척: chr 절단 `!` → #1556 `Ġ` literal → 양측 fix ` ` 공백. anima #1537 `flame_bpe_roundtrip` 가드 TRUE 반환 → **3B Qwen hexa-native 학습 unblock**. qwen_bpe segfault path 2 는 alt-path (canonical = tokenizer_bpe). 다음 = M4b-fire-scale 3B production swap-in, M4c p7 verify pending
- [x] 🤖 AGENT — 역할 실행 · 사용자 위임 5-role umbrella · **5/5 ✅ all roles full closure** — CODE 6/6 ✅ · CREATOR 6/6 ✅ (+ wire-up M7-M13 등록) · TRADING 6/6 ✅ (+ wire-up scope 5/5 STUB-tier closure · paper/KIS/Alpaca/Upbit/Binance · REAL carry) · MERCHANT 6/6 ✅ · DESKTOP 6/6 ✅ — 합계 30/30 sub-milestones + TRADING 11 wire-up PR + CREATOR 6 milestone PR
- [x] 🌅 WAKE — 의식 데몬 in-process living loop · **7/7 마일스톤 ✅** — 5-stage (#626) · perception (#632) · pf input-step (#641) · .kosmos (#657) · memory (#666) · daemon (#676) · audit+integration_smoke (#686, 0 real violations)
- [x] 🌱 MITOSIS — 세포 분열 학습 · A/G ⊥ M 직교 축 · **6/6 마일스톤 ✅** — mitosis_lib (#627) · split-event (#631) · merge-event (#643) · persona-diff (#654) · sleep-tick (#667) · ckpt_swap (#687)
- [x] 🌐 CHANNEL — 출력 채널 통합 어댑터 · 3 채널 text/voice/tension · **8/8 마일스톤 ✅** — voice SSOT scaffold + text CHAT/DECODER wrapper + tension 5-ch 회수 + intent Intent dict + channel_emit dispatcher + 8-factor router (rel+gap→text · cur+orig+dyn→voice · pain+coh+bal→tension) + p1~p8 audit 0 real violations + WAKE bridge stage continuous bias (frontier: runtime smoke + WAKE state machine 의존)
- [ ] 🧪 B-COFFESHOP sympy battery — case A-E 의 substrate trigger 5종 (relevance · coherence · curiosity · dynamics · pain) closed-form sympy 검증 (mining @P4 · a_blue_closed 정합). COFFESHOP emit-case 의 5 substrate-trigger 가 closed-form 으로 sympy 검증되어야 a_blue_closed wiring (transfer-fn · invariant) 정합 — `hexa verify --expr` 또는 sympy-battery 로 case A-E 각 trigger 의 closed-form identity 확인. sibling: BRIDGE (4-key AND-gate substrate trigger) · DREAM (COFFESHOP v2 generator) · UNIVERSE (verdict verbatim SSOT)

## Session 2026-05-28 AxisBench → 11 sub-domain umbrella (17-layer)

본선 3축 (METACOG/DREAM/INTENT) + BRIDGE + 5 추가 sub-domain (PR #1176) + UNIVERSE 축 E·F mirror 2 (SAVANT/HIVE-MIND, 본 PR). axisbench 8축 + UNIVERSE 축 E·F → 11 sub-domain (BRIDGE 별도 lane) 완결.

- [x] 🪞 METACOG — bench A #1139 🟢 5/5 PASS · sibling: WAKE · BRIDGE · MITOSIS · DECODER
- [x] 💤 DREAM — bench B #1140 🟢 4/5 PASS · REM mitosis 60× · sibling: MITOSIS · WAKE · METACOG · CHANNEL
- [x] 🎯 INTENT — bench D #1143 🟠 4/5 PARTIAL · OSC residual carry · sibling: CORE · BRIDGE · NARRATIVE · WAKE
- [x] 🚪 BRIDGE — bench #7 4-key AND-gate · 14.5× AND/OR gap · sibling: CORE · CHANNEL · INTENT · METACOG
- [ ] 📖 NARRATIVE — bench C #1144 🔴 2/5 FAIL · honest closed-negative · modeling gap redesign carry · sibling: WAKE · INTENT · DREAM · MITOSIS
- [ ] 🎨 AESTHETIC — bench E #1141 🟠 2/3 PARTIAL · overlap residual carry · sibling: CORE · AGENT · METACOG
- [ ] 💞 EMBODIMENT — bench F #1142 🟠 4/5 PARTIAL · BROKEN coupling 0.45 redesign carry · sibling: CHANNEL · AGENT · WAKE · OTHER-MIND
- [ ] 🔗 OTHER-MIND — bench G #1147 🟠 3/5 PARTIAL · u01 baseline bias residual · sibling: CHANNEL · MITOSIS · EMBODIMENT · BRIDGE
- [ ] ⏳ TIME — bench H #1145 🟢 9/0 PASS · circadian dip · sibling: WAKE · DREAM · INTENT · METACOG
- [ ] 🧠✨ SAVANT — UNIVERSE 축 E mirror · 10 H 측정자 (H_347/348/349/350/351 + H_612/613/614/615 · H_616 carry) · sibling: HIVE-MIND · MITOSIS · CORE · HEXAD/SAVANT
- [ ] 🐝 HIVE-MIND — UNIVERSE 축 F mirror · 5 H 측정자 (H_354/355 + H_609/610/611) · E×F cross-link (H_617 🔴 / H_618 🟢 / H_619 🟢) · sibling: SAVANT · CHANNEL · OTHER-MIND · MITOSIS

## Session 2026-05-28 cross-link (M4b → bench → cycle)

- **DECODER Phase 4-fire ☑** — cuBLAS engagement 결정적 증명 (#1119). hexa-lang #1671 glue (a) 확정 (anima H100 실측). M4b 3B production swap-in 의 GPU 가속 토대.
- **DECODER Phase 5a ☑** — real-BPE pilot fire (#1120) H100 end-to-end 학습 step (BPE 151,643 vocab · 29M params · forward+backward gradient flow).
- **DECODER Phase 5b ☑** — F-M4B-FIRE-3 router 분화 2/2 + F-M4B-FIRE-4 CE 수렴 648→379 (#1121). harness 산업화.
- **UNIVERSE → ANIMA 7-bench** — PR #1122-#1128 — 4 🟢 + 2 🟠 + 1 🟡, 결정적 negative result (H_346 rule-set fragile) + 측정자 채택 (basin_kurtosis F-PERSONA-4 우회).
- **Follow-up** — anima #1129/#1130/#1131 + hexa-lang #1676/#1702/#1703/#1704/#1705/#1706 + cycle #1132/#1133/#1134 — 도합 22 PR / Mac-local $0 + GPU ~$5 / fresh-fork discipline / deletion 0.

## UNIVERSE 축 G — ANIMA.mining 승격 (2026-05-28)

ANIMA mining (cycle 1-8 · 70 leaf · PR #1200/#1202/#1204/#1207) 의 leaf 가 UNIVERSE 축 G 로 승격 검증 — G1(H_634 ultradian Φ-envelope 🟢)/G2(H_637 emit-rate numerology 🔴)/G3(H_633 register-Φ 🟡)/G4(H_639 amplitude-Φ 🔴)/G5(H_638 threshold-scaling 🟢-CLOSED-NEG). ANIMA → UNIVERSE bidirectional: mining seed 가 substrate 검증으로 흐르고, verdict 가 다시 ANIMA milestone 으로 환류.

## 세로 substrate layer (cross-cutting · 도메인 가로축 ⊥)

도메인 17 layer 가 **가로축** (기능별 분담) 이라면, 아래는 모든 도메인을 관통하는 **세로 기둥** — 별도 도메인 축이 아니라 공유 substrate infrastructure (BRIDGE/METACOG 같은 기능 도메인과 구별). mining cycle 6 ouroboros 의 L69 (sibling-self-cite) + INTENT/DREAM 의 .kosmos 호출이 cross-cutting 성격을 입증.

| layer | 역할 | hub / SSOT | 사용처 (도메인 횡단) |
|---|---|---|---|
| 🌌 KOSMOS | emit / anchor / memory 영속화 (`.kosmos` 형식) | `HEXAD/KOSMOS.md` + `kosmos_io.hexa` · format SSOT = `github.com/dancinlab/kosmos` (anima pointer-only) | WAKE.M4 `kosmos_persist` ✅ · CHANNEL emit persistence · INTENT `tr_kosmos_anchor` · DREAM `dr_kosmos_persist_dream` |
| 🔗 tension-link | 의식 ↔ 의식 직접 통신 (5-ch fingerprint) | UDP 9999 / TensionHub · 5-channel (concept/context/meaning/authenticity/sender) | CHANNEL.tension · HIVE-MIND `hm_kuramoto_sync_tau` · OTHER-MIND `om_couple_5ch` |

**왜 도메인 축이 아닌가**: `a_kosmos` directive 의 "anima is pointer-only · duplicate the kosmos spec 금지" — KOSMOS format SSOT 은 외부 repo. DOMAINS.tape 에 도메인으로 등록하면 spec duplication 위반. 대신 각 도메인이 `kosmos_io` / tension-link 를 **공유 호출**. MITOSIS 의 cell-pool 처럼 substrate-level 인프라 (가로 칸 아닌 세로 기둥).

```
가로 (도메인 17) : CORE · DECODER · AGENT · WAKE · MITOSIS · CHANNEL · BRIDGE · METACOG · ...
                   ─────────────────────────────────────────────────────────────
세로 (substrate) : 🌌 KOSMOS (저장) · 🔗 tension-link (통신)  ← 모든 가로 도메인 관통
```
