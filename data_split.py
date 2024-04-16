import chess.pgn
import pandas as pd
import glob
import numpy as np

#pgnFilePath =  r"\\wsl.localhost\Ubuntu\home\mdurrani\lichess_db_standard_rated_2024-03.pgn"
pgnFilePath = r'./data/*.pgn'
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
        if(totalGameCount % 2000 == 0): # print every 2000 games
            print("Total Game Count: ", totalGameCount)
            print("Eval Game Count: ", totalEvalGameCount)
        if(totalGameCount % 1000000 == 0):
            df = pd.DataFrame(rows_list) # add everything to the dataframe 
            df.to_csv(outputFilePath)
        if(len(variations) > 0 and 'eval' in variations[0].comment): # if this game was evaluated by a computer, add it
            totalEvalGameCount+=1
            h = game.headers
                
            # adding a dictionary is faster than appending to a dataframe 
            rows_list.append({
                "UTCDate": h.get("UTCDate", np.NaN),
                "UTCTime": h.get("UTCTime", np.NaN),
                'WhiteElo': h.get('WhiteElo', np.NaN),
                'BlackElo': h.get('BlackElo', np.NaN),
                "Opening": h.get("Opening", np.NaN),
                "ECO": h.get("ECO", np.NaN),
                'Result': h.get('Result', np.NaN),
                "Termination": h.get("Termination", np.NaN),
                "Variations": str(variations[0]) if variations else np.NaN,
                'WhiteRatingDiff': h.get('WhiteRatingDiff', np.NaN),
                'BlackRatingDiff': h.get("BlackRatingDiff", np.NaN)
            })

        # Iterator reading next game
        game = chess.pgn.read_game(pgn)          

