#!/usr/local/bin/python3

from urllib.request import urlopen, urlretrieve
from json import loads
from random import randint
from time import sleep
from os.path import join, expanduser, isfile, exists
from os import makedirs, remove
from subprocess import call
import subprocess
from sys import platform
from nudenet import NudeDetector

# initialize the nude detector once
detector = NudeDetector()


def main():
    # get that shit!
    wallpaper = download_wallpaper()
    set_wallpaper(wallpaper)


# assures the path for the file is good
def get_wallpaper_path(filename):
    directory_path = join(expanduser("~"), "Pictures/wallpapers")

    if not exists(directory_path):
        makedirs(directory_path)

    filepath = join(directory_path, filename)
    return filepath


# uses the 4chan api to get an image from /wg/
# returns the filepath
def download_wallpaper():
    # random page & thread
    page = str(randint(0, 9))
    thread = randint(0, 14)
    post = 0

    # make sure we receive the object from the api
    attempts = 0
    max_attempts = 10
    while attempts < max_attempts:
        try:
            # random page & thread
            page = str(randint(0, 9))
            thread = randint(0, 14)
            with urlopen("https://a.4cdn.org/wg/" + page + ".json") as url:
                json = loads(url.read().decode())

                # set the thread and post
                thread = json["threads"][thread]
                posts = thread["posts"]

                # random number post
                post = randint(0, len(posts) - 1)

                # makes sure the post we have has an image
                if "ext" in posts[post]:
                    extension = str(posts[post]["ext"])

                    # this better not be a gif or webm..
                    if extension in [".jpg", ".png", "jpeg"]:
                        filename = str(posts[post]["tim"])
                        full_url = "http://i.4cdn.org/wg/" + filename + extension
                        print("Found file from /wg/ @: " + full_url)

                        # output file path
                        filepath = get_wallpaper_path(filename + extension)

                        # put the image in the directory specified
                        urlretrieve(full_url, filepath)

                        # check for nudity
                        detections = detector.detect(filepath)
                        if detections:
                            print(f"Nude content detected, skipping {filepath}")
                            remove(filepath)
                            attempts += 1
                            sleep(1)
                            continue

                        # if no nudity was detected, return the safe wallpaper
                        return filepath

        except Exception as e:
            attempts += 1
            print("Couldn't get wallpaper, e={} attempts={}".format(e, attempts))
            sleep(1)

    raise RuntimeError("Failed to download a safe wallpaper after multiple attempts")


# sets the wallpaper using sqlite3 db
def set_wallpaper(filepath):
    if platform == "darwin":
        if isfile(filepath):
            subprocess.call(
                [
                    "osascript",
                    "-e",
                    f'tell application "Finder" to set desktop picture to POSIX file "{filepath}"',
                ]
            )
            print("Wallpaper set to " + filepath)
    elif platform == "linux":
        if isfile(filepath):
            call(["feh", "--bg-fill", filepath])


if __name__ == "__main__":
    main()
