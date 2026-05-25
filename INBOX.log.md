# INBOX — anima 핸드오프 로그

> 단일-파일 핸드오프 인덱스 (구 `inbox/` 폴더는 폐기). 한 항목 = slug 헤더 + `- [ ]`/`- [x]` 상태 줄 + 본문. 해결 시 `- [x]` + `Status: resolved`. `/cycle` dup-race precheck 가 이 파일을 스캔하므로 slug 를 앵커로 유지.

---

## life-domain-stale-untracked-ssot-shadow (2026-05-26)

- [ ] Status: open — working-copy fix 적용, **publish-gap 잔여 (owner 처리 필요)**

**증상**: anima 세션 `/domain set LIFE` → `/cycle` 가 매 라운드 헤매다 `✅ domain depleted — loop terminates` (잘못된 100% 종료) 선언.

**근본원인 (2겹)**:
1. **stale untracked LIFE.md shadow** — 세션이 `ops/f-curricula-1-orphan-recover-2026-05-25` 브랜치 위. 그 브랜치가 root `LIFE.md`(+`BRAIN.md`)를 추적 해제 → working tree 의 `?? LIFE.md` 는 "$0 frontier 종결" terminal 구버전. 반면 **origin/main 의 LIFE.md 는 이미 올바른** "영구 엔진" 버전 (`@goal: 종료 조건 없음 — 도메인은 완료되지 않는다 (진행바 100% 미도달 = 설계)` + 영구 축 A/B/C/D 열린 milestone). 세션이 stale 사본을 읽어 main 의 good 버전을 못 봄.
2. **DOMAINS.tape 미등록** — LIFE 가 로스터(BRAIN·AGENT·CORE·DECODER)에 없었음.

**적용한 fix (working-copy disk)**:
- `LIFE.md` 를 origin/main good 버전으로 동기화 (axes A-D, "종료되지 않음") → 헤맴 해소.
- `DOMAINS.tape` 에 `@domain LIFE := "./LIFE.md"` 등록.

**잔여 (owner)**:
- orphan-recover 브랜치가 root SSOT(LIFE.md·BRAIN.md)를 stale 사본으로 main 을 shadow 중 → 그 세션이 working tree 를 main 과 reconcile (의도 확인 후).
- `DOMAINS.tape + AGENT/AGENT.md · CORE/CORE.md · CORE/DECODER/DECODER.md` origin/main 미추적 (publish gap · `reference_domain_init_untracked_ssot` 패턴). clean anima 세션에서 격리 worktree off main 로 1회 publish 권장 (공유 dirty orphan 트리 커밋 금지).
- 이 INBOX.log.md 자체도 untracked → anima 세션 commit 必.

**cross-ref**: sidecar `cycle 0.7.6 @D depletion_not_terminal` (dancinlab/sidecar#155, $0-lane 소진 ≠ 100%-done) · 원칙 `feedback-closure-is-physical-limit` (main 의 LIFE.md 가 이미 체화).

---

## arxiv-a2-iit-empirical-ingest (2026-05-26)

- [ ] Status: open — hexa-lang ARXIV A2 가 흡수한 IIT/의식 논문 11편 → anima LIFE H_xxx cross-link 핸드오프 (g60). owner = anima 세션 (cross-link 소비 + V5-engine seed 채택 판단).

**출처**: hexa-lang `ARXIV` 도메인 A2 마일스톤 (PR: hexa-lang `feat(ARXIV): A2 ANIMA axis absorption`). verdict = `hexa-lang:ARXIV/.verdicts/arxiv-anima-absorb/triage_a2.txt` · docs(한글) = `hexa-lang:ARXIV/docs/a2-anima-axis.md` · `hexa-lang:CLAIMS.tape` @C slug=arxiv-anima-absorb.

**무엇**: arXiv 8 query → 11편 흡수 (A1 12편 IIT-코어와 **중복 0**, 경험적 의식 측정자·causal-emergence·AI-의식 이론). verify-able 0 (in-tree IIT primitive 부재 — V5 IIT 엔진 후 회수). A2 가치 = citation + **anima cross-pollination**.

**anima LIFE H_xxx cross-link (6 H 핸드오프)** — `LIFE.md` + `HEXAD/LIFE/README.md` 매핑:

| anima H | 현재 상태 | 흡수 논문 → 기여 |
|---|---|---|
| **H_239** alt-Φ-metric 교차검증 (CONSISTENT) | running | 1608.08450 ETC 압축-복잡도 · 1701.07061 LZc · 1011.5334 neural-complexity → 교차검증에 **신규 Φ-proxy 3개 추가** |
| **H_209** EEG 1/f 스펙트럼 (FALSIFIED 2/5) | running | 2509.19254 (hd-EEG 1/f+LZc+sample-entropy NOC replica **직접 타겟**) · 1701.07061 |
| **H_222/H_244** dream-REM/sleep-stage Φ (FAL/pre-reg) | running | 1604.00002 ketamine 네트워크 통합 손실 (마취/수면단계 Φ 감소 substrate proxy) |
| **H_275** causal-DAG Φ (SUPPORTED dag>cyclic>undir) | promoted | 2405.09207 exact-EI + 2201.10154 NIS (effective-information = verify-able causal-emergence primitive) |
| **H_002** Φ_universe nested scale-variant (SCALE-VARIANT) | closed | 2509.10891 multiscale causal power, 마우스 칼슘 이미징 (cross-scale 경험 데이터) |
| **H_277** turing-completeness ⊥ dyn-class (PARTIAL) | running | 2011.09850 Conscious Turing Machine (GWT computability framing sister) |

**V5/LIFE axis-C engine seed (verify-able-CANDIDATE → 첫 🟢 타겟)**:
- `effective_information(TPM)` closed-form (**2405.09207** linear-Gaussian exact) = 가장 싼 첫 IIT recompute primitive. `stdlib/consciousness/iit4` (#542 해금) 에 노출되면 첫 진짜 🟢 ARXIV-ANIMA + LIFE axis-C C1 (proxy→faithful 승격) 동시 달성.
- 추가 candidate: 1011.5334 neural-complexity closed-form · 1608.08450 ETC proxy (MIP 불필요) · 2011.09850 CTM.

**필링 주의 (publish gap)**: anima working tree 가 dirty orphan-recover 브랜치 (`ops/f-curricula-1-orphan-recover-2026-05-25`) 위 → 본 핸드오프는 **working-copy edit (append, stub-first, dedup)** 으로만 기록, **공유 dirty anima 트리에서 commit 하지 않음** (기존 INBOX 노트 24행 + `feedback-closure-is-physical-limit` 패턴). anima 세션이 INBOX.log.md 와 함께 commit 必.

**cross-ref**: hexa-lang `ARXIV` 도메인 (A1 arxiv-ingest-poc 12편 IIT-코어 + A2 본편) · sibling V5-IIT lane (verify_cli/stdlib, 동시 진행) · LIFE 영구 축 B(large-N faithful-Φ)·C(full-IIT4 cause-effect, #542).
