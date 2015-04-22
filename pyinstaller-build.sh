#!/usr/bin/env bash

#/usr/bin/yum install -y python-virtualenv gcc unzip
virtualenv esxi-reclaim_venv
source esxi-reclaim_venv/bin/activate
wget https://github.com/gmelillo/esxi-reclaim/archive/master.zip
unzip master.zip
pip install -r esxi-reclaim-master/requirements.txt
pip install pyinstaller
#sed -i "s/misc.check_not_running_as_root()//g" esxi-reclaim_venv/lib/python2.6/site-packages/PyInstaller/main.py
cd esxi-reclaim-master
python setup.py install
cd ..
pyinstaller -F -n esxi-reclaim -s --paths=esxi-reclaim-master/ esxi-reclaim-master/esxireclaim/cmd.py
deactivate
mv dist/esxi-reclaim .
mv esxi-reclaim-master/esxi.ini.sample esxi.ini
rm -rf build dist esxi-reclaim-master esxi-reclaim.spec esxi-reclaim_venv master.zip