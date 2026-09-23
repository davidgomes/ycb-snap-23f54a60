# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest
from py._path.local import LocalPath  # type: ignore[import]

from pylint import run_epylint, run_pylint, run_pyreverse, run_symilar
from pylint.lint.run import _cpu_count, _query_cpu


@pytest.mark.parametrize(
    "runner", [run_epylint, run_pylint, run_pyreverse, run_symilar]
)
def test_runner(runner: Callable, tmpdir: LocalPath) -> None:
    filepath = os.path.abspath(__file__)
    testargs = ["", filepath]
    with tmpdir.as_cwd():
        with patch.object(sys, "argv", testargs):
            with pytest.raises(SystemExit) as err:
                runner()
            assert err.value.code == 0


@pytest.mark.parametrize(
    "runner", [run_epylint, run_pylint, run_pyreverse, run_symilar]
)
def test_runner_with_arguments(runner: Callable, tmpdir: LocalPath) -> None:
    """Check the runners with arguments as parameter instead of sys.argv."""
    filepath = os.path.abspath(__file__)
    testargs = [filepath]
    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            runner(testargs)
        assert err.value.code == 0


def _cgroup_cpu(quota: str | None, period: str | None, shares: str | None):
    """Return patches that fake the cgroup v1 cpu files ``_query_cpu`` reads."""
    contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": quota,
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": period,
        "/sys/fs/cgroup/cpu/cpu.shares": shares,
    }
    builtin_open = open

    def _mock_open(*args, **kwargs):
        path = args[0] if args else kwargs.get("file")
        data = contents.get(path)
        if data is not None:
            return mock_open(read_data=data)(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    def _mock_path(path, *args, **kwargs):
        if path in contents:
            return MagicMock(is_file=lambda: contents[path] is not None)
        return Path(path, *args, **kwargs)

    return (
        patch("builtins.open", _mock_open),
        patch("pylint.lint.run.Path", _mock_path),
    )


def test_query_cpu_fractional_shares_is_at_least_one() -> None:
    """A Kubernetes pod with ``cpu.shares`` below 1024 must not yield 0 jobs.

    ``cpu.cfs_quota_us == -1`` skips the quota and ``2 / 1024`` used to be
    truncated to 0, which crashes ``multiprocessing.Pool``.
    """
    open_patch, path_patch = _cgroup_cpu(quota="-1\n", period="100000\n", shares="2\n")
    with open_patch, path_patch:
        assert _query_cpu() == 1
        assert _cpu_count() >= 1


def test_query_cpu_fractional_quota_is_at_least_one() -> None:
    """A limit below one core (quota < period) must not yield 0 jobs either."""
    open_patch, path_patch = _cgroup_cpu(
        quota="50000\n", period="100000\n", shares=None
    )
    with open_patch, path_patch:
        assert _query_cpu() == 1


def test_query_cpu_whole_cores_are_preserved() -> None:
    """Whole allotted cores from shares or quota stay unchanged."""
    shares_open, shares_path = _cgroup_cpu(quota="-1\n", period=None, shares="2048\n")
    with shares_open, shares_path:
        assert _query_cpu() == 2

    quota_open, quota_path = _cgroup_cpu(
        quota="200000\n", period="100000\n", shares=None
    )
    with quota_open, quota_path:
        assert _query_cpu() == 2
