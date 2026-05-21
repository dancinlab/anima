# BrainChip AKD1000 documentation survey — 2026-05-21

> Pi 5 + AKD1000 Dev Kit ($1495) arrival prep — full survey of
> `doc.brainchipinc.com` AKD1000-relevant pages + local cache + pack API
> correction.  Mac local, $0 cost.

## §1 GOAL

User has Raspberry Pi 5 + AKD1000 M.2 Dev Kit ordered. To enable
plug-and-play on arrival:

1. The pack's MetaTF API contract (`pack/runtime/metatf_runtime.py`,
   `pack/mocks/metatf_mock.py`, `pack/adapters/*`) must match the **real
   BrainChip API surface**.
2. All AKD1000-relevant documentation must be **locally cached** (offline
   reference + drift-resistance).
3. Real AKD1000 capability + constraints must be **reflected** in adapter
   design and falsifier thresholds.

## §2 page traversal — classification table

WebFetch traversal of `doc.brainchipinc.com` (root sitemap pulled 2026-05-21).
~80 total pages on the site; AKD1000 filter passes 12 (15%). External:
PyPI + product page + Edge Impulse + Pi 5 integration blog.

| Section | Total pages | Cached | Skipped (Akida 2.0 / TENNs / Pico / TF tutorials) | 404 |
|---|---|---|---|---|
| `/` (root) | 1 | 1 | 0 | 0 |
| `/installation.html` | 1 | 1 | 0 | 0 |
| `/user_guide/` | 8 | 6 | 2 (akida_models, hardware/2.0) | 0 |
| `/api_reference/` | 5 | 3 (akida_apis, cnn2snn_apis, partial quantizeml) | 2 (akida_models, tenns) | 0 |
| `/examples/` | 25+ | 4 (global workflow + 3 edge learning) | 21+ (Akida 2.0 / TENNs / PyTorch / training tutorials) | 0 |
| `/model_zoo_performance.html` | 1 | INDEX entry only | 0 | 0 |
| `/changelog.html` | 1 | 0 | 1 | 0 |
| External (PyPI, shop, edgeimpulse) | 4 | 4 | 0 | 1 (developer.brainchip.com/akd1000/ → fallback to shop) |
| **Totals** | **~45 traversed** | **20 traversed-and-extracted, 10 markdown distilled** | **26+** | **1** |

### Cached file inventory

```
doc/
├── INDEX.md                                  (sitemap + filter rationale)
├── SOURCE_URLS.md                            (per-page URL + fetched UTC + honest C3 on cache completeness)
├── akd1000_hardware_spec.md                  (20 NPU mesh / 8 MB / 1 W / layer constraints)
├── metatf_install_linux_arm.md               (Pi 5 aarch64 wheel install + driver TODO)
├── metatf_api_model.md                       (akida.Model class — constructor + all methods)
├── metatf_api_layers.md                      (V1 layers verbatim signatures)
├── metatf_api_devices.md                     (Device / HwDevice / NP.Mesh / ClockMode)
├── akd1000_quantization.md                   (QuantizeML + CNN2SNN — host pipeline)
├── akd1000_onchip_learning.md                (AkidaUnsupervised edge learning, AKD1000-only)
├── akd1000_power_spec.md                     (PowerMeter + power calibration)
├── akd1000_samples_workflow.md               (end-to-end Keras → AKD1000 + edge-learn example)
└── metatf_api_engine_cpp.md                  (C++ embedded path — out-of-scope for Pi 5 default)
```

**11 markdown files**, 92 KB total. All AKD1000-essential API + install +
edge-learning + datasheet covered.

## §3 pack improvement — per-file diff summary

