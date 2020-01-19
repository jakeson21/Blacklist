import tarfile
from os import makedirs, path, remove
from pathlib import Path
import re
import urllib.parse


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=path.basename(source_dir))


def dump_to_domains(in_path, out_path):
    # Create target directory & all intermediate directories if don't exists
    out_dir_name = out_path.parent.absolute()
    if not path.exists(out_dir_name):
        makedirs(out_dir_name)
        print("Directory ", out_dir_name, " created")
    else:
        print("Directory ", out_dir_name, " already exists")

    in_file = open(in_path, 'r')
    out_file = open(out_path, 'a+')
    for line in in_file:
        line = line.rstrip()
        if re.search('^0\.0\.0\.0', line):
            line = line.split()
            line = line[1]
            line = line.replace('..', '.')
            # These don't work in SquidGuard
            if re.search('_', line):
                continue
            out_file.write(line + ' ')
    print('Finished processing', in_path)


try:
    remove('BL/domains')
except FileNotFoundError:
    print('file does not exist yet')
# Process the input files
dump_to_domains(Path('pornhosts/0.0.0.0/hosts'), Path('BL/domains'))
dump_to_domains(Path('pornhosts/Mobile 0.0.0.0/hosts'), Path('BL/domains'))

# try:
#     remove('my-blacklist.tar.gz')
# except FileNotFoundError:
#     print('file does not exist yet')
# make_tarfile('my-blacklist.tar.gz', Path('archive/pornhosts/BL'))
# print('Created', 'my-blacklist.tar.gz')
