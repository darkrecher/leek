
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



(
	pl_guess, pl_int, pl_hex, pl_hexu, pl_hexl, pl_hexu_space, pl_hexl_space, pl_asc, pl_ut8,
	pl_lint, pl_lasc, pl_lut8, pl_asc_lint, pl_asc_lhex, pl_all
) = range(15)


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

def _asc_lint_to_lint(asc_lint):
	asc_lint = asc_lint.translate(str.maketrans(",.-_;", "     "))
	asc_lint_splitted = asc_lint.split()
	return list([int(elem) for elem in asc_lint_splitted])

def _asc_lhex_to_lint(asc_lhex):
	asc_lhex = asc_lhex.translate(str.maketrans(",.-_;", "     "))
	asc_lhex_splitted = asc_lhex.split()
	return list([int(elem, 16) for elem in asc_lhex_splitted])


def _lint_to_int(lint):
	big_int = 0
	for cur_int in lint:
		big_int *= 256
		big_int += cur_int
	return str(big_int)

def _lint_to_lhex(lint):
	lhex = [
		hex(cur_int)[2:].rjust(2, '0')
		for cur_int in lint
	]
	return lhex

def _lint_to_hexu(lint):
	lhex = _lint_to_lhex(lint)
	return ''.join(lhex).upper()

def _lint_to_hexl(lint):
	lhex = _lint_to_lhex(lint)
	return ''.join(lhex).lower()

def _lint_to_hexu_space(lint):
	lhex = _lint_to_lhex(lint)
	return ' '.join(lhex).upper()

def _lint_to_hexl_space(lint):
	lhex = _lint_to_lhex(lint)
	return ' '.join(lhex).lower()

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
	pl_asc_lint: _asc_lint_to_lint,
	pl_asc_lhex: _asc_lhex_to_lint,
}

DICT_FUNCTION_OUT_FROM_PL_TYPE = {
	pl_int: ('entier', _lint_to_int),
	pl_hexu: ('hexa upcase', _lint_to_hexu),
	pl_hexl: ('hexa lowcase', _lint_to_hexl),
	pl_hexu_space: ('hexa-space upcase', _lint_to_hexu_space),
	pl_hexl_space: ('hexa-space lowcase', _lint_to_hexl_space),
	pl_asc: ('str ascii', _lint_to_asc),
	pl_ut8: ('str utf-8', _lint_to_ut8),
	pl_lint: ('liste entier', lambda data: str(data)),
}

PL_TYPES_FOR_PL_ALL = (pl_int, pl_lint, pl_hexu, pl_hexl, pl_hexu_space, pl_hexl_space, pl_asc, pl_ut8)

label_length_max = max([
	len(value[0])
	for key, value
	in DICT_FUNCTION_OUT_FROM_PL_TYPE.items()
])


def _only_allowed_chars(str_data, allowed_chars):
	unauthorized_chars = set(str_data) - set(allowed_chars)
	return not bool(unauthorized_chars)

def _guess(data):
	if isinstance(data, (list, tuple)):
		if all([ isinstance(elem, int) for elem in data ]):
			return pl_lint
		if all([ isinstance(elem, str) for elem in data ]):
			data = ''.join(data)
			# Pas de détection d'encodage. C'est ascii ou utf-8. Tant pis si ça pète après.
			try:
				data.encode('ascii')
				return pl_lasc
			except:
				return pl_lut8

	if isinstance(data, str):
		if _only_allowed_chars(data, '0123456789abcdefABCDEF'):
			return pl_hex
		if _only_allowed_chars(data, ',.-_;0123456789 '):
			return pl_asc_lint
		if _only_allowed_chars(data, ',.-_;0123456789 abcdefABCDEF'):
			return pl_asc_lhex
		# Toujours pas de détection d'encodage
		try:
			data.encode('ascii')
			return pl_asc
		except:
			return pl_ut8

	if isinstance(data, int):
		return pl_int

	return None


def plop(data, pl_type_out=pl_all, pl_type_in=pl_guess):

	if pl_type_in == pl_guess:
		pl_type_in = _guess(data)
	if pl_type_in is None:
		raise Exception("Fail guess")
	function_in = DICT_FUNCTION_IN_FROM_PL_TYPE.get(pl_type_in)
	if pl_type_in is None:
		raise Exception("Fail arguments pl_type_in")
	lint = function_in(data)

	if pl_type_out == pl_all:
		print('')
		for pl_type_out_current in PL_TYPES_FOR_PL_ALL:
			label, function_out = DICT_FUNCTION_OUT_FROM_PL_TYPE[pl_type_out_current]
			try:
				print('%s : %s' % (label.ljust(label_length_max), function_out(lint)))
			except:
				print('%s : %s' % (label.ljust(label_length_max), 'fail'))
			print('')

	else:
		out_infos = DICT_FUNCTION_OUT_FROM_PL_TYPE.get(pl_type_out)
		if out_infos is None:
			raise Exception("Fail arguments pl_type_out")
		function_out = out_infos[1]
		return function_out(lint)


# snippets de code pour faire du ssh et du snmp à travers un rebond ssh.

#	def start_ssh():
#		self.ssh_client = paramiko.SSHClient()
#		self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#		# https://docs.python.org/2/library/getpass.html
#		password = getpass.getpass('Veuillez entrer le mot de passe pour la connexion SSH : ')
#		self.ssh_client.connect(ip, port=port, username=username, password=password)
#
#	def config(
#		self, version='v2c', community='NAGIOS', walker_ip='194.199.57.51', walker_port=50161,
#		oid_prefix_in='1.3.6.1.4.1.42229.6.22.', line_prefix_out='SNMPv2-SMI::enterprises.42229.6.22.'
#	):
#		"""
#		Le oid_prefix_in doit se terminer par un '.', sinon ça ne marche pas.
#		Le line_prefix_out doit correspondre à l'oid_prefix_in.
#		"""
#		self.version = version
#		self.community = community
#		self.walker_ip = walker_ip
#		self.walker_port = walker_port
#		self.oid_prefix_in = oid_prefix_in
#		self.line_prefix_out = line_prefix_out
#		param_commands = (self.version, self.community, self.walker_ip, str(self.walker_port))
#		self._walk_commmand = 'snmpwalk -%s -c %s %s:%s ' % param_commands
#		self._get_commmand = 'snmpget -%s -c %s %s:%s ' % param_commands
#		self._set_commmand = 'snmpset -%s -c %s %s:%s ' % param_commands
#
#	def test(self):
#		stdin, stdout, stderr = self.ssh_client.exec_command('ls -l')
#		logger.info(''.join(stdout))


if __name__ == '__main__':

	plop(123456)
	print('-' * 10)
	plop('deadBEEF')
	print('-' * 10)
	plop('tralala;$_pouet')
	print('-' * 10)
	plop('abcdéèê')
	print('-' * 10)
	plop('αβ')
	print('-' * 10)
	plop(list(range(41)))
	print('-' * 10)
	plop(('a', 'b', 'c'))
	print('-' * 10)
	plop(('é', 'è', 'ñ'))
	print('-' * 10)

	print(plop('deadbeef', pl_lint, pl_hex))
	print('-' * 10)

	# Bof... Mais on n'a pas besoin de ça.
	plop('a1,b2,100')
