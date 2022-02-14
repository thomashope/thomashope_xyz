#!/usr/bin/python3
import os
import glob
import markdown

src_dir = 'src'
md = markdown.Markdown(extensions=['fenced_code'])

def create_dirs(dirpath):
	if not os.path.exists(dirpath):
		os.makedirs(dirpath)

def mirror_files(globpath):
	globpath = os.path.join(src_dir, globpath)
	print('mirroring files', globpath)
	for path in glob.iglob(globpath, recursive=True):
		with open(path, 'r') as file:
			raw = file.read();

		destination = os.path.join('public', path[len(src_dir)+1:])
		create_dirs(os.path.split(destination)[0])
		print('copying', path, destination)

		with open(destination, 'w') as file:
			file.write(raw)

def build_markdown_files():
	globpath = os.path.join(src_dir, "**", "*.md")
	print('mirroring files', globpath)

	header = open(os.path.join('src', 'header.template')).read()
	footer = open(os.path.join('src', 'footer.template')).read()

	for path in glob.iglob(globpath, recursive=True):
		with open(path, 'r') as file:
			raw = file.read();
			html = md.convert(raw)

		destination = os.path.join('public', os.path.splitext(path[len(src_dir)+1:])[0] + '.html')
		create_dirs(os.path.split(destination)[0])
		print('copying', path, destination)

		with open(destination, 'w') as file:
			file.write(header)
			file.write(html)
			file.write(footer)

def main():
	print('Starting build...')
	create_dirs('public')
	mirror_files(os.path.join('**', '*.html'))
	mirror_files(os.path.join('**', '*.css'))
	build_markdown_files()
	print('Done!')

if __name__ == '__main__':
	main()