from dmp_cli.dmp.checksums import SHA
from dmp_cli.utils.filehandler import get_file_contents
from dmp_cli.aws.s3 import S3I

# TODO add typing and docstrings

class manifest:

    description = 'Manifest'

    def __init__(self, infile):
        self.infile = infile

    def create(self):

        checksum = SHA(filename=self.infile)
        sha256 = checksum.sha256()

        return sha256, self.infile

    def check(self):

        print(f'--- Performing checks on manifest file: {self.infile} ---\n')
        lines = get_file_contents(file_name=self.infile)
        mismatch_count = 0
        for line in lines:
            line = line.strip().split("\t")  # split on tab delimitation
            stored_file = line[1].strip('"')  # remove quotes from filename
            stored_sha = line[0]

            try:
                with open(stored_file, 'r') as sf:
                    checksum = SHA(filename=str(sf.name))
                    calculated_sha = checksum.sha256()

                    if calculated_sha == stored_sha:
                        print(f'{sf.name}:\tOK')
                    else:
                        mismatch_count += 1
                        print(f'{sf.name}:\tX')  # {stored_sha} to {calculated_sha}

            except FileNotFoundError:  # catch all missing files
                print(f'{stored_file}:\tMISSING FILE')

        if mismatch_count > 0:
            print(f'\nWARNING: Mismatched ID count X = {mismatch_count}')

        return None


class s3_vault:

        description = 'S3 Data Account Vault'

        def __init__(self, session, infile, bucket, key, all):
            self.session = session
            self.infile = infile
            self.bucket = bucket
            self.key = key
            self.all = all

        def archive(self):
            vault_result = manifest(infile=self.infile).vault()
            unvaulted_list = vault_result[0]
            print(unvaulted_list[1])

            if all == True:

                vaulted_list = vault_result[1]
                print(vaulted_list)
                print(f'\nAll file(s) uploaded to: s3://{self.bucket}/{self.key}/')
            else:
                print(f'\nUnvaulted file(s) uploaded to: s3://{self.bucket}/{self.key}/')

            if len(unvaulted_list) > 0:  # check empty list
                for uf in unvaulted_list:
                    self.session.upload_file_to_bucket(bucket=self.bucket, file_path=uf, key=f'{self.key}/{uf}')

            if len(vaulted_list) > 0:  # check empty list
                for uf in vaulted_list:
                    self.session.upload_file_to_bucket(bucket=self.bucket, file_path=uf, key=f'{self.key}/{uf}')









