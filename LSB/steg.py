from PIL import Image

# image used: 512 x 512

# Convert encoding data into 8-bit binary
def genData(data):
		# list of binary codes of given data
		newd = []

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd

# Pixels are modified according to the8-bit binary data and finally returned
def modPix(pix, data):
	datalist = genData(data) # generates the binary equivalent of the data ['01011120', '10100011']
	lendata = len(datalist) # length of the word entered
	imdata = iter(pix) # pixel data of the image

	# here we will set the array and set the pixels to be chosen
	# i and j pertains to the datalist array
	# for i in range(lendata):
	for i in range(lendata):
		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# Pixel value determined using XNOR gate
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1

		# Eighth pixel of every set tells
		# 0 means keep reading; 1 means the message is over.
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

pix_loc_xy = [(10,50), (5,80), (42,40)]

def encode_enc(newimg, data):
	i = 0
	for pixel in modPix(newimg.getdata(), data):
		# Putting modified pixels in the new image
		print(f'pixel: {pixel}')
		print(f'pix_loc_xy: {pix_loc_xy[i]}')
		newimg.putpixel(pix_loc_xy[i], pixel)
		i+=1

def encode():
	img = input("Enter image name(with extension) : ")
	image = Image.open(img, 'r')

	data = input("Enter data to be encoded : ")
	if (len(data) == 0):
		raise ValueError('Data is empty')

	newimg = image.copy()
	encode_enc(newimg, data)

	new_img_name = input("Enter the name of new image(with extension) : ")
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

def decode():
	img = input("Enter image name(with extension) : ")
	image = Image.open(img, 'r')

	data = ''
	binstr = ''

	# imgdata = iter(image.getdata())

	imgdata = list(iter(image.getdata()))


	# while (True):
	# 	pixels = [value for value in imgdata.__next__()[:3] +
	# 							imgdata.__next__()[:3] +
	# 							imgdata.__next__()[:3]]

	# 	for i in pixels[:8]:
	# 		if (i % 2 == 0):
	# 			binstr += '0'
	# 		else:
	# 			binstr += '1'

	# 	data += chr(int(binstr, 2))

	# 	print(f'pixels: {pixels}')
	# 	print(f'binstr: {binstr}')
	# 	print(f'data: {data}')

	# 	if (pixels[-1] % 2 != 0):
	# 		return data
	

	for z in range(0, len(pix_loc_xy), 3):
		target_cords_A = pix_loc_xy[z]
		target_cords_B = pix_loc_xy[z+1]
		target_cords_C = pix_loc_xy[z+2]
		

		# Calculate the index of the target pixel in the flattened pixel array
		pix_loc_A = target_cords_A[1] * image.width + target_cords_A[0]
		pix_loc_B = target_cords_B[1] * image.width + target_cords_B[0]
		pix_loc_C = target_cords_C[1] * image.width + target_cords_C[0]


		# Skip to the target pixel
		# TODO make it so that it skips to a pixel not just scans it
		# for _ in range(target_pixel_index):
		# 	imgdata.__next__()
		# # Extract RGB values of the target pixel
		# pixels = [value for value in imgdata.__next__()[:3]]


		pixels = [value for value in imgdata[pix_loc_A][:3] + 
								imgdata[pix_loc_B][:3] + 
								imgdata[pix_loc_C][:3]]
	
		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))

		print(f'target_cordsA: {target_cords_A}\ntarget_cordsB: {target_cords_B}\ntarget_cordsC: {target_cords_C}')
		print(f'pix_locA: {pix_loc_A}\npix_locB: {pix_loc_B}\npix_locC: {pix_loc_C}')
		print(f'pixels: {pixels}')
		print(f'binstr: {binstr}')
		print(f'data: {data}')

	return data

	# go to this pixel
	# do imgdata__next__
	# for i in pixels then if
	# concatinate the data and convert to binstr

def main():
	a = int(input(":: Welcome to Steganography ::\n"
						"1. Encode\n2. Decode\n"))
	if (a == 1):
		encode()

	elif (a == 2):
		print("Decoded Word : " + decode())
	else:
		raise Exception("Enter correct input")

# Driver Code
if __name__ == '__main__' :
	main()
