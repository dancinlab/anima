https://github.com/Samsung/TICO/issues/637
# [quantization] Make range expansion (including zero) configurable in observer

## Summary

The recent fix for asymmetric quantization updates the observed range to always include zero when the original range does not cross zero. While this resolves the inconsistency between `scale` and `zero_point` (e.g., clamping issues), it also changes the quantization behavior and may reduce precision in certain cases.

This issue proposes making this behavior configurable.

Related: #634

## Background

In asymmetric quantization, when the observed range does not include zero (e.g., strictly positive or strictly negative values), computing `zero_point` from the original range can result in values outside the representable integer range, leading to clamping and inconsistent quantization.

To address this, the current implementation expands the range to include zero:
- if `min > 0`, set `min = 0`
- if `max < 0`, set `max = 0`

This ensures a valid `(scale, zero_point)` pair but introduces a trade-off.

## Problem

Expanding the range to include zero can significantly increase the scale when the original range is far from zero.

Example:
- Original range: `[1024, 1030]`
- Adjusted range: `[0, 1030]`
- Result: much larger scale → reduced quantization resolution

This may negatively impact accuracy for tensors with large offsets.

## Proposal

Introduce a configuration option to control this behavior.

### Option 1: Boolean flag

```python
include_zero_in_range: bool = True
```

### Option 2: Policy-based configuration

```python
asym_range_policy: Literal[
    "force_include_zero",  # current behavior
    "keep_original"        # do not modify observed range
]
```

###  Additional Considerations

- Emit a warning when the observed range does not include zero, especially when range expansion is applied.
- Consider extending support for more advanced heuristics (e.g., conditionally expanding only when the range is close to zero).

### Expected Outcome

- Provide users with control over the trade-off between numerical stability and quantization precision.
- Improve transparency and debuggability of quantization behavior.
