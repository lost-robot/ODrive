
was able to flash board in this state
connected via stlink and only used the 3.3v from the stlink
followed the general instructions here: https://docs.odriverobotics.com/v/0.5.6/developer-guide.html

with instructions such as: To customize the compile time parameters, copy or rename the file Firmware/tup.config.default to Firmware/tup.config

added this alias to bash for python: 
alias python=python3

had issues with cantools

pip show cantools
pip install cantools==36.0.0

...edited the create_can_dbc.py file and Makefile

successfully flashed and connected via odrivetool