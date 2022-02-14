#!/usr/bin/python3
import os
import glob
import markdown

def create_dir(dirpath):
	if not os.path.exists(dirpath):
		os.mkdir(dirpath)

def mirror_src_files(globpath):	
	globpath = os.path.join('src', globpath)
	print('copying files', globpath)
	for path in glob.iglob(globpath):
		with open(path, 'r') as file:
			raw = file.read();
		
		file_name = os.path.basename(path)
		destination = os.path.join('public', file_name)
		print('copying', path, destination)

		with open(destination, 'w') as file:
			file.write(raw)

def mirror_markdown_files():
	header = open(os.path.join('src', 'header.template')).read()
	footer = open(os.path.join('src', 'footer.template')).read()
	globpath = os.path.join('src', '*.md')
	print('copying files', globpath)
	for path in glob.iglob(globpath):
		with open(path, 'r') as file:
			raw = file.read();
			html = markdown.markdown(raw)
		
		file_name = os.path.basename(path)
		destination = os.path.join('public', os.path.splitext(file_name)[0] + '.html')
		print('copying', path, destination)

		with open(destination, 'w') as file:
			file.write(header)
			file.write(html)
			file.write(footer)

def main():
	print('Starting build...')
	create_dir('public')
	mirror_src_files('*.html')
	mirror_src_files('*.css')
	mirror_markdown_files()
	print('Done!')

if __name__ == '__main__':
	main()