import ctypes
from pathlib import Path

from core import cuda_paths


def test_ensure_cuda_libs_preloads_split_pip_wheel_directories(monkeypatch, tmp_path):
    cublas = tmp_path / "nvidia/cublas/lib"
    nvrtc = tmp_path / "nvidia/cuda_nvrtc/lib"
    cublas.mkdir(parents=True)
    nvrtc.mkdir(parents=True)
    (cublas / "libcublasLt.so.12").touch()
    (cublas / "libcublas.so.12").touch()
    (nvrtc / "libnvrtc-builtins.so.12.8").touch()
    (nvrtc / "libnvrtc.so.12").touch()
    loaded = []

    def fake_cdll(path, mode=None):
        if path == "libcublas.so.12":
            raise OSError("plain SONAME is not resolvable")
        loaded.append(Path(path).name)
        return object()

    monkeypatch.setattr(cuda_paths.sys, "platform", "linux")
    monkeypatch.setattr(cuda_paths, "_gpu_present", lambda: True)
    monkeypatch.setattr(cuda_paths, "_installed_cupy_major", lambda: 12)
    monkeypatch.setattr(cuda_paths, "_candidate_dirs", lambda major: [str(cublas), str(nvrtc)])
    monkeypatch.setattr(cuda_paths.ctypes, "CDLL", fake_cdll)
    monkeypatch.setattr(cuda_paths, "_RESULT", None)
    monkeypatch.delenv("LD_LIBRARY_PATH", raising=False)
    monkeypatch.delenv("CUDA_PATH", raising=False)

    result = cuda_paths.ensure_cuda_libs()

    assert result["configured"] is True
    assert "libnvrtc.so.12" in loaded
    assert "libcublas.so.12" in loaded
    paths = cuda_paths.os.environ["LD_LIBRARY_PATH"].split(cuda_paths.os.pathsep)
    assert paths == [str(cublas), str(nvrtc)]
