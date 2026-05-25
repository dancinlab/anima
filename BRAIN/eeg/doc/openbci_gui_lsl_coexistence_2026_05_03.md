# OpenBCI GUI ↔ anima-eeg LSL Coexistence Guide

**Date:** 2026-05-03
**Schema:** `anima-eeg/lsl_coexistence/1`
**Status:** lsl_capture.hexa + board_health_check_lsl.hexa landed

---

## 1. The Problem

OpenBCI Cyton+Daisy connects via a single FTDI USB-serial dongle
(`/dev/cu.usbserial-DP04WGIQ` on this machine). That serial node is a
**single-owner resource** — only one process can hold it open at a time.

When the OpenBCI GUI is running with the board connected, it owns the port.
Any anima-eeg module that calls BrainFlow directly
(`collect.hexa`, `realtime.hexa`, `eeg_brainflow_sanity.hexa`, etc.) will
fail with `BOARD_NOT_READY_ERROR:7` or `PORT_ALREADY_OPEN_ERROR:1` because
the GUI is already holding the FTDI handle.

Forcing the user to toggle which app owns the port is brittle.

## 2. The Architecture

The OpenBCI GUI ships a `Networking` widget that re-publishes its
already-acquired EEG stream over **LSL** (Lab Streaming Layer). LSL is a
push/pull pub-sub protocol over UDP multicast on localhost; multiple
consumers can subscribe to one outlet without contending for the original
USB-serial port.

```
+--------------+      USB-serial      +-----------+    LSL outlet     +--------------------+
| Cyton+Daisy  | ───────────────────> | OpenBCI   | ───────────────>  | anima-eeg/         |
| dongle       |  /dev/cu.usbserial-* |   GUI     |  obci_eeg1        | lsl_capture.hexa   |
+--------------+                      +-----------+   16ch x 125Hz    +--------------------+
                                            │                                  │
                                            ▼                                  ▼
                                       GUI visualization                .npy + .meta.json
                                       (FFT, headplot, etc.)            for analyze.hexa
```

GUI keeps the port. anima-eeg subscribes to the LSL outlet. Both run
concurrently with no contention.

## 3. Module Map

| Module                                  | Role                                          | Transport         |
|-----------------------------------------|-----------------------------------------------|-------------------|
| `anima-eeg/realtime.hexa`               | BrainFlow → JSONL stream (publisher-side)     | BrainFlow direct  |
| `anima-eeg/collect.hexa`                | BrainFlow → .npy capture                      | BrainFlow direct  |
| `anima-eeg/board_health_check.hexa`     | BrainFlow hardware sanity (16ch / 125Hz / pin)| BrainFlow direct  |
| `anima-eeg/lsl_capture.hexa`            | **LSL inlet → .npy capture** (this cycle)     | LSL (subscriber)  |
| `anima-eeg/board_health_check_lsl.hexa` | **LSL outlet probe** (this cycle)             | LSL (subscriber)  |

The two new modules are **subscribers** — they never touch BrainFlow or the
USB port. They are safe to run while the GUI is open.

## 4. User Flow (step-by-step)

### 4.1 Launch the GUI and connect

1. Open the OpenBCI GUI.
2. Choose **LIVE (from Cyton)** → **Serial (from Dongle)** → auto-detect or
   pick `/dev/cu.usbserial-DP04WGIQ`.
3. Channel count = **16** (Cyton + Daisy).
4. Press **START SYSTEM**. The GUI now owns the port.

### 4.2 Enable the LSL outlet

