#!/usr/bin/env python3

import json
import logging
import re
import subprocess
from argparse import ArgumentParser
from difflib import unified_diff
from pathlib import Path
from typing import Any


logger = logging.getLogger(__name__)


parser = ArgumentParser(description="Create module files for already built containers.")
parser.add_argument("paths", type=Path, nargs="+", help="Path(s) to existing .sif files")
parser.add_argument("--force", "-f", action="store_true")
parser.add_argument("--skip-on-error", action="store_true")
parser.add_argument("--log-level", default="WARNING", choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])


def parse_metadata(sif: Path) -> dict[str, Any]:
    """Parse metadata for sif file"""
    # First check for related .metadata.json file
    metadata = {}
    metadata_file = sif.parent / ".metadata.json"
    if metadata_file.is_file():
        metadata = json.loads(metadata_file.read_text())
    if "version" in metadata:
        raise RuntimeError(f"Default value for version found, this is not valid. File {metadata_file}.")

    # If specific entry exists for filename use that
    specific_metadata = metadata.get(sif.name, {})
    metadata.update(specific_metadata)

    # Abort parsing early if create_module is False
    if not metadata.get("create_module", True):
        return metadata

    # Parse filename for name and version
    namepattern = re.escape(metadata["name"]) if "name" in metadata else "[^-]+"
    versionpattern = metadata.get("versionpattern", ".+")
    pattern = fr"(?P<name>{namepattern})-(?P<version>{versionpattern})\.sif"
    m = re.fullmatch(pattern, sif.name, flags=re.IGNORECASE)
    if not m:
        raise RuntimeError(f"Failed to parse name and version from {sif.name}")

    parsed_name = m.group("name")
    if "name" not in metadata and parsed_name != sif.parent.name:
        raise RuntimeError(f'Mismatch between parsed name "{parsed_name}" and parent directory "{sif.parent.name}".')

    parsed_version = m.group("version")
    if (
        "version" not in metadata
        and "versionpattern" not in metadata
        and not parsed_version[:1].isdigit()
    ):
        raise RuntimeError(f'Unexpected version format "{parsed_version}" from {sif.name}.')

    # .metadata.json preceeds parsing rules
    name = metadata.get("name", parsed_name)

    # Add defaults
    defaults = {
        "name": parsed_name,
        "version": parsed_version,
        "help": f"""

Description
===========
{name} container.
""",
        "whatis": f"Description: {name}",
        "create_module": True,
    }
    for k, v in defaults.items():
        # Add values, but don't overwrite
        if k not in metadata:
            metadata[k] = v
    return metadata


def create_module(sif: Path, tree: Path, force: bool = False):
    """Create a lmod module file for sif file."""
    # Parse metadata
    sif = Path(sif).resolve()
    metadata = parse_metadata(sif)
    if not metadata["create_module"]:
        logger.info(f"Skipping {sif.name} based on metadata.")
        return
    name = metadata["name"]
    version = metadata["version"]

    # Create content of lua file
    template = f"""help([==[{metadata["help"]}]==])

whatis([==[{metadata["whatis"]}]==])

local root = "{sif.parent}"
local name = "{name}"
local version = "{version}"

conflict(name)

local container_image = pathJoin(root, "{sif.name}")
setenv("CONTAINER_IMAGE", container_image)
set_alias(name .. "_exec", "apptainer exec " .. container_image)
set_alias(name .. "_shell", "apptainer shell " .. container_image)
LmodMessage('Use "apptainer cmd $CONTAINER_IMAGE ..." or the "' .. name .. '_exec" and "' .. name .. '_shell" helper aliases')
"""

    logger.info(f'Creating module "container/{name}/{version}" from\n  {sif}.')

    out = tree / "container" / name / f"{version}.lua"
    
    # Handle possibly already existing module file
    if out.is_file():
        existing = out.read_text()

        if template == existing:
            # Skip if no changes
            logger.debug(f"Skipped {out} (identical file exists).")
            return

        elif not force:
            # Ask if overwrite or not
            prompt = "Module file exists. Overwrite? [Y/N] "
            print(
                '\n'.join(
                    unified_diff(
                        a=existing.splitlines(),
                        b=template.splitlines(),
                        fromfile=str(out),
                        tofile="new file",
                    )
                )
            )
            while (answer := input(prompt).strip().lower()) not in {"y", "n"}:
                print("Please enter Y or N.")
            if answer == "n":
                return
        else:
            logger.warning(f"Writing over existing {out}.")
                
    # Write template to file
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(template)
    logger.info(f"Created {out}")


def update_spider_cache(tree: Path):
    logger.info(f'Regenerating spider cache for {tree}')
    subprocess.run(
        [
            'flock', '-n', f'{tree}/.spider.lock', 
            '/usr/share/lmod/lmod/libexec/update_lmod_system_cache_files',
            '-d', f'{tree}/../cacheDir', 
            '-t', f'{tree}/../cacheTS.txt',
            f'{tree}/',
        ],
        check=True,
    )


def main():
    args = parser.parse_args()
    tree = Path("/apps/containers/modules/")
    logging.basicConfig(level=args.log_level)

    for path in args.paths:
        try:
            create_module(path, tree=tree, force=args.force)
        except RuntimeError as e:
            logger.error(f"Failed to create module for {path}")
            if args.skip_on_error:
                logger.error(e)
                continue
            raise

    update_spider_cache(tree=tree)


if __name__ == "__main__":
    main()
