import pandas as pd

# import data
df = pd.read_csv('/Users/oliverbrown/Desktop/Oli/Renewable-Energy-Connect/cee-members.csv')
feet = "yo"
for k in range(len(df)):
    print(df['Member Name'][k])