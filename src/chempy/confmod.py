#!/usr/bin/env python3
# This file is part of ChemPy.
# Copyright (C) 2026 Chem
#
# ChemPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ChemPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ChemPy. If not, see <http://www.gnu.org/licenses/>.

import argparse
import os
import shutil
import stat
import tempfile
from pathlib import Path


def replace_line(
    filename,
    old_line,
    new_line,
    backup=True,
    replace_all=False,
):
    """
    Replace a specific line in a Linux configuration file while preserving:
      - File owner (UID)
      - File group (GID)
      - File permissions/mode
      - SELinux context where possible

    Returns the number of replacements made.
    """

    path = Path(filename)

    if not path.is_file():
        raise FileNotFoundError(f"File does not exist: {filename}")

    # Get original file metadata BEFORE modifying it.
    original_stat = os.stat(path, follow_symlinks=False)

    original_uid = original_stat.st_uid
    original_gid = original_stat.st_gid
    original_mode = stat.S_IMODE(original_stat.st_mode)

    # Read the file while preserving line endings.
    with open(path, "r", encoding="utf-8", newline="") as f:
        lines = f.readlines()

    replacements = 0
    new_lines = []

    for line in lines:
        # Compare without the line ending so the caller doesn't
        # need to include \n in old_line.
        content = line.rstrip("\r\n")

        if content == old_line and (replace_all or replacements == 0):
            # Preserve the original line ending.
            if line.endswith("\r\n"):
                ending = "\r\n"
            elif line.endswith("\n"):
                ending = "\n"
            elif line.endswith("\r"):
                ending = "\r"
            else:
                ending = ""

            new_lines.append(new_line + ending)
            replacements += 1
        else:
            new_lines.append(line)

    if replacements == 0:
        return 0

    # Create a backup before modifying the original.
    if backup:
        backup_path = Path(str(path) + ".bak")
        shutil.copy2(path, backup_path)

    # Write to a temporary file in the SAME directory.
    #
    # This is important because os.replace() is atomic when the
    # source and destination are on the same filesystem.
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=str(path.parent),
        text=True,
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as temp_file:
            temp_file.writelines(new_lines)
            temp_file.flush()
            os.fsync(temp_file.fileno())

        # Restore the original ownership and permissions on the
        # temporary file BEFORE replacing the original.
        os.chown(temp_name, original_uid, original_gid)
        os.chmod(temp_name, original_mode)

        # Atomically replace the original file.
        os.replace(temp_name, path)

        # Best effort: preserve SELinux security context if the
        # system provides the appropriate utilities.
        #
        # restorecon will restore the expected context for the path.
        restorecon = shutil.which("restorecon")
        if restorecon:
            import subprocess

            subprocess.run(
                [restorecon, str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )

        return replacements

    except Exception:
        # Clean up the temporary file if anything went wrong.
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass

        raise


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Replace an exact line in a Linux configuration file "
            "while preserving ownership and permissions."
        )
    )

    parser.add_argument(
        "file",
        help="Configuration file to modify",
    )

    parser.add_argument(
        "old_line",
        help="Exact existing line to replace",
    )

    parser.add_argument(
        "new_line",
        help="Replacement line",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Replace every matching line instead of only the first",
    )

    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create a .bak backup",
    )

    args = parser.parse_args()

    try:
        count = replace_line(
            filename=args.file,
            old_line=args.old_line,
            new_line=args.new_line,
            backup=not args.no_backup,
            replace_all=args.all,
        )

        if count == 0:
            print("No matching line found.")
            return 1

        print(f"Successfully replaced {count} line(s) in {args.file}")

        if not args.no_backup:
            print(f"Backup created: {args.file}.bak")

        return 0

    except PermissionError:
        print(
            "ERROR: Permission denied. "
            "You may need to run this command as root."
        )
        return 2

    except Exception as e:
        print(f"ERROR: {e}")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())