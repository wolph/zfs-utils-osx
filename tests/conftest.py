"""Block external commands and filesystem traversal in every test."""

import os
import subprocess

import pytest


@pytest.fixture(autouse=True)
def isolate_system(monkeypatch):
    # type: (object) -> None
    def forbidden(*args, **kwargs):
        # type: (*object, **object) -> None
        pytest.fail('Unexpected external command or filesystem traversal')

    monkeypatch.setattr(subprocess, 'check_output', forbidden)
    monkeypatch.setattr(os, 'walk', forbidden)
