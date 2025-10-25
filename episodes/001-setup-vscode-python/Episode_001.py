#!/usr/bin/env python3
"""
DISCLAIMER
This script moves files on your disk. Use it at your own risk.
- Default behavior is live mode: it will MOVE files into subfolders under the chosen root.
- There is no recycle bin step inside this script. Moves are performed with shutil.move.
- Test on a small sample folder first. If you want a preview, run with --dry-run.
- You are responsible for backups and for verifying that file paths and permissions are correct.

Main program flow
  1. Parse arguments
  2. Validate the root folder
  3. Scan for files
  4. Plan moves and print a readable preview
  5. Execute moves unless --dry-run is set

Copyright and license
- You may copy, modify, and use this script in your projects.
- No warranty of any kind is provided. The authors or distributors are not liable for any loss or damage.
"""

from __future__ import annotations  # enables future annotations behavior for type hints
import argparse                     # CLI parsing
import pathlib                      # object oriented paths
import shutil                       # high level file operations such as move
import sys                          # system exit and exceptions
from typing import Dict, List, Tuple  # type aliases for readability

# ===== USER CONFIG ===========================================================
# Default root folder to tidy. You can override this via the first CLI argument.
FOLDER = r"D:\MindSnippet\Akyao_Create\Python\Demo\Episode_001"

# How many planned moves to print as a preview before executing
SHOW = 20

# Scan subfolders by default. Disable recursion with the flag --no-recurse
RECURSE = True

# File type groups. Keys are destination subfolder names. Values are lists of extensions.
# Extensions must be without a leading dot and are matched case insensitive.
GROUPS: Dict[str, List[str]] = {
    "Images":   "jpg jpeg png gif webp bmp tiff heic".split(),
    "Docs":     "pdf doc docx xls xlsx ppt pptx txt rtf csv md".split(),
    "Videos":   "mp4 mov avi mkv webm m4v".split(),
    "Audio":    "mp3 wav m4a flac ogg".split(),
    "Archives": "zip 7z rar gz tar".split(),
    "Installers":"exe msi".split(),
    "Code":     "py js ts html css json xml yml yaml ps1 bat cmd".split(),
}

# Fallback folder used when a file has an unknown or empty extension
OTHER = "_Other"
# ============================================================================


def choose_folder(ext: str) -> str:
    """
    Decide the destination subfolder name for a given file extension.
    Returns OTHER when the extension is empty or not listed in GROUPS.
    """
    ext = ext.lower().lstrip(".")          # normalize to lowercase and strip a leading dot
    if not ext:                            # files without an extension go to OTHER
        return OTHER
    for folder, exts in GROUPS.items():
        if ext in exts:                    # check if the extension belongs to this group
            return folder
    return OTHER                           # return OTHER if no group matches


def unique_path(target: pathlib.Path) -> pathlib.Path:
    """
    Ensure the destination path is unique.
    If target exists, append " (i)" before the suffix, incrementing i until free.
    Example: "file.txt" -> "file (1).txt", "file (2).txt", etc.
    """
    if not target.exists():                # no collision, return as is
        return target
    stem, suffix = target.stem, target.suffix
    i = 1
    while True:
        candidate = target.with_name(f"{stem} ({i}){suffix}")  # try a numbered variant
        if not candidate.exists():         # stop once a free name is found
            return candidate
        i += 1                              # increment and try again


def enumerate_files(root: pathlib.Path, recurse: bool) -> List[pathlib.Path]:
    """
    Collect files to process under the given root.
    If recurse is True, scan all subfolders with rglob.
    Otherwise only the top level is scanned.
    """
    if recurse:
        return [p for p in root.rglob("*") if p.is_file()]
    return [p for p in root.iterdir() if p.is_file()]