1. In the widget grid, switch one of the panels to **Networking**.
2. Protocol dropdown → **LSL**.
3. In the first column:
   - **Data Type** → `TimeSeriesRaw` (or `TimeSeriesFilt` if you want the
     GUI's filter bank applied upstream).
   - **LSL_name1** → `obci_eeg1` (default).
   - **LSL_type1** → `EEG` (default).
4. Press **Start LSL Stream** (the button below the textfields).
5. Press **START DATA STREAM** at the top of the GUI window.

The GUI is now publishing 16 channels × 125 Hz at LSL stream
`name=obci_eeg1, type=EEG`.

### 4.3 Verify the outlet (anima side)

In a **separate terminal**:

```bash
hexa run anima-eeg/board_health_check_lsl.hexa --check --source obci_eeg1
```

Expected output ends with:

```
verdict: LSL_HEALTHY ✓
__EEG_LSL_HEALTH__ PASS chunks=<N> samples=<M>
```

If you get `LSL_STREAM_NOT_FOUND`, re-check steps 4.2.4 and 4.2.5.
If you get `LSL_NO_SAMPLES`, the outlet exists but the GUI is not streaming
— press **START DATA STREAM** at the top.
If you get `LSL_SHAPE_MISMATCH`, the GUI Data Type is not `TimeSeriesRaw`
or `TimeSeriesFilt` (16ch); check it.

### 4.4 Capture data

```bash
hexa run anima-eeg/lsl_capture.hexa --capture \
    --source obci_eeg1 \
    --seconds 60 \
    --output recordings/sessions/lsl_capture_$(date -u +%Y%m%dT%H%M%SZ).npy
```

Output:
- `.npy` shape `(16, samples)` float32, ready for `analyze.hexa`.
- `.npy.meta.json` sidecar with stream name, observed sample rate,
  retention ratio, and `raw10_honest` caveat string.

### 4.5 Concurrent visualization

While `lsl_capture.hexa` is running, the GUI continues to display FFT,
headplot, time-series, etc. You can pause/resume capture without restarting
the GUI.


`lsl_capture.hexa`:

| ID         | Predicate                                              | On fail            | Exit |
|------------|--------------------------------------------------------|--------------------|------|
| F_LSL_01   | stream resolves within `--resolve-timeout`             | EEG_LSL_NOT_FOUND  | 4    |
| F_LSL_02   | `channel_count == 16` AND `nominal_srate ≈ 125 Hz`     | EEG_LSL_SHAPE_MISMATCH | 5 |
| F_LSL_03   | `pulled_samples / target_samples >= 0.80`              | EEG_LSL_DROPOUT    | 6    |

`board_health_check_lsl.hexa`:

| ID            | Predicate                                       | On fail                | Exit |
|---------------|-------------------------------------------------|------------------------|------|
| F_LSL_HC_01   | `import pylsl` succeeds                         | LSL_PYLSL_MISSING      | 4    |
| F_LSL_HC_02   | stream resolves within `--resolve-timeout`      | LSL_STREAM_NOT_FOUND   | 5    |
| F_LSL_HC_03   | shape match (16ch + 125Hz ±1)                   | LSL_SHAPE_MISMATCH     | 6    |
| F_LSL_HC_04   | ≥1 chunk pulled within `--probe-seconds`        | LSL_NO_SAMPLES         | 7    |


1. **LSL latency vs BrainFlow direct.** LSL adds ~5-50 ms transport latency
   over localhost UDP multicast. Acceptable for offline analyze.hexa, NOT
   phenomenal-tier for closed-loop control. For tight feedback loops
   (`closed_loop.hexa`) the GUI must be off and BrainFlow direct used.

2. **Manual GUI Networking setup.** The Processing-based OpenBCI GUI is an
   external app outside our control. The Networking widget MUST be enabled
   by the user (steps 4.2.1–4.2.5). There is no auto-toggle. If the user
   forgets step 4.2.5 (START DATA STREAM), the outlet exists but emits no
   samples — `LSL_NO_SAMPLES` verdict surfaces this.

3. **Sample dropout under load.** pylsl/lab_streaming_layer uses UDP
   multicast on localhost. Under CPU saturation, swap pressure, or GUI
   buffer underflow, chunks can be lost. F_LSL_03 enforces ≥80% retention
   and writes the partial .npy with `partial=True` so the user can inspect
   what was captured before failing the verdict.

## 7. Selftest

Both modules ship a `--selftest` mode that creates a synthetic LSL outlet
and consumes it as an inlet in the same process. This validates the pylsl
install and the push_chunk/pull_chunk paths without needing the GUI:

```bash
hexa run anima-eeg/board_health_check_lsl.hexa --selftest
hexa run anima-eeg/lsl_capture.hexa --selftest --seconds 2
```

Expected sentinels:

```
__EEG_LSL_HEALTH__   PASS pushed=<N> pulled=<M>
__EEG_LSL_CAPTURE__  PASS chunks=<N>
```

## 8. Next Cycle Recommendations

1. **GUI Networking auto-config docs.** Capture screenshots of the
   Networking widget configuration and pin them into `references/` so
   future operators do not need to re-discover the textfield layout.

2. **lsl_capture BrainFlow inlet compat.** Add a `--source brainflow`
   compatibility mode to `lsl_capture.hexa` that internally spawns a
   BrainFlow → LSL outlet (mirror of OpenBCI GUI behavior) for synthetic /
   GUI-less workflows. Useful for headless CI / Hetzner playback testing.

3. **Latency measurement helper.** Optional `--measure-latency` flag that
   round-trips a synthetic timestamp through a co-running outlet to give
   the operator an honest LSL transport latency number for the current
   machine + GUI version, instead of the generic ~5-50 ms estimate.

---

## Appendix A. OpenBCI GUI LSL Outlet Pattern (from
`references/OpenBCI_GUI/OpenBCI_GUI/`)

`W_Networking.pde` (lines 81-82, 993-1015):

```java
private String[] lslTextDefaultVals = { "obci_eeg1", "EEG", ... };
// Stream creation triggered by user pressing "Start LSL Stream":
name = cp5_networking.get(Textfield.class, "LSL_name1").getText();
type = cp5_networking.get(Textfield.class, "LSL_type1").getText();
numLslDataPoints = getDataTypeNumChanLSL(dt1);  // 16 for TimeSeriesRaw
stream1 = new NetworkStreamOut(dt1, name, type, numLslDataPoints, streamNumber);
```

`NetworkStreamOut.pde` (lines 1229-1233):

```java
String stream_id = "openbcigui";
info_data = new LSL.StreamInfo(this.streamName, this.streamType,
                               this.numLslDataPoints,
                               currentBoard.getSampleRate(),  // 125 for Cyton+Daisy
                               LSL.ChannelFormat.float32, stream_id);
outlet_data = new LSL.StreamOutlet(info_data);
```

Sample push (line 369-380):

```java
} else if (this.protocol.equals("LSL")) {
    // (channel-major buffer flattened to sample-major float[])
    outlet_data.push_chunk(dataToSend);
}
```

So the GUI's outlet contract is exactly:
- name: user textfield (default `obci_eeg1`)
- type: user textfield (default `EEG`)
- channel count: from `getDataTypeNumChanLSL(dt)` — `16` for
  `TimeSeriesRaw` / `TimeSeriesFilt` on Cyton+Daisy
- sample rate: `currentBoard.getSampleRate()` = `125` for Cyton+Daisy
- format: `float32`
- stream_id (source_id): `"openbcigui"` (constant)

This is what `lsl_capture.hexa` and `board_health_check_lsl.hexa` resolve
against.
