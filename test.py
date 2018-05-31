#!/usr/bin/python

import requests
import time
import string
import re

URL = "http://upe.42069.fun/piL60"
seq = "etaoinshrdlcumwfgypbvkjxqz"
alpha = []
file = open('file.txt', 'r')

for num in range (0, 500):
    alpha.append(0)

while True:
    for num in range (0, 100):
        alpha[num] = 0
    level = 1
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
              
        if status == ("DEAD") or status == ("FREE"):
            rate = data["win_rate"]
            games = data["games"]
            lyrics = data["lyrics"]
            print("WIN RATE:%f\n"
                %(rate))
            print("GAMES PLAYED:%f\n"
                %(games))
            print("LYRICS:%s\n"
                %(lyrics))
            break
        
        if remaining_guesses == 2:
            if done == 0:
                level = 1

        time.sleep(1)
        
        if level == 0:
            while alpha[ord(seq[i])-97] == -1:
                i += 1
            char = seq[i]
            alpha[ord(char)-97] = -1
            i += 1
        else:
            for num in range (0, 30):
                if alpha[num] >= 0:
                    alpha[num] = 0
            incomplete = 0
            exp = "^"
            for letter in state:
                if letter == '_':
                    incomplete = 1
                    exp += "."
                elif not letter.isalpha():
                    if incomplete == 1:
                        exp += "$"
                        file = open('file.txt', 'r')
                        uncertain = 0
                        for line in file:
                            if re.search(r""+exp, line, re.IGNORECASE):
                                valid = 1
                                for let in line:
                                    if alpha[ord(let)-97] < 0:
                                        check = 0
                                        for baselet in exp:
                                            if let == baselet:
                                                check = 1
                                                break
                                        if check == 0:
                                            valid = 0
                                            break
                                if valid == 1:
                                    uncertain += 1
                        file = open('file.txt', 'r')
                        for line in file:
                            if re.search(r""+exp, line, re.IGNORECASE):
                                valid = 1
                                for let in line:
                                    if alpha[ord(let)-97] < 0:
                                        check = 0
                                        for baselet in exp:
                                            if let == baselet:
                                                check = 1
                                                break
                                        if check == 0:
                                            valid = 0
                                            break
                                if valid == 0:
                                    continue
                                for let in line:
                                    if alpha[ord(let)-97] >= 0:
                                        if uncertain == 1:
                                            alpha[ord(let)-97] += 200
                                        if uncertain == 2:
                                            alpha[ord(let)-97] += 100
                                        if uncertain == 3:
                                            alpha[ord(let)-97] += 50
                                        if uncertain == 4:
                                            alpha[ord(let)-97] += 25
                                        alpha[ord(let)-97] += 1
                    exp = "^"
                    incomplete = 0
                else:
                    exp += letter
            if incomplete == 1:
                exp += "$"
                file = open('file.txt', 'r')
                uncertain = 0
                for line in file:
                    if re.search(r""+exp, line, re.IGNORECASE):
                        valid = 1
                        for let in line:
                            if alpha[ord(let)-97] < 0:
                                check = 0
                                for baselet in exp:
                                    if let == baselet:
                                        check = 1
                                        break
                                if check == 0:
                                    valid = 0
                                    break
                        if valid == 1:
                            uncertain += 1
                file = open('file.txt', 'r')
                for line in file:
                    if re.search(r""+exp, line, re.IGNORECASE):
                        valid = 1
                        for let in line:
                            if alpha[ord(let)-97] < 0:
                                check = 0
                                for baselet in exp:
                                    if let == baselet:
                                        check = 1
                                        break
                                if check == 0:
                                    valid = 0
                                    break
                        if valid == 0:
                            continue
                        for let in line:
                            if alpha[ord(let)-97] >= 0:
                                if uncertain == 1:
                                    alpha[ord(let)-97] += 200
                                if uncertain == 2:
                                    alpha[ord(let)-97] += 100
                                if uncertain == 3:
                                    alpha[ord(let)-97] += 50
                                if uncertain == 4:
                                    alpha[ord(let)-97] += 25
                                alpha[ord(let)-97] += 1
            maxy = 0
            c = 0
            for thing in range(0,30):
                if alpha[thing] > maxy:
                    maxy = alpha[thing]
                    c = thing
            if maxy == 0:
                done = 1
                level = 0
                while alpha[ord(seq[i])-97] == -1:
                    i += 1
                char = seq[i]
                alpha[ord(seq[i])-97] = -1
                i += 1

            alpha[c] = -1
            char = chr( c + 97 )
        
        print ("Guessed:", char)
        data = {"guess" : char}
        r = requests.post(url = URL, data = data)
        
    time.sleep(2)
