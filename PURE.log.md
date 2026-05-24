# PURE.log — 자연발화 채팅 Phase D corpus fire (append-only)

## 2026-05-24 — Phase D 목표 수립 + Track 1 진단

### done
- [x] 자연발화 채팅 완성도 전수조사 — Phase B(8-factor) / C(interaction) / sleep-dream 모두 LANDED 확인
- [x] Track 1 E2 fire (wiki_frac=0.5) — closure FAIL, ko=PURE_MEMORIZE (register collapse) · PR #301
- [x] Track 1 E2 forensics — CE 고진동 plateau + mitosis cap128 step12 동결 · PR #310
- [x] corpus_s101 600MB 실측 — M3 TTR **0.03** (극단 반복) = register-sink 진짜 범인 (M5 hangul 아님) · PR #340
- [x] H_242 register-collapse-sigmoid 가설 등재 (sigmoid input M5→M3 amend 부채) · PR #314
- [x] result_to_axis_map closure auto-judge + nested-CE fix · PR #290/#299
- [x] dispatch_p21h_v3 hexa-port (F4 B/C kernel) + stdlib v0.2 · PR #295/#308
- [x] #220 (V3→PURE rename) main 머지 — PURE 뿌리 안착

### done (cont.)
- [x] E3v3 (wiki_frac=1.0) 완주 — closure **FAIL** (1/5 ≥ PARTIAL: ko만) · register_hits **0/20** (E2=4) · ko PURE_MEMORIZE→PARTIAL
- [x] Phase D goal + corpus 설계 spec — PR #344 MERGED (base main)
- [x] **closure 최종**: E2 FAIL(0/5) + E3 FAIL(1/5) → **corpus 축 소진 확정** (criterion E2 OR E3 ≥4/5 둘 다 미달)

