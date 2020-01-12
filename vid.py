#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Coyright (C) 2019 Niels Joubert
# Contact: Niels Joubert <njoubert@gmail.com>
#
# This source is subject to the license found in the file 'LICENSE' which must
# be be distributed together with this source. All other rights reserved.
#
# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
"""
"""
############################
# Python 2to3 Compatibility
############################
# from __future__ import print_function

############################
# Python System Packages
############################
import os
import sys
import glob
# import math
# import cmath
import time
import datetime
import dateutil.parser
import re
# import itertools
# import functools
# import random
# import pickle
# import json
# import csv
# import urllib
# import requests
import argparse
import subprocess
# print(sys.version)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process Raw Videos')
  parser.add_argument('--datetime')
  parser.add_argument('--filetype', default="MP4")
  parser.add_argument('folder')
  # parser.add_argument('integers', metavar='N', type=int, nargs='+',
  #                   help='an integer for the accumulator')
  args = parser.parse_args()

  date_time_obj = dateutil.parser.parse(args.datetime)
  
  # Get all the video files
  f = []
  filepaths = []
  for root, dirs, files in os.walk(args.folder):
    for file in files:
      if file.endswith(args.filetype):
        f.append(file)
        filepaths.append(os.path.join(args.folder, file))

  # Get the start time of this clip. 
  # GoPro has special stuff which might be better. For the moment we just use the format tag.

  # def get_creation(filepath):
  #   cmd = "ffprobe -v error -show_entries format_tags=creation_time -of default=noprint_wrappers=1:nokey=1 \"" + filepath +  "\""
  #   return subprocess.check_output(cmd, shell=True)

  # def get_duration(filepath):
  #   cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 \"" + filepath +  "\""
  #   return subprocess.check_output(cmd, shell=True)

  def ffprobe_output(filepath):
    cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=duration:stream_tags=creation_time -of default=noprint_wrappers=1 \"" + filepath +  "\""
    lines = subprocess.check_output(cmd, shell=True)
    lines = re.split('=|\n| ',str(lines.decode("utf-8")).strip().replace('TAG:', ''))
    it = iter(lines) 
    lines = dict(zip(it, it))
    print(lines)
    return lines



  ffprobe = [ffprobe_output(fp) for fp in filepaths]
  # creation = [get_creation(fp) for fp in filepaths]
  # duration = [get_duration(fp) for fp in filepaths] 







