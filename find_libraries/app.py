import argparse
import ast
import json
from importlib.metadata import packages_distributions, version
from typing import Any

from .utils._logger import logger
from .utils._validation import config_args

with open(config_args.libraries) as file:
    libraries_json = json.load(file)

default_libraries: set[Any] = set(libraries_json["libraries"])
distributions = packages_distributions()


def find_imported_libraries(
    file_path,
):
    """Find libraries imported to script other than the default libraries."""
    libraries_found = set()
    libraries_found_versions = list()
    try:
        with open(file_path, encoding="utf-8") as file:
            tree = ast.parse(file.read(), filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        libraries_found.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    libraries_found.add(node.module.split(".")[0])

        if (
            len(installed_libraries := libraries_found.difference(default_libraries))
            > 0
        ):
            for module in installed_libraries:
                module: str = distributions[module][0].casefold()
                module = module + ">=" + version(module)
                libraries_found_versions.append(module)
            logger.info("Process comleted.")
            return libraries_found_versions
        else:
            return "Could not found any installed library."
    except Exception as e:
        logger.error(f"Process failed: {e}")
        print("Process failed.")


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description="Returns installed libraries with versions."
        )
        parser.add_argument("-p", "--file_path", metavar="", help="Path to the file")
        args: argparse.Namespace = parser.parse_args()
        print(find_imported_libraries(args.file_path))

    except Exception as e:
        logger.error(f"An error occured: {e}")
        print("An error occured.")
