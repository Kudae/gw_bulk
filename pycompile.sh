#!/bin/bash 

filename="gw_bulk.py"
rmpy=${filename%.py}

read -p "Enter git comment: " com

vi $filename

printf "Clear directories / files \n"
rm -v -R build dist $rmpy.spec __pycache__

printf "run pyinstaller for gw_rename.py\n"
/root/.pyenv/shims/python -m PyInstaller $filename --onefile

printf "copy file over to remote server\n"
sshpass -p 'vpn123' scp dist/$rmpy admin@172.25.84.166:/home/admin

git add $filename dist/ pycompile.sh
git commit -m "$com"

git push -u origin main 

