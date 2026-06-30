https://github.com/Samsung/TICO/issues/117
# Define Minimum Supported PyTorch Version Based on Feature Requirements

## What

We are establishing a policy for managing the minimum supported PyTorch version in TICO.

## Decision

The minimum required PyTorch version will be determined **based solely on feature requirements** (e.g., usage of torch.export, torch.compile, etc.).
We will not raise errors or enforce version upgrades solely due to security vulnerabilities in older PyTorch versions. Instead, if a user is running a version known to have critical security issues, we will emit a warning recommending an upgrade.

## Security-related Warning

A runtime warning will be displayed if the user’s PyTorch version is below a known secure baseline. For example:

```python
import warnings
from packaging.version import Version

import torch

RECOMMENDED_TORCH_VERSION = "2.6.0"

if Version(torch.__version__) < Version(RECOMMENDED_TORCH_VERSION):
    warnings.warn(
        f"Detected PyTorch version {torch.__version__}, which may include known security vulnerabilities. "
        f"We recommend upgrading to {RECOMMENDED_TORCH_VERSION} or later for better security.\n"
        "Upgrade command: pip install --upgrade torch\n"
        "For more details, see: https://pytorch.org/security"
    )
```

This allows users to make an informed decision while preserving backward compatibility where possible.

## Rationale

- Clearly separates supported versions (based on functionality) from recommended versions (based on security).
- Minimizes disruption for users unable to upgrade immediately while still promoting best practices.
- Provides a clean boundary of responsibility between this library and upstream dependencies like PyTorch.

