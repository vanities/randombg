from appscript import app, mactypes
from urllib.request import urlopen
from json import loads
from random import randint
from time import sleep


def main():

	page = str(randint(0,9))
	thread = randint(0,14)
	post = 0

	with urlopen('https://a.4cdn.org/wg/' + page + '.json') as url:
	    json = loads(url.read().decode())

	    thread = json['threads'][thread]
	    posts = thread['posts']

	    for p in posts:
	    	post += 1
	    	print(post)

	    post = randint(0,post-1)

	    print(posts[post])
	    
	    try:
	    	extension = str(posts[post]['ext'])
	    	print(extension)

	    	if extension == '.jpg' or extenstion == '.png':
	    		filename = str(posts[post]['tim'])

	    		print('http://i.4cdn.org/wg/' + filename + extension)
	    		app('Finder').desktop_picture.set(mactypes.File(urlopen('http://i.4cdn.org/wg/' + filename + extension)))

	    except:
	    	print('No file in this post..')
	    	sleep(1)
	    	



if __name__ == "__main__":
    main()