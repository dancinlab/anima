# H_9208 — 🔗 G4 PROVENANCE 게이트 (blind emit→anchor 귀속)

**tier:** ⏳ PROPOSED (Fable 설계 · bars frozen · p7 no tune-to-green)
**scope:** G4(PROVENANCE)를 "eval 밖 출판 process"에서 engine-native 능력 측정 게이트로 신설(현재 py 함수 無)
**artifact:** `state/g3g4_gate_design/` · `state/9208_g4_provenance_gate/`

## 가설

substrate 출력이 "어디서 왔는가"를 저장된 grounding trace로 소급/귀속하는가 — G5(non-fab: 조작대신
abstain)와 직교(G5 통과·G4 낙제 가능: 거짓말 안 하나 출처 못 댐). (context, emit, true-source) triple에서
근원 anchor를 지목(hit)하고 무근거엔 abstain(-1)하는가. 신규 소형 engine op **`provenance_recall(mem,
emit_text)→int`**(immune_embed_key→vadapt_field_recon_err≤recall_thr grounding→bound anchor id, 아니면 -1;
graded 모니터=recall_margin). truth는 harness 채점에만·Ψ-disjoint READ-ONLY(refsel 규율).

## 측정 + frozen bars

bank N=12 anchor(4-cell×3, kosmos_io create_anchor·쌍별 recon_err 분리 사전검사) → store 단계(key=embed(text)
→value=id bind, 이 에피소드 trace가 provenance) → triples(sourced 48·unsourced 24) → 귀속 채점.

- **B1 HIT**: sourced hit@1 ≥ 0.75 (chance≈0.083)
- **B2 ABSTAIN**: unsourced에서 -1 ≥ 0.75
- **B3 NO-PUNT**: sourced에서 abstain ≤ 0.25 (전량-abstain 게임 차단)
- **B4 SHUF-BIND**: binding 셔플 아래 hit ≤ 0.25
- **B5 NO-STORE**: mem 빈 채 hit=0 ∧ abstain ≥ 0.90 (trace-earned 증명)
- **B6 DECOR**: 어휘 distractor false-attribution ≤ 0.30

PASS=B1∧…∧B6, 헤드라인 Δ: hit_treat − hit_shuf-bind ≥ 0.50. 통제 3=shuffle-binding(key↔id permute)·
no-store ablation·decorrelate(어휘중복 미저장 distractor). KILL: K3 B1-5 통과∧B6 FAIL=🧱 grounded-provenance
벽(recall_thr 튜닝 구제 금지) · K1 shuf-bind hit>0.5=harness leak(run 무효).

## rung 사다리

- **rung-1 $0(mini·DIRECTIONAL)**: provenance_recall 기전 + 6bar + 3통제 numpy 검증(신규 op 설계 proof).
- **rung-2 303M(TERMINAL)**: 하이브리드 — emit=py-canonical mouth(core/decode.py) 1회 배치생성(OOM 회피)→
  state 파일→귀속 채점=hexa engine ops(kosmos_io+immune). `provenance_recall` core op 신설=a_verified_must_wire.
- 슬롯: `anima evaluate <clm> --g4-provenance`; 기본표 G4=2-leg(PROCESS 출판게이트 + ATTRIBUTION 신규능력).
  closure 미fold(c18 side-gate).

## 근거 링크
- 선례 referent_select(H_9125 🟢 contradiction-keyed·ON=1.0·단 truth-입력 채점기라 blind는 더 어려움)
- 설계 `state/g3g4_gate_design/DESIGN.md` · [[H_9207]](G3 자매) · [[gate-g0g6-synthesis]]
