#! /usr/bin/env python3

import requests
import re
import os

auto = input('Do you want to automatically enumerate site w/ dirb?[y/N]: ')
if auto.lower() == 'y':
  url = input('Enter site url here: ')
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
else:
  inputfile = input('Enter site enumeration filename here: ')
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
