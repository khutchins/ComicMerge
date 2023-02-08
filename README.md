# ComicMerge [Fork]

## Description

This is a simple tool that allows you to merge multiple .cbz files into a single .cbz file.

## Usage
```
usage: python comicmerge_cmd.py [-h] [-v] [-p PREFIX] [-r start end] OUTPUT_FILE

Merge multiple cbz files into one.

positional arguments:
	OUTPUT_FILE           Name of the .cbz file to be created

optional arguments:
	-h, --help            show this help message and exit
	-v, --verbose         More information as to the merging progress
	-p PREFIX, --prefix PREFIX
						Prefix to restrict comics to
	-r start end, --range start end
						Specified by the format X Y. Only the Xth to Yth comic
						in the folder will be merged into the output file.
						Counting starts at 1. The range is inclusive.
```

This script will probably work on Linux, Mac, and Windows, but it has only been tested on Windows.

## Features of this fork
- also works without providing either range or prefix (merges all comics in folder)

## TODO
- [ ] select input folder
- [x] work without range for all in folder
- [ ] don't flatten flag
- [ ] progress bar
- [ ] flag to delete comics afterwards
- [ ] create my fork
- [ ] don't rely on windows-specific os stuff like the 1 fork did
- [ ] after these are done put them into #features or whatever

## License

This project is licensed under the BSD license. For more information, check out LICENSE.md.
