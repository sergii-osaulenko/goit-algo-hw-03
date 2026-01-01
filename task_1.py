#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли з вихідної директорії "
                    "та сортує їх у директорії призначення за розширенням."
    )
    parser.add_argument(
        "src",
        help="Шлях до вихідної директорії"
    )
    parser.add_argument(
        "dst",
        nargs="?",
        default="dist",
        help="Шлях до директорії призначення (за замовчуванням: dist)"
    )
    return parser.parse_args()


def ensure_dir(path: Path):
    """Створити директорію, якщо вона ще не існує."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Не вдалося створити директорію {path}: {e}")


def copy_file_to_ext_dir(file_path: Path, dst_root: Path):
    """
    Копіює файл у піддиректорію всередині dst_root, названу за його розширенням.
    Напр.: example.txt -> dst_root/txt/example.txt
    Якщо розширення немає, використовується піддиректорія 'no_ext'.
    """
    ext = file_path.suffix.lower().lstrip(".")
    if not ext:
        ext = "no_ext"
    target_dir = dst_root / ext
    ensure_dir(target_dir)

    target_file = target_dir / file_path.name
    try:
        shutil.copy2(file_path, target_file)  # зберігає метадані файлу [web:4]
        print(f"Скопійовано: {file_path} -> {target_file}")
    except (OSError, shutil.Error) as e:
        print(f"Помилка копіювання {file_path}: {e}")


def walk_and_copy(src_dir: Path, dst_root: Path):
    """
    Рекурсивно обходить директорію src_dir.
    Якщо знаходить файл — копіює його в dst_root/<розширення>/.
    Якщо знаходить піддиректорію — рекурсивно заходить у неї.
    """
    try:
        entries = list(src_dir.iterdir())
    except OSError as e:
        print(f"Помилка доступу до директорії {src_dir}: {e}")
        return

    for entry in entries:
        if entry.is_dir():
            # рекурсивний виклик для піддиректорії
            walk_and_copy(entry, dst_root)
        elif entry.is_file():
            copy_file_to_ext_dir(entry, dst_root)
        else:
            # наприклад, символічні лінки чи інші типи
            print(f"Пропущено не-файл/не-директорію: {entry}")


def main():
    args = parse_args()
    src = Path(args.src).resolve()
    dst = Path(args.dst).resolve()

    if not src.exists() or not src.is_dir():
        print(f"Вихідна директорія не існує або не є директорією: {src}")
        return

    ensure_dir(dst)
    walk_and_copy(src, dst)
    print(f"Готово. Всі файли з {src} скопійовано в {dst} та "
          f"розсортовано за розширенням.")


if __name__ == "__main__":
    main()