#!/bin/bash 

read -p "Enter git comment: " com

git add $filename dist/ pycompile.sh
git commit -m "$com"

git push -u origin main

