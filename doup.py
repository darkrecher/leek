
import os
import argparse
from subprocess import call

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
	'-f', metavar='files', action='store',
	help='Fichiers ou répertoire à mettre dans le doub. (Même format que l\'argument d\'un tar.gz.)')


def upload(args):
	# rm doup.tar.gz
	# rm doup.tar.gz.enc
	# tar -zcvf doup.tar.gz directory_to_test_doup/

	# https://superuser.com/questions/724986/how-to-use-password-argument-in-via-command-line-to-openssl-for-decryption
	call([
		'openssl',
		'aes-256-cbc', '-salt', '-in', 'doup.tar.gz',
		'-out', 'doup.tar.gz.enc',
		'-pass', 'pass:machin_bidule'])

def download(args):

	# rm doup.tar.gz
	# rm doup.tar.gz.enc

	call([
		'openssl',
		'aes-256-cbc', '-d', '-salt', '-in', 'doup.tar.gz.enc',
		'-out', 'doup.tar.gz',
		'-pass', 'pass:machin_bidule'])

	# tar -zxvf doup.tar.gz


def main():
	args = parser.parse_args()
	print(args)


if __name__ == '__main__':
	main()

