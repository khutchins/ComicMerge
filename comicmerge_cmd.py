import argparse
import sys
from ComicMerge import ComicMerge

parser = argparse.ArgumentParser(prog='ComicMerge', description='Merge multiple cbz files into one.')
parser.add_argument('-v', '--verbose', action='store_true', help='More information as to the merging progress')
parser.add_argument('output_name', metavar='OUTPUT_FILE', type=str,
					help='Name of the .cbz file to be created. Will automatically append .cbz if necessary.')
parser.add_argument('-p', '--prefix', type=str, help='Prefix to restrict comics to')
parser.add_argument('-r', '--range', nargs=2, metavar=('start', 'end'), type=int,
					help='Specified by the format X Y. Only the Xth to Yth comic in the folder will be merged into the '
						 'output file.')
parser.add_argument('-f', '--folders', action='store_true', help='Don\'t flatten the directory tree, keep subfolders')
args = parser.parse_args()

if args.prefix is not None: # prefix is king
	comics_to_merge = ComicMerge.comics_from_prefix(args.prefix)
elif args.range is not None: # fallback to range
	if (len(args.range)) == 0:
		comics_to_merge = ComicMerge.comics_from_indices(0, -1)
	else:
		comics_to_merge = ComicMerge.comics_from_indices(args.range[0], args.range[1])
elif args.range is None: # no range = all comics in folder
	comics_to_merge = ComicMerge.comics_in_folder()
else:
	raise "ran out of options for comic input: no range, no prefix, no comics in folder apparently."
	
comic_merge = ComicMerge(args.output_name, comics_to_merge, args.verbose, args.folders)
comic_merge.merge()
