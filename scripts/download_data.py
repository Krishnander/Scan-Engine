import requests
import hashlib
import tarfile
import os
from tqdm import tqdm

def download_ember_dataset(data_dir="data"):
    """
    Downloads and extracts the EMBER 2018 dataset.
    """
    url = "https://ember.elastic.co/ember_dataset_2018_2.tar.bz2"
    filename = "ember_dataset_2018_2.tar.bz2"
    expected_sha256 = "b6052eb8d350a49a8d5a5396fbe7d16cf42848b86ff969b77464434cf2997812"
    filepath = os.path.join(data_dir, filename)
    ember_2018_dir = os.path.join(data_dir, "ember2018")

    if os.path.exists(ember_2018_dir):
        print("EMBER 2018 dataset already found. Skipping download.")
        return

    os.makedirs(data_dir, exist_ok=True)

    print(f"Downloading {filename}...")
    try:
        # Download the file with a progress bar
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(filepath, 'wb') as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()

        if total_size != 0 and progress_bar.n != total_size:
            print("ERROR, something went wrong during download")
            return

        print("Download complete. Verifying SHA256 hash...")
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        calculated_sha256 = sha256_hash.hexdigest()
        print(f"Expected SHA256: {expected_sha256}")
        print(f"Calculated SHA256: {calculated_sha256}")

        if calculated_sha256 != expected_sha256:
            print("SHA256 hash mismatch. Deleting downloaded file.")
            os.remove(filepath)
            raise ValueError("SHA256 hash mismatch!")

        print("Hash verified. Extracting data...")
        with tarfile.open(filepath, "r:bz2") as tar:
            tar.extractall(path=data_dir)

        print("Extraction complete.")

    finally:
        # Clean up the downloaded tarball
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Removed {filepath}.")

if __name__ == "__main__":
    download_ember_dataset()
