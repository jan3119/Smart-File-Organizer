import os
import shutil
import hashlib
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox


file_type = {
    "images": [".jpg", ".png", ".jpeg", ".gif"],
    "documents": [".txt", ".pdf", ".docx", ".xlsx", ".zip"],
    "videos": [".mp4", ".mkv"],
    "music": [".mp3", ".wav"]
}


def log_action(message):
    with open("log.txt", "a", encoding="utf-8") as f:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] {message}\n")


def get_file_hash(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None


def organize_file(folder_path, callback=None):

    seen_hashes = set()

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        if os.path.isdir(file_path):
            continue

        file_hash = get_file_hash(file_path)

        if file_hash is None:
            continue

        # duplicates
        if file_hash in seen_hashes:
            dup_folder = os.path.join(folder_path, "duplicates")
            os.makedirs(dup_folder, exist_ok=True)

            shutil.move(file_path, os.path.join(dup_folder, file))
            log_action(f"Duplicate moved: {file}")

            if callback:
                callback(f"Duplicate → {file}")

            continue

        seen_hashes.add(file_hash)

        file_lower = file.lower()
        moved = False

        for folder, extensions in file_type.items():
            if any(file_lower.endswith(ext) for ext in extensions):

                target_folder = os.path.join(folder_path, folder)
                os.makedirs(target_folder, exist_ok=True)

                shutil.move(file_path, os.path.join(target_folder, file))
                log_action(f"Moved {file} -> {folder}")

                if callback:
                    callback(f"Moved → {file} -> {folder}")

                moved = True
                break

        if not moved and callback:
            callback(f"Skipped → {file}")
