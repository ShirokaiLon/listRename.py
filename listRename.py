#!/usr/bin/python

import sys
import getopt
from os import listdir, access, rename, R_OK, F_OK
from os.path import isfile, isdir, join, samefile

# args
workingdir = ''
namelist = ''
sortby = ''
simulate = False
hasnames = False
extensions = []


def main(argv):
    # Parse arguments
    getArgs(argv)
    # Enumerate files to operate on
    files, newnames = enumerateFiles()
    # Select files with given extensions (if applicable)
    if extensions:
        files, newnames = filterExtensions(files, newnames)
    # Verify number of files = names in list
    if not hasnames and len(files) != len(newnames):
        print('Number of files in directory and name list not equal')
        sys.exit()
    # Sort files
    if hasnames:
        files.sort()
    # Apply renaming on files
    applyRename(files, newnames)


def getArgs(argv):
    global workingdir
    global namelist
    global sortby
    global simulate
    global hasnames
    global extensions

    try:
        opts, args = getopt.getopt(argv, "he:s:nS",
            ["--help", "--extension=", "--sort=", "--names=", "--simulate"])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printHelp()
            sys.exit()
        elif opt in ("-e", "--extension"):
            extensions.append(arg)
        elif opt in ("-s", "--sort"):
            if hasnames != '':
                print('Error: -s in conjunction with -f not supported')
                print('')
                sys.exit()
            sortby = arg
        elif opt in ("-n", "--names"):
            if sortby != '':
                print('Error: -s in conjunction with -n not supported')
                print('')
                sys.exit()
            hasnames = True
        elif opt in ("-S", "--simulate"):
            simulate = True
    if len(args) != 2:
        printHelp()
        sys.exit()
    else:
        workingdir = args[0]
        namelist = args[1]
        if not isdir(workingdir):
            print(workingdir, 'is not a directory.')
            sys.exit()
        if not access(namelist, R_OK):
            print('Cannot access name list ', namelist)
            sys.exit()


def parseFile(file):
    try:
        return [line.rstrip('\n') for line in open(file)]
    except IOError:
        print("Could not read file: ", file)
        sys.exit(2)


def enumerateFiles():
    files = []
    newnames = []

    lines = parseFile(namelist)

    for line in lines:
        splitline = line.split(",")
        if hasnames:
            if len(splitline) != 2:
                print('Error: Invalid input file format')
                sys.exit()

            files.append(splitline[0].strip())
            newnames.append(splitline[1].strip())

            if not access(join(workingdir, files[len(files) - 1]), F_OK):
                print('Error: Cannot access file', files[len(files) - 1], "from given file list")
                sys.exit()
        else:
            if len(splitline) != 1:
                print('Error: Invalid input file format')
                sys.exit()

            files = [f for f in listdir(workingdir) if not samefile(join(workingdir, f), namelist)
                     and isfile(join(workingdir, f))]
            newnames = [name.strip() for name in lines]

    return files, newnames


def filterExtensions(files, newnames):
    if hasnames:
        tempfiles = []
        tempnames = []
        for i in range(len(files)):
            if files[i].endswith(tuple(extensions)):
                tempfiles.append(files[i])
                tempnames.append(newnames[i])
        files = tempfiles
        newnames = tempnames
    else:
        files = [file for file in files if file.endswith(tuple(extensions))]

    return files, newnames


def applyRename(files, newnames):
    for i in range(len(files)):
        if simulate:
            print(join(workingdir, files[i]), ' -> ', join(workingdir, newnames[i]))
        else:
            try:
                rename(join(workingdir, files[i]), join(workingdir, newnames[i]))
            except OSError:
                print('Error renaming file', files[i])


def printHelp():
    print('listRename.py: Renames files based on a list of new names.')
    print('')
    print('Takes a newline separated list of names and applies them to files in a directory')
    print('')
    print('Usage:')
    print('python listRename.py [options] <working directory> <name list>')
    print('')
    print('Options:')
    print('-h --help                  Show this screen.')
    print('-e --extension <extension> Apply rename to given extensions only. Can be used multiple times.')
    print('-s --sort <sort method>    Sort method to apply to files to be renamed [default: name].')
    print('                               Supported options: "name". :(')
    print('-n --names                 <name list> contains names of files to apply rename to. Format: <source file>,<new name>')
    print('-S --simulate              Simulates rename operations and prints expected outcome.')
    print('')


main(sys.argv[1:])
