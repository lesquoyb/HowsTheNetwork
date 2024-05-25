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
There's a GUI mode, if you wish to run it you will need to install one more package: `PySide6`. You can do so with the following commands:
```
pip install PySide6
```

# How to run it

There are currently two main feature to this project:
  - repeatedly check if the computer has access to the internet
  - monitor the real network use

And of course the program can execute both at the same time.
To get more information about the program parameters, run it with the option `--help`

## Try it in console

The script to run the program in console only is `main_console.py`.

### On MacOs and Linux
run the command:
```
python3 main_console.py -irt -brt
```
### On Windows
run the command:
```
python3.exe main_console.py -irt -brt
```
### Expected output

Right after running the command you should see the first lines about the connectivity in the console, and after 30 seconds you should see something similar to this:
![image](https://github.com/lesquoyb/HowsTheNetwork/assets/6374469/58482faa-ebd6-4773-add8-7b10e3d05fd6)

The console will refresh itself everytime it has new data, so with the default values it would be every 10 seconds.

To exit press the 'q' key on your keyboard

## Try it in GUI

The script to run the program in GUI mode is `main_gui.py`. Don't forget to install the `PySide6` dependencies mentionned above!

It works with the same parameters as the console one. And just like the console program, it will be refreshed everytime it has new data, so by default every 10 seconds.

### On MacOs and Linux
run the command:
```
python3 main_gui.py -irt -brt
```
### On Windows
run the command:
```
python3.exe main_gui.py -irt -brt
```
### Expected output

A new window should open with a chart in the middle and some stats in plain text above and under it. This should look something like this:
![image](https://github.com/lesquoyb/HowsTheNetwork/assets/6374469/c662ad75-fb00-4220-9d3c-5094d5c944f6)


## Check internet connection

To check the internet connection in real time and gather some statistics about it, use the option `--internet_real_time` or its alias `-irt`.

If you want to log the information connection you can use the option `--internet-file` and give it a path for a file, the program will write at each internet connection check one line 
with the timestamp followed by the time in millisecond it took to reach the host (by default 8.8.8.8, see `--help` option to get more details), in case of timeout the value would be -1. If you find it more convenient you can use the `--datetime` option to save a datetime instead of a timestamp in the csv file.

You can use both options at the same time or you can pick only one to have either just real time value or stats recorded without anything written in the console or showed on the display of the gui.

## Monitor network usage

This option will look at the actual quantity of data sent and received by your computer over the network. Your can activate it to read it live with the option `--bandwidth-real-time` or shorter with `-brt`.

You can also chose to save those data to a file with the option `--bandwidth-file`, as for the internet access, it will save one line containing a timestamp followed by the total amount of
data sent and received since the launch of the program.

As for the internet connection data, you can pick both options or only one of them.

## Reload old data

You can reload the data saved in csv files with the options `--read-bandwidth-file` (`-rbf`) and `--read-internet-file` (`rif`) followed by the path to the file to read.
You can use this option in addition to the other options to get data in real time and to save data in a file, it will load the values as an "initial state" and then continue with the program's normal life-cycle. You can even save in the same file that you are reading from if you want and the new data is going to get append in those file. You have to be aware that it may cause problem of incoherence for the the network use in case you restart your computer between two saves in the same file though.


