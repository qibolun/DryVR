#!/bin/bash

echo "This script automatically run all the examples in inputFile folder"
echo "The script will start in 1 seconds"

sleep 1

for entry in "inputFile"/*
do
	echo "Now running $entry"
	echo " "
	echo " "
	echo " "
	echo " "
	sleep 3
	python main.py $entry
	sleep 3
	echo " "
	echo " "
	echo " "
	echo " "

done
