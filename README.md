# ComicMerge [Fork]

## Description

This is a simple tool that allows you to merge multiple .cbz files into a single .cbz file.

## Usage
```
usage: ComicMerge [-h] [-v] [-p PREFIX] [-r start end] [-f] OUTPUT_FILE

Merge multiple cbz files into one.

positional arguments:
  OUTPUT_FILE       Name of the .cbz file to be created. Will automatically append .cbz if necessary.

options:
  -h, --help        show this help message and exit
  -v, --verbose     More information as to the merging progress
  -p PREFIX, --prefix PREFIX
                    Prefix to restrict comics to
  -r start end, --range start end
                    Specified by the format X Y. Only the Xth to Yth comic in the folder will be merged into the output file.
  -f, --folders     Don't flatten the directory tree, keep subfolders
```
## Features of this fork
- also works without providing either range or prefix (merges all comics in folder)
- `-f`/`--folders` flag, outputs a cbz with internally separated chapters by folders
- proper information about merging progress in stdout
  
### notes:
- This script will probably work on Linux, Mac, and Windows, but it has only been tested on Windows.
- The `-f`/`--folders` flag was tested on PockedBook Touch Lux 4, it does create chapters internally in it's reader



## TODO
- [ ] select input folder
- [ ] cleanup flag: delete comics afterwards
- [x] work without range for all in folder
- [x] don't flatten flag
- [x] progress bar

## License

This project is licensed under the BSD license. For more information, check out LICENSE.md.
