#!/slowfs/us01dwt2p106/char_sw_chute/tools/bin/python3
"""
File containing the helper functions for the realease_check project
"""

import sys
import os
from glob import glob
sys.path.append('/slowfs/us01dwt2p106/char_sw_chute/releases/latest/src/share/py')
import sge


def create_folder(folder_name):
    """
    Creates a folder called folder_name without overwriting anything by incrementing n until folder_name_copy(n)
     is available
    :param folder_name:Name of folder to create
    :return: the name of the output folder
    """
    n = 0
    while os.path.isdir(folder_name):
        folder_name += '_{}'.format(n)
        n += 1
    os.makedirs(folder_name)
    return folder_name


def farm_job(commands, output=None):
    """
    Given a list of cammands or a single command, the function will send each command to the Synopsys farm
    :param commands: accepts a list (list of commands) or a string (one command)
    :param output: the name of the process, if not provided then it's 'Farm_job' by default. Them the function
    'create_folder' will be called with the name to create the folder.
    :return: the name of the folder containing the results of the commands.
    """
    # Enables the function to deal with a single command provided as a string or a list of commands
    commands = [[commands]] if type(commands) is str else [[command] for command in commands]
    output = 'Farm_job' if not output else output
    output = create_folder(output)
    sgeJobs = sge.JOBS('.', 'setup')
    for n, command in enumerate(commands):
        script_name = '{}_{}.csh'.format(output, n)
        cjob = sge.JOB(cmds=command, otherQsubOpts='-A quick',
                       sgeRes='os_version=\!WS4.0,arch=glinux,cputype=amd64|emt64,mem_free=48G,qsc=g|h|i|j|k|l|m',
                       logDir='fast_grep', scriptName=script_name, scriptDir='{}/scripts'.format(output))
        sgeJobs.append(cjob)
    print('Submitting individual jobs to SGE farm \n results will be under {} folder'.format(output))
    l = open('log', 'w+')
    sge.runjobs(l)
    return output


def count_files(files):
    """
    :param files:a wildcard expression or a list of wildcard expressions (list of str)
    :return: the combined count of files found using all the expressions (int)
    """
    count = 0
    files = [files] if type(files) is str else files
    for i in files:
        count += len(glob(i))
    return count


if __name__ == '__main__':
    pass
