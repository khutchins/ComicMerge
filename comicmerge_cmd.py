import argparse
import sys
from ComicMerge import ComicMerge

parser = argparse.ArgumentParser(prog='ComicMerge', description='Merge multiple cbz files into one.')
parser.add_argument('-v', '--verbose', action='store_true', help='More information as to the merging progress')
parser.add_argument('output_name', metavar='OUTPUT_FILE', type=str,
                    help='Name of the .cbz file to be created')
parser.add_argument('-r', '--range', nargs=2, metavar=('start', 'end'), type=int,
                    help='Specified by the format X-Y. Only the Xth to Yth comic in the folder will be merged into the '
                         'output file. If multiple ranges are specified, OUTPUT_FILE will take the format '
                         'OUTPUT_FILE-1, OUTPUT_FILE-2...')
args = parser.parse_args()

if(len(args.range)) == 0:
	comic_merge = ComicMerge(args.output_name,-1,-1,args.verbose)
else:
	comic_merge = ComicMerge(args.output_name,args.range[0],args.range[1],args.verbose)
comic_merge.merge()