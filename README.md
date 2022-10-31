# dmp-cli

This is the dmp-cli 
The aim is to wrap aws cli tools using boto3
This package should be used when using s3, sqs, etc elements rather than re-writing these.

# Currently under development

{TODO}

- define sessions
- define resource
- define client
- add tests
- run as a package
- add documentation
- use in another script/executable

# DMP Manifest

One useful feature for the DMP will be 'manifest' files, which are simply a list of (ID,path) pairs. In fact, they are nothing more than the output of `sha256sum`, run over a number of files:

```
> sha256sum */*.py | tee manifest
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  dmp_cli/__init__.py
08d87841053a95d70749b489c5ff03dc0167a2d826ea24bb0a9f77175d5a7b72  dmp_cli/dmp_backfill.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  dmp_cli/logger.py
6d20b3310487c68d840d8f604efb6be58ee7755292606b01c23a3db1432f928f  dmp_cli/sessions.py
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  tests/__init__.py
32c33979cdfd3d11e90f8adefeb797f463a55dc64a4704ffc014aa216e333a4c  tests/test_to_remove.py
```

Once you have a manifest, one useful thing you can do is to verify that the files match the manifest:

```
> sha256sum --check manifest 
dmp_cli/__init__.py: OK
dmp_cli/dmp_backfill.py: OK
dmp_cli/logger.py: OK
dmp_cli/sessions.py: OK
tests/__init__.py: OK
tests/test_to_remove.py: OK
```

If one of the files in the manifest has a different shasum, or no longer exists, you will get an error.

The DMP CLI can build on this, and do more useful things. Since the DMP CLI will be modular, all the commands should go in a `manifest` Python module, and the general form of each command will be `dmp manifest ...`.

## Creating a manifest

The CLI must support these variations for creating a manifest file:

```
# All files matching the regular expressions
dmp manifest --create *.py *.txt data/*.csv

# All files in the named directories
dmp manifest --create --dir mydir1 --dir mydir2

# Ditto, but recursively
dmp manifest --create --dir mydir --recursive

# Naming the manifest file. Without this, just write to the terminal
dmp manifest --create *.txt --manifest my-manifest.txt
```

### Error handling

  * If no filenames are given, and no directory names are given, report an error
  * If `--recursive` is given but no directory names are given, report an error
  * If the manifest file is given, and it already exists, report an error
  * If the manifest file can't be created, report an error
  * If filenames or directory names are given, but the total number of files found is zero, report an error
  * If any of the input files can't be read, report an error

## Verify files in a manifest exist locally

Verify that the files exist and have the correct checksums (identical to sha256sum)

```
dmp manifest --check --manifest <manifest-file>
```

### Error handling

  * If a file listed in the manifest does not exist on disk, report an error
  * If a file listed in the manifest has a different checksum, count how often that happens, then report that number with an error at the end of the program
  * If the manifest file doesn't exist, or can't be read, report an error
  * If any of the files listed in the manifest can't be read, report an error

## Verify files in a manifest exist in the vault

Use the sha256sums to verify if the files listed in the manifest are archived already or not

```
dmp manifest --vault --manifest <manifest-file>
```

### Error handling

  * If the manifest file doesn't exist, report an error
  * If a file listed in the manifest doesn't exist in the vault, report a warning, not an error

## Archive data listed in a manifest

From the list of files in the manifest, verify that the vault contains a file with the correct sha256sum, and if it doesn't, upload the file to the named S3 bucket.

```
dmp manifest --archive --manifest <manifest-file> [--path s3://bucket/prefix] [--all]
```

The S3 path is optional. If the user doesn't supply one, use a default bucket (any bucket in the Data account with expiration enabled will do) and use the checksum as the key. That will get the file into the vault, and if the user really cared about where it was to go, they should have specified the destination.

The `--all` argument tells the DMP to upload all files, even if they exist in the vault. Useful if the user wants all the files together in S3.

### Error handling

  * If the manifest file doesn't exist, report an error
  * Giving `--all` without `--path` is also an error. If the user wants everything archived together, they should specify where to put it.

## Retrieving data listed in a manifest

The above in reverse. Given a manifest, pull files out of the vault and store them locally, in locations given in the manifest.

```
dmp manifest --fetch --manifest <manifest-file> [--overwrite]
```

### Error handling

  * If the manifest file doesn't exist, you know what to do by now
  * If a file doesn't exist in the vault with a given sha256sum, report an error
  * If a file exists locally with the destination name already, verify that it has the correct sha256sum, and report an error if it doesn't
    * *unless* the user has specified `--overwrite`, in which case you just overwrite the file

## General points

Filenames in the manifest must be enclosed in double quotes, since we have files in S3 or on disk with embedded spaces and other special characters.

Given a sha256sum, the path to the file in the vault can be calculated in Python as follows:

```
sha256sum = "bdc1d21e2ea3f4d48e18fc860f1b7cf71237272e575bd19a754e6b8ccb8c384b"
path = "s3://etx-dmp-vault/object/" + "/".join( ( sha256sum[0:2], sha256sum[2:4], sha256sum[4:8], sha256sum[8:16], sha256sum[16:] ) )
```

E.g. for the sha256sum above, the path is `s3://etx-dmp-vault/object/bd/c1/d21e/2ea3f4d4/8e18fc860f1b7cf71237272e575bd19a754e6b8ccb8c384b`

