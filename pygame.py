import pandas as pd
import matplotlib.pyplot as plt

# 1. LOAD THE DATA
# Make sure the csv file is in the same folder as this script
df = pd.read_csv('video_games_sales.csv')

# Clean up column names just in case (strip spaces and make lowercase)
df.columns = df.columns.str.strip().str.lower()

# ---------------------------------------------------------
# PART 1: COMPUTE KPIs
# ---------------------------------------------------------

# KPI 1: Demand (Market Share %)
# Counts how many games are in each genre and divides by total games
genre_counts = df['genre'].value_counts()
total_games = len(df)
market_share = (genre_counts / total_games * 100).round(2)

# KPI 2: Performance (Average Global Sales)
# Average millions of copies sold per game in that genre
avg_sales = df.groupby('genre')['global_sales'].mean().round(2)

# KPI 3: Risk (Hit Rate > 1 Million Copies)
# Calculates what % of games in a genre sold more than 1.0 million units
hits = df[df['global_sales'] > 1.0].groupby('genre').size()
total_genre_games = df.groupby('genre').size()
hit_rate = ((hits / total_genre_games).fillna(0) * 100).round(2)

# KPI 4: Feasibility (Manual Complexity Score for Pygame)
# 1 = Easy, 5 = Hard. (Based on coding difficulty)
complexity_scores = {
    'Action': 4, 'Adventure': 3, 'Fighting': 4, 'Misc': 2, 'Platform': 2, 
    'Puzzle': 1, 'Racing': 3, 'Role-Playing': 5, 'Shooter': 3, 
    'Simulation': 3, 'Sports': 3, 'Strategy': 4
}
# Map these scores to the dataframe index
complexity = pd.Series(complexity_scores, name='Complexity')

# Combine all KPIs into one table to print
kpi_table = pd.DataFrame({
    'Market Share (%)': market_share,
    'Avg Sales (Millions)': avg_sales,
    'Hit Rate (>1M %)': hit_rate
})
# Add complexity column (handling genres that might be missing from our list)
kpi_table['Complexity (1-5)'] = kpi_table.index.map(complexity_scores).fillna(3)

print("--- KPI DATA FOR YOUR WORKSHEET ---")
print(kpi_table)
print("\n")

# ---------------------------------------------------------
# PART 2: VISUALIZE RESULTS (Make 2 Charts)
# ---------------------------------------------------------

# Chart 1: Average Sales by Genre (Bar Chart)
plt.figure(figsize=(12, 6))
avg_sales.sort_values(ascending=False).plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Average Global Sales by Genre (Performance)')
plt.ylabel('Global Sales (Millions)')
plt.xlabel('Genre')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('chart1_avg_sales.png') # Saves the image
plt.show()

# Chart 2: Market Saturation (Count of Games)
plt.figure(figsize=(12, 6))
genre_counts.sort_values(ascending=False).plot(kind='bar', color='salmon', edgecolor='black')
plt.title('Market Saturation: Number of Games by Genre')
plt.ylabel('Number of Titles Released')
plt.xlabel('Genre')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('chart2_saturation.png') # Saves the image
plt.show()