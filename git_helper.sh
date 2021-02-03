#!/bin/bash
print_menu()
{
local ITEM1=${1}
local ITEM2=${2}
local ITEM3=${3}
local ITEM4=${4}

LINE1="***GIT_MENU***"
LINE2="1. git "${ITEM1}
LINE3="2. git "${ITEM2}
LINE4="3. git "${ITEM3}
LINE5="4. git "${ITEM4}
 echo -e "${LINE1}\n${LINE2}\n${LINE3}\n${LINE4}\n${LINE5}"
}
EXIT=0

while [ $EXIT != 1 ]
do
	print_menu "pull" "add" "commit -m" "push"
	read -p "Choose One: " rp1

	if [ $rp1 == "1" ];then
	    git pull
	elif [ $rp1 == "2" ];then
	    read -p "What is the file or directory path/name? " rp2
	    git add $rp2
	elif [ $rp1 == "3" ];then
	    read -p "Do you want to commit ${rp2}(y/n): " rp3
	    if [ $rp3 == "y" ]; then
	      git commit -m $rp2
	    fi
	fi
done
