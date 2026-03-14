# 🐉 LUO GATE — FILE SYSTEM
import os
from datetime import datetime

WORKSPACE = "workspace"

def ensure():
    os.makedirs(WORKSPACE, exist_ok=True)

def write_file(filename, content):
    ensure()
    path = f"{WORKSPACE}/{filename}"
    with open(path, "w") as f:
        f.write(content)
    print(f"💾 Saved: {path}")
    return path

def read_file(filename):
    try:
        with open(f"{WORKSPACE}/{filename}") as f:
            return f.read()
    except: return "File not found"

def list_files():
    ensure()
    files = os.listdir(WORKSPACE)
    return files if files else []

print("📁 File System loaded!")
