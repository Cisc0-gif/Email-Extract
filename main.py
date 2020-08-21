#! /usr/bin/env python3

import requests
import re
import os
import sys

username = os.getlogin()

print('[*] Current User: ' + str(username))

if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
  print('Email-Extract v1.0 Website Email-Extraction Tool')
  print('Sourced on Github and created by Cisc0-gif, Ecorp7@protonmail.com\n')
  print('        -h, --help                  This help menu')
  print('        -a, --auto                  Use dirb to automatically enumerate and parse website source')
  print('        -m, --manual <filename.*>   Import formatted file of website directories with return code 200')
  print('        -f, --format <filename.*>   Formats list of website directories to be parsed by Email-Extract')
  sys.exit(1)

short = ['-h', '-a', '-m', '-f']
long = ['--help', '--auto', '--manual', '--format']

tool = sys.argv[1]

if tool == '-a' or tool == '--auto':
  url = input('Enter site url: ')
  print('Enumerating site directories w/ dirb...')
  try:
    os.system('sudo dirb ' + str(url) + ' > dirb.txt')
  except:
    print(':ERROR: Is dirb installed?')
    exit()
  with open('dirb.txt', 'r') as f:
    contents = f.read()
    lines = contents.splitlines()
    cleanurls = []
    for i in lines:
      if "CODE:200" in i:
        cleanurls.append(i)
    str_clean = str(cleanurls)
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str_clean)
    emails = []
    for i in urls:
      content = requests.get(i).text
      email = re.findall('([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', content)
      emails.append(email)
    clean_emails = [x for x in emails if x]
    print('Emails Found: ')
    for i in clean_emails:
      for l in i:
        print(l)
    output = input("Do you want to output to 'emails.txt'[y/N]? ")
    if output.lower() == 'y':
      with open('emails.txt', 'w+') as f:
        for i in clean_emails:
          for l in i:
            f.write(l + '\n')
      f.close()
      print("Emails output to 'emails.txt'...")
    else:
      exit()
  f.close()

if tool == '-m' or tool == '--manual':
  try:
    inputfile = sys.argv[2]
  except:
    print(":ERROR: Input File Required")
    exit()
  print("Parsing '" + str(inputfile) + "' and scanning directories...")
  with open(inputfile, "r") as f:
    contents = f.read()
    lines = contents.splitlines()
    cleanurls = []
    for i in lines:
      if "CODE:200" in i:
        cleanurls.append(i)
    str_clean = str(cleanurls)
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str_clean)
    emails = []
    for i in urls:
      content = requests.get(i).text
      email = re.findall('([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', content)
      emails.append(email)
    clean_emails = [x for x in emails if x]
    print('Emails Found: ')
    for i in clean_emails:
      for l in i:
        print(l)
    output = input("Do you want to output to 'emails.txt'[y/N]? ")
    if output.lower() == 'y':
      with open('emails.txt', 'w+') as f:
        for i in clean_emails:
          for l in i:
            f.write(l + '\n')
      f.close()
      print("Emails output to 'emails.txt'...")
    else:
      exit()
  f.close()

if tool == '-f' or tool == '--format':
  try:
    inputfile = sys.argv[2]
  except:
    print(":ERROR: Input File Required")
    exit()
  print("Parsing '" + str(inputfile) + "', checking status codes, and formatting directories...")
  with open(inputfile, 'r') as f:
    contents = f.read()
  f.close()
  cleanurls = []
  urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', contents)
  for i in urls:
    code = requests.get(i).status_code
    if str(code) == "200":
      cleanurls.append(i)
  with open(inputfile, 'w') as f:
    for i in cleanurls:
      f.write(i + ' (CODE:200)\n')
  f.close()
  print("'" + str(inputfile) + "' formatted for email extraction, use -m to scan!")
