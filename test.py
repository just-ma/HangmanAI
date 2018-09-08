#!/usr/bin/python

import requests
import time
import string
import re

URL = "http://upe.42069.fun/piL60"
seq = "etaoinshrdlcumwfgypbvkjxqz"
alphabet = []                       #alphabet frequency list. -1 means the letter has been guessed already. Any number greater denotes how many times it shows up in possible words
file = open('file.txt', 'r')

for num in range (0, 25):           #initialize alphabet frequency list
    alphabet.append(0)

while True:
    for num in range (0, 25):       #reset frequency to 0 for new game
        alphabet[num] = 0
    level = 0                       #reset level (initial state) to 0
    gameOver = 0
    i = 0
    r = requests.get(url = URL)
    
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
        
        if remaining_guesses == 2:      #if the last guess was wrong, switch to level 1
            if gameOver == 0:
                level = 1

        time.sleep(1)
        
        if level == 0:                  #start with first letter not already guessed
            while alphabet[ord(seq[i])-97] == -1:
                i += 1
            char = seq[i]
            alphabet[ord(char)-97] = -1
            i += 1
        else:                           #determine all possible words
            for num in range (0, 30):
                if alphabet[num] >= 0:
                    alphabet[num] = 0
            incomplete = 0
            exp = "^"
            for letter in state:
                if letter == '_':
                    incomplete = 1
                    exp += "."
                elif not letter.isalphabet():
                    if incomplete == 1:
                        exp += "$"
                        file = open('file.txt', 'r')
                        uncertain = 0
                        for line in file:
                            if re.search(r""+exp, line, re.IGNORECASE):
                                valid = 1
                                for let in line:
                                    if alphabet[ord(let)-97] < 0:
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
                                    if alphabet[ord(let)-97] < 0:
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
                                    if alphabet[ord(let)-97] >= 0:  #add weights when less than 5 words are possible
                                        if uncertain == 1:
                                            alphabet[ord(let)-97] += 200
                                        if uncertain == 2:
                                            alphabet[ord(let)-97] += 100
                                        if uncertain == 3:
                                            alphabet[ord(let)-97] += 50
                                        if uncertain == 4:
                                            alphabet[ord(let)-97] += 25
                                        alphabet[ord(let)-97] += 1
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
                            if alphabet[ord(let)-97] < 0:
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
                            if alphabet[ord(let)-97] < 0:
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
                            if alphabet[ord(let)-97] >= 0:
                                if uncertain == 1:
                                    alphabet[ord(let)-97] += 200
                                if uncertain == 2:
                                    alphabet[ord(let)-97] += 100
                                if uncertain == 3:
                                    alphabet[ord(let)-97] += 50
                                if uncertain == 4:
                                    alphabet[ord(let)-97] += 25
                                alphabet[ord(let)-97] += 1
            maxWeight = 0
            c = 0
            for k in range(0,25):
                if alphabet[k] > maxWeight:     #go through list of frequencies and find highest one
                    maxWeight = alphabet[k]
                    c = k
            if maxWeight == 0:
                gameOver = 1
                level = 0
                while alphabet[ord(seq[i])-97] == -1:
                    i += 1
                char = seq[i]
                alphabet[ord(seq[i])-97] = -1
                i += 1

            alphabet[c] = -1                    #mark guessed one as -1 in frequency list
            char = chr( c + 97 )
        
        print ("Guessed:", char)
        data = {"guess" : char}
        r = requests.post(url = URL, data = data)   #submit guessed letter
        
    time.sleep(2)
