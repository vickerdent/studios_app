from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Also print the public key in URL-safe base64 format (useful for web push)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import base64

# Generate private key
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

# Generate public key
public_key = private_key.public_key()

# Save private key to PEM file
with open("aprivate_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Save public key to PEM file
with open("apublic_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("✓ Keys generated successfully!")
print("  - private_key.pem")
print("  - public_key.pem")


public_key_bytes = public_key.public_bytes(
    encoding=Encoding.X962,
    format=PublicFormat.UncompressedPoint
)
public_key_b64 = base64.urlsafe_b64encode(public_key_bytes).strip(b'=').decode('utf-8')

print(f"\nPublic key (URL-safe base64):\n{public_key_b64}")