def plan_moves(root: pathlib.Path, files: List[pathlib.Path]) -> List[Tuple[pathlib.Path, pathlib.Path]]:
    """
    Build a list of planned moves as tuples of (source, destination).
    Destination subfolders are created under the root folder only.
    Files from subfolders are moved up into grouped subfolders under root.
    """
    plans: List[Tuple[pathlib.Path, pathlib.Path]] = []
    for src in sorted(files):                           # stable order for readability
        dest_folder = root / choose_folder(src.suffix)  # group subfolder under root
        dest = unique_path(dest_folder / src.name)      # ensure destination is unique
        if dest != src:                                 # skip already well placed files
            plans.append((src, dest))
    return plans


def summarize(plans: List[Tuple[pathlib.Path, pathlib.Path]]) -> Dict[str, int]:
    """
    Count planned moves per destination subfolder name.
    """
    counts: Dict[str, int] = {}
    for _, dest in plans:
        counts[dest.parent.name] = counts.get(dest.parent.name, 0) + 1
    return counts


def parse_args() -> argparse.Namespace:
    """
    [1] Parse arguments
    Define and parse command line options.
    Default mode is live mode. Use --dry-run for a preview without moving files.
    """
    ap = argparse.ArgumentParser(
        description="Tidy a folder by moving files into subfolders by type. Default is live mode."
    )
    ap.add_argument(
        "folder",
        nargs="?",
        default=FOLDER,
        help="Folder to tidy. Defaults to configured FOLDER"
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only. Do not move files"
    )
    ap.add_argument(
        "--show",
        type=int,
        default=SHOW,
        help="Preview limit for planned moves"
    )
    ap.add_argument(
        "--no-recurse",
        dest="recurse",
        action="store_false",
        default=RECURSE,
        help="Do not scan subfolders"
    )
    ap.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print diagnostic information"
    )
    return ap.parse_args()


def main() -> None:
    """
    Orchestrates the 5 numbered steps described at the top.
    """
    args = parse_args()  # [1] Parse arguments

    root = pathlib.Path(args.folder).expanduser().resolve()  # normalize to absolute path
    # [2] Validate the root folder
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Folder not found: {root}")

    if args.verbose:
        # Diagnostics to help with understanding what will be processed
        print("=== Diagnostics ===")
        print(f"Root: {root}")
        print(f"Recursive scan: {args.recurse}")

    # [3] Scan for files
    files = enumerate_files(root, args.recurse)
    if args.verbose:
        top_only = [p for p in root.iterdir() if p.is_file()]
        print(f"Files in top level: {len(top_only)}")
        print(f"Files total{' recursive' if args.recurse else ''}: {len(files)}")
        print("===================")

    if not files:
        print("No files found to process. Nothing to do.")
        return

    # [4] Plan moves and print a readable preview
    plans = plan_moves(root, files)
    if not plans:
        print("Nothing to do. This folder already looks tidy.")
        return

    print(f"Planned moves in: {root}")
    for i, (src, dst) in enumerate(plans):
        if i < args.show:
            rel = src.relative_to(root) if root in src.parents or src == root else src
            print(f"  {rel}  ->  {dst.parent.name}/{dst.name}")
        elif i == args.show:
            print(f"  ... and {len(plans) - args.show} more")
            break

    sums = summarize(plans)
    print("\nSummary:")
    for k in sorted(sums):
        print(f"  {k:<12} : {sums[k]} file(s)")
    print(f"  TOTAL        : {len(plans)} file(s)\n")

    # [5] Execute moves unless --dry-run is set
    if args.dry_run:
        print("Dry run only. Run without --dry-run to perform the moves.")
        return

    print("LIVE MODE: moving files now. Use --dry-run if you want a preview.")
    moved = 0
    for src, dst in plans:
        dst.parent.mkdir(parents=True, exist_ok=True)  # create target folder if needed
        shutil.move(str(src), str(dst))                # perform the move
        moved += 1
    print(f"Done. Moved {moved} file(s).")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)  # conventional exit code when user presses Ctrl+C
