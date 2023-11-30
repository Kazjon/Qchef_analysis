import glob, os, sys
import pandas as pd

folder_path = "data/extracted_user_reports/"

def retrieveUserSurpriseDetails(userID,recipeID):
    # load up that user's report file
    match_pattern = userID+"_ratings_*"
    file_list = glob.glob(os.path.join(folder_path, match_pattern))
    if len(file_list) != 1:
        print("Something weird happened, oh no.")
        print(recipeID)
        print(userID)
        sys.exit()
    for file_path in file_list:
        df = pd.read_csv(file_path)
    # Find the time they were recommended that recipe.
        matched_rows = df[df["recipeID"] == recipeID]
        matched_rows = matched_rows[matched_rows["picked"].str.contains("P")] 
        if len(matched_rows) != 1:
            print("Something weird happened, I can't handle this kind of pressure.")
            print(recipeID)
            print(userID)
            sys.exit()
        return {"Raw Surprise": matched_rows["rawSurp"].iloc[0], 
                "Predicted Surprise": matched_rows["predSurp"].iloc[0],
                "Predicted Unfamiliarity": matched_rows["predUnfam"].iloc[0],
                "Predicted Tastiness": matched_rows["predTaste"].iloc[0], 
                }
    # Return their predSurp,predUnfam,rawSurp and predTaste.