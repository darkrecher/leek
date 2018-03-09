
def read_file(pathfile):
	with open(pathfile, 'r', encoding='utf-8') as file:
		return file.read()


def read_file_by_lines(pathfile):
	with open(pathfile, 'r', encoding='utf-8') as file:
		for file_line in file:
			print(file_line)


def write_file(pathfile, value):
	with open(pathfile, 'a', encoding='utf-8') as file:
		return file.write(value)



def int_from_strhex(str_hex):
	b = str_hex[::2]
	c = str_hex[1::2]
	dd = list(zip(list(b), list(c)))
	ee = [ ''.join(elem) for elem in dd ]
	ff = [ int(elem, 16) for elem in ee ]
	return ff

# [ chr(elem) for elem in ff ]


int_from_strhex("aaa")