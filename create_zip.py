import os
import sys
import zipfile
from pathlib import Path

def create_project_zip():
    project_dir = Path(__file__).resolve().parent
    parent_dir = project_dir.parent
    output_zip = parent_dir / "SentinelAI_MajorProject_Complete.zip"
    
    print("=" * 65)
    print("      SENTINELAI MAJOR PROJECT - ZIP GENERATOR")
    print("=" * 65)
    print(f"Source Folder : {project_dir}")
    print(f"Destination   : {output_zip}\n")
    print("Zipping all folders and files (excluding caches & git metadata)...")
    
    # Folders/files to exclude to keep zip clean and lightweight
    exclude_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', '.env_dir', '.idea', '.vscode'}
    exclude_exts = {'.pyc', '.pyo', '.tmp'}

    count = 0
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in exclude_exts):
                    continue
                file_path = Path(root) / file
                arcname = file_path.relative_to(project_dir)
                try:
                    zipf.write(file_path, arcname)
                    count += 1
                except Exception as e:
                    print(f"Skipping {arcname}: {e}")
                    
    print(f"\n[SUCCESS] Successfully packaged {count} files!")
    print(f"[ZIP FILE PATH]: {output_zip}")
    print("=" * 65)

if __name__ == "__main__":
    create_project_zip()
