#!/usr/bin/python3
import os
import glob
import markdown
import subprocess

src_dir = 'src'
md = markdown.Markdown(extensions=['fenced_code'])

def create_dirs(dirpath):
	if not os.path.exists(dirpath):
		os.makedirs(dirpath)

def run_cmd(args):
	result = subprocess.run(args, stdout=subprocess.PIPE)
	return result.stdout.decode('utf-8')

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
		date_edited = run_cmd(['git','log','-1','--pretty="%aD"', path]).strip(' \n"')
		git_history_link = 'https://github.com/thomashope/thomashope_xyz/commits/main/' + path
		create_dirs(os.path.split(destination)[0])
		print('copying', path, date_edited, destination)

		with open(destination, 'w') as file:
			file.write(header)
			file.write(html)
			file.write(footer.replace('$$DATE_EDITED$$', date_edited).replace('$$GIT_HISTORY_LINK$$', git_history_link))

def main():
	print('Starting build...')
	create_dirs('public')
	mirror_files(os.path.join('**', '*.html'))
	mirror_files(os.path.join('**', '*.css'))
	build_markdown_files()
	print('Done!')

if __name__ == '__main__':
	main()