# coding: utf-8
import argparse
import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore

parser = argparse.ArgumentParser()
parser.add_argument('dir', help='dir for downloading web pages')
args = parser.parse_args()


nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created "soft" magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''
bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Credence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''
history = {}


def load_url(final_url):
    r = requests.get(f'https://{final_url}')
    history[final_url[:-4]] = final_url
    soup = BeautifulSoup(r.content, 'html.parser')
    paragraphs = soup.find_all(['p', 'title'])
    url_file = f'{args.dir}//{final_url[:-4]}.txt'
    with open(url_file, 'w') as file:
        file.write("")
    with open(url_file, 'r+') as file:
        for p in paragraphs:
            if p.find_all('a'):
                print(Fore.BLUE + p.text)
            else:
                print(Fore.WHITE + p.text)
            print(p.text, file=file, sep='\n')


def get_url():
    url = input()
    if url == 'exit':
        exit()
    elif url == 'back':
        with open(f'{args.dir}//{history[-2]}.txt', 'r', encoding='utf-8') as file:
            data = file.read()
            print(data)
    else:
        if not url.startswith('https://') and not url.startswith('http://') and url.__contains__('.'):
            load_url(url)

        elif url.startswith('https://') or url.startswith('http://'):
            load_url(url.replace('https://', '').replace('http://', ''))

        elif url in history:
            with open(f'{args.dir}//{url}.txt', 'r') as file:
                data = file.read()
                print(data)

        else:
            print("Invalid URL")


if len(sys.argv) > 2:
    print("Error more than 2 arguments were given.")
    exit()
try:
    os.mkdir(os.getcwd() + '/' + args.dir)
except FileExistsError as e:
    pass

while True:
    get_url()
