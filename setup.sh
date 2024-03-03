#!/bin/bash

echo "installing python libraries"
pip install -r requirements.txt

echo "setting up the database for the first time"
python appdb.py

