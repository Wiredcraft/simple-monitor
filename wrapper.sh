#!/bin/bash

LOG=/home/devops/simple-monitor.log

date >> $LOG
python monitor.py >> $LOG
