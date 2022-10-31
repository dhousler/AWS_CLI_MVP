#!/usr/bin/env python3

# external package import
import argparse
import uuid
import os

# internal package imports
from dmp_cli.dmp.manifest import manifest
from dmp_cli.dmp.manifest import s3_vault
from dmp_cli.utils.filehandler import file_handler, directory_handler
from dmp_cli.utils.writehandler import write_manifest_stdout, write_manifest_file
from dmp_cli.aws.s3 import S3I

# TODO work on grouping for each set

""" parse arguments from command line """
parser = argparse.ArgumentParser()
# create manifest
parser.add_argument("-c", "--create", action='store_true')
parser.add_argument("-f", "--files", nargs="+")
parser.add_argument("-d", "--directories", nargs="+")
parser.add_argument("-m", "--manifest", action='store_true')

# validate manifest
parser.add_argument("-k", "--check", action='store_true')
parser.add_argument("-v", "--vault", action='store_true')

# archive files using manifest
parser.add_argument("-x", "--archive", action='store_true')
parser.add_argument("-a", "--all", action='store_true')
parser.add_argument("-b", "--bucket")
parser.add_argument("-p", "--path")

# pull files using manifest
parser.add_argument("-g", "--get", action='store_true')
parser.add_argument("-o", "--outdir")

args = parser.parse_args()

"""Globals"""
# TO DO add to TOML file or inject
REGION = "" # e.g., eu-west-2
SERVICE = "s3"
PROFILE = ""  # e.g., informatics

session = S3I(aws_region=REGION, aws_service=SERVICE, aws_profile=PROFILE)


def main():

    file_list = []  # defines list of files to be written to the manifest
    manifest_list = []  # defines the list with filepath and ID

    """File collection"""
    if args.files:  # takes in all file arguments
        for file in args.files:
            file_list += file_handler(file)

    if args.directories:  # handles directories recursively
        file_list += directory_handler(directory_list=args.directories)

    """----- Manifest as stdout -----"""

    if args.create:

        for f in file_list:
            manifest_list += [manifest(infile=f).create()]

        print('\n--- MANIFEST ---')
        write_manifest_stdout(manifest_list=manifest_list)

    """----- Manifest saved to file -----"""
    if args.manifest:

        outfile = args.manifest
        write_manifest_file(manifest_list=manifest_list, outfile=outfile)

    """Manifest check manifest against local files"""
    if args.check:

        for f in file_list:
            manifest(infile=f).check()

    """Manifest: check manifest against vault"""
    if args.vault:
        for f in file_list:
            manifest(infile=f).vault()

    """Manifest: check manifest against vault"""
    if args.archive:

        """If user provides bucket and path write files to user location else write to dmp-working cleared 7 days"""

        if args.bucket and args.path:
            BUCKET = str(args.bucket)
            KEY = str(args.path.rstrip("/"))
            print(BUCKET)
            print(KEY)
        else:
            BUCKET = "etx-dmp-working"
            KEY = str(uuid.uuid4())[:8]

        for f in file_list:
            s3_vault(session=session, infile=f, bucket=BUCKET, key=KEY, all=args.all)

    """Manifest: pull files in manifest from vault"""
    if args.get:

        BUCKET_NAME = 'etx-dmp-vault'  # replace with your bucket name

        for f in file_list:
            vault = manifest(infile=f).vault()
            vaulted_dict = vault[3]  # 3rd return value is a dict of the vaulted files
            print(vaulted_dict)  # vaulted dict

            for vk in vaulted_dict:  # vk = vault key/dict key, vaule = vaulted_dict[vk]

                # extract the directory path as the filepath
                file_path = os.path.dirname(vaulted_dict[vk])

                if args.outdir:
                    try:
                        os.makedirs(args.outdir)
                    except FileExistsError:
                        pass

                    """The directory structure"""
                    # if there is a file path create it, if it exists pass
                    if file_path != "":
                        # Create a new directory if it doesn't exist
                        try:
                            os.makedirs(f'{args.outdir}/{file_path}')
                        except FileExistsError:
                            pass

                    """download from s3"""
                    session.download_file_from_bucket(bucket=BUCKET_NAME,
                                                      key=vk,
                                                      file_path=f'{args.outdir}/{vaulted_dict[vk]}')
                else:
                    """The directory structure"""
                    # if there is a file path create it, if it exists pass
                    if file_path != "":
                        # Create a new directory if it doesn't exist
                        try:
                            os.makedirs(file_path)
                        except FileExistsError:
                            pass
                    """download from s3"""
                    session.download_file_from_bucket(bucket=BUCKET_NAME,
                                                      key=vk,
                                                      file_path=f'{vaulted_dict[vk]}.m')


if __name__ == "__main__":
    main()