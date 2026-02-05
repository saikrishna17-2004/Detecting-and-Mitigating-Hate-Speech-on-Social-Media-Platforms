import pandas as pd

# Load dataset
df = pd.read_csv('data/sample_data.csv', comment='#')

print(f'Total rows: {len(df)}')
print(f'Hate speech: {df["label"].sum()}')
print(f'Non-hate speech: {(df["label"]==0).sum()}')
print(f'Duplicates found: {df.duplicated().sum()}')

# Remove duplicates
df_clean = df.drop_duplicates()

print(f'\nAfter removing duplicates: {len(df_clean)}')
print(f'Hate speech: {df_clean["label"].sum()}')
print(f'Non-hate speech: {(df_clean["label"]==0).sum()}')

# Save only 500 samples (250 each)
hate = df_clean[df_clean['label'] == 1].head(250)
non_hate = df_clean[df_clean['label'] == 0].head(250)

df_final = pd.concat([hate, non_hate]).sample(frac=1, random_state=42).reset_index(drop=True)

print(f'\nFinal dataset: {len(df_final)} samples')
print(f'Hate speech: {df_final["label"].sum()}')
print(f'Non-hate speech: {(df_final["label"]==0).sum()}')

# Add header comments
header = """# Hate Speech Detection Training Dataset
# Enhanced with 500 examples (250 hate speech + 250 non-hate speech)
# Format: text,label
# label: 0=non-hate, 1=hate speech
# Categories: racial, religious, gender, LGBTQ+, body-shaming, ageism, ableism, threats, and more
"""

with open('data/sample_data_final.csv', 'w', encoding='utf-8') as f:
    f.write(header)
    df_final.to_csv(f, index=False)

print('\n✅ Clean dataset saved to data/sample_data_final.csv')
