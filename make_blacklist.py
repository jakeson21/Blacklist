import tarfile
from os import makedirs, path
from pathlib import Path
import re


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
    out_file = open(out_path, 'w+')
    for line in in_file:
        line = line.rstrip()
        if re.search('^0.0.0.0', line):
            line = line.split()
            # print(line[1])
            out_file.write(line[1] + '\n')
    print('Finished processing', in_path)


# Process the input files
host_paths = dict()
host_paths['hosts'] = Path('pornhosts/0.0.0.0/hosts')
host_paths['mobile-hosts'] = Path('pornhosts/Mobile 0.0.0.0/hosts')

dump_to_domains(host_paths['hosts'], Path('archive/pornhosts/BL/porn/domains'))
dump_to_domains(host_paths['mobile-hosts'], Path('archive/pornhosts/BL/mobile-porn/domains'))

make_tarfile('my-blacklist.tar.gz', Path('archive/pornhosts/BL'))
print('Created', 'my-blacklist.tar.gz')
