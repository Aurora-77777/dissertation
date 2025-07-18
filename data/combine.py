import pandas as pd
from difflib import get_close_matches

df_all_members = pd.read_csv("all_members.csv")
df_financial = pd.read_csv("mp_financial_interests.csv")
name_display_all = df_all_members['nameDisplayAs'].dropna().unique()
member_names = df_financial['Member'].dropna().unique()
mapping_display = {}
for name in member_names:
    match = get_close_matches(name, name_display_all, n=1, cutoff=0.8)
    if match:
        mapping_display[name] = match[0]

df_financial['Matched_nameDisplayAs'] = df_financial['Member'].map(mapping_display)

df_merged = pd.merge(
    df_financial,
    df_all_members[['nameDisplayAs', 'constituency']],
    left_on='Matched_nameDisplayAs',
    right_on='nameDisplayAs',
    how='left'
)

num_total_records = len(df_merged)
num_successful_matches = df_merged['constituency'].notna().sum()
num_unique_constituencies = df_merged['constituency'].nunique()
# print(df_merged['constituency'].unique())
print(f"Total number of records: {num_total_records}")
print(f"Records with matched constituency: {num_successful_matches}")
print(f"Unique constituencies matched: {num_unique_constituencies}")
df_merged.to_csv("financial_interests_with_constituency.csv", index=False)