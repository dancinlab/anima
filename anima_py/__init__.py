# ==========================================================================
# anima_py — anima py CLI 의 pip 콘솔 런처 (pyproject.toml [project.scripts]).
# 단일진입(a_cli_single_entry): 이 파일은 디스패처가 아니다 — sys.path 부트만
# 하고 canonical 디스패처 cli/anima.py:main 에 그대로 위임한다(동일 진입,
# 채널은 pip). 유일한 활성 진입은 `anima-py`(pip install anima-python)다.
# #2603 가드는 __main__ 전용이라
# import 경유인 이 경로에선 발화하지 않는다(무손상).
# ==========================================================================
import os
import sys

_PKG = os.path.dirname(os.path.abspath(__file__))


def _bootstrap():
    # 설치 레이아웃 = site-packages/anima_py/{cli,core}/ (repo 의 cli/·core/ 를
    # package-dir 매핑으로 그대로 실은 형제 디렉토리). flat import (`import anima`,
    # `import decode` 등) 해석을 위해 두 디렉토리를 sys.path 선두에 삽입 —
    # cli/evaluate.py 등이 spawn 된 뒤에는 각자의 __file__-상대 shim 이 이어받는다.
    installed = (os.path.join(_PKG, "core"), os.path.join(_PKG, "cli"))
    repo = os.path.dirname(_PKG)
    editable = (os.path.join(repo, "core"), os.path.join(repo, "cli"))
    for p in installed + editable:
        if not os.path.isdir(p):
            continue
        if p not in sys.path:
            sys.path.insert(0, p)


def main():
    _bootstrap()
    import anima  # = 설치된 anima_py/cli/anima.py (canonical py 디스패처)
    return anima.main(sys.argv[1:]) or 0
