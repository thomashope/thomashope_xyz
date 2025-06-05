#!/usr/bin/python3
import os
import glob
import markdown
import subprocess
import shutil
import re

src_dir = 'src'
dest_dir = 'public'
page_template = open(os.path.join(src_dir, 'res', 'template.html')).read()

md = markdown.Markdown(extensions=['fenced_code', 'meta', 'tables', 'footnotes'])

pages = []

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

def get_macro_expansion(macro):
	if macro[0] == 'AUTOPLAY_VIDEO':
		# argument is the path to a video file. This requires that
		snippet = '<video autoplay loop muted playsinline disableRemotePlayback x-webkit-airplay="deny" disablePictureInPicture><source src="$$FILE$$.webm" type="video/webm" /><source src="$$FILE$$.mp4" type="video/mp4"/></video>'
		file_no_ext = os.path.splitext(macro[1])[0]
		return snippet.replace('$$FILE$$', file_no_ext)
	return '<!-- ERROR EXPANDING MACRO ' + str(macro) + '-->'

def build_markdown_files():
	globpath = os.path.join(src_dir, "**", "*.md")
	print('mirroring files', globpath)

	for path in glob.iglob(globpath, recursive=True):
		with open(path, 'r') as file:
			text = file.read()
			matches = re.findall('\\$\\$.+\\$\\$', text) # find $$macros$$
			for match in matches:
				macro = match.strip('$)').split('(', 1) # split macro into ['name', 'args']
				text = text.replace(match, get_macro_expansion(macro))
			html = md.convert(text)

		if 'published' not in md.Meta or md.Meta['published'][0].lower() != 'true':
			continue

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

		date = 'YYYY-MM-DD'
		if 'date' in md.Meta:
			date = md.Meta['date'][0]

		site_path = os.path.splitext(path[len(src_dir)+1:])[0] + '.html'
		destination = os.path.join(dest_dir, site_path)
		date_edited = run_cmd(['git','log','-1','--pretty="%aD"', path]).strip(' \n"')
		git_history_link = 'https://github.com/thomashope/thomashope_xyz/commits/main/' + path
		create_dirs(os.path.split(destination)[0])

		url = 'https://thomashope.xyz/' + site_path

		pages.append([date, site_path, title])		

		with open(destination, 'w') as file:
			file.write(page_template
				.replace('$$TITLE$$', title)
				.replace('$$DESCRIPTION$$', description)
				.replace('$$URL$$', url)
				.replace('$$IMAGE$$', image_path)
				.replace('$$CONTENT$$', html)
				.replace('$$DATE_EDITED$$', date_edited)
				.replace('$$GIT_HISTORY_LINK$$', git_history_link))

		md.reset()

def build_archive():
	# Sort pages by date descending (assuming ISO format: YYYY-MM-DD)
	sorted_pages = sorted(pages, key=lambda p: p[0], reverse=True)

	items = []
	for date, site_path, title in sorted_pages:
		item_html = f'<li><time>{date}</time><a href="../{site_path}">{title}</a></li>'
		items.append(item_html)

	content = '<ul style="list-style: none; padding: 0;">\n' + '\n'.join(items) + '\n</ul>'

	archive_html = page_template \
		.replace('$$TITLE$$', 'Thomas Hope') \
		.replace('$$DESCRIPTION$$', 'Homepage') \
		.replace('$$URL$$', 'https://thomashope.xyz/') \
		.replace('$$IMAGE$$', '/res/diving.jpg') \
		.replace('$$CONTENT$$', content) \
		.replace('$$DATE_EDITED$$', 'TODO: insert date edited') \
		.replace('$$GIT_HISTORY_LINK$$', 'TODO: insert link to file in git')

	destination = os.path.join(dest_dir, 'archive', 'index.html')
	create_dirs(os.path.split(destination)[0])

	with open(destination, 'w') as file:
		file.write(archive_html)

def main():
	print('Starting build...')
	create_dirs(dest_dir)
	mirror_files_with_extensions(['html', 'css', 'jpg', 'jpeg', 'png', 'webm', 'mp4', 'ico', 'svg', 'webmanifest'])
	build_markdown_files()
	build_archive()
	print('Done!')

if __name__ == '__main__':
	main()