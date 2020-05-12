import math

BIGS = [4, 9, 16, 25]
BIG = 9

def chunk(big, small):
	chunk_size = math.sqrt(big)
	return (math.ceil(small/chunk_size))

for big in BIGS:
	print(str(big) + ': ')
	for small in range(1, big + 1):
		mod_n = 1
		mod = math.sqrt(big)
		ch = chunk(big, small)
		last = int(ch/mod * big - 1)
		first = int(last - mod + 1)
		#print(small, 'is', (small - 1)%chunk(big, big) + 1,
		#	'in', chunk(big, small))
		print('first:', first, 'last,:', last)
	print('\n')