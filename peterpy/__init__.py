from importlib.metadata import PackageNotFoundError, version

from aiohttp.web import RouteTableDef

routes = RouteTableDef()

try:
    __version__ = version("peterpy")
except PackageNotFoundError:
    from tomlkit import load

    with open("pyproject.toml", "rb") as pyproject_f:
        __version__ = load(pyproject_f)["tool"]["poetry"]["version"]  # type: ignore
