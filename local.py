# type: ignore
# ruff: noqa
import argparse
import asyncio
import json
import logging
import subprocess
from argparse import Namespace
from configparser import ConfigParser
from logging import Logger
from pathlib import Path
from pprint import pformat, pprint
from time import time
from typing import TYPE_CHECKING, Any, ClassVar, Optional
from logging.handlers import TimedRotatingFileHandler
import datetime
import sys


local_data_path: Path = Path(__file__).parent.joinpath("")
LOGGER: logging.Logger = logging.getLogger(__name__)


async def local_test() -> None:
    pass


def ini_load(file: Path, section: str, options: list[str]) -> list[str | None]:
    """Parse an ini file.

    Parameters
    ----------
    file: :class:`Path`
        The file path.
    section: :class:`str`
        The name of the section. `[section_name]`.
    options: :class:`list[str]`
        The options to load as a list.

    Returns
    -------
        The list of options loaded in the same order.
    """
    if file.is_file():
        settings = ConfigParser(converters={"list": lambda setting: [value.strip() for value in setting.split(",")]})
        settings.read(filenames=file)
        res: list[str | None] = []
        for entry in options:
            res.append(settings.get(section=section, option=entry, fallback=None))
        return res
    else:
        raise FileNotFoundError("<%s> | Failed to load file. | Path: %s", "local.ini_load", file.as_posix())


def flatten(data: list, new_list: list) -> list:
    """Flatten a list."""
    for i in data:
        if isinstance(i, list):
            flatten(i, new_list)
        else:
            new_list.append(i)
    return new_list


def load_data_from_file(path: Path, size: Optional[int] = None, is_json: bool = False, encoding: str = "utf-8") -> str | dict[Any, Any]:
    """Basic file read.

    Parameters
    -----------
    path: :class:`Path`
        The Path to load the data from.
    size: :class:`Optional[int]`, optional
        The amount of data to read if needed, by default None will read until EOF.

    Returns
    --------
    :class:`str`
        The file data.

    Raises
    -------
    FileNotFoundError
        If the file path doesn't exist.
    TypeError
        If the path provided is not a Path object.
    """

    if isinstance(path, Path) is False:
        msg = "<%s.%s> | The Path provided is not a Path object. | Path: %s"
        raise TypeError(msg, __name__, "load_data_from_file", path)

    elif path.exists() is False:
        msg = "<%s.%s> | The Path provided does not exist. | Path: %s"
        raise FileNotFoundError(msg, __name__, "load_data_from_file", path)

    with path.open(mode="r", encoding=encoding) as file:
        if is_json is True:
            data = json.loads(file.read(size))
            return data

        data = file.read(size)
        return data


def write_data_to_file(
    file_name: str,
    data: bytes | dict[Any, Any] | str | list,
    path: Path = Path(__file__).parent,
    *,
    mode: str = "w+",
    **kwargs: Any,
) -> None:
    """Basic file dump with json handling. If the data parameter is of type `dict`, `json.dumps()` will be used with an indent of 4.

    Parameters
    ----------
    path: :class:`Path`, optional
        The Path to write the data, default's to `Path(__file__).parent`.
    file_name: :class:`str`
        The name of the file, include the file extension.
    data: :class:`bytes | dict | str | list`
        The data to write out to the path and file_name provided.
    mode: :class:`str`, optional
        The mode to open the provided file path with using `<Path.open()>`.
    **kwargs: :class:`Any`
        Any additional kwargs to be supplied to `<json.dumps()>`, if applicable.

    """
    with path.joinpath(file_name).open(mode=mode) as file:
        LOGGER.debug("<%s.%s> | Wrote data to file %s located at: %s", __name__, "write_data_to_file", path, file_name)
        if isinstance(data, bytes):
            file.write(data.decode(encoding="utf-8"))
        elif isinstance(data, dict):
            file.write(json.dumps(data, indent=4, **kwargs))
        elif isinstance(data, list):
            file.write("\n".join(data))
        else:
            file.write(data)
    LOGGER.info(
        "<%s.%s> | File write successful to path: %s ",
        __name__,
        "write_data_to_file",
        path.joinpath(file_name).as_posix(),
    )


class LogHandler:
    """
    Discord Multi-line code block formats:
    - https://github.com/highlightjs/highlight.js/blob/main/SUPPORTED_LANGUAGES.md

    """

    cur_log: Path
    code_formats: ClassVar[list[str]] = ["excel", "nc", "ml", " nim", " ps", " prolog", "thor"]
    default_code_format: str = "ps"

    def __init__(self, sentry: str, level: int = logging.INFO, webhook_url: str = "", local_dev: bool = True) -> None:
        if local_dev == False:
            LOGGER.info("Sentry SDK is Enabled -- Flag: %s", local_dev)
            # sentry_sdk.init(dsn=sentry, integrations=[AioHttpIntegration(), AsyncioIntegration()])
        else:
            LOGGER.warning("Sentry SDK is Disabled -- Flag: %s", local_dev)
        # self.webhook_url: str = webhook_url
        # self.session: aiohttp.ClientSession
        self.path: Path = Path(__file__).parent.joinpath("logs")
        self.cur_log: Path = Path(__file__).parent.joinpath("logs/log.log")

        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
            handlers=[
                logging.StreamHandler(stream=sys.stdout),
                TimedRotatingFileHandler(
                    filename=Path.as_posix(self=self.path) + "/log.log",
                    when="midnight",
                    atTime=datetime.datetime.min.time(),
                    backupCount=4,
                    encoding="utf-8",
                    utc=True,
                ),
            ],
        )


class Launcher(Namespace):
    local: bool
    build: bool
    info: bool
    debug: bool
    upgrade: Optional[bool]


_parser = argparse.ArgumentParser(description="Local arg parse for Python Package development")
_parser.add_argument("-local", help="Run our local_test() function", default=False, required=False, action="store_true")
_parser.add_argument("-build", help="Run our development_text() function", default=False, required=False, action="store_true")
# uv sync -n --upgrade-package foo
_parser.add_argument("--upgrade", help="Run `uv sync -n --upgrade-package package_name`")
# If I want to add a group, this is what I use.
# group: argparse._MutuallyExclusiveGroup = _parser.add_mutually_exclusive_group(required=False)
_parser.add_argument("-info", help="Set the logging level to `INFO`.", default=False, required=False, action="store_true")
_parser.add_argument("-debug", help="Set the logging level to `INFO`.", default=False, required=False, action="store_true")
_parsed_args: Launcher = _parser.parse_known_args()[0]

# Logging section.
LOGGER.name = "Local Logging - "
if _parsed_args.info:
    LogHandler(level=logging.INFO)
elif _parsed_args.debug:
    LogHandler(level=logging.DEBUG)


# Any specific handling of launch args.
# Update `Launcher` class with new args and type def.
stime: float = time()
if _parsed_args.upgrade:
    LOGGER.info("Running uv sync upgrade. | Package: %s", _parsed_args.upgrade)
    subprocess.run([f"uv sync -n --upgrade-package {_parsed_args.upgrade}"], check=False, shell=True)  # noqa: S602
    LOGGER.info("Completed in %s seconds...", format(time() - stime, ".3f"))

if _parsed_args.local:
    LOGGER.info("Running local_test()...")
    asyncio.run(local_test())
    LOGGER.info("Completed in %s seconds...", format(time() - stime, ".3f"))

if _parsed_args.build:
    LOGGER.info("Build...")
    # subprocess.call("./build.bash")
    LOGGER.info("Completed in %s seconds...", format(time() - stime, ".3f"))
