import chess.pgn
import pandas as pd
import glob

pgnFilePath =  r"C:\Users\mdurr\Code\cmsc320\final\data\*.pgn"
# pgnFilePath = r"C:\Users\pranavshah\Code\320\cmsc320_final_project\data\*.pgn"
outputFilePath = "./evaluations.csv"
totalGameCount = 0
totalEvalGameCount = 0
fileList = glob.glob(pgnFilePath) # modify this line for the directory that has all the pgn files 
rows_list = [] # list of dictionaries for each game 
for file in fileList:
    pgn = open(fileList[0])
    game = chess.pgn.read_game(pgn)
    while game != None:
        totalGameCount += 1
        variations = game.variations # list of either the eval or clock score
        if(totalGameCount % 100 == 0): # print every 2000 games
            print("Total Game Count: ", totalGameCount)
            print("Eval Game Count: ", totalEvalGameCount)
        if(len(variations) > 0 and 'eval' in variations[0].comment): # if this game was evaluated by a computer, add it
            totalEvalGameCount+=1
            h = game.headers
            # adding a dictionary is faster than appending to a dataframe 
            rows_list.append({"UTCDate": h["UTCDate"], "UTCTime": h["UTCTime"], 'WhiteElo':h['WhiteElo'], 'BlackElo':h['BlackElo'], "Opening": h["Opening"], "ECO":h["ECO"],'Result':h['Result'], "Termination": h["Termination"], "Variations":str(variations[0]), 'WhiteRatingDiff':h['WhiteRatingDiff'], 'BlackRatingDiff':h["BlackRatingDiff"]})
        # Iterator reading next game
        game = chess.pgn.read_game(pgn)

df = pd.DataFrame(rows_list) # add everything to the dataframe 
df.to_csv(outputFilePath)             

