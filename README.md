# listRename.py
```
listRename.py: Renames files based on a list of new names.

Takes a newline separated list of names and applies them to files in a directory

Usage:
python listRename.py [--option] <working directory> <name list>

Options:
-h --help                  Show this screen.
-e --extension <extension> Apply rename to given extensions only. Can be used multiple times.
-s --sort <sort method>    Sort method to apply to files to be renamed [Default: name].
                               Supported options: "name". :(
-n --names                 <name list> contains names of files to apply rename to. Format: <source file>,<new name>
-S --simulate              Simulates rename operations and prints expected outcome.
```
