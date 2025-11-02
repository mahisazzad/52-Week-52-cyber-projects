import os
import hashlib
import json

# === CONFIGURATION ===
FILE_PATH = r"C:\Users\mahis\OneDrive\Desktop\52cyber projects\Week3 file intregrity checker\sample_files\simple.txt"
BASELINE_FILE = "baseline_hashes.json"

# === CORE FUNCTIONS ===
def calc_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def save_baseline(file_path, hash_value):
    baseline = {file_path: hash_value}
    with open(BASELINE_FILE, 'w') as f:
        json.dump(baseline, f, indent=2)
    print("✅ Baseline saved.")

def check_integrity(file_path):
    if not os.path.exists(BASELINE_FILE):
        print("❌ Baseline file missing.")
        return

    with open(BASELINE_FILE, 'r') as f:
        baseline = json.load(f)

    old_hash = baseline.get(file_path)
    if old_hash is None:
        print("⚠️ File not found in baseline.")
        return

    current_hash = calc_sha256(file_path)
    print(f"🔍 Comparing hashes...")
    print(f"Old: {old_hash}")
    print(f"New: {current_hash}")

    if current_hash != old_hash:
        print(f"❗ Integrity violation detected!")
    else:
        print(f"✅ File verified. No changes detected.")

# === TESTER FUNCTIONS ===
def tamper_file(file_path):
    with open(file_path, 'a') as f:
        f.write("\n# Tampered content\n")
    print("✏️ File tampered.")

def restore_file(file_path, original_content):
    with open(file_path, 'w') as f:
        f.write(original_content)
    print("🔄 File restored.")

# === MAIN EXECUTION ===
if __name__ == '__main__':
    print("📁 Starting file integrity test...")

    # Step 1: Read original content
    with open(FILE_PATH, 'r') as f:
        original = f.read()

    # Step 2: Generate baseline
    original_hash = calc_sha256(FILE_PATH)
    save_baseline(FILE_PATH, original_hash)

    # Step 3: Tamper the file
    tamper_file(FILE_PATH)

    # Step 4: Check integrity
    check_integrity(FILE_PATH)

    # Step 5: Restore original content
    restore_file(FILE_PATH, original)

    # Step 6: Recheck integrity
    check_integrity(FILE_PATH)

    print("✅ Test complete.")