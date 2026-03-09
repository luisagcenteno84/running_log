from __future__ import annotations

import hashlib
import hmac
import os

PBKDF2_ALGORITHM = 'sha256'
PBKDF2_ITERATIONS = 390000
SALT_BYTES = 16


def hash_password(password: str) -> str:
    """Hash a password with PBKDF2-HMAC using a per-password salt."""
    salt = os.urandom(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode('utf-8'),
        salt,
        PBKDF2_ITERATIONS,
    )
    return f'pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}'


def verify_password(password: str, encoded_password: str | None) -> bool:
    """Verify a plain-text password against the stored encoded hash."""
    if not encoded_password:
        return False

    try:
        scheme, iterations, salt_hex, digest_hex = encoded_password.split('$', 3)
    except ValueError:
        return False

    if scheme != 'pbkdf2_sha256':
        return False

    derived = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode('utf-8'),
        bytes.fromhex(salt_hex),
        int(iterations),
    )
    return hmac.compare_digest(derived.hex(), digest_hex)
