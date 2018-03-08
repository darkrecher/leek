
# ## alias

echo "alias ll='ls -l'" >> ~/.bash_aliases
echo "alias gitlog='git log --all --oneline --decorate --graph'" >> ~/.bash_aliases

# Pour lancer un terminal : gnome-terminal
# Pour ajouter le raccourci clavier d'ouverture d'un terminal :
# https://www.hacking-tutorial.com/tips-and-trick/how-to-create-keyboard-shortcuts-on-kali-linux/#sthash.p5RC2RAq.jcbpvl9x.dpbs
# Application (en haut à gauche), usual application (cliquer), system tools - preferences - settings - keyboard


# ## clavier

cd

setxkbmap fr
setxkbmap fr bepo

# git est déjà installé.

# git clone https://github.com/blabla


# ## apt-get et sublime text

wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -

sudo apt-get install apt-transport-https

echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list

sudo apt-get update

sudo apt-get install sublime-text

# lancement direct de Sublime Text.
subl


# ## Firefox

# désactiver la pop-up à la con qui propose de sauvegarder un mot de passe.
# https://developer.mozilla.org/fr/Firefox/deploiement_Entreprise
# https://support.mozilla.org/en-US/questions/1158069

# Ça marche pas bien, alors je met directement la config que je veux dans le fichier existant.

echo "lockPref(\"signon.rememberSignons\", false);" >> /usr/lib/firefox-esr/defaults/pref/channel-prefs.js


# ## Lib python, et test

apt-get -y install python3 python3-dev python3-pip git

pip3 install --upgrade git+https://github.com/arthaud/python3-pwntools.git
pip3 install python-twitter

echo "alias python='python3'" >> ~/.bash_aliases
echo "alias pip='pip3'" >> ~/.bash_aliases

echo "print(\"coucou\")" >> test_python3.py
echo "print(1 / 3)" >> test_python3.py
echo "print(1 // 3)" >> test_python3.py
python test_python3.py


# ## Activation des alias

. ~/.bash_aliases

echo "C'est fait."
