"""Check the SSH signatures of the Phase 1G tags against their embedded keys.

Evidence script of reports/phase1g_h_freeze_status_successor.md, Sec. 2.1.
It reimplements the SSHSIG check (PROTOCOL.sshsig of OpenSSH) because
`ssh-keygen` was not installed in the session that wrote the record. It
needs the third-party `cryptography` package (not a project dependency).

For each tag it extracts the signed payload and the signature from the tag
object, verifies the Ed25519 signature against the public key embedded in
the signature, and prints that key's fingerprint. It also checks that a
one-byte change of the payload is rejected.

This shows that each tag object is unaltered since it was signed and which
key signed it. It does not show whose key that is: binding the key to the
owner needs the owner's allowed-signers file (`git tag -v`).

Usage, from the repository root:
    python3 reports/phase1g_h_freeze_status_successor_logs/verify_tag_ssh_signatures.py
"""
import base64
import hashlib
import json
import struct
import subprocess

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

TAGS = [
    "phase-1g-a-sigma8-derivation-path-v1",
    "phase-1g-b-lagrangian-sigma-v1",
    "phase-1g-c-two-scale-growth-law-v1",
    "phase-1g-d-separate-universe-growth-v1",
    "phase-1g-e-two-phase-sigma-v1",
    "phase-1g-f-void-population-v1",
    "phase-1g-g-void-evolution-v1",
    "phase-1g-h-global-variance-closure-v1",
]
BEGIN = b"-----BEGIN SSH SIGNATURE-----"


def read_string(buf, offset):
    (n,) = struct.unpack(">I", buf[offset:offset + 4])
    return buf[offset + 4:offset + 4 + n], offset + 4 + n


def ssh_string(data):
    return struct.pack(">I", len(data)) + data


def check(tag):
    raw = subprocess.run(["git", "cat-file", "tag", tag], check=True,
                         capture_output=True).stdout
    start = raw.index(BEGIN)
    payload, armored = raw[:start], raw[start:]
    blob = base64.b64decode(b"".join(armored.strip().splitlines()[1:-1]))
    if blob[:6] != b"SSHSIG":
        raise ValueError(f"{tag}: not an SSHSIG blob")
    (version,) = struct.unpack(">I", blob[6:10])
    public_key, offset = read_string(blob, 10)
    namespace, offset = read_string(blob, offset)
    reserved, offset = read_string(blob, offset)
    hash_alg, offset = read_string(blob, offset)
    signature, offset = read_string(blob, offset)
    key_type, key_offset = read_string(public_key, 0)
    raw_key, _ = read_string(public_key, key_offset)
    sig_type, sig_offset = read_string(signature, 0)
    raw_sig, _ = read_string(signature, sig_offset)
    if key_type != b"ssh-ed25519" or sig_type != b"ssh-ed25519":
        raise ValueError(f"{tag}: unsupported key or signature type")
    if hash_alg not in (b"sha256", b"sha512"):
        raise ValueError(f"{tag}: unsupported hash {hash_alg!r}")

    def signed_data(message):
        digest = hashlib.new(hash_alg.decode(), message).digest()
        return (b"SSHSIG" + ssh_string(namespace) + ssh_string(reserved)
                + ssh_string(hash_alg) + ssh_string(digest))

    verifier = Ed25519PublicKey.from_public_bytes(raw_key)
    verifier.verify(raw_sig, signed_data(payload))  # raises if invalid
    tampered = bytearray(payload)
    tampered[0] ^= 1
    try:
        verifier.verify(raw_sig, signed_data(bytes(tampered)))
        tamper_rejected = False
    except InvalidSignature:
        tamper_rejected = True
    fingerprint = base64.b64encode(hashlib.sha256(public_key).digest())
    return {
        "tag": tag,
        "tag_object": subprocess.run(["git", "rev-parse", tag], check=True,
                                     capture_output=True, text=True).stdout.strip(),
        "target_commit": subprocess.run(["git", "rev-parse", tag + "^{commit}"],
                                        check=True, capture_output=True,
                                        text=True).stdout.strip(),
        "sshsig_version": version,
        "namespace": namespace.decode(),
        "hash": hash_alg.decode(),
        "key_type": key_type.decode(),
        "key_fingerprint": "SHA256:" + fingerprint.decode().rstrip("="),
        "signature_valid_for_embedded_key": True,
        "one_byte_payload_change_rejected": tamper_rejected,
    }


if __name__ == "__main__":
    results = [check(tag) for tag in TAGS]
    print(json.dumps({
        "results": results,
        "same_key_for_all": len({r["key_fingerprint"] for r in results}) == 1,
    }, indent=1))
