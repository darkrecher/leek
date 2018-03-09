
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



(pl_guess, pl_int, pl_hex, pl_hexu, pl_hexl, pl_asc, pl_ut8, pl_lint, pl_lasc, pl_lut8, pl_all) = range(11)


def _asc_to_lint(data):
	return list(data.encode('ascii', 'replace'))

def _ut8_to_lint(data):
	return list(data.encode('utf-8', 'replace'))

def _lasc_to_lint(datas):
	data = ''.join(datas)
	return list(data.encode('ascii', 'replace'))

def _lut8_to_lint(datas):
	data = ''.join(datas)
	return list(data.encode('utf-8', 'replace'))

def _int_to_lint(data):
	lint = []
	while data:
		lint.insert(0, data % 256)
		data = data // 256
	return lint

def _hex_to_lint(data):
	hex_digits_half_1 = data[::2]
	hex_digits_half_2 = data[1::2]
	hex_digits = zip(hex_digits_half_1, hex_digits_half_2)
	lint = [
		int('%s%s' % (dig_1, dig_2), 16)
		for dig_1, dig_2
		in hex_digits ]
	return list(lint)


def _lint_to_int(lint):
	big_int = 0
	for cur_int in lint[::-1]:
		big_int *= 256
		big_int += cur_int
	return str(big_int)

def _lint_to_hexu(lint):
	hexus = [
		hex(cur_int).upper()[2:]
		for cur_int in lint
	]
	return ''.join(hexus)

def _lint_to_hexl(lint):
	hexls = [
		hex(cur_int)[2:]
		for cur_int in lint
	]
	return ''.join(hexls)

def _lint_to_asc(lint):
	return str((bytes(lint)).decode("ascii", "replace"))

def _lint_to_ut8(lint):
	return str((bytes(lint)).decode("utf-8", "replace"))


DICT_FUNCTION_IN_FROM_PL_TYPE = {
	pl_int: _int_to_lint,
	pl_hex: _hex_to_lint,
	pl_hexu: _hex_to_lint,
	pl_hexl: _hex_to_lint,
	pl_asc: _asc_to_lint,
	pl_ut8: _ut8_to_lint,
	pl_lint: lambda data: data,
	pl_lasc: _lasc_to_lint,
	pl_lut8: _lut8_to_lint,
}

DICT_FUNCTION_OUT_FROM_PL_TYPE = {
	pl_int: ('entier', _lint_to_int),
	pl_hexu: ('hexa upcase', _lint_to_hexu),
	pl_hexl: ('hexa lowcase', _lint_to_hexl),
	pl_asc: ('str ascii', _lint_to_asc),
	pl_ut8: ('str utf-8', _lint_to_ut8),
	pl_lint: ('liste entier', lambda data: str(data)),
}

label_length_max = max([
	len(value[0])
	for key, value
	in DICT_FUNCTION_OUT_FROM_PL_TYPE.items()
])

print("TODO debug :", label_length_max)

def plop(data, pl_type_in=pl_guess, pl_type_out=pl_all):

	if pl_type_in == pl_guess:
		raise NotImplemented("TODO")
	function_in = DICT_FUNCTION_IN_FROM_PL_TYPE.get(pl_type_in)
	if pl_type_in is None:
		raise Exception("Fail arguments pl_type_in")
	lint = function_in(data)

	if pl_type_out == pl_all:
		raise NotImplemented("TODO")
	out_infos = DICT_FUNCTION_OUT_FROM_PL_TYPE.get(pl_type_out)
	if out_infos is None:
		raise Exception("Fail arguments pl_type_out")
	function_out = out_infos[1]
	return function_out(lint)

