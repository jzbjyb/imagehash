# -*- coding:utf-8 -*-

import os
from PIL import Image

def resize(image, width, height, **kwargs):
	default = {
		'cache': False,
		'trans_func': None,
		'path': None
	}
	default.update(kwargs)
	if default['cache'] and hasattr(default['trans_func'], '__call__') and default['path'] != None and os.path.exist(default['trans_func'](default['path'])):
		return Image.open(default['path'])
	image = image.convert("L").resize((width, height), Image.ANTIALIAS)
	if default['cache'] and hasattr(default['trans_func'], '__call__') and default['path'] != None:
		path = default['trans_func'](default['path'])
		if not os.path.exist(os.path.dirname(path)):
			os.mkdir(os.path.dirname(path))
		image.save(path)
	return image