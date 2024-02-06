from PIL import Image
import numpy as np
from scipy.integrate import solve_ivp

from NTRU.NTRUencrypt import NTRUencrypt
from NTRU.NTRUdecrypt import NTRUdecrypt
from NTRU.NTRUutil import *

# image used: 512 x 512

global pix_loc_xy
# Initialise the private and public keys, write them out (and test reading)
NTRUdecrypt = NTRUdecrypt()
NTRUdecrypt.setNpq(N=107,p=3,q=64,df=15,dg=12,d=5)
NTRUdecrypt.genPubPriv()

NTRUencrypt = NTRUencrypt()

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

def lorenz_chaos_system(t, xyz, sigma=10, rho=28, beta=8/3):
    x, y, z = xyz
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# width of pic
def lorenz_integration(data):
	## Solve the Lorenz system
	initial_conditions = [1.0, 1.0, 1.0]

	t_span = (0, 100)
	t_eval = np.linspace(*t_span, num=10000)
	sol = solve_ivp(lorenz_chaos_system, t_span, initial_conditions, t_eval=t_eval)

	# Use the solution as seeds for generating random numbers
	random_seeds = sol.y[:, ::100].flatten()  # Extract every 100th value
	np.random.seed(int(random_seeds[0]))

	## Generate random integers within a specified range (size of the image) - 3
	lower_bound = 0
	# TODO 512 - 3 (Change this to depend on the size of the image)
	upper_bound = 509

	## 1 letter = 6 numbers/ 3 pixels
	num_random_numbers = len(data) * 6 # 6 because 1 letter is 3 pixels and 3 pixels make up of 6 numbers x,y
	random_numbers = np.random.randint(lower_bound, upper_bound, size=num_random_numbers)

	paired_numbers = random_numbers.reshape(-1,2)
	global pix_loc_xy
	pix_loc_xy = [tuple(row) for row in paired_numbers]
	print(pix_loc_xy)
	
	with open("lorenz_dec.txt", "w") as file:
		for item in pix_loc_xy:
			file.write(f"{item[0]}, {item[1]}\n")

def encode_enc(newimg, data):
	i = 0
	for pixel in modPix(newimg.getdata(), data):
		# Putting modified pixels in the new image
		# print(f'pixel: {pixel}')
		print(f'pix_loc_xy: {pix_loc_xy[i]}')
		newimg.putpixel(pix_loc_xy[i], pixel)
		i+=1

def encode():
	NTRUencrypt.readPub()
	NTRUencrypt.setM([1,-1,0,0,0,0,0,1,-1])
	NTRUencrypt.encrypt()

	img = input("Enter image name(with extension) : ")
	image = Image.open(img, 'r')

	data = input("Enter data to be encoded : ")
	if (len(data) == 0):
		raise ValueError('Data is empty')
	
	print(f"data before: {data}")
	NTRUencrypt.encryptString(data)
	data = NTRUencrypt.Me
	print(f"DATA Entered: {data}")

	lorenz_integration(data)
	newimg = image.copy()
	encode_enc(newimg, data)

	new_img_name = input("Enter the name of new image(with extension) : ")
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

def decode():
	img = input("Enter image name(with extension) : ")
	image = Image.open(img, 'r')

	file_path = input('Please enter the file path of key (with extension): ')

	pix_loc_xy = []

	with open(file_path, "r") as file:
		for line in file:
			values = line.strip().split(',')
			pix_loc_xy.append((int(values[0]), int(values[1])))

	print(pix_loc_xy)
	
	data = ''
	binstr = ''

	imgdata = list(iter(image.getdata()))


	for z in range(0, len(pix_loc_xy), 3):
		target_cords_A = pix_loc_xy[z]
		target_cords_B = pix_loc_xy[z+1]
		target_cords_C = pix_loc_xy[z+2]
		
		# Calculate the index of the target pixel in the flattened pixel array
		pix_loc_A = target_cords_A[1] * image.width + target_cords_A[0]
		pix_loc_B = target_cords_B[1] * image.width + target_cords_B[0]
		pix_loc_C = target_cords_C[1] * image.width + target_cords_C[0]

		pixels = [value for value in imgdata[pix_loc_A][:3] + 
								imgdata[pix_loc_B][:3] + 
								imgdata[pix_loc_C][:3]]
	
		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))

		# print(f'target_cordsA: {target_cords_A}\ntarget_cordsB: {target_cords_B}\ntarget_cordsC: {target_cords_C}')
		# print(f'pix_locA: {pix_loc_A}\npix_locB: {pix_loc_B}\npix_locC: {pix_loc_C}')
		print(f'pixels: {pixels}')
		print(f'binstr: {binstr}')
		binstr = ''
		print(f'data: {data}')

	print('Reached the end', NTRUencrypt.Me)
	NTRUdecrypt.decryptString(data)
	data = NTRUdecrypt.M
	return data

def main():
	while True:
		a = int(input("\033[H\033[J:: Welcome to Steganography ::\n"
							"1. Encode\n2. Decode\n3. Exit\n"))
		if (a == 1):
			encode()
		elif (a == 2):
			print("Decoded Word : " + decode())
			input("\n\nPlease press enter to continue\n")
		elif (a == 3):
			exit()
		else:
			raise Exception("Enter correct input")

# Driver Code
if __name__ == '__main__' :
	main()
