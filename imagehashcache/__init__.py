"""
Image hashing library
======================

Example:

>>> from PIL import Image
>>> import imagehash
>>> hash = imagehash.average_hash(Image.open('test.png'))
>>> print(hash)
d879f8f89b1bbf
>>> otherhash = imagehash.average_hash(Image.open('other.bmp'))
>>> print(otherhash)
ffff3720200ffff
>>> print(hash == otherhash)
False
>>> print(hash - otherhash)
36
>>> for r in range(1, 30, 5):
...     rothash = imagehash.average_hash(Image.open('test.png').rotate(r))
...     print('Rotation by %d: %d Hamming difference' % (r, hash - rothash))
...
Rotation by 1: 2 Hamming difference
Rotation by 6: 11 Hamming difference
Rotation by 11: 13 Hamming difference
Rotation by 16: 17 Hamming difference
Rotation by 21: 19 Hamming difference
Rotation by 26: 21 Hamming difference
>>>

"""

from PIL import Image
import numpy
import scipy.fftpack
from .util import resize

def _binary_array_to_hex(arr):
	"""
	internal function to make a hex string out of a binary array
	"""
	h = 0
	s = []
	for i, v in enumerate(arr.flatten()):
		if v: 
			h += 2**(i % 8)
		if (i % 8) == 7:
			s.append(hex(h)[2:].rjust(2, '0'))
			h = 0
	return "".join(s)

class ImageHash(object):
	"""
	Hash encapsulation. Can be used for dictionary keys and comparisons.
	"""
	def __init__(self, binary_array):
		self.hash = binary_array

	def __str__(self):
		return _binary_array_to_hex(self.hash.flatten())

	def __repr__(self):
		return repr(self.hash)

	def __sub__(self, other):
		if other is None:
			raise TypeError('Other hash must not be None.')
		if self.hash.size != other.hash.size:
			raise TypeError('ImageHashes must be of the same shape.', self.hash.shape, other.hash.shape)
		return (self.hash.flatten() != other.hash.flatten()).sum()

	def __eq__(self, other):
		if other is None:
			return False
		return numpy.array_equal(self.hash.flatten(), other.hash.flatten())

	def __ne__(self, other):
		if other is None:
			return False
		return not numpy.array_equal(self.hash.flatten(), other.hash.flatten())

	def __hash__(self):
		# this returns a 8 bit integer, intentionally shortening the information
		return sum([2**(i % 8) for i, v in enumerate(self.hash.flatten()) if v])

def hex_to_hash(hexstr):
	"""
	Convert a stored hash (hex, as retrieved from str(Imagehash))
	back to a Imagehash object.
	"""
	l = []
	if len(hexstr) != 16:
		raise ValueError('The hex string has the wrong length')
	for i in range(8):
		h = hexstr[i*2:i*2+2]
		v = int("0x" + h, 16)
		l.append([v & 2**i > 0 for i in range(8)])
	return ImageHash(numpy.array(l))


def average_hash(image, hash_size=8, **kwargs):
	"""
	Average Hash computation

	Implementation follows http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

	@image must be a PIL instance.
	"""
	#image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
	image = resize(image, hash_size, hash_size, **kwargs)
	pixels = numpy.array(image.getdata()).reshape((hash_size, hash_size))
	avg = pixels.mean()
	diff = pixels > avg
	# make a hash
	return ImageHash(diff)

def phash(image, hash_size=8, highfreq_factor=4, **kwargs):
	"""
	Perceptual Hash computation.

	Implementation follows http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

	@image must be a PIL instance.
	"""
	img_size = hash_size * highfreq_factor
	image = resize(img_size, img_size, **kwargs)
	pixels = numpy.array(image.getdata(), dtype=numpy.float).reshape((img_size, img_size))
	dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
	dctlowfreq = dct[:hash_size, :hash_size]
	med = numpy.median(dctlowfreq)
	diff = dctlowfreq > med
	return ImageHash(diff)

def phash_simple(image, hash_size=8, highfreq_factor=4, **kwargs):
	"""
	Perceptual Hash computation.

	Implementation follows http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

	@image must be a PIL instance.
	"""
	img_size = hash_size * highfreq_factor
	image = resize(img_size, img_size, **kwargs)
	pixels = numpy.array(image.getdata(), dtype=numpy.float).reshape((img_size, img_size))
	dct = scipy.fftpack.dct(pixels)
	dctlowfreq = dct[:hash_size, 1:hash_size+1]
	avg = dctlowfreq.mean()
	diff = dctlowfreq > avg
	return ImageHash(diff)

def dhash(image, hash_size=8, **kwargs):
	"""
	Difference Hash computation.

	following http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

	@image must be a PIL instance.
	"""
	image = resize(hash_size + 1, hash_size, **kwargs)
	pixels = numpy.array(image.getdata(), dtype=numpy.float).reshape((hash_size + 1, hash_size))
	# compute differences
	diff = pixels[1:, :] > pixels[:-1, :]
	return ImageHash(diff)



