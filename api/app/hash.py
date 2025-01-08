import hashlib

# r = hashlib.sha256(b"### passw0rd ###").hexdigest()

def hash_password(raw_string: str) -> str:
    return hashlib.sha256(raw_string.encode()).hexdigest()


