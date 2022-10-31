import hashlib


class SHA:

    description = "Set of methods for constructing different hashes or checksums for files"

    def __init__(self, filename):
        self.filename = filename

        # print(filename)

    def sha256(self):

        sha256_hash = hashlib.sha256()

        with open(self.filename, "rb") as f:

            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

            sha256sum = sha256_hash.hexdigest()

        return sha256sum

    def sha256_quoted(self):

        sha256sum = f'"{self.sha256()}"'

        return sha256sum

    def sha256_vault(self):

        etx_path = "s3://etx-dmp-vault/object/"
        sha256sum = str(self.sha256())
        sha256sum_path = "/".join((sha256sum[0:2], sha256sum[2:4], sha256sum[4:8], sha256sum[8:16], sha256sum[16:]))
        vault_path = f'{etx_path}{sha256sum_path}'

        return vault_path
