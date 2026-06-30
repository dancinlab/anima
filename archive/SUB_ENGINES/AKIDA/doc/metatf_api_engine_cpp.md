# MetaTF C++ Engine — embedded path

> SOURCE: https://doc.brainchipinc.com/user_guide/engine.html
> CACHED: 2026-05-21 UTC
> SCOPE: AKD1000 embedded / non-Python deployment (out-of-scope for Pi 5 default path, included for completeness)

## When you'd use this

The C++ Engine is the **non-Python** path for embedded MCU / RTOS deployment of AKD1000. Pi 5 + Python path (cached in `metatf_install_linux_arm.md`) is **strictly easier** and covers all anima Pack needs.

The C++ path is documented here in case:
1. Someone reads "no Pi 5 aarch64 wheel" wrong info → falls through to C++
2. Sub-1-second cold-boot inference required (Python wheel import ~500 ms)
3. anima moves to a bare-metal ESP32 + AKD1000 mini board (see `docs/IMPLEMENTATION.md §6.3`)

## Directory structure (deployed via `akida engine deploy --dest-path .`)

```
api/                     # public headers
  akida/                 # Akida-generic
  infra/                 # platform abstractions
  akd1000/               # AKD1000-specific
  akd1500/               # AKD1500-specific (not used)
cmake/                   # build config + flatbuffers fetch
devices/                 # engineering-sample chip drivers
inc/                     # internal headers
src/                     # core engine
test/                    # device-specific tests
```

## Primary API components

### `HardwareDriver` (`infra/hardware_device.h`)

Virtual base — you implement this for your platform. Methods:

```cpp
class HardwareDriver {
public:
    virtual void read(uint32_t address, uint8_t* data, size_t size) = 0;
    virtual void write(uint32_t address, const uint8_t* data, size_t size) = 0;
    virtual std::string desc() const = 0;
    virtual uint8_t* scratch_memory() = 0;
    virtual size_t scratch_memory_size() const = 0;
    virtual uint8_t* akida_visible_memory() = 0;
    virtual size_t akida_visible_memory_size() const = 0;
};
```

On Pi 5 over PCIe, BrainChip provides a Linux PCIe `HardwareDriver` impl in their driver package — you don't reimplement.

### `HardwareDevice` (`akida/hardware_device.h`)

```cpp
class HardwareDevice {
public:
    static std::unique_ptr<HardwareDevice> create(HardwareDriver* driver);
    HwVersion version() const;
    void program(const uint8_t* model_buf, size_t model_size);
    void set_batch_size(uint32_t batch);
    void enqueue(const Dense* input);
    Dense* fetch();
    void dequantize(Dense* output, float scale, float bias);
};
```

### `Dense` (`akida/dense.h`) — buffer

```cpp
class Dense {
public:
    static std::unique_ptr<Dense> create(const Shape& shape, DataType dtype);
    static std::unique_ptr<Dense> create_view(uint8_t* data, const Shape& shape, DataType dtype);
    std::vector<std::unique_ptr<Dense>> split() const;   // 4D → 3D vectors
    uint8_t* buffer();
    const Shape& dimensions() const;
};
```

### `Shape` (`akida/shape.h`)

```cpp
struct Shape {
    static constexpr size_t MAX_DIMS = 4;
    uint32_t dims[MAX_DIMS];
    uint32_t ndims;
};
```

### `HwVersion` (`akida/hw_version.h`)

```cpp
struct HwVersion {
    uint16_t vendor_id;     // 0x1f87 = BrainChip
    uint16_t product_id;    // 0x1000 = AKD1000
    uint8_t major_rev;
    uint8_t minor_rev;
};
```

### Sparse / Input conversion (`api/input_conversion.h`)

Dense ↔ sparse tensor utilities — needed when feeding event-camera input or compressing first-layer activations.

## Platform requirements (embedded)

Implement these in `infra/system.h`:
- `system_memcpy()`, `system_memset()`, `system_assert()`
- `system_clock_ms()` (for timeouts)
- `system_log()` (for debug)

CMake build uses Flatbuffers (auto-fetched via `cmake/`).

## Pack relation

Pack's Pi 5 path uses Python `akida.Model("foo.fbz")` which internally calls the C++ Engine (the Python wheel is a thin C-extension wrapping libakida.so). **You don't need to touch C++ for anima Pi 5 deployment.**

Future ESP32 path (`docs/IMPLEMENTATION.md §6.3`) would use this C++ Engine API directly — TBD.
