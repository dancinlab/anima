# ANU QRNG provenance (committed snapshots)

양자 harness들은 **커밋된 실 ANU paid 스냅샷**을 읽는다(silent pseudo 폴백 제거 — 없으면 에러로 중단).
재현·증명 가능: 같은 양자 draw를 누구나 동일하게 사용.

| snapshot | bytes | tier | sha256 (전체 512B draw) |
|---|---|---|---|
| TENSION-LINK/anu_seed_512.bin | 512 | anu_paid | `3eeba42ba49940f5fc2e92f9b1d8cc9fe40e6152adfac086d89d155b057716f2` |
| TENSION-LINK/anu_seed_shared.bin | 256 = [:256] | (위 draw 분할) | shared 슬라이스 |
| TENSION-LINK/anu_seed_indep.bin | 256 = [256:] | (위 draw 분할) | independent 슬라이스 |
| FORECAST/anu_seed.bin | 256 = [:256] | (위 draw 분할) | forecast seed |

원천: `mirror/qmirror/seed/anu_pull.py` (ANU vacuum-fluctuation, api.quantumnumbers.anu.edu.au, x-api-key paid tier).
정정 사유: 기존 harness가 /tmp 경로 + `or os.urandom()` silent 폴백이라, .bin 부재 시 pseudo가 양자인 척할 위험 → 커밋 스냅샷 + loud-fail로 강제.
