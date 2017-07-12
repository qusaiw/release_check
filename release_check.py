#!/slowfs/us01dwt2p106/char_sw_chute/tools/bin/python3
"""
Automatic test for released cells
"""
import helper as hp
import argparse
import os
from glob import glob
MODELS_FOLDER = 'char/sis/models'


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=__doc__)
parser.add_argument('paths', nargs='+', help="path1 path2 path3 ....")
args = parser.parse_args()


def main():
    out_folder = hp.create_folder('Release_check')
    main_log = open(os.path.join(out_folder, 'Main.log'), 'w+')

    for library in args.paths:
        while library[-1] == '/':
            library = library[:-1]
        individual_log = open(os.path.join(out_folder, library.split('')), 'w+')

        if not os.path.isdir(library):
            individual_log.write('Folder not found\nFAIL')
            individual_log.close()
            main_log.write("{} folder doesn't exist: Fail")
            # Skip because folder doesn't exist
            continue
        messages = []

        # counts lib, db and aocv files
        lib_count = hp.count_files(os.path.join(MODELS_FOLDER, '*/.lib'))
        db_count = hp.count_files(os.path.join(MODELS_FOLDER, '*/.db'))
        aocv_count = hp.count_files(os.path.join(MODELS_FOLDER, '*/.aocv'))

        # checks if all dbs are newer than their lib counterparts
        lib_files = glob(os.path.join(MODELS_FOLDER, '*/.lib'))
        db_files = glob(os.path.join(MODELS_FOLDER, '*/.lib'))
        for db in db_files:
            for lib in lib_files:
                if lib.replace('.lib', '.db') == db:
                    if os.path.getatime(lib) < os.path.getatime():
                        messages.append('Error lib is newer than db for {}'.format(lib))
                    break


if __name__ == '__main__':
    main()