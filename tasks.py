# type: ignore

import subprocess
from typing import Union

from invoke import task


@task
def lint(c, path="app"):
    """コードチェック"""
    run(f"poetry run mypy {path}")


@task
def clear(c, all=False, mypy=False, pytest=False):
    """キャッシュを削除"""
    caches = ["__pycache__"]
    mypy_cache_name = ".mypy_cache"
    pytest_cache_name = ".pytest_cache"
    if all:
        caches.append(mypy_cache_name)
        caches.append(pytest_cache_name)
    elif mypy:
        caches.append(mypy_cache_name)
    elif pytest:
        caches.append(pytest_cache_name)

    run(f'find . | grep -E "({"|".join(caches)}$)" | xargs rm -rf')


@task
def test(c, all=False, file="", duration=False, coverage=False, init=False):
    """テストを実行"""
    cmd = [
        "ENV=test",
        "poetry run pytest",
        f"tests/app/{file}",
        "--log-cli-level=DEBUG",
    ]
    if all or duration:
        cmd.append("--durations=0 -vv")
    if all or coverage:
        cmd.append("--cov=app --cov-report=term-missing")
    run(cmd)


def run(cmd: Union[str, list]) -> None:
    cmd_type = type(cmd)

    inner_cmd = ""
    if cmd_type is str:
        inner_cmd = str(cmd)
    elif cmd_type is list:
        inner_cmd = " ".join(cmd)
    else:
        raise Exception("引数cmdの型は[str|list]です")

    print(f"\033[32mrun cmd\033[0m: {inner_cmd}")
    subprocess.run(inner_cmd, shell=True)
