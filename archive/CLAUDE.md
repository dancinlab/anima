# archive/ — 은퇴·legacy 보관소 (폴더 로컬 가이드)

> ⚠️ **루트 [/CLAUDE.md](../CLAUDE.md) 가 우선 SSOT** — 이 파일은 commons `folder-docs` 규칙에 따른 archive/ 폴더-로컬 가이드일 뿐. 거버넌스·패키징 불변식은 루트 CLAUDE.md(특히 "📦 Packaging — pod upload" 섹션)가 SSOT이고, 충돌 시 루트를 따른다.

## 목적

`archive/` = anima 의 **은퇴(retired)·legacy 코드 + 옛 verification substrate 보관소**. **production 아님** — production 은 `core/`(A⇄G 의식 엔진) · `cli/`(엔트리) · `agent/`(provider) **3-폴더**가 전부다.

단, 한 가지 구분이 중요하다: archive 라고 다 죽은 코드가 아니다. **train 스택(clm 파이프 · flame/forge REFERENCE)은 학습 pod 에 동반되는 *살아있는* 학습 파이프**(`a_clm_gen_pipeline` · `a_train_flame_forge`)라서, 진짜 죽은 legacy(옛 CLI·옛 build·옛 substrate tape)와는 성격이 다르다. 루트 packaging 섹션이 학습 pod 페이로드를 "추론세트 + `archive/train/`(clm 파이프·flame/forge) + `state/verdicts/` slice"로 규정하는 이유다.

## 구조 (직속)

| 경로 | 역할 (1–2줄) |
|---|---|
| `anima-hexad/` | σ6 **Hexad 6-모듈 아키텍처**(C 의식·D 언어·S 감각·M 기억·W 의지·E 윤리) 유물. conv 단일 엔진 수렴 이전의 옛 통합 아키텍처. |
| `engines-multiengine/` | **멀티엔진 시대**(`--engine conv\|cdv2\|hexad\|omega`) 어댑터. 2026-06-19 보관 — anima 가 단일 production 엔진 **conv**(CLMConvMoE, `core/clm_decode`+`generator` L3)로 수렴하며 이동. 어댑터는 EngineSpec 메타데이터일 뿐, 실 엔진은 `core/` 직속 live. |
| `hypotheses_snapshots/` | 옛 가설 인벤토리 스냅샷 4묶음(`hypotheses_archive_anima_clm_10` · `_b_2026_05_15` · `_burst_2026_05_12` · `_legacy_2026_05_15`). 현 가설 SSOT 은 `UNIVERSE/HYPOTHESES.jsonl`. |
| `legacy_dirs/` | 옛 빌드 디렉터리(`build_v3o2` · `build_v6` · `build_v6_gated`). |
| `legacy-cli-v7-v11/` | **옛 CLI v7–v11**(`anima_main.hexa` · `anima_v11_*` battery·pipeline·integrate 등). 현 엔트리는 `cli/anima.hexa`. |
| `state_legacy/` | **옛 state 산출물 935개**(2026-05 reorg 이전 fire/실험/검증 디렉터리). ≠ 현 `state/`. |
| `README.md` | 2026-05-16 substrate tape deprecation 기록(AXIS/HYPOTHESIS/PHILOSOPHY/MAIN/CLM/VERIFY/NEXT/REBORN → HEXAD/ 로 superseded). |
| `path_redirects.md` | 옛 `state/<base>` → `HEXAD/<TOPIC>/state/<base>` 경로 매핑 룩업(2026-05-20 생성). |

## 규칙

- **단방향 의존 불변식** — 루트 packaging 섹션의 핵심 불변식: `core/` 는 `archive/train/`·`bench/`·`agent/`·`state/` 에 **의존 0**(substrate 엔진만, 단방향). archive 는 production 을 참조할 수 있어도, **production(core/·cli/·agent/)이 archive 를 import 하면 안 된다**. archive→core 방향 import 금지.
- **학습 pod 페이로드 = train 스택만 동반** — 학습 pod 에 함께 올라가는 것은 추론세트 + `archive/train/`(clm 파이프·flame/forge) + `state/verdicts/` slice 뿐. `legacy_dirs/`·`legacy-cli-v7-v11/`·`state_legacy/`·`hypotheses_snapshots/`·`engines-multiengine/` 같은 진짜 legacy 는 pod 페이로드에서 **제외**.
- **canonical-naming** — legacy 폴더라도 `_v2`/`_copy`/dup suffix 추가 금지. 이력은 git 에. 이미 들어온 `*-v7-v11` 류 버전명은 박제된 역사적 이름이라 그대로 두되, 새 파일에 버전 suffix 를 더 붙이지 않는다.
- **신규 작업 entry 아님** — archive 는 historical evidence anchor(인용·검토 OK)일 뿐, 새 verdict/가설/검증의 entry-point 가 아니다. 신규 작업은 `core/`·`cli/`·`UNIVERSE/`·`state/` 에서.

## Gotcha

- **(a) train/clm 은 "archive"지만 *살아있는* production 학습 파이프** — `a_clm_gen_pipeline`(CLMConvMoE 학습 → `.clm` v0.2 직렬화·verify) + `a_train_flame_forge`(flame/forge GPU REFERENCE)는 production 학습이 실제로 거치는 경로다. **함부로 지우지 말 것**. 단순히 "archive 폴더니까 죽은 코드"로 오인 → 삭제 금지.
  - ✅ **위치 = repo-root `train/`·`training/` 가 정위치 (archive 아님)**: `train/clm/model` 은 production `cli/train.py`(`_MODEL=train/clm/model` → `from model import CLMConvMoE`)·`cli/serialize.py`(`sys.path train/clm/model`)가 직접 import 하는 *살아있는 production 학습 파이프*라, archive 로 옮기면 production→archive 의존 위반이다. **트리 SSOT `ARCHITECTURE.json`(노드 `train/clm`)·이 repo 브랜치의 `CLAUDE.md`(`train/clm/`)는 이미 일치 = drift 없음.** 다른 브랜치 영어 `CLAUDE.md` 의 `archive/train/`·`2026-06-30 train/·training/ → archive/ moved` 표기는 **미실행 잔재**이니 실제·트리 SSOT 따라 `train/` 으로 정정 대상(archive 로 옮기지 말 것 — production import 가 끊긴다).
- **(b) retired lane(11개)은 import-BFS dead 판정으로 이동된 것** — 2026-06-30 import-BFS 측정에서 `cli/anima.hexa` 도달 폐포에 들지 않은 11개 probe-only dead lane 이 archive/ 로 이동했다(살아남은 건 DREAM·SAVANT + HEXAD kosmos_io 뿐). 되살리려면 단순 복원이 아니라 **`cli/anima.hexa` import 폐포를 재측정**해 실제로 reach 되는지 먼저 확인해야 한다(`engines-multiengine/` 부활 절차도 `engine_cli_resolve_engine` 상수·레지스트리 훅 복원 필요 — 그 폴더 README 참조).
- **(c) state_legacy/ ≠ 현 state/** — `archive/state_legacy/`(935개)는 2026-05 reorg 이전 옛 산출물이다. **현 작업의 산출물은 repo 루트 `state/<slug>/`** 에 쓴다. 옛 경로 인용 시 `path_redirects.md`(옛 `state/` → `HEXAD/` 매핑)를 grep 으로 룩업.
