import os
import shutil
import zipfile
import re


class ComicMerge:
    def __init__(self, output_name, comics_to_merge, is_verbose=True):
        self.output_name = output_name
        if not self.output_name.endswith(".cbz"):
            self.output_name = self.output_name + ".cbz"
        self.comics_to_merge = comics_to_merge
        self.is_verbose = is_verbose

    def _log(self, msg):
        self._log_static(msg, self.is_verbose)

    @staticmethod
    def _log_static(msg, verbose):
        if verbose:
            print(msg)

    @staticmethod
    def _extract_cbz(file_name, destination, verbose):
        output_dir = os.path.join(destination, os.path.splitext(file_name)[0])
        os.mkdir(output_dir)
        ComicMerge._log_static('Unzipping ' + file_name, verbose)
        zip_file = zipfile.ZipFile(file_name)
        zip_file.extractall(output_dir)
        zip_file.close()

    @staticmethod
    def _remove_file(file_name):
        if os.path.exists(file_name):
            os.remove(file_name)

    @staticmethod
    def _find_temp_folder():
        base_dir = 'temp_merge'
        mod = 0
        temp_dir = base_dir
        while os.path.exists(temp_dir):
            mod += 1
            temp_dir = base_dir + str(mod)
        return temp_dir

    @staticmethod
    def _extract_comics(comics_to_extract, temp_dir, verbose):
        for file_name in comics_to_extract:
            ComicMerge._extract_cbz(file_name, temp_dir, verbose)

        # Flatten file structure (subdirectories mess with some readers)
        files_moved = 1
        for path_to_dir, subdir_names, file_names in os.walk(temp_dir, True):
            for subdir_name in ComicMerge.natsorted(subdir_names):
                for path_to_dir2, subdir_names2, file_names2 in os.walk(f"{temp_dir}/{subdir_name}"):
                    for file_name in file_names2:
                        file_path = os.path.join(path_to_dir2, file_name)
                        ext = os.path.splitext(file_name)[1]
                        new_name = 'P' + str(files_moved).rjust(5, '0') + ext
                        ComicMerge._log_static('Renaming & moving ' + file_name + ' to ' + new_name, verbose)
                        shutil.copy(file_path, os.path.join(temp_dir, new_name))
                        files_moved += 1

            # Deletes all subdirectories (in the end we want a flat structure)
            # This will not affect walking through the rest of the directories,
            # because it is traversed from the bottom up instead of top down
            for subdir_name in subdir_names:
                shutil.rmtree(os.path.join(path_to_dir, subdir_name))

    def _make_cbz_from_dir(self, temp_dir):
        self._log('Initializing cbz ' + self.output_name)

        zip_file = zipfile.ZipFile(self.output_name, 'w', zipfile.ZIP_DEFLATED)
        self._log('Adding files to cbz ' + self.output_name)
        add_count = 0
        for path_to_dir, subdir_names, file_names in os.walk(temp_dir):
            for file_name in file_names:
                file_path = os.path.join(path_to_dir, file_name)
                zip_file.write(file_path, os.path.split(file_path)[1])
                add_count += 1
                if add_count % 10 == 0:
                    self._log(str(add_count) + ' files added.')

    @staticmethod
    # Passing in a start_idx of <= 0 will cause it to start at the beginning of the folder
    # Passing in an end_idx of < 0 will cause it to end at the end of the folder
    # Both start_idx and end_idx are inclusive
    # Index count starts at 1
    def comics_from_indices(start_idx, end_idx):
        all_comics = ComicMerge.comics_in_folder()
        comics = []
        comic_idx = 1
        for file_name in all_comics:
            if start_idx <= comic_idx and (comic_idx <= end_idx or end_idx < 0):
                comics.append(file_name)
            comic_idx += 1
        return comics

    @staticmethod
    def comics_from_prefix(prefix):
        all_comics = ComicMerge.comics_in_folder()
        comics = []
        for file_name in all_comics:
            if file_name.startswith(prefix):
                comics.append(file_name)
        return comics

    @staticmethod
    def comics_in_folder():
        comics = []
        for file_name in os.listdir('.'):  # We're not traversing subdirectories because that's a boondoggle
            if os.path.splitext(file_name)[1] == '.cbz':
                comics.append(file_name)
        return comics

    @staticmethod
    def natsorted(l):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key=alphanum_key)
    
    def merge(self):
        # Remove existing file, if any (we're going to overwrite it anyway)
        self._remove_file(self.output_name)

        self._log('Merging comics ' + str(self.comics_to_merge) + ' into file ' + self.output_name)

        # Find and create temporary directory
        # (we don't want to use a static one, no need to mess with something extant)
        temp_dir = self._find_temp_folder()
        os.mkdir(temp_dir)

        self._extract_comics(self.comics_to_merge, temp_dir, self.is_verbose)
        self._make_cbz_from_dir(temp_dir)

        # Clean up temporary folder
        shutil.rmtree(temp_dir)
        self._log('')
        print('Successfully merged comics into ' + self.output_name + '!')
