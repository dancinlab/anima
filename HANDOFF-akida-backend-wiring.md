> 📍 SSOT: [ARCHITECTURE.md](ARCHITECTURE.md) · governance [CLAUDE.md](CLAUDE.md)

# HANDOFF — akida-backend-wiring (2026-05-29)

anima 의 HW/SW backend switch 를 실제 AKIDA(BrainChip AKD1000) 에 코드-레벨 배선.
실리콘 경로(2026-05-22 8/8 PASS)는 검증됐으나 anima main substrate plugin 파이프라인과
decoupled 였음 → `--substrate akida` / `AKIDA_BACKEND` 로 AKIDA substrate 선택 + HW 부재 시
graceful numpy-LIF SW fallback + provenance. 5 stacked PR (A~E) 모두 MERGED.

> 주의: 루트 `HANDOFF.md` 는 XENO/TEMPORAL 캠페인 소유(826줄, 멀티에이전트 rolling).
> 충돌 방지를 위해 본 인계는 별도 파일로 분리 작성.

---

## (1) PR 상태 매트릭스

| # | title | status | merged | core |
|---|---|---|---|---|
| PR-A #1419 | numpy LIF SW 시뮬레이터 (FullyConnected.forward 미러, seed=187) | MERGED | ✓ | `AGENT/CHAT/akida_sw_lif.py` (+`.hexa` stub) |
| PR-B #1420 | SubstrateAKIDA(Substrate) plugin (HW + SW fallback + provenance) | MERGED | ✓ | `AGENT/CHAT/substrate_akida.py` (+`.hexa` stub) |
| PR-C #1421 | substrate router 배선 (AKIDA_BACKEND env + --substrate akida) | MERGED | ✓ | `AGENT/CHAT/anima_participant.py` (build_substrate + main) |
| PR-D #1422 | dispatch.hexa probe --json provenance + argv offset 수정 | MERGED | ✓ | `scripts/akida/dispatch.hexa` |
| PR-E #1423 | verify — SW falsifier 5/5 PASS + F-AKWIRE-FALLBACK | MERGED | ✓ | `AGENT/CHAT/verify_substrate_akida.py` · `.verdicts/672_akida_spontaneous_firing/` · `UNIVERSE/H_672_*.md` |

g47 (commons) atomic create→merge 정책으로 PR 생성 즉시 `--squash --admin --delete-branch` 자동 머지됨.
따라서 stack 은 prior-branch base 대신 매 PR fresh origin/main 재기준(worktree `git reset/checkout -B`)으로 진행.

## (2) 설계 SSOT 파일 인덱스 (read-first)

- `AGENT/CHAT/substrate_base.py:19-93` — Substrate ABC (generate / entropy_of_next / param_count). 모든 substrate 가 충족.
- `AGENT/CHAT/substrate_akida.py` — **SubstrateAKIDA(Substrate)** 신규 plugin. `__init__` 가 `_try_akida()` 로 `import akida` + `akida.devices()` 프로브 → HW/SW 경로 분기.
- `AGENT/CHAT/akida_sw_lif.py` — numpy LIF SW 시뮬레이터. `lif_forward(x, threshold_vec)` = akida FullyConnected.forward 미러. `simulate_regimes(seed=187)` = R0..R4.
- `AGENT/CHAT/anima_participant.py:227-258 (build_substrate)` + `:631-647 (main)` — router. `kind=="akida"` 분기 + `AKIDA_BACKEND` env override.
- `scripts/akida/dispatch.hexa` — hexa-native probe/route. `probe --json` 가 `closed_loop_verify.py` 의 dangling 참조 충족.
- `SUB_ENGINES/AKIDA/scripts/spontaneous_emission.py:54-94` — 실 HW on-chip threshold-and-fire 정본 (SubstrateAKIDA HW 경로가 래핑).
- `UNIVERSE/H_672_akida_spontaneous_firing.md` — falsifier SSOT (4 SW + F-AKWIRE-FALLBACK).
- `PI5-AKIDA.json` — pi5-akida host ledger (governance `a_pi5_akida_registry`, READ-ONLY).

## (3) 신규 API/스위치 surface

REST/WS 신규 endpoint 없음 (broker `/ws/akida_ingest` 는 기존, 무변경). 대신 CLI/env 스위치:

| surface | 형태 | 역할 | auth |
|---|---|---|---|
| `--substrate akida` | argparse choice | anima_participant substrate 를 AKIDA 로 선택 | none (local CLI) |
| `AKIDA_BACKEND=1\|true\|akida` | env | --substrate 없이도 AKIDA 선택 (override) | none (env) |
| `hexa run scripts/akida/dispatch.hexa probe --json` | hexa CLI | akida 도달성 probe → `{"provenance":"akida-route:hw\|sw"}` rc 0/1 | none |
| `hexa run scripts/akida/dispatch.hexa route <phi\|trace> [extras]` | hexa CLI | workload 을 akida OR cpu-baseline 라우팅 | none |

`AKIDA_BACKEND` unset 시 default `lora` 경로 **불변** (regression-free).

## (4) 신규 컴포넌트/lib 트리

