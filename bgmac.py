from urllib.request import urlopen, urlretrieve
from json import loads
from random import randint
from time import sleep
from os.path import join, expanduser, isfile, exists
from os import makedirs
from subprocess import call
from sys import stdout

# OSA script used for mac
SCRIPT = """/usr/bin/osascript<<END 
tell application "Finder" 
set desktop picture to POSIX file "%s" 
end tell 
END"""

# custom directory
IMAGE_DIR = ''

def main():
	# get that shit!
	get_wallpaper()

# assures the path for the file is good
def get_wallpaper_path(file_name):
	if '' != IMAGE_DIR.strip():
		dir = IMAGE_DIR
	else:
		dir = join(expanduser("~"), 'Pictures/wallpapers')

	if not exists(dir):
		makedirs(dir)

	file_path = join(dir, file_name)
	return file_path

# uses the 4chan api to get an image from /wg/			
def get_wallpaper():

	# random page & thread
	page = str(randint(0,9))
	thread = randint(0,14)
	post = 0

	# make sure we recieve the object from the api
	try:
		with urlopen('https://a.4cdn.org/wg/' + page + '.json') as url:
			json = loads(url.read().decode())

			# set the thread and post
			thread = json['threads'][thread]
			posts = thread['posts']

			# count the # of posts in thread
			for p in posts:
				post += 1

			# random number post
			post = randint(0,post-1)
			
			# makes sure the post we have has an image
			if 'ext' in posts[post]:
				extension = str(posts[post]['ext'])

				# this better not be a gif or webm..
				if extension == '.jpg' or extension == '.png' or extension == 'jpeg':

					# TODO implement another filter to filter nsfw
					filename = str(posts[post]['tim'])
					full_url = 'http://i.4cdn.org/wg/' + filename + extension
					print('Found file from /wg/ @: ' + full_url)
					
					# output file path
					file_path = get_wallpaper_path(filename + extension)
					
					# put the image in the directory specified
					response = urlretrieve(full_url,file_path)
					
					# set the wallpaper
					set_wallpaper(file_path)
			else:
				print('No file in this post..')
				sleep(1)	# api rule
				main()
	# why does 4chan time me out?
	except (HTTPError):
		print('Could not connect to /wsg/..')
		sleep(1)	 # api rule
		main()

# script for setting the wallpaper
def script(code):
	return call(
		['bash', '-c', code],
		shell=False,
		stdin=None,
		stdout=stdout,
		stderr=stdout)


# sets the wallpaper using sqlite3 db
def set_wallpaper(file_path):
	if isfile(file_path):
	# See http://superuser.com/a/689804.
		assert \
			script('''
			sqlite3 ~/Library/Application\ Support/Dock/desktoppicture.db "update data set value = '%(file)s'"
			killall Dock
			''' % {
			'file': file_path,
			}) == 0, \
			'Failed to set wallpaper'
		print('Wallpaper set to ' + file_path)

if __name__ == "__main__":
	main()