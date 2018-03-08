

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

# Pas encore testé !!

echo "// commentaire obligatoire mais osef" >> /usr/lib/firefox-esr/defaults/pref/autoconfig.js
echo "pref(\"general.config.filename\", \"mozilla.cfg\");" >> /usr/lib/firefox-esr/defaults/pref/autoconfig.js
echo "pref(\"general.config.obscure_value\", 0);" >> /usr/lib/firefox-esr/defaults/pref/autoconfig.js

echo "// commentaire obligatoire mais osef" >> /usr/lib/firefox-esr/defaults/pref/mozilla.cfg
echo "lockPref(\"signon.rememberSignons\", false);" >> /usr/lib/firefox-esr/defaults/pref/mozilla.cfg



