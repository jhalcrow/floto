#!/usr/bin/python
import os

num_pokemon = 7

with open("../static/pokemon.json", "w") as f:
	f.write('[\n')
	for dirname, dirnames, imgfiles in os.walk('../static/img/pokemon'):
		imgfiles = imgfiles[:num_pokemon]
		for i in range(num_pokemon-1):
			imgfile = imgfiles[i]
			if(imgfile != ".DS_Store"):
				f.write('\t{\n')
				f.write('\t\t"name": "' + imgfile[:-4] + '",\n')
				f.write('\t\t"imageUrl": "' + os.path.join(dirname, imgfile)[2:] + '"\n')
				f.write('\t},\n')

		imgfile = imgfiles[num_pokemon-1]
		f.write('\t{\n')
		f.write('\t\t"name": "' + imgfile[:-4] + '",\n')
		f.write('\t\t"imageUrl": "' + os.path.join(dirname, imgfile)[2:] + '"\n')
		f.write('\t}\n')
	f.write(']\n')