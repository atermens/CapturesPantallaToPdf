#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob, os, sys

import json

import img2pdf
from PIL import Image

WRK_PATH = os.getcwd()

if __name__ == "__main__":
	# Storaging RunOptions.json
	with open(os.path.join(WRK_PATH,sys.argv[1]),'r') as jsonRunOptionsFile:
		options = json.load(jsonRunOptionsFile)
	print("Options: ", options)

	# change directory to options["pathDir"], on processarem tot el que ens interessa
	os.chdir(options["pathDir"])

	# carreguem informacio a processar. Es comprovara que no tingui canal Alpha.
	# Si en te s'eliminara...
	imgList = []
	for arxiu in glob.glob("*."+options["imgType"]):
		try:
			image = Image.open(arxiu)
			if image.mode == "RGBA":
				print(" remove Alpha channel of " + arxiu + " ...")
				# create a blank background Image
				bg = Image.new('RGB', image.size, (255, 255, 255))
				# Paste image to background image
				bg.paste(image, (0, 0), image)
				# Save pasted image as image
				bg.save("c_"+arxiu, "PNG")
				imgList.append("c_"+arxiu)
			else:
				imgList.append(arxiu)
		except:
			pass
	print(" Num imatges a processar: {}".format(len(imgList)))

	# definim ara l'arxiu PDF de sortida i el generem
	outPDF = options["outFileName"] + ".pdf"
	# specify paper size DIN A4 Portrait/Landscape
	if options["a4inpt"] == "landscape":
		a4inpt = (img2pdf.mm_to_pt(297), img2pdf.mm_to_pt(210))
	else:
		a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
	layout_fun = img2pdf.get_layout_fun(a4inpt)

	# abans de generar el PDF anem a ordenar la llista imgList
	imgList.sort(reverse=False)
	print(imgList)

	# escrivim arxiu PDF
	with open(outPDF,"wb") as pdfOutFile:
		pdfOutFile.write(img2pdf.convert(imgList, layout_fun=layout_fun))
