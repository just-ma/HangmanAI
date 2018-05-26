#!/usr/bin/python

import requests
import time
import string
import re

URL = "http://upe.42069.fun/O936B"
seq = "etaoinshrdlcumwfgypbvkjxqz"
alpha = []
file = open('file.txt', 'r')

for num in range (0, 500):
    alpha.append(0)

while True:
    level = 0
    done = 0
    r = requests.get(url = URL)
    i = 0
    
    while True:
        data = r.json()

        state = data["state"]
        status = data["status"]
        remaining_guesses = data["remaining_guesses"]

        print("STATE:%s\nSTATUS:%s\nREMAINING GUESSES:%d\n"
              %(state, status, remaining_guesses))
              
        if status == ("DEAD"):
            rate = data["win_rate"]
            print("WIN RATE:%f\n"
                %(rate))
            break

        if status == ("FREE"):
            rate = data["win_rate"]
            print("WIN RATE:%f\n"
                %(rate))
            break

        if remaining_guesses == 2:
            if done == 0:
                level = 1
        
        
        if level == 0:
            char = seq[i]
            alpha[ord(char)-97] = -1
            i += 1
        else:
            for num in range (0, 256):
                if alpha[num] >= 0:
                    alpha[num] = 0
            incomplete = 0
            exp = "^"
            for letter in state:
                if letter == '_':
                    incomplete = 1
                    exp += "."
                elif letter == ' ':
                    if incomplete == 1:
                        exp += "$"
                        file = open('file.txt', 'r')
                        for line in file:
                            if re.search(r""+exp, line, re.IGNORECASE):
                                for let in line:
                                    if alpha[ord(let)-97] >= 0:
                                        alpha[ord(let)-97] += 1
                    exp = "^"
                    incomplete = 0
                else:
                    exp += letter
            if incomplete == 1:
                exp += "$"
                file = open('file.txt', 'r')
                for line in file:
                    if re.search(r""+exp, line, re.IGNORECASE):
                        for let in line:
                            if alpha[ord(let)-97] >= 0:
                                alpha[ord(let)-97] += 1
            maxy = 0
            c = 0
            for thing in range(0,256):
                if alpha[thing] > maxy:
                    maxy = alpha[thing]
                    c = thing
            if maxy == 0:
                done = 1
                level = 0

            alpha[c] = -1
            char = chr( c + 97 )

        print ("Guessed:", char)
        data = {"guess" : char}
        r = requests.post(url = URL, data = data)
        
        
        time.sleep(1)
    
    time.sleep(2)
