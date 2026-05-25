# Source URL register

> SOURCE: WebFetch traversal of doc.brainchipinc.com
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 only (Akida 1.0 / NSoC_v1)

## Fetched pages with timestamp

| Cached file | Source URL | Fetched UTC | Status |
|---|---|---|---|
| `INDEX.md` | https://doc.brainchipinc.com/index.html | 2026-05-21 | OK (sitemap) |
| `akd1000_hardware_spec.md` | https://doc.brainchipinc.com/user_guide/hardware/1.0.html | 2026-05-21 | OK |
| `akd1000_hardware_spec.md` | https://shop.brainchipinc.com/products/m-2-card-m-key | 2026-05-21 | OK |
| `metatf_install_linux_arm.md` | https://doc.brainchipinc.com/installation.html | 2026-05-21 | OK |
| `metatf_install_linux_arm.md` | https://pypi.org/project/akida/ | 2026-05-21 | OK |
| `metatf_install_linux_arm.md` | https://docs.edgeimpulse.com/hardware/boards/brainchip-akd1000 | 2026-05-21 | partial (no driver detail) |
| `metatf_api_model.md` | https://doc.brainchipinc.com/api_reference/akida_apis.html | 2026-05-21 | OK |
| `metatf_api_layers.md` | https://doc.brainchipinc.com/api_reference/akida_apis.html#akida-v1-layers | 2026-05-21 | OK |
| `metatf_api_devices.md` | https://doc.brainchipinc.com/user_guide/akida.html#devices | 2026-05-21 | OK |
| `metatf_api_devices.md` | https://doc.brainchipinc.com/api_reference/akida_apis.html#np | 2026-05-21 | partial (NP class signatures stub) |
| `akd1000_quantization.md` | https://doc.brainchipinc.com/user_guide/quantizeml.html | 2026-05-21 | OK |
| `akd1000_quantization.md` | https://doc.brainchipinc.com/user_guide/cnn2snn.html | 2026-05-21 | OK |
| `akd1000_quantization.md` | https://doc.brainchipinc.com/api_reference/cnn2snn_apis.html | 2026-05-21 | OK |
| `akd1000_onchip_learning.md` | https://doc.brainchipinc.com/user_guide/akida.html#using-akida-edge-learning | 2026-05-21 | OK |
| `akd1000_onchip_learning.md` | https://doc.brainchipinc.com/examples/edge/plot_1_edge_learning_kws.html | 2026-05-21 | OK |
| `akd1000_onchip_learning.md` | https://doc.brainchipinc.com/examples/edge/plot_2_edge_learning_parameters.html | 2026-05-21 | OK |
| `akd1000_power_spec.md` | https://doc.brainchipinc.com/api_reference/akida_apis.html#powermeter | 2026-05-21 | OK |
| `akd1000_samples_workflow.md` | https://doc.brainchipinc.com/examples/general/plot_0_global_workflow.html | 2026-05-21 | partial (quantize/convert steps truncated) |
| `metatf_api_engine_cpp.md` | https://doc.brainchipinc.com/user_guide/engine.html | 2026-05-21 | OK |

## Pages attempted but 404 / unavailable

| URL | Reason | Workaround |
|---|---|---|
| https://developer.brainchip.com/akd1000/ | HTTP 404 | datasheet specs sourced from M.2 product page + hardware/1.0.html |

## Honest C3 (re: cache completeness)

1. `model_zoo_performance.html` cached as INDEX entry only — full Akida 1.0 model NP-requirement table omitted (not needed for anima adapters, which are toy/substrate-class not ImageNet-class).
2. NP.Mesh / NP.Info / NP.MemoryInfo class signatures partial — the API ref page shows class names but field detail requires running `help(akida.NP)` on a real install. Stub captured.
3. Akida PCIe driver kernel-module install (modprobe, dkms) — no fetch-able URL with verbatim commands found; medium.com tutorial paywall + BrainChip GitHub private. **gap noted** in `metatf_install_linux_arm.md` § "driver install (TODO on real Pi 5)".
4. PowerEvent / PowerMeter exact event schema — page indexes the class but doesn't dump event field names. Stub captured.
5. The `akida.fit()` exact return type (`None` vs progress dict) — examples show it consumes input + labels but no return-doc.

## Cache verification

```
$ find doc -type f -name '*.md' | wc -l
11   # INDEX + SOURCE_URLS + 9 content pages
```
