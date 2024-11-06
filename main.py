#!/bin/python3

import os
import random
import requests
import argparse
import math
import re
import threading

def banner():
    ban = """ ______                                               ____            __      
/\\__  _\\                          __                 /\\  _`\\         /\\ \\__   
\\/_/\\ \\/     ___     ____  _____ /\\_\\  _ __   ___    \\ \\ \\L\\ \\    ___\\ \\ ,_\\  
   \\ \\ \\   /' _ `\\  /',__\\/\\ '__`\\/\\ \\/\\`'__\\/ __`\\   \\ \\  _ <'  / __`\\ \\ \\/  
    \\_\\ \\__/\\ \\/\\ \\/\\__, `\\ \\ \\L\\ \\ \\ \\ \\ \\//\\ \\L\\ \\   \\ \\ \\L\\ \\/\\ \\L\\ \\ \\ \\_ 
    /\\_____\\ \\_\\ \\_\\/\\____/\\ \\ ,__/\\ \\_\\ \\_\\\\ \\____/    \\ \\____/\\ \\____/\\ \\__\\
    \\/_____/\\/_/\\/_/\\/___/  \\ \\ \\/  \\/_/\\/_/ \\/___/      \\/___/  \\/___/  \\/__/
                             \\ \\_\\                                            
                              \\/_/                                            
    """
    print(ban)

banner()

def quote_cleaner(quotes):
    return [re.sub(r"\[.*?]", "", quote) for quote in quotes]

def download_image(output_dir):
    res = requests.get('https://inspirobot.me/api', params={'generate': 'true'})
    image_res = requests.get(res.text)
    file_path = os.path.join(output_dir, res.text.split('/')[-1])
    with open(file_path, "wb") as f:
        f.write(image_res.content)
    print(f"Downloaded: {file_path}")

def fetch_quotes(quotes, batch_size=3):
    params = {'generateFlow': '1'}
    for _ in range(batch_size):
        res = requests.get('https://inspirobot.me/api', params=params)
        data = res.json()["data"]
        quotes.extend([i["text"] for i in data if i["type"] == "quote"])

def threaded_image_download(count, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    threads = [threading.Thread(target=download_image, args=(output_dir,)) for _ in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def threaded_quote_fetch(count):
    quotes = []
    threads = []
    for _ in range(math.ceil(count / 3)):
        thread = threading.Thread(target=fetch_quotes, args=(quotes, 3))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return quote_cleaner(quotes)[:count]

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", action="store_true")
parser.add_argument("-t", "--text", action="store_true")
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-c", "--count", type=int)
parser.add_argument("-o", "--output")
args = parser.parse_args()

quote_count = args.count if args.count else None
output_dir = args.output if args.output else "output"

if args.image:
    if quote_count:
        threaded_image_download(quote_count, output_dir)
    else:
        download_image(output_dir)

elif args.text:
    if quote_count:
        quotes = threaded_quote_fetch(quote_count)
        for count, quote in enumerate(quotes, start=1):
            print(f"{count}. {quote}")
    else:
        quotes = threaded_quote_fetch(3)
        print(random.choice(quotes))

else:
    parser.print_help()
