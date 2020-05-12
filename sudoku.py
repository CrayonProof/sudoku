import numpy as np
import math

N = 9
FILE_NAME = 'sku03.csv'
IS = 1
ISNT = 2
UNKNOWN = 0

grd = np.genfromtxt(FILE_NAME, delimiter=',')

#reformats the sudoku from a 2d to a 3d matrix
def reformat_array(input_array):
	gd_size = len(input_array)
	output_array = np.zeros((gd_size, gd_size, gd_size))
	for rw in range(gd_size):
		for cl in range(gd_size):
			val = input_array[rw, cl]
			if (not math.isnan(val)):
				output_array[int(val-1), rw, cl] = IS
	return output_array

def shade_crosshair(arr, val, rw, cl):
	#print('shade_crosshair['+str(val)+', '+str(rw)+', '+str(cl)+']')
	gd_size = len(arr)
	#shade row
	for val_rw in range(rw):
		arr[val, val_rw, cl] = ISNT
	for val_rw in range(rw + 1, gd_size):
		arr[val, val_rw, cl] = ISNT
	#shade column
	for val_cl in range(cl):
		arr[val, rw, val_cl] = ISNT
	for val_cl in range(cl + 1, gd_size):
		arr[val, rw, val_cl] = ISNT
	#shade z (value)
	for z_val in range(val):
		arr[z_val, rw, cl] = ISNT
	for z_val in range(val + 1, gd_size):
		arr[z_val, rw, cl] = ISNT
	#shade box
	bx_size = math.sqrt(gd_size)
	r_bx = math.ceil((rw + 1)/bx_size)
	r_last = int((r_bx/bx_size) * gd_size - 1)
	r_first = int(r_last - bx_size + 1)
	for rs in range(r_first, r_last + 1):
		c_bx = math.ceil((cl + 1)/bx_size)
		c_last = int((c_bx/bx_size) * gd_size - 1)
		c_first = int(c_last - bx_size + 1)
		for cs in range (c_first, c_last + 1):
			if not arr[val, rs, cs] == IS:
				arr[val, rs, cs] = ISNT	
	return arr

def shade_all(arr):
	gd_size = len(arr)
	arr = arr
	for val in range(gd_size):
		for rw in range(gd_size):
			for cl in range(gd_size):
				if (arr[val, rw, cl] == IS):
					arr = shade_crosshair(arr, val, rw, cl)
	return arr

#reformats from a 3d array to a 2d one
def sudokufy(arr):
	gd_size = len(arr)
	output_array = np.zeros((gd_size, gd_size))
	for val in range(gd_size):
		for rw in range(gd_size):
			for cl in range(gd_size):
				if arr[val, rw, cl] == IS:
					output_array[rw, cl] = val + 1;
	return output_array

def isAlone(z, arr):
	zero_count = 0;
	val = z[0]
	rw = z[1]
	cl = z[2]
	gd_size = len(arr)
	bx_size = math.sqrt(gd_size)
	r_bx = math.ceil((rw + 1)/bx_size)
	r_last = int((r_bx/bx_size) * gd_size - 1)
	r_first = int(r_last - bx_size + 1)
	for rs in range(r_first, r_last + 1):
		c_bx = math.ceil((cl + 1)/bx_size)
		c_last = int((c_bx/bx_size) * gd_size - 1)
		c_first = int(c_last - bx_size + 1)
		for cs in range (c_first, c_last + 1):
			if arr[val, rs, cs] == UNKNOWN:
				zero_count += 1
	return zero_count == 1

def solve(arr):
	gd_size = len(arr)
	#create array of all unknown cells
	zeros = []
	for val in range(gd_size):
			for rw in range(gd_size):
				for cl in range(gd_size):
					if arr[val, rw, cl] == UNKNOWN:
						zeros.append([val, rw, cl])
	while len(zeros) > 0:
		zeros.clear()
		for val in range(gd_size):
			for rw in range(gd_size):
				for cl in range(gd_size):
					if arr[val, rw, cl] == UNKNOWN:
						zeros.append([val, rw, cl])
		#print('zero length: ', len(zeros))
		for z in range(len(zeros)):
			#print(isAlone(z, arr))
			if isAlone(zeros[z], arr):
				arr[zeros[z][0], zeros[z][1], zeros[z][2]] = IS
				arr = shade_crosshair(arr, zeros[z][0], zeros[z][1], zeros[z][2])
				del zeros[z]

				break
		if z == len(zeros) - 1:
				break

	return arr

program_array = reformat_array(grd)
program_array = shade_all(program_array)
print('unsolved')
print(sudokufy(program_array))
print('solved')
print(sudokufy(solve(program_array)))