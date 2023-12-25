	
# Importing Image class from PIL module
from PIL import Image
 
# Opens a image in RGB mode
im = Image.open('monster_9.png')
 
# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size
 
# Setting the points for cropped image
left = 16
top = 32
right = 32
bottom = 48
 
# Cropped image of above dimension
# (It will not change original image)
for i in range(2, 3):
	for j in range(0, 3):
		# print((left + j * 32 + 16, top + i * 32, right + j * 32, bottom + i * 32))
		im1 = im.crop((left + j * 48, top + i * 48, right + j * 48, bottom + i * 48))
		im1 = im1.save(f"agent9-right-{j}.png") 

# Shows the image in image viewer
# im1.show()