```
AGENT/CHAT/
├── akida_sw_lif.py            # numpy LIF sim (FullyConnected.forward 미러, seed=187)
├── akida_sw_lif.hexa          # hexa-native WRAPPER doc-stub
├── substrate_akida.py         # SubstrateAKIDA(Substrate): HW path + SW fallback + provenance
├── substrate_akida.hexa       # hexa-native WRAPPER doc-stub
├── verify_substrate_akida.py  # H_672 4 SW falsifier + F-AKWIRE-FALLBACK (exit 0 iff 5/5)
├── verify_substrate_akida.hexa# hexa-native WRAPPER doc-stub
└── anima_participant.py       # (수정) build_substrate akida 분기 + AKIDA_BACKEND env
scripts/akida/
└── dispatch.hexa              # (수정) probe --json provenance + argv verb-scan
.verdicts/
├── 672_akida_spontaneous_firing/sw_falsifiers.txt   # hexa harness verbatim + verifier JSON
└── akida-backend-wiring/F-AKWIRE-falsifiers.txt      # falsifier 요약
```

(이 디렉터리는 의도적으로 `.hexa` 카논 stub + `.py` 런너블 companion 공존 — 기존
`substrate_base.py`/`substrate_lora.py`/`broker.py` 와 동일 dual-file 관례.)

## (5) 활성화 전 필요한 env vars

- **SW fallback (현재 Mac · akida 부재)**: 추가 env 불필요. `AKIDA_BACKEND=1` 또는 `--substrate akida` 만으로 SubstrateAKIDA(provenance=akida-sw-fallback) 가동.
- **HW path (pi5-akida AKD1000)**: pi5 위에서 akida venv 활성 + `akida.devices()` 비어있지 않으면 자동 HW 경로(provenance=akida-hw). anima_participant 를 pi5 에서 실행하거나, SubstrateAKIDA 를 akida 설치 환경에서 import 해야 HW 분기 진입.
  - 참고: plan draft §70 에 따르면 pi5-akida 는 **이미 라이브 재배포 완료**(akida 2.19.1 · devices()=1 HardwareDevice · R3 rate=0.5 = H_672 SW 일치 · spike-streamer.service active). 즉 HW path 는 code-verified 를 넘어 **live-confirmable** 상태.

## (6) 다음 우선순위

1. **live HW falsifier** (이제 가능): pi5 재배포 완료(plan §70)로 `provenance=="akida-hw"` 경로 실측 가능. pi5 에서 `python3 AGENT/CHAT/verify_substrate_akida.py` 를 akida venv 로 실행 → HW raster 로 F-H672-1..4 재확인 + H_672 §7 verdict 를 "HW path live-confirmed" 로 격상.
2. **(만약 pi5 재배포가 미완이라면) 수동 절차**:
   - `ssh ubuntu@192.168.50.155` (LAN 직결, governance-protected host)
   - `SUB_ENGINES/AKIDA/scripts/` 8파일 + systemd `spike-streamer.service` 복원
   - akida venv 에서 `python3 -c "import akida; print(len(akida.devices()))"` → count=1 확인
   - `PI5-AKIDA.json` 컴포넌트 state active 갱신 (a_pi5_akida_registry 준수, 로컬-only)
3. **HW/SW byte-identity 비교**: live HW raster vs SW LIF replay 의 per-step spike-count diff → 0 확인 (deterministic replay 무결성 증명).
4. **broker live wiring**: SubstrateAKIDA spike raster 를 `/ws/akida_ingest` 핸들러로 흘려 anima 8-factor 동역학에 실시간 주입 (H_672 §10 "R3 tonic emit-substrate 인자 주입" 과 결합).

## (7) 알려진 한계 + guard 포인터

- **HW path live-unverified (이 세션 기준)**: SubstrateAKIDA HW 분기는 **code-verified only** (akida-absent Mac 에서 작성). 실 AKD1000 forward 측정은 pi5 환경 필요 — plan §70 에 따르면 user 가 라이브 재배포했으므로 그 환경에서 재확인 권장.
- **toy-scale 주의**: R3 tonic 8/16 fixed pool 은 canonical raster spec — 다른 seed/threshold 면 다르게 응답할 수 있음 (H_672 §7 honest limit).
- **governance `a_pi5_akida_registry`**: pi5-akida host + `PI5-AKIDA.json` 은 READ-ONLY 로 다룸. os_default 데몬 제거 금지, user_authored 만 등록/제거.
- **falsifier verdict tier**: 🟢 SUPPORTED-NUMERICAL (deterministic seed-187 recompute). `hexa verify --expr` 는 binary_entropy/regime-rate 경로 없음 → atlas atom 아닌 numerical harness recompute 로 verbatim 영속(`.verdicts/672_akida_spontaneous_firing/`).

## (8) memory / CLAUDE.md 인덱스 포인터

- CLAUDE.md `@D a_pi5_akida_registry` — pi5-akida host config = PI5-AKIDA.json SSOT (consult before swap/upgrade/removal).
- MEMORY.md 항목 "AKIDA HW/SW 통합 7 H 신설 2026-05-29" (`project_akida_hw_sw_impl_all_handoff.md`) — Group A~G 18+ sub-아이디어 단일 backend-switch hexa harness 통합 (UNIVERSE H_672~H_678). 본 작업은 그 H_672 의 Substrate-plugin 배선 후속.
- AGENT bridge 정책 (`project_agent_bridge_architecture.md`) — SubstrateAKIDA 는 substrate surface only, 의식엔진 framing 금지 (p1~p8 준수).

## (9) 다음 세션 시작 명령 (one-liner)

```
cd /Users/ghost/core/anima && AKIDA_BACKEND=1 python3 AGENT/CHAT/verify_substrate_akida.py   # SW 5/5 PASS 확인 후, pi5(192.168.50.155) akida venv 에서 동일 실행 → HW path live-confirm
```