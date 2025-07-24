import hashlib

exe_path = 'dist/AdobeRenewalTool/AdobeRenewalTool.exe'

with open(exe_path, 'rb') as f:
    bytes = f.read()
    hash = hashlib.sha256(bytes).hexdigest()

print(f"SHA256: {hash}")