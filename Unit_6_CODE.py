import pandas as pd
import matplotlib.pyplot as plt
#Load and Inspect
#Goal: Load the dataset and see what we are working with

df = pd.read_csv("IndieQuest_GameSales.csv")
print("--- Dataset Overview ---")
print(df.head()) # Shows first 5 rows
print("\n--- Data Info ---")
df.info() # Shows column types and missing values

#Cleaning
#Identify and fix issues like missing values or duplicates
#Fix Ratings: Fill missing values with the average

df["Rating"] = df["Rating"].fillna(df["Rating"].mean())

#Fix Revenue: Convert to numeric (handling strings like 'N/A') and fill blanks with 0

df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce").fillna(0)

# Remove any duplicate records
df = df.drop_duplicates()

#Filter and Sort
#Goal: Answer specific questions through subsets of data
#Question 1: What are the highest-rated games (9.0 or higher)?

high_rated = df[df["Rating"] >= 9.0]
print("\n--- High Rated Games ---")
print(high_rated.head())

# Question 2: What are the top 5 Switch games by revenue?

switch_games = df[df["Platform"] == "Switch"]
top_5_switch = switch_games.sort_values(by="Revenue", ascending=False).head(5)
print("\n--- Top 5 Switch Games by Revenue ---")
print(top_5_switch)

#Group and Summarize

#Goal: Compute summaries to find trends
#Summary 1: Total Revenue by Platform

platform_revenue = df.groupby("Platform")["Revenue"].sum().reset_index()

print("\n--- Total Revenue by Platform ---")

print(platform_revenue)

#Summary 2: Average Rating by Genre

genre_rating = df.groupby("Genre")["Rating"].mean().reset_index()

print("\n--- Average Rating by Genre ---")

print(genre_rating)

#Visualization
# Goal: Create a chart to communicate findings

plt.figure(figsize=(10, 6))
plt.bar(platform_revenue["Platform"], platform_revenue["Revenue"], color='skyblue')
plt.title("Total Revenue by Platform")
plt.xlabel("Platform")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Data story narative
#Based on the output, PlayStation leads in revenue despite Switch having high volume.
#This cleaned data can be used for future Machine Learning to predict sales based on genre.
 