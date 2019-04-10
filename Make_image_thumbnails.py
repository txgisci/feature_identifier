from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from shutil import copy
from resizeimage import resizeimage
import os
from PIL import ExifTags

input_dir = '//home//aaron//projectDir//island_images//test//not_your_feature'
output_dir = '//home//aaron//projectDir//island_images_336x224//test//not_your_feature'


# input_dir='E:\\Images\\ESC\\Large'
# output_dir='E:\\Images\\ESC\\672x448'

#dir_ext='\\ISS058' #directory extension

#file_list=os.listdir(input_dir+dir_ext)

#took out directory extension from original code
file_list=os.listdir(input_dir)
size = 336, 224 #width and height of image in pixels

#resize copies maintaining aspect ratio
for file_name in file_list:
	print(file_name)
	file, ext = os.path.splitext(file_name)
	#im = Image.open(input_dir+dir_ext+'\\'+file_name)
	im = Image.open(input_dir+'//'+file_name)
	width,height=im.size
	if(height>width):
		im=im.rotate(90, expand=True)
	im.thumbnail(size, Image.ANTIALIAS)
	#resize copies to EXACT specifications, cropping slightly to fit
	im = resizeimage.resize_cover(im, size)
	#im.save(output_dir+dir_ext+'\\'+file_name, "JPEG", quality=90)
	im.save(output_dir+'//'+file_name, "JPEG", quality=90)

	