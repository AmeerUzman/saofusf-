import pandas as pd
#Load the messy dataset
df = pd.read_csv("IndieQuest_GameSales_Messy.csv")
#Detect missing values in each column
print("Missing values per column:")
missing_counts = df.isna().sum()
print(missing_counts)
print()
#Fill missing Rating values with the mean rating
#This handles gaps in qualitative data without losing the row.
df["Rating"] = df["Rating"].fillna(df["Rating"].mean())
#Drop rows where the Title is missing
#We drop these because a game record without a title is usually not useful for analysis.
df = df.dropna(subset=["Title"])
#Convert Revenue to numeric turning "N/A" strings into NaN, then fill with 0
df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce").fillna(0)
#Remove any completely duplicated rows
df = df.drop_duplicates()
# Final Check: Display cleaned data info and a preview
print("Cleaned DataFrame info:")
print(df.info())
print()
print("Preview of cleaned data:")
print(df.head())
print()