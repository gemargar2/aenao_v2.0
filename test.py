import pandas as pd

# Load the data into a pandas dataframe
df = pd.read_csv('data/vibration/vib_sample.csv', header=None)

# Check the existing header row
print(df.columns)

# Remove the header row
df = df.iloc[1:]

# Reset the index of the dataframe
df = df.reset_index(drop=True)

# Check the updated dataframe
print(df.head())

df.to_csv('data/vibration/copy_of_' + 'file.csv', index=False)