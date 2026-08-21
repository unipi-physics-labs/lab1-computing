#!/usr/bin/env python
#
# Copyright (C) 2026, Luca Baldini (luca.baldini@pi.infn.it).
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

""" Rudimentary release manager.
"""


import argparse
import pathlib
import subprocess
import sys
from datetime import date

import yaml
from loguru import logger

# Configure the logger.
logger.remove()
logger.add(sink=sys.stderr, colorize=True, format='>>> <level>{message}</level>')


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
METADATA_FILE_PATH = REPO_ROOT / 'meta.yml'
README_FILE_PATH = REPO_ROOT / 'README.md'
GITHUB_RELEASE_URL = 'https://github.com/unipi-physics-labs/lab1-computing/releases'

INCREMENT_MODES = ('major', 'minor', 'patch')

_ENCODING = 'utf-8'


def execute_shell_command(arguments):
    """Execute a shell command.
    """
    logger.info(f'About to execute "{" ".join(arguments)}"...')
    return subprocess.run(arguments, check=True)

def _read_metadata():
    """ Read the metadata from the appropriate file.
    """
    logger.info(f"Reading metadata from {METADATA_FILE_PATH}...")
    with open(METADATA_FILE_PATH, encoding=_ENCODING) as input_file:
        metadata = yaml.safe_load(input_file)
    logger.debug(metadata)
    return metadata

def _write_metadata(metadata: dict):
    """ Write the metadata to the appropriate file.
    """
    logger.info(f"Writing metadata to {METADATA_FILE_PATH}...")
    logger.debug(metadata)
    with open(METADATA_FILE_PATH, "w", encoding=_ENCODING) as output_file:
        yaml.safe_dump(metadata, output_file, sort_keys=False)

def _asset_url(name: str, version: str) -> str:
    """ Return the URL for an asset.
    """
    return f"{GITHUB_RELEASE_URL}/download/{version}/{name}-{version}.pdf"

def _write_readme(metadata: dict) -> None:
    """ Update the README file.
    """
    readme_path = REPO_ROOT / "README.md"
    logger.info(f"Writing README file to {readme_path}...")
    with open(readme_path, "w", encoding=_ENCODING) as readme_file:
        readme_file.write("# lab1-computing\n\n")
        readme_file.write("Materiale didattico a supporto del modulo di computazione.\n")

def _update_history(metadata: dict) -> None:
    """ Update the history file.
    """
    history_path = REPO_ROOT / "chapters" / "history.qmd"
    logger.info(f"Updating history file {history_path}...")
    _tag, _date = metadata['tag'], metadata['date']
    with open(history_path, encoding=_ENCODING) as input_file:
        lines = input_file.readlines()
    with open(history_path, "w", encoding=_ENCODING) as output_file:
        output_file.write("# Cronologia delle versioni {#sec-history}\n\n")
        output_file.write(f"### Versione {_tag} ({_date}) {{.unnumbered}}\n\n")
        # Note we skip the title and the first empty line.
        for line in lines[2:]:
            output_file.write(line)

def bump_version(mode: str) -> str:
    """Update the version.tex file.
    """
    logger.info(f'Bumping version (mode = {mode})...')
    old_version = _read_metadata().get('tag')
    major, minor, patch = (int(item) for item in old_version.split('.'))
    if mode == 'major':
        major += 1
        minor = 0
        patch = 0
    elif mode == 'minor':
        minor += 1
        patch = 0
    elif mode == 'patch':
        patch += 1
    new_version = f'{major}.{minor}.{patch}'
    logger.info(f'Target version is {new_version}')
    metadata = dict(tag=new_version, date=date.today().isoformat())
    _write_metadata(metadata)
    _write_readme(metadata)
    _update_history(metadata)
    return metadata

def release(mode: str) -> None:
    """ Tag the package and create a release.
    """
    execute_shell_command(['git', 'pull'])
    meta = bump_version(mode)
    return
    version = meta['tag']
    msg = f'Prepare for tag {version}.'
    execute_shell_command(['git', 'commit', '-a', '-m', msg])
    execute_shell_command(['git', 'push'])
    msg = f'Tagging version {version}...'
    execute_shell_command(['git', 'tag', '-a', version, '-m', msg])
    execute_shell_command(['git', 'push', '--tags'])
    execute_shell_command(['git', 'status'])
    logger.info(f'Release {version} completed successfully.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, choices=INCREMENT_MODES,
                        help='Version increment mode')
    args = parser.parse_args()
    release(args.mode)
