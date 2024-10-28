import os
import random
import requests
import argparse
import math
import re

def quote_cleaner(quotes:list):
    formated_quotes = []
    for quote in quotes:
         formated_quotes.append(re.sub(r"\[.*?]", "", quote))
    return formated_quotes

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--image", action="store_true")
parser.add_argument("-t", "--text", action="store_true")
parser.add_argument("-c", "--count")

parser.add_argument("-o", "--output")

args = parser.parse_args()

if args.count:
    quote_count = int(args.count)
else:
    quote_count = None

if args.image:
    params = {
        'generate': 'true',
    }

    res = requests.get('https://inspirobot.me/api', params=params)

    if args.output:
        output_dir = args.output
    else:
        output_dir = "output"
    os.mkdir(output_dir)

    with open(f"{output_dir}/{res.text.split('/')[-1]}", "wb") as f:
        f.write(res.content)
elif args.text:
    quotes = []

    params = {
        'generateFlow': '1',
    }

    if quote_count == None:
        res = requests.get('https://inspirobot.me/api', params=params)

        data = res.json()["data"]

        quotes = quote_cleaner(quotes)

        for i in data:
            if i["type"] == "quote":
                quotes.append(i["text"])

        print(random.choice(quotes))
    else:
        for i in range(math.ceil(quote_count/3)):
            res = requests.get('https://inspirobot.me/api', params=params)

            data = res.json()["data"]

            for i in data:
                if i["type"] == "quote":
                    quotes.append(i["text"])

        quotes = quote_cleaner(quotes)

        count = 0

        for i in quotes:
            if count != quote_count:
                print(f"{count+1}. {i}")
                count += 1
