import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import json

# --- Function for Step 1.1: File Chunking ---
def chunk_file(file_path, chunk_size=1024*1024):
    """
    Splits a file into smaller, fixed-size chunks.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return []
    
    chunk_dir = f"{os.path.basename(file_path)}_chunks"
    if not os.path.exists(chunk_dir):
        os.makedirs(chunk_dir)

    chunks = []
    chunk_num = 0
    with open(file_path, 'rb') as f:
        while True:
            chunk_data = f.read(chunk_size)
            if not chunk_data:
                break
            chunk_num += 1
            chunk_file_path = os.path.join(chunk_dir, f"chunk_{chunk_num}")
            with open(chunk_file_path, 'wb') as chunk_f:
                chunk_f.write(chunk_data)
            chunks.append(chunk_file_path)
    
    print(f"Successfully split '{file_path}' into {len(chunks)} chunks.")
    return chunks

# --- Function for Step 1.2: Symmetric Encryption ---
def encrypt_chunk(chunk_path, key):
    """
    Encrypts a file chunk using AES-256.
    """
    try:
        nonce = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        
        with open(chunk_path, 'rb') as f_in:
            data = f_in.read()
            
        ciphertext, tag = cipher.encrypt_and_digest(data)
            
        with open(chunk_path, 'wb') as f_out:
            f_out.write(nonce)
            f_out.write(tag)
            f_out.write(ciphertext)
            
        print(f"Successfully encrypted {chunk_path}")
        return True
    except Exception as e:
        print(f"Error encrypting {chunk_path}: {e}")
        return False

# --- Function for Step 1.3: Metadata Generation ---
def generate_metadata(original_file_path, chunk_file_paths, key):
    """
    Generates a JSON metadata file with encryption key and chunk hashes.
    """
    metadata = {
        "original_file_name": os.path.basename(original_file_path),
        "original_file_size": os.path.getsize(original_file_path),
        "total_chunks": len(chunk_file_paths),
        "encryption_key": key.hex(),
        "chunk_hashes": []
    }
    
    for chunk_path in chunk_file_paths:
        with open(chunk_path, 'rb') as f:
            chunk_data = f.read()
            file_hash = hashlib.sha256(chunk_data).hexdigest()
            metadata["chunk_hashes"].append(file_hash)
            
    metadata_file_path = os.path.join(os.path.dirname(chunk_file_paths[0]), "metadata.json")
    with open(metadata_file_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Metadata file created at: {metadata_file_path}")
    return metadata_file_path

# ------------------------------------------------------------------
# --- Main Script ---
# ------------------------------------------------------------------

# ⬇️ ⬇️ ⬇️ This is the only line you need to change. ⬇️ ⬇️ ⬇️
your_file_path = r"D:\Pictures\english-cocker-spaniel-5937757_640.jpg"

# Step 1: Chunk the file
chunk_file_paths = chunk_file(your_file_path)

# If chunking was successful, proceed to encrypt and generate metadata
if chunk_file_paths:
    # Step 2: Generate a key
    encryption_key = get_random_bytes(32)
    
    # Step 3: Encrypt all the chunks
    for chunk_path in chunk_file_paths:
        encrypt_chunk(chunk_path, encryption_key)
    
    # Step 4: Generate the metadata file
    metadata_file = generate_metadata(your_file_path, chunk_file_paths, encryption_key)

    print("\nProcess completed successfully! 🎉")
    print(f"The original key is: {encryption_key.hex()}")
    print(f"The metadata file is stored in the '{os.path.basename(your_file_path)}_chunks' folder.")
    print("This key will be stored in a smart contract in the next step of the challenge.")