https://github.com/Samsung/TICO/issues/417
# DynamicCache pytree-flattenable registration depends on transformers version

### What?

Some transformers versions requires DynamicCache to be registered to pytree-flattenable whereas others don't.
I made an inspection on that.

transformers version | description |
---|---|
v < 4.50.0 | requires respective call of `register_dynamic_cache()`.
4.50.0<= v < 4.54.0 | already have DynamicCache registered in pytree
4.54.0 <= v <= 4.57.1(latest) | already have DynamicCache registered in pytree AND have different version of DynamicCache (layer-based)

#### Inspection

I share the result of `torch.utils._pytree._get_node_type(DynamicCache)` using below script.

```py
4.51.0: ✅ Pre-registered (list-based)
4.51.1: ✅ Pre-registered (list-based)
4.52.0: ✅ Pre-registered (list-based)
4.52.1: ✅ Pre-registered (list-based)
4.53.0: ✅ Pre-registered (list-based)
4.54.0: ✅ Pre-registered (layers-based)
4.54.1: ✅ Pre-registered (layers-based)
4.55.0: ✅ Pre-registered (layers-based)
4.55.1: ✅ Pre-registered (layers-based)
4.56.0: ❌ Not registered (layers-based)
4.56.1: ❌ Not registered (layers-based)
4.57.0: ❌ Not registered (layers-based)
4.57.1: ❌ Not registered (layers-based)
4.57.2: ❌ Not registered (layers-based)
4.57.3: ❌ Not registered (layers-based)
4.57.4: ❌ Not registered (layers-based)
4.57.5: ❌ Not registered (layers-based)
4.57.6: ❌ Not registered (layers-based)
5.0.0: ❌ Not registered (layers-based)
```

<details>

<summary> Script </summary>

```py
#!/usr/bin/env python3
"""
Test script to check if DynamicCache is pre-registered as a pytree node
in different transformers versions.
"""

import subprocess
import sys

def check_version(version):
    """Check if DynamicCache is registered in a given transformers version."""
    print(f"\n{'='*60}")
    print(f"Testing transformers {version}")
    print('='*60)
    
    # Install the version
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", f"transformers=={version}"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Failed to install transformers {version}")
        print(result.stderr)
        return None
    
    # Check registration
    test_code = """
import torch
from transformers.cache_utils import DynamicCache
try:
    is_registered = DynamicCache in torch.utils._pytree.SUPPORTED_NODES
    print(f"Registered: {is_registered}")
    
    # Check for DynamicLayer classes
    import transformers.cache_utils as cache_utils
    has_dynamic_layer = hasattr(cache_utils, 'DynamicLayer')
    has_sliding_layer = hasattr(cache_utils, 'DynamicSlidingWindowLayer')
    cache = DynamicCache()
    has_layers_attr = hasattr(cache, 'layers')
    
    print(f"DynamicLayer: {has_dynamic_layer}")
    print(f"DynamicSlidingWindowLayer: {has_sliding_layer}")
    print(f"Has layers attr: {has_layers_attr}")
except Exception as e:
    print(f"Error: {e}")
"""
    
    result = subprocess.run(
        [sys.executable, "-c", test_code],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr and "UserWarning" not in result.stderr:
        print("Errors:", result.stderr)
    
    return result.stdout

# Test versions
versions = [
    # "4.51.0",
    # "4.51.1", 
    # "4.52.0",
    # "4.52.1",
    # "4.53.0",
    # "4.54.0",
    # "4.54.1",
    # "4.55.0",
    # "4.55.1",
    # "4.56.0",
    # "4.56.1",
    # "4.57.0",
    # "4.57.1",
    "4.57.2",
    "4.57.3",
    "4.57.4",
    "4.57.5",
    "4.57.6",
    "5.0.0",
]

results = {}
for version in versions:
    output = check_version(version)
    if output:
        results[version] = output

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
for version, output in results.items():
    registered = "Registered: True" in output
    has_layers = "Has layers attr: True" in output
    status = "✅ Pre-registered" if registered else "❌ Not registered"
    structure = "layers-based" if has_layers else "list-based"
    print(f"{version}: {status} ({structure})")


```

</details>


### DynamicCache is 'not welcomed' anyways

DynamicCache is actually unfriendly structure for `torch.export`, because unknown shape is not supported with `torch.export` by default, only some with restrictions are supported - so that DynamicCache nature no longer exists.
In a same sense, executorch team has recently altered most of them to `StaticCache`.

