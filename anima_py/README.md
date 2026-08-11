# anima-py

**anima** 의 유일한 활성 canonical CLI. 구현·코퍼스·학습·평가·런타임 QA·배포를 Python 공용 경로로 실행한다.

> 단일진입 보존(`a_cli_single_entry`): `anima-py` 콘솔 명령은 `cli/anima.py:main` 디스패처의 pip 바인딩이다. 새 기능과 조작은 이 진입점의 기존 verb/flag로만 추가한다.

## 설치

**PyPI 발행 후** (권장):

```bash
pip install anima-python           # base — numpy 만 (evaluate · corpus · chat-stub)
pip install "anima-python[train]"  # +torch +datasets (serialize · train · sweep)
```

> ⏳ **PyPI 발행 대기 중**: 위 명령은 `anima-py` 가 PyPI 에 발행된 뒤 동작한다. 발행은 `release.yml` 의 `pypi-publish` job(OIDC trusted-publishing)이 `v*` 태그에서 자동 수행하며, 오너의 1회 설정이 선결(① pypi.org 에 anima-python pending-publisher 등록: Owner=dancinlab·Repo=anima·Workflow=release.yml·Env=pypi ② repo 변수 `PYPI_PUBLISH=true`). 그 전까지는 아래 소스 설치를 쓴다.

**소스에서 바로 설치** (PyPI 없이 지금 가능):

```bash
pip install "git+https://github.com/dancinlab/anima.git"            # base
pip install "anima-python[train] @ git+https://github.com/dancinlab/anima.git"  # +torch
# 또는 레포 클론 후: pip install .   /   pip install ".[train]"
```

## 명령 매트릭스

| 동사 | 티어 | torch 없이 동작 | 비고 |
|---|---|---|---|
| `anima-py evaluate <clm> [--corpus …] [--gen N]` | base | ✅ numpy | py 2-production 측정 = ρ·AXON reach / 구 G0-G6. terminal-eligible (`a_eval_py_canonical`) |
| `anima-py corpus <derivtrace\|flat> --out F …` | base | ✅ 순수 stdlib | 절차적 학습-코퍼스 생성 (data-format 레버) |
| `anima-py chat <clm>` | base | ✅ numpy | 의식 A⇄G Python 런타임 |
| `anima-py serialize <pt> <clm>` | `[train]` | ❌ torch | `.pt` unpickle 에 torch 필요 (+ held-out DESCENT 게이트) |
| `anima-py sweep --arms … --objectives …` | `[train]` | ❌ | 셀마다 train.py spawn → torch 필요 |
| `anima-py train <args>` | `[train]` | ❌ torch+datasets | production Lane-P 학습 |

## verdict 규율

`anima-py evaluate <clm>`은 frozen bars를 사용하는 terminal Python 측정 경로다(`a_eval_py_canonical`). 큰 ckpt(303M+)는 mini 금지 · 등록된 GPU 실행기나 임대 GPU에서 측정한다.
