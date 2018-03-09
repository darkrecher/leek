
import os
import argparse
from subprocess import call, check_output
import doup_conf

parser = argparse.ArgumentParser(description='Script qui balance des "doup".')

parser.add_argument(
	'action', choices=['up', 'do', 'ul', 'dl', 'upload', 'download'],
	help='Action à effectuer')
parser.add_argument(
	'-n', metavar='name', action='store', required=False,
	help='Nom du doup (Ce nom sera écrit dans twitter)')
parser.add_argument(
	'-p', metavar='password', action='store', required=False,
	help='Mot de passe de chiffrement du doup.')
parser.add_argument(
	'-pp', metavar='file_password', action='store', required=False,
	help='Fichier contenant le mot de passe de chiffrement du doup.')
parser.add_argument(
	'-f', metavar='files', action='store', required=False,
	help='Fichiers ou répertoire à mettre dans le doub. (Même format que l\'argument d\'un tar.gz.)')
parser.add_argument(
	'-t', metavar='transfer_id', action='store', required=False,
	help='identifiant du fichier sur transfer.sh. (Par exemple : "D84JU" pour "https://transfer.sh/D84JU/doup.tar.gz.enc"')


def upload(doup_name, doup_files, pass_type, pass_text, pass_file):

	call(['rm', 'doup.tar.gz'])
	call(['rm', 'doup.tar.gz.enc'])

	call(['tar', '-zcvf', 'doup.tar.gz', doup_files])

	if pass_type == 'pass_from_cmd_line':
		pass_argument = 'pass:' + pass_text
	else:
		pass_argument = 'file:' + pass_file

	# https://superuser.com/questions/724986/how-to-use-password-argument-in-via-command-line-to-openssl-for-decryption
	call([
		'openssl',
		'aes-256-cbc', '-salt', '-in', 'doup.tar.gz',
		'-out', 'doup.tar.gz.enc',
		'-pass', pass_argument])

	print('envoi du fichier.')
	print('')
	url_uploaded = check_output(['curl', '--upload-file', 'doup.tar.gz.enc', 'https://transfer.sh/doup.tar.gz.enc'])
	print('')
	url_uploaded = url_uploaded.decode('ascii')
	print(url_uploaded)
	print('')

	print('Envoi d\'un twit pour conserver l\'url.')
	try:
		import twitter
	except:
		raise Exception("Fail. Il faut exécuter : pip3 install python-twitter")
	print('TODO')


def download(transfer_id, pass_type, pass_text, pass_file):

	call(['rm', 'doup.tar.gz'])
	call(['rm', 'doup.tar.gz.enc'])

	url_download = 'https://transfer.sh/%s/doup.tar.gz.enc' % transfer_id

	with open('doup.tar.gz.enc', 'w') as doup_file:
		call(['curl', url_download], stdout=doup_file)

	if pass_type == 'pass_from_cmd_line':
		pass_argument = 'pass:' + pass_text
	else:
		pass_argument = 'file:' + pass_file

	call([
		'openssl',
		'aes-256-cbc', '-d', '-salt', '-in', 'doup.tar.gz.enc',
		'-out', 'doup.tar.gz',
		'-pass', pass_argument])

	call(['tar', '-zxvf', 'doup.tar.gz'])


def main():
	args = parser.parse_args()
	doup_name = args.n or doup_conf.DEFAULT_NAME
	doup_files = args.f or '.'
	if args.p is None and args.pp is None:
		raise Exception("Il faut spécifier un mot de passe. Utiliser python doup.py -h pour plus de détails.")
	pass_text = args.p
	pass_file = args.pp

	if pass_text is not None:
		pass_type = 'pass_from_cmd_line'
	else:
		pass_type = 'pass_from_file'

	print('action : %s. name : %s. files : "%s". pass_type : %s' % (args.action, doup_name, doup_files, pass_type))

	if args.action == 'up':
		upload(doup_name, doup_files, pass_type, pass_text, pass_file)

	else:
		transfer_id = args.t
		if transfer_id is None:
			raise Exception("Le paramètre -u est obligatoire pour un download.")
		download(transfer_id, pass_type, pass_text, pass_file)


if __name__ == '__main__':
	main()

