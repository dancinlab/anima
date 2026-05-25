from __future__ import annotations


def pytest_configure(config):
    config.addinivalue_line("markers", "auto: stdlib-only check")
    config.addinivalue_line("markers", "hexa: requires hexa-lang runtime")
