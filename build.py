#!/usr/bin/python3
import os
import glob
import markdown
import subprocess
import shutil
import re

src_dir = 'src'
dest_dir = 'public'
publish_domain = 'https://thope.xyz'
page_template = open(os.path.join(src_dir, 'res', 'template.html')).read()

md = markdown.Markdown(extensions=['fenced_code', 'meta', 'tables', 'footnotes', 'toc', 'admonition'])

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

def get_page_data(meta_data, path):
	title = meta_data.get('title', ['Thomas Hope'])[0]
	description = meta_data.get('description', [''])[0]
	image_path = meta_data.get('image', ['/res/diving.jpg'])[0]
	date = meta_data.get('date', ['YYYY-MM-DD'])[0]
	published = meta_data.get('published', [''])[0].lower() == 'true'
	featured = meta_data.get('featured', [''])[0].lower() == 'true'
	series = meta_data.get('series', [''])[0].lower()
	date_edited = get_date_edited(path)
	git_history_link = get_git_history_link(path)

	if len(description) > 120:
		print_warning(f'Description should be kept under 120 characters! Length is {len(description)}')

	return {
		'title': title,
		'description': description,
		'image_path': image_path,
		'date': date,
		'published': published,
		'featured': featured,
		'series': series,
		'date_edited': date_edited,
		'git_history_link': git_history_link,
	}

def get_date_edited(path):
	return run_cmd(['git','log','-1','--pretty="%aD"', path]).strip(' \n"')

def get_git_history_link(path):
	return 'https://github.com/thomashope/thomashope_xyz/commits/main/' + path

def insert_page_data(text, page_data):
	return text \
		.replace('$$TITLE$$', page_data['title']) \
		.replace('$$DESCRIPTION$$', page_data['description']) \
		.replace('$$IMAGE$$', publish_domain + page_data['image_path']) \
		.replace('$$DATE_EDITED$$', page_data['date_edited']) \
		.replace('$$GIT_HISTORY_LINK$$', page_data['git_history_link'])

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

		page_data = get_page_data(md.Meta, path)

		if not page_data['published']:
			continue

		site_path = os.path.splitext(path[len(src_dir)+1:])[0] + '.html'

		pages.append([site_path, page_data, html])

		md.reset()

 	# Sort pages by date, assuming ISO format: YYYY-MM-DD
	pages = sorted(pages, key=lambda p: p[1]['date'], reverse=True)

	for site_path, page_data, page_html in pages:
		series_info = create_series_info(page_data['series'], site_path)
		destination = os.path.join(dest_dir, site_path)
		create_dirs(os.path.split(destination)[0])
		with open(destination, 'w') as file:
			file.write(insert_page_data(page_template, page_data)
				.replace('$$URL$$', publish_domain + '/' + site_path)
				.replace('$$CONTENT$$', page_html + series_info))

def create_series_info(series, this_site_path):
	if not series:
		return ''
	entries = []
	for site_path, page_data, html in pages:
		if page_data['series'] == series:
			entries.append([site_path, page_data['title']])
	entries.reverse() # pages are sorted newest first, but we want entries sorted oldest first
	html = f'<div class="series-footer">\n<p>This page is part of the series \'{series}\'. Check out the other entries in the series below.</p>\n<ol>\n'
	for site_path, title in entries:
		html += f'<li><a href="/{site_path}">{title}</a> {" <- you are here" if site_path == this_site_path else ""}</li>'
	html += '</ol></div>\n'
	return html

def create_pages_list(pages):
	items = []
	for site_path, page_data, html in pages:
		title = page_data['title']
		date = page_data['date']
		series = page_data['series']
		item_html = f'<time>{date}</time><a href="/{site_path}">{title}</a>'
		if series:
			item_html = f'{item_html}<small>{series}</small>'
		item_html = f'<li>{item_html}</li>'
		items.append(item_html)
	return '<ul style="list-style: none; padding: 0;">\n' + '\n'.join(items) + '\n</ul>'

def build_archive():
	published_pages_html_list = create_pages_list(pages)
	
	src_path = os.path.join(src_dir, 'archive', 'index.md')
	archive_md = open(src_path).read()
	archive_md = archive_md.replace('$$PUBLISHED_PAGES_LIST$$', published_pages_html_list)
	html = md.convert(archive_md)

	page_data = get_page_data(md.Meta, src_path)
	date_edited = get_date_edited(src_path)
	git_history_link = get_git_history_link(src_path)
	html = insert_page_data(page_template, page_data) \
		.replace('$$URL$$', publish_domain + '/archive') \
		.replace('$$CONTENT$$', html)

	destination = os.path.join(dest_dir, 'archive', 'index.html')
	create_dirs(os.path.split(destination)[0])

	with open(destination, 'w') as file:
		file.write(html)

def build_homepage():
	featured_pages_html_list = create_pages_list([page for page in pages if page[1]['featured']])
	
	src_path = os.path.join(src_dir, 'index.md')
	homepage_md = open(src_path).read()
	homepage_md = homepage_md.replace('$$FEATURED_PAGES_LIST$$', featured_pages_html_list)
	html = md.convert(homepage_md)

	page_data = get_page_data(md.Meta, src_path)
	date_edited = get_date_edited(src_path)
	git_history_link = get_git_history_link(src_path)
	html = insert_page_data(page_template, page_data) \
		.replace('$$URL$$', publish_domain) \
		.replace('$$CONTENT$$', html)

	with open(os.path.join(dest_dir, 'index.html'), 'w') as file:
		file.write(html)

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