from __future__ import print_function
from PIL import Image
import imagehash, os

filename = 'testfile.jpg'

def retrieve_example():
	import os
	if not os.path.exists(filename):
		url = 'http://www.liaoxuefeng.com/files/attachments/001407671964310a6b503be6fcb4648928e2e4c522d04c7000'
		import urllib2
		response = urllib2.urlopen(url)
		open(filename, 'w').write(response.read())
		print('download test image over')
	return Image.open(filename)

def run_hash_algorithm(algo):
	img = retrieve_example()
	hash = algo(img)
	print(hash)
	print("rotate slightly")
	imgrot = img.rotate(-1)
	otherhash = algo(imgrot)
	print(otherhash)
	print(hash == otherhash)
	assert hash - otherhash <= 8, ('slightly rotated image should have similar hash', hash, otherhash)
	#assert hash == otherhash, ('slightly rotated image should have same hash', hash, otherhash)
	
	print("rotate 90 degrees")
	imgrot = img.rotate(-90)
	otherhash = algo(imgrot)
	print(otherhash)
	print(hash == otherhash)
	assert hash != otherhash, ('rotated image should have different hash', hash, otherhash)
	assert hash - otherhash > 10, ('rotated image should have different hash', hash, otherhash)

def run_hash_algorithm_with_cache(algo):
	img = retrieve_example()
	hash = algo(img, cache=True, path='test_cache.jpg', trans_func=lambda path: 'cache' + os.sep + path)
	img_cache = Image.open('cache' + os.sep + 'test_cache.jpg')
	img.show()
	img_cache.show()
 
def test_average_hash():
	run_hash_algorithm(imagehash.average_hash)

def test_dhash():
	run_hash_algorithm(imagehash.dhash)

def test_phash():
	run_hash_algorithm(imagehash.phash)

def test_average_hash_cache():
	print(1)
	run_hash_algorithm_with_cache(imagehash.average_hash)


def test_average_hash_length():
	for hash_size in [8, 20]:
		print('checking if hash_size=%d is respected' % hash_size)
		hash = imagehash.average_hash(retrieve_example(), hash_size=hash_size)
		assert hash.hash.size == hash_size**2, hash.hash.shape

def test_dhash_length():
	for hash_size in [8, 20]:
		print('checking if hash_size=%d is respected' % hash_size)
		hash = imagehash.dhash(retrieve_example(), hash_size=hash_size)
		assert hash.hash.size == hash_size**2, hash.hash.shape

def test_phash_length():
	for hash_size in [8, 20]:
		print('checking if hash_size=%d is respected' % hash_size)
		hash = imagehash.phash(retrieve_example(), hash_size=hash_size)
		assert hash.hash.size == hash_size**2, hash.hash.shape

def test_stored_hashes():
	img = retrieve_example()
	hash = imagehash.average_hash(img)
	stored_hex = str(hash)
	print('checking if stringified hash is the same')
	otherhash = imagehash.hex_to_hash(stored_hex)
	print(otherhash)
	print(hash == otherhash)
	assert hash == otherhash
	assert hash - otherhash == 0
	
	
	
	


