import pandas as pd

# Starter data
books = [
    {"title": "Data Magic", "pages": 220, "genre": "CS"},
    {"title": "History of Time", "pages": 310, "genre": "Science"},
    {"title": "Poems at Midnight", "pages": 120, "genre": "Literature"},
    {"title": "Python for All", "pages": 280, "genre": "CS"},
    {"title": "World Stories", "pages": 195, "genre": "Literature"}
]

# Task 1: Create the DataFrame
df_books = pd.DataFrame(books)
print("Full df_books Table")
print(df_books)
print()

# Task 2: Inspect the structure
print("Shape and Columns")
print("Shape:", df_books.shape)
print("Columns:", df_books.columns)
print()

# Task 3:Select columns
titles = df_books["title"]

# Selecting CS books (Filtering) and specific columns
# We filter for genre "CS", then select only "title" and "pages" columns
df_cs = df_books[df_books["genre"] == "CS"][["title", "pages"]]
print("--- CS Books Only ---")
print(df_cs)
print()

# Task 4:Select rows
third_book = df_books.iloc[2]   # Index 2 is the 3rd item (0, 1, 2)
fourth_row = df_books.loc[4]    # Row with index label 4

print("Third Book (iloc[2]):")
print(third_book)
print("\nRow Index 4 (loc[4]):")
print(fourth_row)

# Task 5: Reflection
# Both examples use a list of dictionaries where each dictionary 
# represents one row and the keys represent the column headers.