import subprocess
import os
import json

def download_chunk(cid, output_dir):
    """
    Downloads a single chunk from IPFS to the specified folder using the local IPFS gateway.
    """
    filename = f"{cid}.chunk"
    output_path = os.path.join(output_dir, filename)
    result = subprocess.run(
        ["ipfs", "get", "-o", output_path, cid],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"Downloaded {cid} -> {output_path}")
        return output_path
    else:
        print(f"Error downloading {cid}: {result.stderr}")
        return None

def reconstruct_file(chunks_paths, output_file):
    """
    Reassembles all chunks into a single file.
    """
    with open(output_file, "wb") as f_out:
        for chunk_path in chunks_paths:
            with open(chunk_path, "rb") as f_in:
                f_out.write(f_in.read())
    print(f"\nOriginal file reconstructed: {output_file}")

# =========================
# Main process
# =========================
if _name_ == "_main_":
    # Folder where chunks and metadata.json are stored
    chunks_dir = r"D:\python_for_hackthon\english-cocker-spaniel-5937757_640.jpg_chunks"
    
    # Metadata file path
    metadata_path = os.path.join(chunks_dir, "metadata.json")
    
    # Output reconstructed file path
    output_file = os.path.join(chunks_dir, "reconstructed_file.jpg")  # adjust extension if needed

    # Step 1: Load CIDs from metadata.json
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    
    cids_list = metadata.get("ipfs_cids", [])
    if not cids_list:
        print("No CIDs found in metadata.json")
        exit()

    # Step 2: Download all chunks
    downloaded_paths = []
    for cid in cids_list:
        path = download_chunk(cid, chunks_dir)
        if path:
            downloaded_paths.append(path)

    # Step 3: Reconstruct original file
    if downloaded_paths:
        reconstruct_file(downloaded_paths, output_file)