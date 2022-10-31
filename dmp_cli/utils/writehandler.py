import os


def write_manifest_stdout(manifest_list):

    for m in manifest_list:
        print(f'{m[0]}\t{m[1]}')

    return None


def write_manifest_file(manifest_list, outfile="manifest.txt"):

    cwd = os.path.abspath(os.getcwd())

    with open(outfile, "w") as f:
        for m in manifest_list:
            f.write(f'{m[0]}\t"{m[1]}"\n')

    print(f'\nManifest results written to {cwd}/{outfile}')

    return None



