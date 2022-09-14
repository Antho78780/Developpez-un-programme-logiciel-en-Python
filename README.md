# Script information
the script allows to create chess tournaments,
to register players and to display all the information relating to the tournament in question

## Setup
Install python 3.10.5 on this site:
https://www.python.org/

When you install python check the option
add path python

If you are not using pycharm
python -m venv env 
env/scripts/activate 
pip install -r requirements.txt

If you are using pycharm
Click on the bottom right of pycharm on your programming language and press add interpretter
Click on New environment and press ok

venv/scripts/activate
pip install -r requirements.txt

to run a flake8 report
cd flake8_rapport
flake8 --format=html --htmldir=flake_report --max-line-length 119

## Usage
to run the script use the python command main.py

You can see the main menu display. 
If you enter one, you access the players menu.
Once in the players menu,
if you enter one, you access the addition of players
if you enter two, you access the players who are registered in the database
and if you enter three you return to the previous menu

If you enter two you access the tournament menu.
Once in the tournament menu,
If you enter one, you access the tournament creation
If you enter two, you access current tournaments
if you enter three, you access the created tournaments
and if you enter four you return to the previous menu

If you enter three you access the reports.

And if you enter four you leave the terminal

## Author
-Anthony
-Github Profile @Antho78780


