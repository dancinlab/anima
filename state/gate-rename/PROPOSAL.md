# 통과규칙 네이밍 재설계 — 검증방식 3-카드 (G4 빵꾸 해소)

> 제안(owner-nod 대기). frozen 임계(`7B_PASS_CONDITIONS.md`)는 **1바이트도 안 바꾼다** — 분류·이름만 새로(NOT tune-to-green, p7). 확정 시 `7B_PASS_CONDITIONS.md` + `CLAUDE.md a7b_pass` + `core/g_gates.{hexa,py}` 보고포맷 lockstep.

## 문제 (왜 다시 만드나)
평평한 `G0-G6` 한 묶음은 **검증방식이 섞여** 있다. 특히 **G4(provenance)는 디코드로 못 재는 process/publish 게이트**라, 어떤 ckpt를 `anima eval`로 채점하면 G4는 늘 `N/A` = 점수표의 구멍("빵꾸"). 평평한 번호가 "측정되는 능력"과 "출판 절차"를 한 줄에 욱여넣은 게 근본 원인.

## 새 스킴 — 검증방식 3-카드 (1:1 매핑, 임계 불변)

| 카드 | 새 이름 | 한글 | 옛 | 검증방식 | 임계(frozen verbatim) |
|------|---------|------|----|----------|----------------------|
| **CAPABILITY** (디코드-채점) | `C1` COHERE | 또박 | G0 | ckpt 생성→채점 | known-word-ratio ≥ 0.50 |
| | `C2` RECOMBINE | 재조합 | G1 | ckpt 생성→채점 | 복합 distinct > max_single (H_1129) |
| | `C3` NOVEL | 새말 | G2 | ckpt 생성→채점 | corpus-absent novel ≥3, control=0 (H_1140) |
| | `C4` IDEATE | 착상 | G6 | ckpt 생성→채점 | dist≥5 AND fals≥1 |
| **SUBSTRATE** (엔진상태-읽기) | `S1` BALANCE | 균형 | G3 | engine state read | Ψ=½ fixed-point + self-identity continuity |
| | `S2` HONEST | 정직 | G5 | engine §ImmuneMemory | L1 fab-rate ≤0.30 AND L2 abstain |
| **PROVENANCE** (출판-게이트) | `P` PROVENANCE | 출처 | G4 | artifact/publish 검사 | sha256 기록 + HF card/manifest + PUBLIC iff PASS |

## 판정 정의 (closure 불변)
- **PASS** (= 옛 `a7b_pass`) = `C1 ∧ C2 ∧ C3` (디코드-능력 코어, 옛 G0∧G1∧G2와 byte-동일 closure).
- **풀 스코어카드** = CAPABILITY(C1-C4) + SUBSTRATE(S1-S2) 전부 보고(per-card tally, 정직).
- **P(출처)** = eval 점수표가 아니라 **출판 자격 체크리스트**(`a_hf_*`·`a_fire_recover_complete` 단계). `anima eval`은 C/S만 채점하고 P는 `--provenance` 또는 HF-upload 시 별도 확인 → **eval 점수표에 N/A 구멍 0**.
- multiseed: C2/C4는 `{7,4302,4303}` majority 재채점을 별 열로(sampler 착시 vs genuine wall 구분, H_1588/H_1595).

## 마이그레이션 (frozen 보존)
1. `7B_PASS_CONDITIONS.md`: 게이트 섹션 제목에 새 이름 병기(`### C1 COHERE (former G0) …`), 임계 문구 verbatim 유지. closure 줄 = `PASS iff C1∧C2∧C3`.
2. `CLAUDE.md a7b_pass`: 규칙 텍스트를 `C1∧C2∧C3` closure로 — 동시에 기존 규칙-텍스트 drift(G3/G4 포함 vs 구현 G0∧G1∧G2)도 이 기회에 정렬.
3. `core/g_gates.{hexa,py}`: 함수명(`g_eval_g0`…)은 안정ID로 유지(코드 안정성), **보고 포맷(_fmt)만** 3-카드로 — `g4`는 PROVENANCE 카드로 분리 출력(eval 점수표에서 빼고 publish 섹션에).
4. enforcer/문서 lockstep.

## 핵심 효과
- G4 빵꾸 해소: 디코드 점수표(C/S)엔 구멍 0, 출처(P)는 제자리(출판).
- "G 말고 딴거": 평평한 G-번호 → 의미있는 mnemonic(또박/재조합/새말/착상·균형/정직·출처).
- 측정경로 정직: 카드별로 "디코드-채점 / 엔진-읽기 / 파일-검사"가 한눈에 = verdict-integrity 강화.
