import pandas as pd 
import re
#from sklearn import preprocessing

# Read data back in from csv and ignore the first column because it just contains the indicies.
# We only want white and black elo, opening category, result, and variations
df= pd.read_csv("miniEvaluations.csv", usecols=["WhiteElo", "BlackElo", "ECO", "Result", "Variations"])

# All data will be from the perspective of white 

# Get mistake differential from a game
def getMistakeDifferential(variation):
    # Find all evaluations
    evalText = re.findall(r'%eval -?\d.\d*', variation)
    # Truncate text and get float eval value
    evalList = []
    for eval in evalText:
        evalList.append(float(eval.split(" ")[1]))

    # Find the mistake differential for white
    evalDifference = 0
    numberOfWhiteMistakes = 0
    numberOfBlackMistakes = 0
    for i in range(len(evalList)):
        if i != 0:
            evalDifference = evalList[i] - evalList[i-1]
        if abs(evalDifference) > 1:
            if i % 2 == 0:
                numberOfWhiteMistakes += 1
            else:
                numberOfBlackMistakes += 1
    whiteMistakeDifferential = numberOfWhiteMistakes - numberOfBlackMistakes
    return whiteMistakeDifferential

# Get time differential from a game
def getTimeDifferential(variation):
    # Find all clock text
    clockText = re.findall(r'%clk \d:\d{2}:\d{2}', variation)
    # Truncate text and get clock data in seconds
    clockList = []
    for clock in clockText:
        time = clock.split(" ")[1]
        hr = int(time.split(":")[0])
        min = int(time.split(":")[1])
        sec = int(time.split(":")[2])
        totalSeconds = hr * 3600 + min * 60 + sec
        clockList.append(totalSeconds)

    # Get clock differential
    whiteTimeElapsed = 0
    blackTimeElapsed = 0
    # If less than 2 moves, then don't worry about calculating time elapsed
    if len(clockList) >= 2:
        whiteBeginClock = clockList[0]
        blackBeginClock = clockList[1]
        if len(clockList) % 2 == 0:
            whiteEndClock = clockList[-2]
            blackEndClock = clockList[-1]
        else:
            whiteEndClock = clockList[-1]
            blackEndClock = clockList[-2]
        whiteTimeElapsed = whiteBeginClock - whiteEndClock
        blackTimeElapsed = blackBeginClock - blackEndClock

    whiteTimeDifferential = whiteTimeElapsed - blackTimeElapsed

    return whiteTimeDifferential

# Turn string result into a number result 
def getResultForWhite(result):
    if result == "0-1":
        return 0
    elif result == "1-0":
        return 1
    else:
        return 0.5

df["MistakeDifferential"] = df["Variations"].apply(getMistakeDifferential)

df["TimeDifferential"] = df["Variations"].apply(getTimeDifferential)

df["EloDifferential"] = df["WhiteElo"] - df["BlackElo"]

df["Result"] = df["Result"].apply(getResultForWhite)

df = df.drop(["Variations", "WhiteElo", "BlackElo"], axis=1)

print(df.head())