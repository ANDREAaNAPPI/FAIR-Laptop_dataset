# %%
import numpy as np
import pandas as pd
import re

# %%
df = pd.read_csv("Main_laptop_dataset.csv", encoding="Windows-1252")

# %%
print(df.shape[0])
print(df.shape[1])

# %%
df = df.iloc[:200]

# %%
# checking for duplicates
duplicates = df.duplicated(subset=[col for col in df.columns if col != 'laptop_ID'], keep='first')
num_duplicates = sum(duplicates)
print(num_duplicates)

# %%
df.head(35)
# %%
df['laptop_ID'] = df.index


# %%
unique_values = df['Company'].unique()
print(unique_values)

# %%
def remove_after_parenthesis(s):
    return s.split(' (')[0].strip()

df['Product'] = df['Product'].apply(remove_after_parenthesis)

# %%
def remove_between_space_and_quote(s):
    return re.sub(r' \S*"', '', s)

df['Product'] = df['Product'].apply(remove_between_space_and_quote)

# %%
unique_values = df['TypeName'].unique()
print(unique_values)
# %%
unique_values = df['Inches'].unique()
print(unique_values)

# %%
def remove_before_last_space(s):
    # Strip leading/trailing spaces to handle trailing spaces correctly
    s = s.rstrip()  
    last_space_index = s.rfind(' ')  # Find the index of the last space
    if last_space_index == -1:  # If no space found, return original string
        return s
    return s[last_space_index + 1:]

df['ScreenResolution'] = df['ScreenResolution'].apply(remove_before_last_space)

# %%
def extract_cpu_speed(cpu_string):
    # Find the index of the last space
    last_space_index = cpu_string.rfind(' ')
    if last_space_index == -1:  # No space found
        return cpu_string  # Return the original string
    return cpu_string[last_space_index + 1:]

df['CPU Speed'] = df['Cpu'].apply(extract_cpu_speed)

# %%

def delete_after_first_number(s):
    # Search for the first occurrence of a digit
    match = re.search(r'\d', s)  # Look for the first digit in the string
    if match:  # If a digit is found
        return s[:match.end()]  # Return everything up to and including the first digit
    return s

df['Cpu'] = df['Cpu'].apply(delete_after_first_number)

def delete_after_series(s):
    # Find the index of the word "Series"
    index = s.find("Series")
    if index != -1:  # If "Series" is found
        return s[:index + len("Series")]  # Return everything up to and including "Series"
    return s  

df['Cpu'] = df['Cpu'].apply(delete_after_series)


# %%
df['Ram'] = df['Ram'].str.replace("GB", "", case=False)

# %%
unique_values = df['OpSys'].unique()
print(unique_values)
# %%
df['Weight'] = df['Weight'].str.replace("kg", "", case=False)

# %%
changes_names = {"Product" : "Model",
                 "TypeName" : "Type",
                 "Inches": "Screen_Size",
                 "ScreenResolution" : "Screen_Resolution",
                 "Cpu":"CPU",
                 "Ram" : "RAM_Size",
                 "Memory" : "Storage",
                 "Gpu": "GPU",
                 "OpSys": "Operating_System",
                 "Price_in_euros":"Price_EUR",
                 "Weight": "Weight_KG",
                 "CPU Speed": "CPU_Speed"
                 }

df.rename(columns= changes_names, inplace=True)

# %%
# creating a function to get insights about the missing data
def nan_info(dataframe):
    nan_counts = dataframe.isnull().sum()
    total_rows = len(dataframe)
    nan_percentages = nan_counts / total_rows * 100
    nan_columns = nan_counts[nan_counts > 0].index.tolist()

    print("NaN Information:")
    print("Total Rows:", total_rows)
    print("\nColumns with NaN values:")
    print(nan_columns)

    if nan_columns:
        print("\nNaN Counts:")
        print(nan_counts[nan_columns])

        print("\nNaN Percentages:")
        print(nan_percentages[nan_columns])

nan_info(df)
# %%
df.to_csv('Main_laptop_dataset_CLEAN.csv', index=False)


# %%
