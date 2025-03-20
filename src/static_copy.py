
import os
import shutil

def directory_clear(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)

def directory_copy(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Directory does not exist: {src_dir}")
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    src_items = os.listdir(src_dir)
    for item in src_items:
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_dir)
            print("copied:", item, "src:", src_path, "dest:", dest_path)
        else:
            directory_copy(src_path, dest_path)
