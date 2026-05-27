# BrainChip AKD1000 reference cache — INDEX

> SOURCE: https://doc.brainchipinc.com/index.html (sitemap traversal)
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 only (Akida 1.0 — Akida 2.0 / TENNs / Pico excluded except where contrasted)

## Cached pages (Phase 1 traversal)

| File | Source URL | Section |
|---|---|---|
| [`akd1000_hardware_spec.md`](akd1000_hardware_spec.md) | M.2 Card product page + Akida 1.0 hardware capabilities | HW datasheet |
| [`metatf_install_linux_arm.md`](metatf_install_linux_arm.md) | `installation.html` + PyPI + Pi 5 search | Pi 5 install |
| [`metatf_api_model.md`](metatf_api_model.md) | `api_reference/akida_apis.html` (Model class) | API ref |
| [`metatf_api_layers.md`](metatf_api_layers.md) | `api_reference/akida_apis.html` (Akida V1 layers) | API ref |
| [`metatf_api_devices.md`](metatf_api_devices.md) | `api_reference/akida_apis.html` (Device / NP) + `user_guide/akida.html` (Devices) | API ref |
| [`akd1000_quantization.md`](akd1000_quantization.md) | `user_guide/quantizeml.html` + `cnn2snn_apis.html` | Quantize/Convert |
| [`akd1000_onchip_learning.md`](akd1000_onchip_learning.md) | `user_guide/akida.html` (Edge learning) + `examples/edge/*` | Edge learning |
| [`akd1000_power_spec.md`](akd1000_power_spec.md) | M.2 Card + PowerMeter API | Power |
| [`akd1000_samples_workflow.md`](akd1000_samples_workflow.md) | `examples/general/plot_0_global_workflow.html` + edge learning examples | Workflow |
| [`metatf_api_engine_cpp.md`](metatf_api_engine_cpp.md) | `user_guide/engine.html` | C++ embedded |
| [`SOURCE_URLS.md`](SOURCE_URLS.md) | — | Source URL register |

## Sitemap (filtered, AKD1000-relevant only)

```
doc.brainchipinc.com/
├── index.html                          (root TOC)
├── installation.html                   ✓ cached → metatf_install_linux_arm.md
├── user_guide/
│   ├── akida.html                      ✓ cached → metatf_api_devices.md + akd1000_onchip_learning.md
│   ├── quantizeml.html                 ✓ cached → akd1000_quantization.md
│   ├── cnn2snn.html                    ✓ cached → akd1000_quantization.md
│   ├── engine.html                     ✓ cached → metatf_api_engine_cpp.md
│   └── hardware/
│       └── 1.0.html                    ✓ cached → akd1000_hardware_spec.md
│       └── 2.0.html                    ✗ skipped (Akida 2.0, not AKD1000)
├── api_reference/
│   ├── akida_apis.html                 ✓ cached → metatf_api_model.md + metatf_api_layers.md + metatf_api_devices.md
│   ├── cnn2snn_apis.html               ✓ cached → akd1000_quantization.md
│   ├── quantizeml_apis.html            ◐ partial (referenced from quantization page)
│   └── akida_models_apis.html          ✗ skipped (model zoo only — not AKD1000 chip spec)
├── examples/
│   ├── general/
│   │   ├── plot_0_global_workflow.html ✓ cached → akd1000_samples_workflow.md
│   │   ├── plot_1..6_*.html            ✗ skipped (TF/Keras tutorials, not AKD1000-specific)
│   │   └── plot_7_global_pytorch_workflow.html ✗ skipped
│   ├── quantization/                   ✗ skipped (general QuantizeML, see quantization cache)
│   ├── spatiotemporal/                 ✗ skipped (TENNs Akida 2.0)
│   └── edge/
│       ├── plot_0_edge_learning_vision.html   ◐ partial → akd1000_onchip_learning.md
│       ├── plot_1_edge_learning_kws.html      ✓ cached → akd1000_onchip_learning.md
│       └── plot_2_edge_learning_parameters.html ✓ cached → akd1000_onchip_learning.md
├── model_zoo_performance.html          ◐ partial (Akida 1.0 model NP requirements only)
├── changelog.html                      ✗ skipped (not API)
└── license.html                        ✗ skipped
```

## External (off doc.brainchipinc.com) sources

| URL | Section | Cached in |
|---|---|---|
| `pypi.org/project/akida/` | aarch64 wheels | `metatf_install_linux_arm.md` |
| `shop.brainchipinc.com/products/m-2-card-m-key` | M.2 form factor + power | `akd1000_hardware_spec.md` + `akd1000_power_spec.md` |
| `brainchip.com/upgrade-the-raspberry-pi-for-ai-with-a-neuromorphic-processor/` | Pi 5 integration narrative | `metatf_install_linux_arm.md` |
| `docs.edgeimpulse.com/hardware/boards/brainchip-akd1000` | aarch64 install confirm | `metatf_install_linux_arm.md` |

## Filter rationale (Phase 1 selection)

Pages skipped intentionally:

- **Akida 2.0 (NSoC_v2) pages** — AKD1000 is `HwVersion.NSoC_v1`, not v2. The M.4 ARM + 20-NPU mesh is v1-only. AKD1500/AKD2000 are separate silicon (out-of-scope per GOAL).
- **TENNs / spatiotemporal / Pico / TF-Keras model zoo training tutorials** — Pi 5 plug-and-play does not retrain on-host; only loads pre-converted `.fbz` from host and runs `forward()` / `fit()` (edge learning).
- **PyTorch workflow** — anima Pack doesn't use PyTorch path; pack targets `akida.Model` directly via mock/HW.

## Coverage gate

Per Phase 2 promise: **10 markdown files cached** (target was 9–11 from prompt). Site has ~80 sub-pages total; AKD1000 filter passes ~12 (15%). All AKD1000-essential API + install + on-chip learning paths covered.
