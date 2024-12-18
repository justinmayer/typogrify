from inspect import cleandoc
import logging
import os
from pathlib import Path
from shutil import which

from invoke import task

logger = logging.getLogger(__name__)

PKG_NAME = "typogrify"
PKG_PATH = Path(f"{PKG_NAME}")

ACTIVE_VENV = os.environ.get("VIRTUAL_ENV", None)
VENV_HOME = Path(os.environ.get("WORKON_HOME", "~/.local/share/virtualenvs"))
VENV_PATH = Path(ACTIVE_VENV) if ACTIVE_VENV else (VENV_HOME.expanduser() / PKG_NAME)
VENV = str(VENV_PATH.expanduser())
BIN_DIR = "bin" if os.name != "nt" else "Scripts"
VENV_BIN = Path(VENV) / Path(BIN_DIR)

CMD_PREFIX = f"{VENV_BIN}/" if ACTIVE_VENV else "uv run "
PRECOMMIT = which("pre-commit") if which("pre-commit") else "uvx run pre-commit"
PTY = os.name != "nt"


@task
def tests(c, deprecations=False):
    """Run the test suite, optionally with `--deprecations`."""
    deprecations_flag = "" if deprecations else "-W ignore::DeprecationWarning"
    c.run(
        f"{CMD_PREFIX}pytest {deprecations_flag} --doctest-modules typogrify/filters.py typogrify/packages/titlecase/tests.py",
        pty=True,
    )


@task
def format(c, check=False, diff=False):
    """Run Ruff's auto-formatter, optionally with `--check` or `--diff`."""
    check_flag, diff_flag = "", ""
    if check:
        check_flag = "--check"
    if diff:
        diff_flag = "--diff"
    c.run(
        f"{CMD_PREFIX}ruff format {check_flag} {diff_flag} {PKG_PATH} tasks.py", pty=PTY
    )


@task
def ruff(c, concise=False, fix=False, diff=False):
    """Run Ruff to ensure code meets project standards."""
    concise_flag, fix_flag, diff_flag = "", "", ""
    if concise:
        concise_flag = "--output-format=concise"
    if fix:
        fix_flag = "--fix"
    if diff:
        diff_flag = "--diff"
    c.run(f"{CMD_PREFIX}ruff check {concise_flag} {diff_flag} {fix_flag} .", pty=PTY)


@task
def lint(c, concise=False, fix=False, diff=False):
    """Check code style via linting tools."""
    ruff(c, concise=concise, fix=fix, diff=diff)
    format(c, check=(not fix), diff=diff)


@task
def precommit(c):
    """Install pre-commit hooks to .git/hooks/pre-commit."""
    logger.info("** Installing pre-commit hooks **")
    c.run(f"{PRECOMMIT} install")


@task
def setup(c):
    """Set up the development environment."""
    if which("uv") or ACTIVE_VENV:
        c.run("uv sync --all-groups", pty=PTY)
        precommit(c)
        logger.info("\nDevelopment environment should now be set up and ready!\n")
    else:
        error_message = """
            uv is not installed, and there is no active virtual environment available.
            You can either manually create and activate a virtual environment, or you can
            install uv via:

            curl -LsSf https://astral.sh/uv/install.sh | sh

            Once you have taken one of the above two steps, run `invoke setup` again.
            """  # noqa: E501
        raise SystemExit(cleandoc(error_message))
