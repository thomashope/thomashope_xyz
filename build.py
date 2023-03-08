#!/usr/bin/python3
import os
import glob
import markdown
import subprocess
import shutil

src_dir = 'src'
dest_dir = 'public'
header = open(os.path.join(src_dir, 'res', 'header.template')).read()
footer = open(os.path.join(src_dir, 'res', 'footer.template')).read()

md = markdown.Markdown(extensions=['fenced_code', 'meta', 'tables', 'footnotes'])

def print_warning(str):
	print('\033[93m' + 'WARNING: ' + str + '\033[0m')

def create_dirs(dirpath):
	if not os.path.exists(dirpath):
		os.makedirs(dirpath)

def run_cmd(args):
	result = subprocess.run(args, stdout=subprocess.PIPE)
	return result.stdout.decode('utf-8')

def mirror_files_with_extensions(exts):
	for ext in exts:
		mirror_files(os.path.join('**', '*.' + ext))

def mirror_files(globpath):
	globpath = os.path.join(src_dir, globpath)
	print('mirroring files', globpath)
	for path in glob.iglob(globpath, recursive=True):
		destination = os.path.join(dest_dir, path[len(src_dir)+1:])
		create_dirs(os.path.split(destination)[0])
		print('copying', path, destination)
		shutil.copy(path, destination)

def build_markdown_files():
	globpath = os.path.join(src_dir, "**", "*.md")
	print('mirroring files', globpath)

	for path in glob.iglob(globpath, recursive=True):
		with open(path, 'r') as file:
			raw = file.read();
			html = md.convert(raw)

		title = 'Thomas Hope'
		if 'title' in md.Meta:
			title = md.Meta['title'][0]

		description = ' '
		if 'description' in md.Meta:
			description = md.Meta['description'][0]

		image_path = '/res/diving.jpg'
		if 'image' in md.Meta:
			image_path = md.Meta['image'][0]

		max_description_length = 120
		if len(description) > max_description_length:
			print_warning('Description should be kept under ' + str(max_description_length) + ' characters! Length is ' + str(len(description)))

		site_path = os.path.splitext(path[len(src_dir)+1:])[0] + '.html'
		destination = os.path.join(dest_dir, site_path)
		date_edited = run_cmd(['git','log','-1','--pretty="%aD"', path]).strip(' \n"')
		git_history_link = 'https://github.com/thomashope/thomashope_xyz/commits/main/' + path
		create_dirs(os.path.split(destination)[0])

		url = 'https://thomashope.xyz/' + site_path

		with open(destination, 'w') as file:
			file.write(header
				.replace('$$TITLE$$', title)
				.replace('$$DESCRIPTION$$', description)
				.replace('$$URL$$', url)
				.replace('$$IMAGE$$', image_path))
			file.write(html)
			file.write(footer
				.replace('$$DATE_EDITED$$', date_edited)
				.replace('$$GIT_HISTORY_LINK$$', git_history_link))

		md.reset()

def main():
	print('Starting build...')
	create_dirs(dest_dir)
	mirror_files_with_extensions(['html', 'css', 'jpg', 'jpeg', 'png', 'webm', 'mp4', 'ico', 'svg', 'webmanifest'])
	build_markdown_files()
	print('Done!')

if __name__ == '__main__':
	main()