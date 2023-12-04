from PIL import Image

# yield
# iter
# img.getdata()


# image used: 512 x 512

# Convert encoding data into 8-bit binary
def genData(data):
		# list of binary codes of given data
		newd = []

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
	datalist = genData(data) # generates the binary equivalent of the data ['01011120', '10100011']
	lendata = len(datalist) # length of the word entered
	imdata = iter(pix) 

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

def encode_enc(newimg, data):
	width = newimg.size[0]
	(x, y) = (0, 0)

	pix_loc_xy = [(10,50), (5,80), (42,40), (30,120), (53,302), (39,120), (8,239), (23,359), (42,201)]

	# HERE FOR EMBEDDING
	for pixel in modPix(newimg.getdata(), data):
		# Putting modified pixels in the new image
		# THIS IS THE ONLY THING I NEED TO CHANGE
		newimg.putpixel((x, y), pixel)
		if (x == width - 1):
			x = 0
			y += 1
		else:
			x += 1

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
	imgdata = iter(image.getdata())

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		# string of binary data
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data

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
