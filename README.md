# ShelfSense
This repository contains the code for a smart shelf system that uses weight as a form of stock control.

This branch relates to the scripts that are loaded onto and read by the raspberry pi.

The file paramiko.py is just a simple example of how I am using ssh to connect to the pi and run commands via the CLI.

The file monitor.py is an example of how the weight sensor monitors products. It contains a loop of numbers that are designed to act as weights that have been read in and so
the script can be tested without the use of a load cell. 

The final script, completeMonitor.py, is the actual script that has been loaded onto and used by the pi.

To run either monitor.py or completeMonitor.py the command would be as follows:

`monitor.py barcode 1, weight 2, barcode 3, weight 3......barcode x, weight x`
`completeMonitor.py barcode 1, weight 2, barcode 3, weight 3......barcode x, weight x`
