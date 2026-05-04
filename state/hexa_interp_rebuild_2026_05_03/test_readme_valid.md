# Test Model

One-line summary: test fixture for hexa_interp rebuild validation.

## Origin

This is a test README for hf_upload_mk2 validation.

- Base model: test/test
- Training data: synthetic
- Trainer: hexa_interp_rebuild test fixture

## Falsifiers

- F-TEST-1: validate-readme returns OK on this file
  - Pass criterion: hexa run hf_upload_mk2.hexa --validate-readme exits 0 with OK

## Substrate

- Hexa interp Mac arm64 build (>= 2026-05-04)

## Caveats

- C1: This is a synthetic test fixture, not a real model card.
- C2: Validation behavior may differ across hexa interp versions.
- C3: Cross-platform Mac arm64 vs x86_64 may produce subtly different validation outcomes (raw#10).

## Composability

- Composes with: nothing (test only).
