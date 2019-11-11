import hashlib
import base64


# So why a sha256 hash?
# Why base64?
# What decode?
def get_soure_code_hash(file_path):
    chunk_size = 8192

    hasher = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk):
                hasher.update(chunk)
            else:
                break

    return base64.b64encode(hasher.digest()).decode("utf-8")
