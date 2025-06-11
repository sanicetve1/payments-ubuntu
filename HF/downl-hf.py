# download_banking77_model.py

from huggingface_hub import snapshot_download
import os

# ✅ Configure model name and target directory
model_id = "mrm8488/bert-tiny-finetuned-banking77"
local_dir = "./HF/banking77"

if not os.path.exists(local_dir):
    print(f"⬇️ Downloading model '{model_id}' to '{local_dir}'...")
    snapshot_download(repo_id=model_id, local_dir=local_dir, local_dir_use_symlinks=False)
    print("✅ Download complete.")
else:
    print(f"✅ Model already downloaded at '{local_dir}'")