| File | Lines before → after | Δ | Change summary |
|---|---|---|---|
| `pack/mocks/metatf_mock.py` | 167 → 720 | **+553** | Full rewrite — added 7 enums (HwVersion, ClockMode, MapMode, Padding, PoolType, ActivationType, LayerType), V1 layer factories (InputData, InputConvolutional, Convolutional, SeparableConvolutional, FullyConnected) with real signatures + input validation, AkidaUnsupervised optimizer, MockHwDevice (NSoC_v1) + SocDriver + PowerMeter + NP.Mesh (20 NPUs), MockModel.{compile, predict, map, add_classes, save, summary, statistics, sequences}, virtual AKD1000() factory, backwards compat for V2-style `akida.layers.*` namespace + legacy `fit(input, target)` signature |
| `pack/mocks/__init__.py` | 35 → 45 | +10 | Export MockHwDevice + MockAkidaUnsupervised; MockDevice kept as back-compat alias |
| `pack/runtime/metatf_runtime.py` | 156 → 217 | +61 | Added `assert_akd1000()` — backend-agnostic NSoC_v1 verification; doc updates pointing to brainchip_reference cache |
| `tests/test_adapters_mock.py` | 126 → 134 | +8 | New mock self-consistency asserts (forward_returns_int32, device_version_v1, virtual_AKD1000_ok, v2_namespace_backcompat, legacy_fit_backcompat) |
| `boot/day1_install.sh` | 75 → 130 | +55 | Pi 5 venv path (no --break-system-packages on Bookworm), apt dkms + linux-headers, PCIe driver reminder, lspci probe, full pack runtime assert_akd1000() probe |
| `docs/ARCHITECTURE.md` | (in-place) | ~6 | L1 silicon row corrected: "1024 NPU · 0.5 mW typ" → "20 NPU mesh · 8 MB · 1 W typ", mock class names updated |
| `docs/IMPLEMENTATION.md` | (in-place) | +10 | Header note added: BrainChip survey 2026-05-21 verified API; pre-survey marketing claims rejected |
| `docs/BOOT_PLAN.md` | (in-place) | +9 | AKD1000 spec line corrected with real datasheet numbers + driver requirement note |
| **+ 11 new cache files** | (new) | +~2700 | `doc/*.md` (full text above) |

## §4 5 mock-vs-HW divergences discovered + fixed

1. **NPU count: 1024 → 20.** Pack docs / ARCHITECTURE.md claimed "1024 NPU" — that was AKD1000 FPGA marketing scale. Real AKD1000 silicon has **20 NPUs in mesh** at 300 MHz with 8 MB on-chip SRAM. Corrected in ARCHITECTURE.md, BOOT_PLAN.md, akd1000_hardware_spec.md.

2. **Power: 0.5 mW typical → 1 W typical module.** The "mW per inference" is per-event amortised energy (sub-mW under sparse spike input). The chip itself burns **~1 W on the M.2 module**. Falsifier F-AKIDA-*-4-POWER threshold and adapter `to_record()`'s `scope_caveats` should reflect this. Corrected in akd1000_power_spec.md.

3. **Layer naming: `Conv2D` → `Convolutional`.** Pack's mock exposed `akida.layers.Conv2D` (Akida 2.0 V2 naming). AKD1000 (Akida 1.0 V1) uses bare `akida.Convolutional` — `Conv2D` doesn't exist in V1. Mock now exposes both: `Convolutional` (canonical V1) + `Conv2D` (V2 alias for forward-compat).

4. **Model constructor: `Model()` only → `Model(filename=None, layers=None)`.** Real API supports loading `.fbz` from disk and building from a layer list — both common production paths. Mock previously only supported empty construction. Now matches.

5. **Edge learning: bare `.fit(x, target)` → `.compile(AkidaUnsupervised(...))` + `.fit(uint8, int32_labels)`.** Real on-chip learning requires (a) binding an `AkidaUnsupervised` optimizer first, (b) int32 class labels (not one-hot, not float targets), (c) `weights_bits=1` + `act_bits=1` on the trainable FC head. Mock now enforces this contract while keeping the old `(input, target)` Hebbian signature as a back-compat branch for adapter regression tests.

**Bonus discovered** (not in the original 5):
- `akida.HwVersion.NSoC_v1` enum (AKD1000 marker) — mock now exposes it; `assert_akd1000()` runtime helper validates.
- `akida.AKD1000()` virtual device factory (offline testing) — mock now exposes.
- `akida.MapMode` enum (`AllNps`/`HwPr`/`Minimal`) — mock now exposes; pack docs note `Minimal` is optimal for anima 8-neuron pools.
- Akida PCIe **driver install is DKMS-class** (Pi 5 needs `linux-headers-$(uname -r)` + manual download from `developer.brainchip.com` — not on PyPI). day1_install.sh now logs this gate explicitly.
- AKD1000 is **NSoC_v1**, ONLY the v1 line supports on-chip edge learning. Akida 2.0 (NSoC_v2) dropped it. Pack `model.map()` mock now refuses non-v1 devices loudly.