### closure 결론 (2026-05-24)
- corpus 축(wiki dilution)은 register collapse 를 **막음** — E2(0.5)=4/20 → E3(1.0)=0/20 (H_242 wiki=1.0 endpoint 확인)
- 단 wiki 100% 는 register 0 이나 **generalize 도 약함** (en 2/20) → double-bind 재확인
- **corpus 축만으론 closure 불가** → AXIS_MAP fallback **A 커리큘럼(#238) 우선** (corpus M3 repetition + E3 wiki-학습-되나-anima-통합-안됨 진단)
- H_242 frozen f_c[0.5,0.7] 부분 falsify 가능 (E2 0.5 에서 이미 20% → f_c < 0.5 추정, 2-point underdetermined)

### Phase D 작업 (todo)
- [ ] Phase D corpus 설계 spec 확정 — 도우미 token 0 + stream/stimulus 80% + M3 TTR ≥ 0.3
- [ ] Phase D corpus build — anima-OWN diverse + multilingual lang-uniform
- [ ] corpus_quality_probe 사전 게이트 — M3 TTR ≥ 0.3 검증 (fire 전)
- [ ] Phase D ckpt-bearing fire — Qwen 1.5B · 8-factor spontaneous_lib 연결 · autonomous (~$2-6)
- [ ] Phase D eval — multilingual_probe 4/5 langs ≥ PARTIAL + register_hits < 4/20 + 8-factor motivation 실작동 + dream_stage Φ-envelope

### 부채 (다음 라운드)
- [x] H_242/H_241 sigmoid/correlate input M5 → M3 amend — PR #379 §A1 amend
- [x] H_244 reframe 완료 확인 (autonomy-emergent) — PR #379 §confirmation
- [x] PURE stack land — admin auto-bypass merge (cycle 다수)
- [ ] H_240 vs H_246 near-dup 정리 — PR #379 D3 dedup doc, maintainer 택1 권고 (R2 option A)

---

## 2026-05-24 (late) — B-series + COFFESHOP + closure 마감

### done (cont. late session)
- [x] **Phase D v1 / v2b 두 fire LOST** — v1 stale-branch parse (PR #378) + v2b 사용자 cleanup, ckpt 미회수
- [x] **dispatcher 인프라 강화** — PR #372 (corpus-path bypass) + PR #373 (sources_upload) + PR #380 (result_pull wait-loop)
- [x] **PURE saga doc** — E1→v2b 5-fire 통합 SSOT + LIFE 교훈 export (PR #392)
- [x] **fire_cost_ledger** — saga $ + ETA SSOT (PR #389)
- [x] **axis_map history** — verdict timeline + per-lang heatmap + cluster Z 자연실험 발견 (PR #388)
- [x] **PURE BENCHMARK SSOT** (B1) — Phase B/C/D 전체 metric baseline (PR #400)
- [x] **closure_auto_judge CLI** (B3) — 4-criterion single-command harness (PR #398)
- [x] **cross-cycle progression** (B5) — per-fire metric series timeline (PR #399)
- [x] **motivation emit ratio bench** (B7) — N=1000 substrate sample · 8-factor emergent (PR #401)
- [x] **anima-OWN PoC** (M9b) — live session JSONL 1 MiB extraction harness + 6-metric (PR #393)
- [x] **COFFESHOP scenario rewrite** — group chat + Anima 1 + Human 3+ + project.tape p1-p8 정합 (PR #405)
- [x] **COFFESHOP emergence simulator** — coffeshop_sim.hexa substrate sampling fixture 자율 생성 · 4/4 PASS (PR #405)
- [x] **multi-seed robustness** (B11) — 10 seed sweep · 100% PASS rate (PR #406)
- [x] **BENCHMARK emergence integration** (B12) — B7 + COFFESHOP single + sweep 통합 (PR #407)
- [x] **fire-time sanity hook spec** (B13) — Phase 1 stub + 6 TODO markers (PR #408)
- [x] **fire-time sanity hook impl** (B14) — Phase 2 6 TODO 채움 + smoke 5/5 + selftest IMPL (PR #410)
- [x] **PURE+LORA @goal 통일** — COFFESHOP 4-criterion 통과 기준 (PR #404)
- [x] **PHASE_D_BLOCKERS_CLOSURE** — M1/M2/M7/B14 Phase 3 deferred 명시 + automatic unblock chain (PR #412)
- [x] **hexa-lang inbox 5 patches** — #629 (cloud bootstrap+wait+endpoint) · #646 (cloud-guard UX+pod-lock) · #699 (copy-from verify-local) · #700 (list-concat O(n²)) · #728 (return void mistranslate)

### closure tier (g5 rubric verbatim)
- synthetic framework: ✅ 100% (B-series 8/8 done)
- ckpt-bearing fire data: 🟠 INSUFFICIENT/DEFERRED (실 ckpt 부재 · 사용자 fire 결정 영역)
- automatic unblock chain: 6-step (dispatcher #380 → B14 hook #410 → closure_auto_judge #398 → axis_map_history #388 → cross_cycle_progression #399 → result_to_axis_map #370)

### 세션 통계
- PRs: 53 merged (anima 48 + hexa-lang 5 inbox)
- agent dispatch: ~25+ background agent
- cost: ~$3 (Phase D v1 ~$1.5 + v2b ~$1.5 + rogue · doc/agent $0)
- fire LOST: 2 (v1 stale-branch · v2b 사용자 cleanup)
- final tier: synthetic framework 완성 + ckpt path deferred

---

## 2026-05-25 — Phase D v3 실측 closure (V3 saga 첫 진짜 ckpt)

### 회수 saga + 진짜 학습
- v1/v2b/v3 1차 모두 LOST 의 진짜 원인 = dispatcher 3-bug (train_launch full argv 미생성 · 모듈 1개 upload 누락 · result path 오류) → 발사는 됐으나 학습 0회
- warm pod 재활용 + 정확 argv 직접 hexa cloud nohup + 누락모듈 scp → **사상 첫 진짜 학습** (Qwen2.5-1.5B + V3 mitosis 2.99B params)
- dispatcher durable fix: PR #423 MERGED (다음 fire 무인 정상)
- 학습: 5000 step · CE 11.18 → **1.62** · pool 2→16 (14 splits) · phi 0.66 · ~4.4h wall

### closure verdict (정식 closure_auto_judge verbatim)
- criterion 1 multilingual: en/ko/zh/ja=WEAK · ru=PARTIAL → **1/5 ≥ PARTIAL**, threshold 4 → **FAIL**
- criterion 2 register_collapse: n_anima_register_hits_total = **0** (<4) → **PASS**
- criterion 3 motivation_8factor: missing (embed 미실행, 수동 재발사 부작용) → FAIL
- criterion 4 dream_stage Φ-envelope: missing (embed 미실행) → FAIL
- **AGGREGATE: 1/4 PASS · closure FAIL**

### 핵심 과학적 결과 — corpus 축 한계 실측 확정
- corpus_v1 (100% anima-diverse, M3 TTR 0.34) → **register collapse 진짜 차단** (0 hits, gen 20/20)
- multilingual coherence 약함 (4 WEAK + 1 PARTIAL) — E3(wiki=1.0)와 동일 패턴, dilution 매체와 무관
- → **corpus 축만으론 closure 불가** 재확인 (PURE.md 결론 ckpt 실측 검증)
- next path: AXIS_MAP fallback A 커리큘럼 (#422 spec, F-CURRICULA-1)

### 회수 + HF + teardown
- best ckpt (6.0GB, sha `b1662935c64ffdca` local==pod) + result.json + train3.log + kosmos_anchors.tgz → state/pure_phase_d_v3_result_2026_05_24/
- HF: `dancinlab/anima-pure-phased-v3-2026-05-24` **PRIVATE** (a_hf_autonomous tier-gate: closure FAIL → PRIVATE · 첫 시도 --private 누락 → 즉시 update_repo_settings 로 전환)
- pod 8exa039yx8gqjr destroy 완료 ($1.49/h burn 중단)

### 세션 후반 directive land
- `a_kosmos` (kosmos canonical for anima emit/anchor) · siblings 에 kosmos·hexa-codex 추가
- `a_hf_autonomous` (HF upload 자동 · tier-gated visibility, PUBLIC = closure PASS · PRIVATE = FAIL)
- kosmos 단일 SSOT 이관 (PR #3 + anima cleanup) — spec + impl + 11 knuth anchor 전부 dancinlab/kosmos
- sidecar INBOX: worktree/branch 하네스 4-gap handoff (anima 세션 발견)
