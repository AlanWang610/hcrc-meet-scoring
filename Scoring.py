import pandas as pd
import sys


print(sys.argv)
# read in data
athlete_data = pd.read_csv(sys.argv[1])
time_data = pd.read_csv(sys.argv[2])


# score teams
def team_scoring(df):
    team_counts = df['Team'].value_counts()
    scoring_data = df[df['Team'].isin(team_counts[team_counts >= 5].index)]
    sorted_times = scoring_data.sort_values('Times').reset_index(drop = True)
    team_dict = {}
    team_scores = {}
    place = 0
    for i in range(len(sorted_times)):
        # subsequent instances of team
        if sorted_times['Team'][i] in team_dict:
            # runner doesn't add to other team scores
            if team_dict[sorted_times['Team'][i]] >= 7:
                team_dict[sorted_times['Team'][i]] += 1
            # runner doesn't score but adds to other team scores
            elif team_dict[sorted_times['Team'][i]] >= 5:
                place += 1
                team_dict[sorted_times['Team'][i]] += 1
            # runner scores normally
            else:
                place += 1
                team_dict[sorted_times['Team'][i]] += 1
                team_scores[sorted_times['Team'][i]] += place
        # first instance of team
        elif sorted_times['Team'][i] not in team_dict:
            place += 1
            team_dict[sorted_times['Team'][i]] = 1
            team_scores[sorted_times['Team'][i]] = place
    return team_scores

# score individuals
def individual_scoring(df):
    return df.sort_values('Times').reset_index(drop = True)

# merge data
merged_data = athlete_data.merge(time_data, on = 'Bib', how = 'inner')
individual_result = individual_scoring(merged_data)
individual_result.index = individual_result.index + 1
individual_result.to_csv(sys.argv[1][:-4] + ' Individual Results.csv')
team_result = pd.DataFrame.from_dict(team_scoring(merged_data), orient = 'index')
team_result.columns = ['Score']
team_result.sort_values('Score').to_csv(sys.argv[1][:-4] + ' Team Results.csv')