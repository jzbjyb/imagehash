try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = ""
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='ImageHashCache',
    version='1.0',
    author='Zhengbao Jiang',
    author_email='rucjzb@163.com',
    packages=['imagehashcache'],
    scripts=['find_similar_images.py'],
    url='https://github.com/jzbjyb/imagehash',
    license='LICENSE',
    description='Image Hashing Library with Cache',
    long_description=long_description,
    install_requires=[
        "scipy",
        "numpy",
        "pillow", # or PIL
    ],
)

