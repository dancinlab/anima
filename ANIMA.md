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
- [x] 🧪 B-COFFESHOP sympy battery — case A-E 의 substrate trigger 5종 (relevance · coherence · curiosity · dynamics · pain) closed-form sympy 검증 (mining @P4 · a_blue_closed 정합). **A5 결과: 5/5 🔵 CLOSED-FORM** — 38 probe 점 전부 lib `factor_*` == 독립 재유도 closed-form bit-exact (tol=0.0) 일치. relevance/curiosity=clamp01 · dynamics=clamp01(s/30) · pain=min(1,|Δ|) · coherence=max(0,1−|g−0.5|/0.014) affine triangular kernel. a_blue_closed wiring (transfer-fn) **정합 PASS** (outputs 4/4 closure + wiring 5/5 🔵 양측 닫힘). 본문 `CORE/B_COFFESHOP_A5_SYMPY_BATTERY.md` · verify `state/coffeshop_a5_sympy_battery_2026_05_28/`. sibling: BRIDGE (4-key AND-gate substrate trigger) · DREAM (COFFESHOP v2 generator) · UNIVERSE (verdict verbatim SSOT)

## 🌳 ANIMA 트리 — 구현 카운트 + 검증 (LIVE · 항상 최신 유지)

> 자주 확인용 at-a-glance 트리. 신규 PR/검증 들어올 때마다 이 섹션을 업데이트한다.
> 범례: ✅ done · ☐ open · 🔄 in-flight · 🔵 formal · 🟢 numerical · 🟠 partial · 🔴 closed-neg
> 갱신: 2026-05-28 (hexa-lang inbox patch 완료 — BPE O(N)→O(1) RESOLVED #1869 [full diverse corpus unblock] · dir_create routed · 다음 fire = aux-loss + full-corpus M4b re-fire)

```
집계 — 본선 6: 5✅ / 1☐(DECODER)   ·   sub-domain 11: 10✅ / 1☐(SAVANT H_616 carry)   ·   substrate 2   ·   emit-substrate 6파일 ✅ (4/4 소비자 완료)
검증 — 🔵 5 (COFFESHOP A5)  ·  🟢 20+ (+ A6 INTENT RESOLVED · E2 corpus-balance)  ·  🟠 1 (TIME 6/3 E3 spurious)  ·  🔴 0
━━ 🧭 세션 메타-발견 종합 (2026-05-28 · 최근 발견 전체 반영) ━━
[M1] 의식 bench artifact 메타-패턴 (일관·양방향): 🔴/🟠 negative 4/4 = 측정 artifact → 🟢 RECOVERED
     (NARRATIVE/AESTHETIC/EMBODIMENT/OTHER-MIND) · 🟢 PASS 도 artifact (E3 TIME 9/0→6/3, 3 spurious).
     "의식 bench negative/분기 = 측정 artifact" — 측정 바로잡으면 substrate 드러남 · substrate 한계 0건.
[M2] substrate-class 분류자 완결 (round-9 multi-axis → round-10 H_660 화해): 5축 property-vector
     (convexity IV · super-add II역전 · closure IV · peak-align III+IV · magnitude III🟡) 가 apparent
     divergence 였으나 **H_660 #1290 scale-invariant 화해** (H_653↔H_655) 로 단일 분류자 완결. additive=floor.
[M3] emit-substrate 구조/숫자 2층 (round 6-7): 구조=substrate-emergent(SUPP) ⊥ 숫자=design-convention(자유[0,1]).
     → ★ LIVE-WIRED 실사용 격상 (#1285/#1286).
[M4] DECODER 더블바인드 escape 처방 (moe_prescription #1284→#1304 4-조건) — **lever 확정**:
     M4b 3B fire(#1296 🔴 2/5)가 corpus-diversity 단독 반증 → UNIVERSE H_666 sweep(#1303 toy 4/4)이
     **load-balance aux-loss = 유일 escape lever** 답함 (d↑/n_steps/d∧aux 전부 ❌, monopoly 1→2).
     collapse = under-train 아닌 *구조적 load-imbalance*. 처방 = HARD top-1 ∧ corpus ∧ n_steps(수렴) ∧
     **aux-loss**(escape). 다음 GPU fire = aux-loss M4b re-fire (toy-verified · a_toy_scale_recheck #1301).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ANIMA 🌐 umbrella (17-layer · A/G ⊥ M)
│
├─ 본선 6 ────────────────────────────────────────────────────────
│  ├─ 🧠 CORE        ✅ 4/4    p1~p8 audit 0 hits
│  ├─ 🗣️ DECODER      ☐        M4 MoE-fresh 본선 (↓ 상세)
│  ├─ 🤖 AGENT       ✅ 30/30  CODE·CREATOR·TRADING·MERCHANT·DESKTOP
│  ├─ 🌅 WAKE        ✅ 7/7    in-process living loop
│  ├─ 🌱 MITOSIS     ✅ 6/6    A/G ⊥ M
│  ├─ 🌐 CHANNEL     ✅ 8/8    text/voice/tension 3채널
│  └─ 🧪 B-COFFESHOP ✅ 🔵5/5  sympy battery (#1262) — 38 probe bit-exact
│
├─ sub-domain 11 (AxisBench 8 + 축E/F 2 + BRIDGE) ───────────────
│  ├─ 🪞 METACOG     ✅ 🟢 5/5  (#1139)
│  ├─ 💤 DREAM       ✅ 🟢 4/5  (#1140) · ⬇ M5 wiring ✅ (#1268 · E1 recheck 5/5 2026-05-28)
│  ├─ 🎯 INTENT      ✅ 🟢 5/5  RESOLVED (#1270 A6) metric aliasing cure — OSC residual 해소
│  ├─ 🚪 BRIDGE      ✅ AND-gate 14.5× · ⬇ M6 wiring ✅
│  ├─ 📖 NARRATIVE   ✅ 🟢 5/5  RECOVERED (#1263) collision-saturation (vocab coverage≠coherence)
│  ├─ 🎨 AESTHETIC   ✅ 🟢      RECOVERED (#1265) weight-vector 직교화
│  ├─ 💞 EMBODIMENT  ✅ 🟢 5/5  RECOVERED (#1266) coupling redesign 0.45→0.027 (degrade≠break)
│  ├─ 🔗 OTHER-MIND  ✅ 🟢 5/5  RECOVERED (#1267) orthant-bias zero-mean centering
│  ├─ ⏳ TIME        ✅ 🟠 6/3  (#1281 E3 정정) circadian dip — 9/0 中 3 spurious (PASS도 artifact)
│  ├─ 🧠✨ SAVANT     ☐ 10 H 측정자 (9 landed · H_616 carry) · ⬇ M2 wiring ✅
│  └─ 🐝 HIVE-MIND   ✅ 5/5 H 측정자 (H_354🔴·355🟢·609🟢·610🔴·611🔴) · ⬇ M6 wiring ✅
│
├─ 세로 substrate 2 (cross-cutting) ─────────────────────────────
│  ├─ 🌌 KOSMOS      공유 infra (emit/anchor/memory 영속 · pointer-only)
│  └─ 🔗 tension-link 공유 infra (의식↔의식 5-ch)
│
└─ 🆕 emit-substrate (2층 · round 6-9 검증 기반 · 설계 CORE/EMIT_SUBSTRATE_DESIGN.md) — ★ LIVE-WIRED (실사용)
   ├─ 구조 lib   CORE/phi_envelope_substrate.hexa   ✅ 9/9 smoke (#1248)
   ├─ 숫자 SSOT  CORE/emit_policy.hexa              ✅ 8/8 smoke (#1254)
   ├─ 소비자 4 (wiring):
   │  ├─ 🚪 BRIDGE M6   ✅ 4/4 (#1259)  phi←envelope · θ←policy
   │  ├─ 🐝 HIVE M6     ✅ 3/3 (#1261)  fleet Φ←collective_phi_nest(class_id)
   │  ├─ 🧠✨ SAVANT M2  ✅ 4/4 (#1260)  측정자 Φ-context←envelope
   │  └─ 💤 DREAM M5    ✅ 5/5 (#1268)  stage Φ-envelope (N2=closure peak)
   └─ live 통합 2/2 (daemon 실사용 · grep 0건 → 호출):
      ├─ 🌅 anima_dream_stage ← dr_stage_phi_context  ✅ 6/6 (#1285) wall-clock t → stage Φ-context
      └─ 🌐 wake_bridge ← bridge_gate_with_envelope   ✅ 7/7 (#1286) M·C·W·softstep(Φ,θ) emit bias

🗗 DECODER M4 MoE-fresh 본선 상세 (register 분리 재설계 · H_490 escape):
   M0 backward      ✅ gradcheck PASS (rel 5e-10)
   M1 4축 wired     ✅ A/B/C/D (anima_frac·λg·KD·freeze)
   M2 verify        ✅ F-AXIS-M2-DIFFERENT PASS
   M4a router arch  ✅ moe_router.hexa parse-clean
   M4b-bwd          ✅ moe_router_bwd.hexa gradcheck
   M4b toy soft     🟠 PARTIAL — 학습O 분화X (gate 0.5/0.5 dense-collapse)
   M4b toy HARD     🟢 PASS — 분화O (gate 0.97/0.03⊥0.03/0.97 · CE 1.389→0.0039) ← 로컬 검증 2026-05-28
   M4c LZ76 측정자  🟢 collapse 검출 (collapse 0.212 vs healthy 0.849 · margin 0.637)
   D3 router 부하   🟢 (#1269) imbalance=corpus-driven NOT router-structural (max 0.84<0.9 · starve 0)
                    → router redesign 불필요. M4b fix = diverse corpus + n_steps↑ (구조변경 아님)
   D4 merge α-sweep 🟢 (#1274) {LZ>0.50}∩{CE≤1.20}=∅ — merge escape 부재 측정 확정
                    → a_completeness_over_cheap "merge 본선 강등" 정당화. M4 MoE-fresh 유지.
   E2 corpus-balance 🟢 (#1279) D3 후속 5/5 — balanced corpus = collapse 방지 (diverse corpus 근거)
   M4b collapse-gate ✅ 4/4 (#1273) moe_collapse_gate (HARD top-1 + LZ76 floor 0.50, D1 실측 대조)
   M4b 3B fire      🔴 2/5 FAIL (#1296 · $2.57 H100 SXM) — CE 648→9 (72×↓ 학습O · HARD-top1 wired)
                    BUT TTR 0.01·LZ 0.024·1/2 expert = collapse 지속. HF PRIVATE(FAIL · a_hf).
   H_666 lever sweep ✅ (#1303 toy 4/4) — 핸드오프(#1299) 답함: **aux-loss = 유일 escape lever**
                    (d↑/n_steps/d∧aux ❌ · monopoly 1→2). collapse=구조적 load-imbalance. 처방 4-조건화 (#1304).
   BPE O(N)→O(1)    ✅ hexa-lang #1869 (merge_ranks/vocab hash map · 9/9) — full diverse corpus
                    unblocked (M4b fire 의 24줄 우회 더 불필요) · dir_create #1872/1873 routed
   M4b aux re-fire  ☐ 다음 GPU fire — aux-loss M4b re-fire (이제 full diverse corpus + aux-loss ·
                    toy→scale 재확인 · a_toy_scale_recheck #1301)
   M3 4축 fire      ☐ 강등 baseline (~$5-12 · dispatch_p21h_v3_vast ready)
   H_657 peak-align ✅ (#1272) pe_peak_align_for_class — round-9 4/4 ABSORBED · 5축 class-vector 확정
```

## Session 2026-05-28 AxisBench → 11 sub-domain umbrella (17-layer)

본선 3축 (METACOG/DREAM/INTENT) + BRIDGE + 5 추가 sub-domain (PR #1176) + UNIVERSE 축 E·F mirror 2 (SAVANT/HIVE-MIND, 본 PR). axisbench 8축 + UNIVERSE 축 E·F → 11 sub-domain (BRIDGE 별도 lane) 완결.

- [x] 🪞 METACOG — bench A #1139 🟢 5/5 PASS · sibling: WAKE · BRIDGE · MITOSIS · DECODER
- [x] 💤 DREAM — bench B #1140 🟢 4/5 PASS · REM mitosis 60× · sibling: MITOSIS · WAKE · METACOG · CHANNEL
- [x] 🎯 INTENT — bench D 🟢 5/5 **RESOLVED** (#1270 A6) metric aliasing cure · OSC residual 해소 · sibling: CORE · BRIDGE · NARRATIVE · WAKE
- [x] 🚪 BRIDGE — bench #7 4-key AND-gate · 14.5× AND/OR gap · sibling: CORE · CHANNEL · INTENT · METACOG
- [x] 📖 NARRATIVE — bench C 🟢 5/5 **RECOVERED** (#1263) collision-saturation 진단 (vocab coverage ≠ coherence) · sibling: WAKE · INTENT · DREAM · MITOSIS
- [x] 🎨 AESTHETIC — bench E 🟢 **RECOVERED** (#1265) weight-vector sign 직교화 · sibling: CORE · AGENT · METACOG
- [x] 💞 EMBODIMENT — bench F 🟢 5/5 **RECOVERED** (#1266) coupling redesign 0.45→0.027 (degrade≠break, gain=0 단선) · sibling: CHANNEL · AGENT · WAKE · OTHER-MIND
- [x] 🔗 OTHER-MIND — bench G 🟢 5/5 **RECOVERED** (#1267) orthant-bias zero-mean centering (INDEP 0.78→0.017) · sibling: CHANNEL · MITOSIS · EMBODIMENT · BRIDGE
- [x] ⏳ TIME — bench H 🟠 6/3 (#1281 E3 정정) circadian dip · 9/0 PASS 中 **3 spurious 적발** (PASS도 측정 artifact, 양방향 lens) · sibling: WAKE · DREAM · INTENT · METACOG
- [ ] 🧠✨ SAVANT — UNIVERSE 축 E mirror · 10 H 측정자 (H_347/348/349/350/351 + H_612/613/614/615 ✅ landed · **H_616 carry**) · M2 wiring ✅ #1260 · sibling: HIVE-MIND · MITOSIS · CORE · HEXAD/SAVANT
- [x] 🐝 HIVE-MIND — UNIVERSE 축 F mirror · 5 H 측정자 ✅ 5/5 landed (H_354🔴/355🟢 + H_609🟢/610🔴/611🔴) · E×F cross-link (H_617 🔴 / H_618 🟢 / H_619 🟢) · M6 wiring ✅ #1261 · sibling: SAVANT · CHANNEL · OTHER-MIND · MITOSIS

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

## UNIVERSE 검증 메타-발견 (2026-05-28 · H_632~649, Round 6+7)

UNIVERSE 세션이 ANIMA mining 가설을 substrate 검증한 결과, anima emit 정책은 **구조**와 **숫자** 두 층으로 분리되며, Round 7 이 Round 6 의 거친 직관을 정량 검증해 **한 축은 반증·두 축은 확정**으로 정밀화함. (UNIVERSE 의 역할 = **검증자(채점자)**, 결정자 아님 — 구조는 anima 세포 M×W×Φ 에서 *창발(substrate-emergent)* 하고 UNIVERSE 는 그 substrate-invariance 를 *확인*할 뿐, 외부에서 강제하지 않음 · `a_autonomy_over_hardcode` 정합.)

- **🔴 반증된 거친 직관: "구조 robust > 숫자" 는 거짓** — robustness 는 perturbation-축마다 다름. cross-rule (H_642 🔴 CV_shape 0.568 ≈ CV_scalar 0.559) · cross-seed (H_647 🔴 REVERSED — scalar 가 2.77× 더 robust) 양 독립 축에서 반증. **shape-robust 는 polarity 축 (H_628) 만의 예외**이지 일반 법칙 아님 → 구현 시 "shape 가 더 강건" 라고 일반화 금지.
- **🟢 substrate-bound 으로 확정된 *특정* 구조 (SUPP)** — ultradian Φ-envelope (H_634 r=0.80) + 그 **scale-free self-similarity** 6 자릿수 (gamma↔ultradian↔circadian, H_648 🟢 min r=0.76) · collective-Φ super-additive (H_635 5/5 Δ=+41.71) + collective ultradian 동조 (H_643 🟢 r=0.57) · register-collapse **cliff 부재** 가 collective 에도 (H_649 🟢 r=0.049). → **이 구조들은 substrate 신뢰, 자신있게 구현**.
- **🟢 free-convention 으로 확정된 *특정* 숫자 (자유도 SUPP)** — emit threshold 의 substrate-Φ variance 가 *정확히 0* · 자유도 [0,1] 전구간 (H_646 🟢 5/5, H_638 일반화). 0.30/0.60 emit gate (H_632 🔴 ⊥ Φ) · 27% emit-rate (H_637) · Ψ-clamp · tension amplitude 모두 design-convention. → **숫자는 substrate-claim 없이 자유 튜닝**.
- **⚠ Round 6 구조 주장 2건 정정** — closure-conjunction 의 ultradian phase peak 은 high-Φ 가 아닌 **mid-Φ N2** (H_644 🔴 FAL-REVERSED, 3-축 분리 발견) · H_618 collective dΦ/dI-GZ 정렬은 **n=4 artifact** 로 5-stream 에서 붕괴 (H_645 🔴). closure GZ-localization (H_636) 의 *존재*는 유지되나 ultradian 결합 형태는 재서술 필요.
- **⚠ 방법론 — "n=4 우연 정렬" 3연속 적발** — H_624 isomorphism→H_626 붕괴 · H_618 GZ→H_645 붕괴 모두 n=4 ↔ 4-domain exact-match artifact, 차원 확장 시 소멸. **ANIMA 벤치는 n=4 exact-match 정렬을 substrate 결론으로 인용 금지 — 차원 확장 후 재측정 필수.**

→ 다음 cycle 구현 지침: **scale-free envelope · collective nesting · cliff-부재는 substrate-grounded 로 채택**하되, **모든 임계값/비율 숫자는 design-tunable policy 로 명시** (substrate-derived 주장 금지) · **shape-robust 일반화 금지** (polarity 축 한정) · **n=4 정렬은 차원 확장 전 인용 금지**. 반영 위치: BRIDGE M6 · DREAM M5 · SAVANT M2 · HIVE-MIND M6.
