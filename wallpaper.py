from urllib.request import urlopen, urlretrieve
from json import loads
from random import randint
from time import sleep
from os.path import join, expanduser, isfile, exists
from os import makedirs
from subprocess import call
from sys import stdout
import subprocess

IMAGE_DIR = ''

class Wallpaper:
    def __init__(self):
        self.full_url = None

    def get_wallpaper_from_wsg(self):
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
            post = randint(0, post-1)

            while True:

                # makes sure the post we have has an image
                if 'ext' in posts[post]:
                    self.extension = str(posts[post]['ext'])

                    # this better not be a gif or webm..
                    if self.extension in ['.jpg', '.png', 'jpeg']:

                        # TODO implement another filter to filter nsfw
                        self.filename = str(posts[post]['tim'])
                        self.full_url = 'http://i.4cdn.org/wg/' + filename + extension
                        print('Found file from /wg/ @: ' + full_url)
                        return

                    else:
                        print('Not a correct extension of this image.. ext={}'.format(extension))
                        sleep(1)
                else:
                    print('No file in this post..')
                    sleep(1)

        # why does 4chan time me out?
        except Exception as e:
            print('Could not connect to /wsg/..', e)
            sleep(1)

    def save():
        try:
            # output file path
            self.file_path = Wallpaper.get_wallpaper_path(self.filename + self.extension)
            # put the image in the directory specified
            response = urlretrieve(self.full_url, self.file_path)

        except Exception as e:
            print('could not save wallpaper path={} e={}'.format(e))

    def set():
        try:
            if isfile(self.file_path):
                subprocess.call(
                        ['feh', '--bg-fill', self.file_path])
        except Exception as e:
            print('could not set wallpaper with feh path={} e={}'.format(self.file_path, e))

    @staticmethod
    def _get_wallpaper_path(file_name):
        """
        ensures saving path for the file is good
        """
        try:
            if '' != IMAGE_DIR.strip():
                dir = IMAGE_DIR
            else:
                dir = join(expanduser("~"), 'Downloads/wallpapers')

            if not exists(dir):
                makedirs(dir)

            file_path = join(dir, file_name)
            return file_path
        except Exception as e:
            print('could not get wallpaper path={} e={}'.format(file_path, e))