## §5 honest C3 (5 items)

1. **No real silicon yet** — every "API contract match" is verified against the doc's documented signature, NOT against running on actual AKD1000. First real call to `akida.devices()` on Pi 5 may surface field-name skew (e.g., `PowerEvent.power_mw` vs `PowerEvent.power_mW`). day1_install.sh logs `print(dev.__dict__)` for this exact reason.

2. **Akida PCIe driver source not publicly cached** — the DKMS kernel module is gated behind `developer.brainchip.com` sign-in. Day 1 on real Pi 5 will need a manual sign-up + tarball download. day1_install.sh logs this reminder; no automation possible until BrainChip publishes the driver tarball URL openly.

3. **Adapter `.fbz` conversion is Phase 5 work, not done here** — the 10 anima adapters are currently numpy-only `step()` implementations. Real AKD1000 deployment requires writing per-adapter Keras source models + quantize + convert + verify byte-parity vs sw. This is a separate ~1-week effort (host TF stack required) and is correctly out-of-scope for this survey. The mock contract update unblocks it.

4. **Mock parity != HW parity** — mock's Hebbian outer-product is a software approximation of AkidaUnsupervised's opaque competitive-WTA algorithm. F-AKIDA-*-5-PARITY assertions on the mock prove deterministic mock behaviour, NOT byte-parity with AKD1000. Real-HW calibration requires Pi 5 + AKD1000 in hand and is a separate falsifier cycle (Days 2-7 of BOOT_PLAN.md).

5. **Doc cache is snapshot — not auto-refreshed** — `doc/` was captured at 2026-05-21 UTC against `akida 2.19.1`. BrainChip publishes minor releases monthly (changelog page). Re-running this survey quarterly or before each anima Pack version bump is recommended. SOURCE_URLS.md provides the URL + timestamp register for diffing.

## §6 verification matrix

| Gate | Before survey | After survey |
|---|---|---|
| Falsifier baseline 50/50 PASS | ✓ | ✓ (regression-free post mock rewrite) |
| Pytest 12/12 PASS | ✓ | ✓ (mock self-consistency tests strengthened) |
| Mock self-test items | 4 | 10 (forward_returns_int32, device_version_v1, virtual_AKD1000_ok, validates_bad_units, v2_namespace_backcompat, legacy_fit_backcompat + originals) |
| `assert_akd1000()` runtime helper | absent | present (works on both backends) |
| API surface mocked | `Model()` / `add` / `forward` / `fit` / `devices()` / `program()` | + `compile(AkidaUnsupervised)` + `map(device, mode)` + `add_classes(n)` + `predict()` + `save/load` + `summary()` + `statistics` + 7 enums + virtual `AKD1000()` |
| Doc reference (offline) | 0 cached pages | 11 cached markdown files (~2700 LoC) |
| Pi 5 install path verified | hand-wave "pip install akida" | explicit aarch64 wheel confirmation + venv + DKMS driver path + lspci probe |

## §7 next-cycle TODO

- [ ] On real Pi 5 + AKD1000 arrival (Day 1): run `boot/day1_install.sh`, capture `dev.__dict__` + `pm.events[0].__dict__` for schema verification → update mock if field-name skew.
- [ ] Phase 5: write 10 adapter Keras sources + quantize + convert to `.fbz` (host TF stack) → byte-parity check against numpy `step()` for each F-AKIDA-*-5-PARITY.
- [ ] Add `boot/day1.5_driver_install.sh` capturing the DKMS install when BrainChip's driver tarball URL becomes scrapeable.
- [ ] Quarterly: re-run this survey against `doc.brainchipinc.com` to catch API drift (especially `AkidaUnsupervised` plasticity defaults + `MapMode` additions).
