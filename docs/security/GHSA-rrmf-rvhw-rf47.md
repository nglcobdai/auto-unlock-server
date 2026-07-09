# GHSA-rrmf-rvhw-rf47

## Status

- Advisory: `GHSA-rrmf-rvhw-rf47` / `CVE-2025-3000`
- Package: `torch`
- GitHub alert: `#48`
- Last reviewed: `2026-07-09`

## Repository assessment

This service depends on `torch` through Whisper model loading, but the application code only uses:

- `whisper.load_model(...)`
- `model.transcribe(...)`

The advisory is specific to `torch.jit.script`, and the repository does not call that API in `server/`.

## Handling

- Keep the GitHub Dependabot alert dismissed only while no patched upstream version exists.
- Re-check the advisory metadata before each dependency refresh or security release.
- The regression test in `tests/test_torch_jit_usage.py` prevents accidental introduction of `torch.jit.script`.
