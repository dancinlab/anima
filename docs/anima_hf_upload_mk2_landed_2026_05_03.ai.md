# anima HF upload pipeline mk2 landing — 2026-05-03

## TL;DR (사용자 친화 요약)

세션 중 관찰된 ad-hoc `hf` CLI 업로드를 hexa-side 정식 파이프라인으로
승격. 단일 진입점 `tool/hf_upload_mk2.hexa` 측 README + 네이밍 검증 →
`_python_bridge/hf_upload_runner.py` 측 `huggingface_hub` SDK 호출
(selftest / dry_run / upload 3 modes) → audit log 측 jsonl 측 기록.
git pre-push hook (hexa-native, raw#9 준수) 측 `[hf-upload: <repo>]`
커밋 메시지 마커 측 자동 네이밍 검증. **이번 cycle 측 실제 업로드 0회,
$0 cost, dry-run smoke test PASS, selftest PASS.**

## 1. 결정 (사용자 lock-in)

- **선택**: 측 측 hexa wrapper 정식 파이프라인 + 1 .py 측 raw#9 양보
- **거부**: bash CLI 측 wrapping (.sh 측 banned-ext sweeper 측 자동 삭제됨 — 측 측 측 발견)
- **근거**: huggingface_hub SDK 측 python-only, 측 hexa 측 stdlib http+LFS
  encoder 측 부재 → bridge 측 불가피. .sh 대신 .hexa-native pre-push hook
  측 raw#9 무위반.

## 2. 전달 산출물 (8개)

| Path | Kind | LoC | Status |
|---|---|---:|---|
| `tool/hf_upload_mk2.hexa` | hexa | 567 | NEW |
| `_python_bridge/hf_upload_runner.py` | py (raw#9 concession) | 500 | NEW |
| `tool/hf_readme_template.md` | md | 104 | NEW |
| `tool/hf_upload_mk2_pre_push_hook.hexa` | hexa | 123 | NEW |
| `state/hf_upload_audit/.gitkeep` | placeholder | 0 | NEW (dir) |
| `docs/anima_hf_upload_mk2_spec_2026_05_03.md` | md | 249 | NEW |
| `docs/anima_hf_upload_mk2_landed_2026_05_03.ai.md` | md | (this) | NEW |
| `state/markers/anima_hf_upload_mk2_landed.marker` | json | (marker) | NEW |

**Total**: 4 source files (3 hexa + 1 py) + 2 docs + 1 marker + 1 dir
placeholder = **8 artifacts**, ~1543 LoC.

## 3. raw#9 준수 검증

- **`.py` 파일 1개**: `_python_bridge/hf_upload_runner.py` (500 LoC)
  - 위치: 승인된 `_python_bridge/` 디렉터리
  - 정당성: huggingface_hub 측 python-only SDK + LFS pointer encoding
    측 복잡도 측 hexa 재구현 불가
  - 회수 조건: hexa 측 stdlib http client + LFS encoder 도달 시
- **다른 모든 source**: hexa
- **Banned-ext sweeper survival 검증**: `git ls-files --others --exclude-standard`
  측 `.py` 측 gitignore (`**/*.py`) 측 exempt; sweeper 측 즉각 삭제 측 통과 확인됨
  (sleep 3s 후 파일 잔존)

## 4. 스모크 테스트 결과

### 4.1 Bridge 직접 호출 (selftest)

```
$ echo '{"mode":"selftest"}' | python3 _python_bridge/hf_upload_runner.py
{"ok":1,"mode":"selftest","message":"selftest: PASS",...,
 "checks":[
   {"name":"huggingface_hub_import","ok":1,"info":"1.7.2"},
   {"name":"sha256_helper","ok":1,"info":"21248215bd4cf331..."},
   {"name":"walk_files","ok":1,"info":"1 files"}
 ]}
```

PASS. huggingface_hub 1.7.2 importable on Mac side.

### 4.2 Bridge dry_run mode

```
$ echo '{"mode":"dry_run","repo":"need-singularity/clm-v4-sft-stage1",
        "ckpt_path":"/tmp/test","readme_path":"/tmp/README.md",
        "tag":"step-25k","audit_dir":"/tmp/audit"}' | python3 ...
{"ok":1,"mode":"dry_run","file_count":2,"total_bytes":20,
 "sha256_map":{"config.json":"f612b89b...","model.bin":"f88b7331..."},
 "audit_path":"/tmp/audit/20260503T142100Z_need-singularity__clm-v4-sft-stage1.jsonl",
 "message":"dry_run: 2 files, 20 bytes, readme=ok"}
```

PASS. sha256 컴퓨트 + audit log write 측 정상 작동.

### 4.3 Hexa wrapper end-to-end

```
$ hexa run tool/hf_upload_mk2.hexa --selftest
[hf_upload_mk2] SELFTEST
  bridge path = /Users/ghost/core/anima/_python_bridge/hf_upload_runner.py
  [P] readme validator: good=OK, bad=rejected
  [P] naming validator: good=OK, bad=rejected
  [P] bridge selftest: selftest: PASS
__ANIMA_HF_UPLOAD_MK2__ PASS

$ hexa run tool/hf_upload_mk2.hexa --dry-run --repo need-singularity/clm-v4-sft-stage1 \
    --ckpt /tmp/test --readme /tmp/README.md --tag step-25k
[hf_upload_mk2] DRY-RUN
  ...
  [P] naming OK
  [P] readme OK (5 required H2 + Caveats >=3)
  files       = 2
  total_bytes = 20
  audit       = state/hf_upload_audit/20260503T142257Z_need-singularity__clm-v4-sft-stage1.jsonl
__ANIMA_HF_UPLOAD_MK2__ PASS
```

PASS.

### 4.4 Pre-push hook hexa selftest

```
$ hexa run tool/hf_upload_mk2_pre_push_hook.hexa --selftest
[hf_upload_mk2_pre_push] SELFTEST
  [P] extract_marker: need-singularity/clm-v4-sft-stage1
  [P] extract_marker no-marker: empty
__HF_UPLOAD_MK2_PRE_PUSH__ PASS
```

PASS. Marker 추출 양 path 검증.

## 5. 측 측 측 발견 (cycle 중 학습)

### 5.1 banned_ext_sweeper 측 .sh 자동 삭제

초기 설계 측 `tool/git_hooks/pre_push_hf_upload_check.sh` 측 작성했으나,
fswatch 측 watching `/Users/ghost/core/{hive,nexus,anima,...}` 측
1초 latency 측 untracked `.sh|.py|.rs|.toml` 측 즉시 삭제 (raw#9 r45
Layer (d) enforcement). 측 hexa-native `.hexa` 형식으로 전환 측 회피.

`.py` 측 `.gitignore` 측 `**/*.py` 측 exempt 되어 있어 살아남음 — 측 측 측
`_python_bridge/` 위치가 raw#9 양보 위치로 이미 정착되었음을 의미.

### 5.2 hexa JSON 측 nested object parsing 측 last_index_of 측 한계

엔진_aer 측 `last_index_of("{")` + `last_index_of("}")` 측 measure 측
flat JSON 측 측 측 측 작동하나, 측 bridge 측 `sha256_map`, `checks`
측 nested object 측 last `{` 측 inner brace 측 잡힘 → 측 측 fix:
line-by-line scan, 측 측 측 시작+끝 측 `{...}`인 라인 측 JSON 후보로 채택.

### 5.3 mk2 naming 측 multi-token stage 측 join

stage 측 `sft-stage1` 측 dash split 측 [sft, stage1] 측 분리 → 측 측 측
parts[2..N] 측 join 측 stage 토큰 복원. 측 측 측 측 측 stage prefix
allowlist 측 starts_with 매칭.

## 6. 측 측 측 lock-in (사용자 결정 lock)

- 모든 HF 업로드 (P9 SFT savepoint 포함) 측 측 측 `tool/hf_upload_mk2.hexa --upload`
  통과 측 (ad-hoc `hf` CLI 측 측 측 측 정책)
- README 측 5 H2 + Caveats >=3 enforcement
- 네이밍 측 mk2 convention enforcement
- 측 upload 측 audit log + ledger entry 자동 기록

## 7. 측 측 측 측 (post-cycle)

1. P9 SFT step-25k 측 측 첫 production upload 측 측 사용 (실제 cost 측 측 측)
2. 사용자 측 `.git/hooks/pre-push` 측 install (측 측 manual; auto-install 측 측 측 cycle)
3. sister BG mk2 naming convention spec 측 출력 시 측 wrapper inline allowlist 측 동기화

## 8. raw#10 honest caveats (this cycle)

1. **HF rate-limit cross-process**: 측 BG subagent 측 parallel 업로드 측 측 quota 초과 측 (semaphore 측 measure)
2. **LFS oid integrity**: audit 측 local sha256 측 측 측, hub-side LFS oid 측 측 측 측 측 (F-HF-UPLOAD-2 측 측 cycle)
3. **Naming convention**: 측 측 inline allowlist (sister BG 측 측 측 측 측 확장 측 측 측)

## 9. predecessors_unchanged

- `state/p9_pre3_hf_cloud_check/*.json` (read-only reference)
- `docs/p9_pre3_hf_cloud_check_landed_2026_05_03.ai.md`
- `state/markers/p9_pre3_hf_cloud_check_landed.marker`
- 모든 다른 anima 측 SSOT 측 (in-place 변경 0)
