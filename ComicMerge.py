import os
import shutil
import zipfile


class ComicMerge:
	def __init__(self, output_name, start_idx, end_idx, is_verbose=True):
		self.output_name = output_name
		self.start_idx = start_idx
		self.end_idx = end_idx
		self.is_verbose = is_verbose

	def _log(self, msg):
		if self.is_verbose:
			print(msg)

	def _extract_cbz(self, file_name, destination):
		output_dir = os.path.join(destination, os.path.splitext(file_name)[0])
		os.mkdir(output_dir)
		self._log('Unzipping ' + file_name)
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

	def _extract_comics(self, temp_dir):
		comic_idx = 1
		for file_name in os.listdir('.'): # We're not traversing subdirectories because that's a boondoggle
			if os.path.splitext(file_name)[1] == '.cbz':
				# If end_idx is -1, we want it all comics in one super-file,
				# so extract EVERYTHING (that's an accepted file format)
				if self.start_idx <= comic_idx <= self.end_idx or self.end_idx == -1:
					self._extract_cbz(file_name, temp_dir)
				comic_idx += 1

		# Flatten file structure (subdirectories mess with some readers)
		files_moved = 1
		for path_to_dir, subdir_names, file_names in os.walk(temp_dir,False):
			for file_name in file_names:
				file_path = os.path.join(path_to_dir,file_name)
				ext = os.path.splitext(file_name)[1]
				new_name = 'P' + str(files_moved).rjust(5, '0') + ext
				self._log('Renaming & moving ' + file_name + ' to ' + new_name)
				shutil.copy(file_path, os.path.join(temp_dir,new_name))
				files_moved += 1

			# Deletes all subdirectories (in the end we want a flat structure)
			# This will not effect walking through the rest of the directories,
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
				if(add_count % 10 == 0):
					self._log(str(add_count) + ' files added.')

	def merge(self):
		# Remove existing file, if any (we're going to overwrite it anyway)
		self._remove_file(self.output_name)

		self._log('Merging comics ' + str(self.start_idx) + '-' + str(self.end_idx) + ' into file ' + self.output_name)

		# Find and create temporary directory
		# (we don't want to use a static one, no need to mess with something extant)
		temp_dir = self._find_temp_folder()
		os.mkdir(temp_dir)

		self._extract_comics(temp_dir)
		self._make_cbz_from_dir(temp_dir)

		# Clean up temporary folder
		shutil.rmtree(temp_dir)
		self._log('')
		print('Successfully merged comics into '+self.output_name+'!')
