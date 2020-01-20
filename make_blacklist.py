import tarfile
from os import makedirs, path, remove
from pathlib import Path
import re
import urllib.parse


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=path.basename(source_dir))


def copy_to_dict(in_path):
    in_file = open(in_path, 'r')
    data = dict()
    for line in in_file:
        line = line.rstrip()
        if re.search('^0\.0\.0\.0', line):
            line = line.split()
            line = line[1]
            line = line.replace('..', '.')
            # These don't work in SquidGuard
            if re.search('_', line):
                continue
            data[line] = True
    print('Finished processing', in_path)
    return data


def dict_to_file(data, out_path):
    # Create target directory & all intermediate directories if don't exists
    out_dir_name = out_path.parent.absolute()
    if not path.exists(out_dir_name):
        makedirs(out_dir_name)
        print("Directory ", out_dir_name, " created")
    else:
        print("Directory ", out_dir_name, " already exists")

    out_file = open(out_path, 'a+')
    for key in data:
        out_file.write(key + ' ')
    print('Finished writing to', out_path)


try:
    remove('BL/domains')
except FileNotFoundError:
    print('file does not exist yet')
# Process the input files
d1 = copy_to_dict(Path('pornhosts/0.0.0.0/hosts'))
d2 = copy_to_dict(Path('pornhosts/Mobile 0.0.0.0/hosts'))
# Dictionary unpacking method of merging dicts
data = {**d1, **d2}
dict_to_file(data, Path('BL/domains'))

# try:
#     remove('my-blacklist.tar.gz')
# except FileNotFoundError:
#     print('file does not exist yet')
# make_tarfile('my-blacklist.tar.gz', Path('archive/pornhosts/BL'))
# print('Created', 'my-blacklist.tar.gz')
