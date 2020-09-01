#!/usr/local/bin/python3

from urllib.request import urlopen, urlretrieve
from json import loads
from random import randint
from time import sleep
from os.path import join, expanduser, isfile, exists
from os import makedirs
from subprocess import call
from sys import stdout, platform

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
                if extension in ['.jpg', '.png', 'jpeg']:

                    # TODO implement another filter to filter nsfw
                    filename = str(posts[post]['tim'])
                    full_url = 'http://i.4cdn.org/wg/' + filename + extension
                    print('Found file from /wg/ @: ' + full_url)

                    # output file path
                    file_path = get_wallpaper_path(filename + extension)

                    # put the image in the directory specified
                    response = urlretrieve(full_url,file_path)

            else:
                print('No file in this post..')
                sleep(1)    # api rule
                main()
    # why does 4chan time me out?
    except Exception as e:
        print('Could not connect to /wsg/..', e)
        sleep(1)     # api rule
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
def set_wallpaper(filepath):
    if platform == "darwin":
        from appscript import app, mactypes

        if isfile(filepath):
            app('Finder').desktop_picture.set(mactypes.File(filepath))
            print('Wallpaper set to ' + filepath)
    elif platform == "linux":
        if isfile(file_path):
                subprocess.call(['feh', '--bg-fill', file_path],
                                env=environ.copy())

if __name__ == "__main__":
    main()
