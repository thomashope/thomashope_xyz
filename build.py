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

def get_page_data(meta_data):
	title = meta_data.get('title', ['Thomas Hope'])[0]
	description = meta_data.get('description', [''])[0]
	image_path = meta_data.get('image', ['/res/diving.jpg'])[0]
	date = meta_data.get('date', ['YYYY-MM-DD'])[0]
	published = meta_data.get('published', [''])[0].lower() == 'true'
	featured = meta_data.get('featured', [''])[0].lower() == 'true'

	if len(description) > 120:
		print_warning(f'Description should be kept under 120 characters! Length is {len(description)}')

	return {
		'title': title,
		'description': description,
		'image_path': image_path,
		'date': date,
		'published': published,
		'featured': featured,
	}

def get_date_edited(path):
	return run_cmd(['git','log','-1','--pretty="%aD"', path]).strip(' \n"')

def get_git_history_link(path):
	return 'https://github.com/thomashope/thomashope_xyz/commits/main/' + path

def insert_page_data(text, page_data):
	return text \
		.replace('$$TITLE$$', page_data['title']) \
		.replace('$$DESCRIPTION$$', page_data['description']) \
		.replace('$$IMAGE$$', page_data['image_path'])

def build_markdown_files():
	globpath = os.path.join(src_dir, "**", "*.md")
	print('mirroring files', globpath)

	global pages

	for path in glob.iglob(globpath, recursive=True):
		with open(path, 'r') as file:
			text = file.read()
			matches = re.findall('\\$\\$.+\\$\\$', text) # find $$macros$$
			for match in matches:
				macro = match.strip('$)').split('(', 1) # split macro into ['name', 'args']
				text = text.replace(match, get_macro_expansion(macro))
			html = md.convert(text)

		page_data = get_page_data(md.Meta)

		if not page_data['published']:
			continue

		site_path = os.path.splitext(path[len(src_dir)+1:])[0] + '.html'
		destination = os.path.join(dest_dir, site_path)
		date_edited = get_date_edited(path)
		git_history_link = get_git_history_link(path)
		create_dirs(os.path.split(destination)[0])

		url = 'https://thomashope.xyz/' + site_path

		pages.append([page_data['date'], site_path, page_data['title'], page_data])

		with open(destination, 'w') as file:
			file.write(insert_page_data(page_template, page_data)
				.replace('$$URL$$', url)
				.replace('$$CONTENT$$', html)
				.replace('$$DATE_EDITED$$', date_edited)
				.replace('$$GIT_HISTORY_LINK$$', git_history_link))

		md.reset()

 	# Sort pages by date, assuming ISO format: YYYY-MM-DD
	pages = sorted(pages, key=lambda p: p[0], reverse=True)

def create_pages_list(pages):
	items = []
	for date, site_path, title, page_data in pages:
		item_html = f'<li><time>{date}</time><a href="../{site_path}">{title}</a></li>'
		items.append(item_html)
	return '<ul style="list-style: none; padding: 0;">\n' + '\n'.join(items) + '\n</ul>'

def build_archive():
	published_pages_html_list = create_pages_list(pages)
	
	src_path = os.path.join(src_dir, 'archive', 'index.md')
	archive_md = open(src_path).read()
	archive_md = archive_md.replace('$$PUBLISHED_PAGES_LIST$$', published_pages_html_list)
	archive_html = md.convert(archive_md)

	page_data = get_page_data(md.Meta)
	date_edited = get_date_edited(src_path)
	git_history_link = get_git_history_link(src_path)
	url = 'https://thomashope.xyz/archive'
	archive_html = insert_page_data(page_template, page_data) \
		.replace('$$URL$$', url) \
		.replace('$$CONTENT$$', archive_html) \
		.replace('$$DATE_EDITED$$', date_edited) \
		.replace('$$GIT_HISTORY_LINK$$', git_history_link)

	destination = os.path.join(dest_dir, 'archive', 'index.html')
	create_dirs(os.path.split(destination)[0])

	with open(destination, 'w') as file:
		file.write(archive_html)

def build_homepage():
	featured_pages_html_list = create_pages_list([page for page in pages if page[3]['featured']])
	
	src_path = os.path.join(src_dir, 'index.md')
	homepage_md = open(src_path).read()
	homepage_md = homepage_md.replace('$$FEATURED_PAGES_LIST$$', featured_pages_html_list)
	homepage_html = md.convert(homepage_md)

	page_data = get_page_data(md.Meta)
	date_edited = get_date_edited(src_path)
	git_history_link = get_git_history_link(src_path)
	url = 'https://thomashope.xyz/archive'
	homepage_html = insert_page_data(page_template, page_data) \
		.replace('$$URL$$', url) \
		.replace('$$CONTENT$$', homepage_html) \
		.replace('$$DATE_EDITED$$', date_edited) \
		.replace('$$GIT_HISTORY_LINK$$', git_history_link)

	with open(os.path.join(dest_dir, 'index.html'), 'w') as file:
		file.write(homepage_html)

def main():
	print('Starting build...')
	create_dirs(dest_dir)
	mirror_files_with_extensions(['html', 'css', 'jpg', 'jpeg', 'png', 'webm', 'mp4', 'ico', 'svg', 'webmanifest'])
	build_markdown_files()
	build_archive()
	build_homepage()
	print('Done!')

if __name__ == '__main__':
	main()