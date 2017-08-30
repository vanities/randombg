from urllib.request import urlopen, urlretrieve
from json import loads
from random import randint
from time import sleep
from os.path import join, expanduser, isfile, exists
from os import makedirs

SCRIPT = """/usr/bin/osascript<<END 
tell application "Finder" 
set desktop picture to POSIX file "%s" 
end tell 
END"""

# Or you can set your own custom directory
IMAGE_DIR = ''

def main():
	get_wallpaper()

def get_wallpaper_path(file_name):
	if '' != IMAGE_DIR.strip():
		dir = IMAGE_DIR
	else:
		dir = join(expanduser("~"), 'Pictures/wallpapers')

	if not exists(dir):
		makedirs(dir)

	file_path = join(dir, file_name)
	return file_path

			
def get_wallpaper():
	page = str(randint(0,9))
	thread = randint(0,14)
	post = 0

	with urlopen('https://a.4cdn.org/wg/' + page + '.json') as url:
		json = loads(url.read().decode())

		thread = json['threads'][thread]
		posts = thread['posts']

		for p in posts:
			post += 1

		post = randint(0,post-1)
		
		if 'ext' in posts[post]:
			extension = str(posts[post]['ext'])
			print('Found file from /wg/ @: ' + extension)

			if extension == '.jpg' or extension == '.png':
				filename = str(posts[post]['tim'])
				full_url = 'http://i.4cdn.org/wg/' + filename + extension
				print(full_url)
				file_path = get_wallpaper_path(filename + extension)

				response = urlretrieve(full_url,file_path)
				set_wallpaper(file_path)
		else:
			print('No file in this post..')
			sleep(1)
			main()

'''
ONLY SETS WALLPAPER FOR ONE DESKTOP AKA USELESS
GOING TO USE THE BUILT IN SHIT FOR MAC TO CHANGE THE DESKTOP
def set_wallpaper(file_path):
	if isfile(file_path):
		import subprocess
		subprocess.Popen(SCRIPT%file_path, shell=True)
		print('Wallpaper set to ' + file_path)
'''
if __name__ == "__main__":
	main()