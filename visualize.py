import matplotlib.pyplot as plt
import prompts
import csv

def responseGraph(lisp):
    promptNum = list(range(50))
    responseAmt = []
    for i in range(50):
        responseAmt.append(0)
    responses = prompts.openFile('responses.csv')
    for row in responses:
        if row != []:
            placeholder = int(row[0])
            responseAmt[placeholder-1] = responseAmt[placeholder-1] + 1
    plt.bar(promptNum, responseAmt)
    plt.title("Total Responses per Prompt")
    plt.xlabel("Responses")
    plt.ylabel("Prompt #")
    plt.rcParams['text.color'] = "white"
    plt.rcParams['axes.labelcolor'] = "white"
    plt.rcParams['xtick.color'] = "orange"
    plt.rcParams['ytick.color'] = "brown"
    plt.savefig("frfresponse.png")

def contestantGraph(lisp):
    contst = []
    wb = responses = prompts.openFile('responses.csv')
    for row in responses:
        if row[2] not in contst:
            contst.append(row[2])
    print(contst)
    respAmt = []
    for i in contst:
        respAmt.append(0)
    print(respAmt)
    for row in responses:
        if row != []:
            respAmt[row[2].index] += 1
    plt.bar(contst, respAmt)
    plt.title("Contestants so far")
    plt.xlabel("Contestants")
    plt.ylabel("Responses Sent")
    plt.ylim(0,50)
    plt.rcParams['text.color'] = "white"
    plt.rcParams['axes.labelcolor'] = "white"
    plt.rcParams['xtick.color'] = "orange"
    plt.rcParams['ytick.color'] = "brown"
    plt.savefig("frfcontestants.png")

def voteGraph(lisp):
    contst = []
    for row in lisp:
        if row[2] not in contst:
            contst.append(row[2])
    print(contst)
    respAmt = []
    for i in contst:
        respAmt.append(0)
    print(respAmt)
    for row in lisp:
        respAmt[contst.index(row[2])] += 1
    plt.bar(contst, respAmt)
    plt.title("Average VPR")
    plt.xlabel("Prompt")
    plt.ylabel("Votes Sent per Response")
    plt.ylim(0,50)
    plt.rcParams['text.color'] = "white"
    plt.rcParams['axes.labelcolor'] = "white"
    plt.rcParams['xtick.color'] = "orange"
    plt.rcParams['ytick.color'] = "brown"
    plt.savefig("frfvotess.png")

