#!/bin/bash
date=`date +%D-%T`
git pull
git commit -a -m $DATE
git push

