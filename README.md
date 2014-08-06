# ComicMerge

## Description

This is a simple tool that allows you to merge multiple .cbz files into a single .cbz file.

## Usage

    usage: comicmerge_cmd.py [-h] [-v] [-r start end] OUTPUT_FILE
    
    Merge multiple cbz files into one.
    
    positional arguments:
      OUTPUT_FILE           Name of the .cbz file to be created
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         More information as to the merging progress
      -r start end, --range start end
                            Specified by the format X-Y. Only the Xth to Yth comic
                            in the folder will be merged into the output file. If
                            multiple ranges are specified, OUTPUT_FILE will take
                            the format OUTPUT_FILE-1, OUTPUT_FILE-2...`

This script will ostensibly work on Linux, Mac, and Windows, but it has only been tested on Windows.

## License

This project is licensed under the BSD license. For more information, check out LICENSE.md.
