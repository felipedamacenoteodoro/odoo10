#!/usr/bin/env bash

virtualenv .

source bin/activate

pip install -r requirements.txt

sudo apt-get install texlive-lang-portuguese -y

make dir=treinamento-tecnico slides html

