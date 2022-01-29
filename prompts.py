import csv

def openFile(string):
    opened = open(string)
    ready = csv.reader(opened)
    prompts = list(ready)
    return prompts

def getPrompt(number, listy):
    if number <= 50 and number >= 1:
        prompt = listy[number-1][1]
    else:
        prompt = "It's called :sparkles: 50 :sparkles: Round February. Not " + str(number) + " Round February."
    return prompt

async def getResponse(string, num, id, file):
    opened = open(file)
    ready = csv.reader(opened)
    responses = list(ready)
    opened.close()
    alert = []
    current = []
    valid = True
    if num <= 50 and num >= 1:
        for row in responses:
           if int(row[0]) == num:
                if row[2] == id:
                    responses.remove(row)
        current = [num, string, id, True]
        alert.append("Response " + str(num) + " has been recorded as: " + string)
        spaces = 0
        for char in string:
            if char == " ":
                spaces = spaces + 1
        if spaces >= 10:
            current = [num, string, id, False]
            alert.append("Response " + str(num) + " is over 10 words. Check for word count and/or double spaces.")
        tech = techCheck(num, string)
        if tech != []:
            current = [num, string, id, False]
            for whoops in tech:
                alert.append(whoops)
        if num == 14:
            alert.append("Response 14 is " + str(len(string)) + " characters.")
    else:
        alert.append("It's called :sparkles: 50 :sparkles: Round February. Not " + str(num) + " Round February.")
    opend = open(file, 'w')
    ready = csv.writer(opend, lineterminator = '\n')
    responses.append(current)
    for row in responses:
        ready.writerow(row)
    opend.close()
    return alert

def obtainResponse(list, id, num):
    response = ""
    exist = False
    for row in list:
        if row[0] == num:
            if row[2] == id:
                exist = True
                response = "Response " + str(row[0]) + ": " + row[1]
    if exist == False:
       response = "You have not submitted a response for prompt " + num + " yet."
    return response



def obtainAll(list, id):
    list.sort()
    newList = []
    for row in list:
        if row[2] == id:
            newList.append(row)
    return newList

def techCheck(num, string):
    alert = []
    if num == 7:
        words = string.split()
        for i in words[:-1]:
            if len(i) > len(words[words.index(i) + 1]):
                alert.append("Response 7 breaks the technical (\"" + i + "\" has more characters than \"" + words[words.index(i) + 1] + "\").")
    if num == 21:
        zees = 0
        for char in string:
            if char == "z":
                zees = zees + 1
            elif char == "Z":
                zees = zees + 1
        if zees < 4:
            alert.append("Response 21 does not contain enough z's (" + str(zees) + "/4).")
    if num == 28:
        acns = 0
        requiredLetters = ['A', 'C', 'N', 'a', 'c', 'n']
        for char in string:
            for i in requiredLetters:
                if char == i:
                    acns = acns + 1
        if acns != 10:
            alert.append("Response 28 does not have enough A\'s, C\'s, or N\'s (" + str(acns) + "/10)")
    if num == 35:
        periods = 0
        for char in string:
            if char == ".":
                periods = periods + 1
        if periods < 5:
            valid = False
            alert.append("Response 35 does not contain enough periods (" + str(periods) + "/10).")
    if num == 42:
        vowels = 0
        consonants = 0
        str1 = string.lower()
        for i in str1:
            if (ord(i) == 65 or ord(i) == 69 or ord(i) == 73
                    or ord(i) == 79 or ord(i) == 85
                    or ord(i) == 97 or ord(i) == 101 or ord(i) == 105
                    or ord(i) == 111 or ord(i) == 117):
                vowels = vowels + 1
            elif ((ord(i) >= 97 and ord(i) <= 122) or (ord(i) >= 65 and ord(i) <= 90)):
                consonants = consonants + 1
        if vowels != consonants:
            alert.append("Response 42 does not contain an equal amount of vowels and consonants (" + str(vowels) + " vowels and " + str(consonants) + " consonants).")
    if num == 49:
        stringCopy = string
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for ele in stringCopy:
            if ele in punc:
                stringCopy = stringCopy.replace(ele, "")
        stringSplit = stringCopy.split()
        promptList = openFile("csvtest.csv")
        for row in promptList:
            promptInd = row[1]
            for ele in promptInd:
                if ele in punc:
                    promptInd = promptInd.replace(ele, "")
            promptWords = promptInd.split()
            for i in promptWords:
                for j in stringSplit:
                    if i.lower() == j.lower():
                        stringSplit.remove(j)
        if stringSplit != []:
            alertWords = ""
            for i in stringSplit:
                alertWords = alertWords + i + ", "
            alert.append("Response 49 contains words not found in any of the prompts: " + alertWords)
    return alert
