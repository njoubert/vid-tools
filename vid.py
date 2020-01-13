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
import logging
import pathlib
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
  logging.basicConfig(level=logging.DEBUG)
  parser = argparse.ArgumentParser(description='Extracts clips at given datetime and duration from all clips in a folder tree')
  parser.add_argument('--datetime', required=True, help='Date and Time of Moment of Interest')
  parser.add_argument('--duration', required=True, help='Duration of Moment of Interest')
  parser.add_argument('--output', help='Location of final clips. Creates folder if it does not exist. Does not cut if not specified')
  parser.add_argument('-f', '--force', action="store_true")
  parser.add_argument('folder', help='Top of folder hierarchy to scan')
  args = parser.parse_args()

  moi_timestamp = dateutil.parser.parse(args.datetime)
  logging.debug(moi_timestamp)

  # First we get offsets
  offsets = {}
  for root, dirs, files in os.walk(args.folder):
    offset = datetime.timedelta(seconds=0)
    for filename in files:
      filepath = os.path.join(root, filename)
      relpath = os.path.relpath(filepath, args.folder)
      if filename == "offset.txt":
        with open(filepath, 'r') as offset_file:
          t = offset_file.read().split(":")
          offset = datetime.timedelta(hours=float(t[0]), minutes=float(t[1]), seconds=float(t[2]))
          offsets[root] = offset
        logging.warning(f'Found offset {offset} for directory {root}')

  # Get a list of all the files in a directory tree as (name, full path) tuples
  foi = []
  for root, dirs, files in os.walk(args.folder):
    offset = datetime.timedelta(seconds=0)
    if root in offsets:
      offset = offsets[root]
    for filename in files:
      filepath = os.path.join(root, filename)
      relpath = os.path.relpath(filepath, args.folder) 
      foi.append({'filename':filename, 'relpath':relpath, 'filepath': filepath, 'offset':offset})

  # Process all files with ffprobe, finding the creation date and duration
  # Filter out non-ffmpeg compatible files
  def ffprobe_output(f):
    cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=duration:stream_tags=creation_time -of default=noprint_wrappers=1 \"" + f['filepath'] +  "\""
    try:
      FNULL = open(os.devnull, 'w')
      lines = subprocess.check_output(cmd, stderr=FNULL, shell=True)
      lines = re.split('=|\n| ',str(lines.decode("utf-8")).strip().replace('TAG:', ''))
      it = iter(lines) 
      metadata = dict(zip(it, it))
      metadata['creation_time'] = dateutil.parser.parse(metadata['creation_time']) + f['offset']
      metadata['end_time'] = metadata['creation_time'] + datetime.timedelta(seconds=float(metadata['duration']))
      f.update(metadata)
      logging.info(f"ffprobe processed '{f['relpath']}' {f['creation_time']} {f['duration']} {f['offset']} ")
      return f
    except:
      return None

  logging.info('Filtering non-media files')
  ffprobe = filter(lambda f: f is not None, [ffprobe_output(f) for f in foi])

  # Find all files and offsets into each file that correspond to the given datetime
  logging.info('Finding matching files')
  matching_files = list(filter(lambda f: f['creation_time'] <= moi_timestamp <= f['end_time'], ffprobe))
  print("### Matching Files: ###")
  for f in matching_files:
    offset_in = moi_timestamp - f['creation_time']
    print(f['relpath'], offset_in)

  if (args.output):
    output_root = os.path.join(args.output, args.datetime)
    logging.info(f"Creating clips in f{args.output}")
    try:
      pathlib.Path(output_root).mkdir(parents=True, exist_ok=args.force)
    except FileExistsError:
      logging.error(f"The output path already exists. Enable --force if you want to override")
      sys.exit(1)
    for f in matching_files:
      output_filepath = os.path.join(output_root, f['relpath'].replace("/","_"))
      clip_offset = moi_timestamp - f['creation_time']
      cmd = f"ffmpeg -ss {clip_offset} -i \"{f['filepath']}\" -t {args.duration} -c copy \"{output_filepath}\""
      logging.info(f"Running {cmd}")
      lines = subprocess.check_output(cmd, shell=True)







