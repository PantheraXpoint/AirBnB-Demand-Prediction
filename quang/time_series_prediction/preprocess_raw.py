import pandas as pd
import numpy as np

# Load the dataframes
df1 = pd.read_csv("Dataset/Raw_Embeddings/Road_Embeddings.csv")
df2 = pd.read_csv("Dataset/Raw_Embeddings/HumanFlow_Embeddings_kor.csv")
df3 = pd.read_csv("Dataset/Raw_Embeddings/AirBnB_Embeddings_with_name_mon.csv")

# Step 1: Prepare DataFrame 1 (expand for all 67 months)
unique_months = df3["Reporting Month"].unique()
unique_months.sort()  # Ensure chronological order
expanded_df1 = df1.loc[df1.index.repeat(len(unique_months))].reset_index(drop=True)
expanded_df1["Reporting Month"] = np.tile(unique_months, len(df1))
expanded_df1.rename(columns={"ADM_NM": "ADM_NM_key"}, inplace=True)

# Step 2: Align `기준일ID` in DataFrame 2 with `Reporting Month` in DataFrame 3
df2["Reporting Month"] = pd.to_datetime(df2["기준일ID"], format='%Y%m').dt.strftime('%Y-%m-%d')
df2.rename(columns={"행정동코드": "ADM_NM_key"}, inplace=True)
df3.rename(columns={"ADM_NM": "ADM_NM_key"}, inplace=True)

# Step 3: Create a Cartesian product of ADM_NM_key and Reporting Month to ensure all combinations
adm_nm_keys = df1["ADM_NM"].unique()
cartesian_product = pd.DataFrame(
    [(adm, month) for month in unique_months for adm in adm_nm_keys],
    columns=["ADM_NM_key", "Reporting Month"]
)

# Merge DataFrames to ensure all ADM_NM_key and Reporting Month pairs are included
merged_df = pd.merge(cartesian_product, expanded_df1, on=["ADM_NM_key", "Reporting Month"], how="left")
merged_df = pd.merge(merged_df, df2, on=["ADM_NM_key", "Reporting Month"], how="left")
merged_df = pd.merge(merged_df, df3, on=["ADM_NM_key", "Reporting Month"], how="left")

# Debug: Check merged_df shape
print(f"Merged DataFrame shape: {merged_df.shape}")

# Step 4: Prepare embeddings
embedding_cols_df1 = [col for col in df1.columns if col != "ADM_NM"]  # Maintain original order from df1
embedding_cols_df2 = [col for col in df2.columns if col not in ["ADM_NM_key", "Reporting Month", "기준일ID"]]  # Original order from df2
embedding_cols_df3 = [col for col in df3.columns if col not in ["ADM_NM_key", "Reporting Month"]]  # Extract all numerical columns from df3

# Combine embeddings from all three dataframes
embeddings = pd.concat([
    merged_df[embedding_cols_df1],  # Columns from df1
    merged_df[embedding_cols_df2],  # Columns from df2
    merged_df[embedding_cols_df3]   # Columns from df3
], axis=1).fillna(0.0).astype(float)  # Fill NaN values with 0.0 and ensure all columns are floats

# Debug: Check embeddings shape
print(f"Embeddings DataFrame shape: {embeddings.shape}")

# Convert the embeddings DataFrame to a NumPy matrix
final_embeddings_matrix = embeddings.values

# Debug: Check final_embeddings_matrix shape
print(f"Final embeddings matrix shape: {final_embeddings_matrix.shape}")

# Check for row count match with 28408
if final_embeddings_matrix.shape[0] == 28408:
    print("Row count matches the expected value: 28408.")
else:
    print(f"Row count mismatch: expected 28408, but got {final_embeddings_matrix.shape[0]}.")

# Step 5: Save as CSV
np.savetxt("quang/time_series_prediction/main_experiments/raw_embeddings/airbnb_raw_ver.csv", final_embeddings_matrix, delimiter=",", fmt="%.8f")  # Save embeddings
