# How's The Network
This python program is aimed at gathering real-time data on one's computer internet connection, mainly: is internet available and what is this device's real use of the bandwidth.
My personal use case is to run it on a raspberry pi just next to my router to have real data on my connection's quality.

# Requirements
## General
This script has been tested with python 3.7 and 3.10 and probably doesn't work with version under 3.5.

To make it work you will need to install the package `psutil`, to do so you can run the command:
```
pip install psutil
```

## On windows
On windows an additional package is required for it to work in a terminal: `windows-curses`, once again, to install run the command:
```
pip install windows-curses
```

## For GUI mode
There's a GUI mode, if you wish to run it you will need to install more packages: `PySide6` as well as `PySide6-Addons`. You can do so with the following commands:
```
pip install PySide6
```
```
pip install PySide6-Addons
```

# How to run it

There are currently two main feature to this project:
  - repeatedly check if the computer has access to the internet
  - monitor the real network use

And of course the program can execute both at the same time.
To get more information about the program parameters, run it with the option `--help`

## Try it in console

The script to run the program in console only is `console_main.py`.

### On MacOs and Linux
run the command:
```
python3 console_main.py -irt -brt
```
### On Windows
run the command:
```
python3.exe console_main.py -irt -brt
```
### Expected output

Right after running the command you should see the first lines about the connectivity in the console, and after 20 seconds you should see something similar to this:
![image](https://github.com/lesquoyb/HowsTheNetwork/assets/6374469/25b7cc74-b0b6-4449-9dff-de096c102343)

## Try it in GUI

The script to run the program in GUI mode is `gui_main.py`. Don't forget to install the `PySide6` dependencies mentionned above!

It works with the same parameters as the console one.

### On MacOs and Linux
run the command:
```
python3 gui_main.py -irt -brt
```
### On Windows
run the command:
```
python3.exe gui_main.py -irt -brt
```
### Expected output

Right after running the command you should see the first lines about the connectivity in the console, and after 20 seconds you should see something similar to this:
![image](https://github.com/lesquoyb/HowsTheNetwork/assets/6374469/25b7cc74-b0b6-4449-9dff-de096c102343)



## Try it in GUI

The script to run the program in console only is `console_main.py`.

### On MacOs and Linux
run the command:
```
python3 console_main.py -irt -brt
```
### On Windows
run the command:
```
python3.exe console_main.py -irt -brt
```

## Check internet connection

To check the internet connection in real time and gather some statistics about it, the program with the options `--internet_real_time` or its alias `-irt`.

If you want to log the information connection you can use the option `--file_internet` and give it a path for a file, the program will write at each internet connection check one line 
with the timestamp followed by a comma and `True` if you had access to internet or `False` otherwise. If you find it more convenient you can use the `--datetime` option to save a
datetime instead of a timestamp in the csv file.

You can use both options at the same time.

## Monitor network usage

This option will look at the actual quantity of data sent and received by your computer over the network. Your can activate it to read it live with the option `--bandwidth-live`.

You can also chose to save those data to a file with the option `--file-bandwidth`, as for the internet access, it will save one line containing a timestamp and the total amount of
data sent and received since the launch of the program.



