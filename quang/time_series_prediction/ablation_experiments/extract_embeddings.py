import pandas as pd

# Load the input CSV file
input_file = "/disk1/jupyter/hongju/Ubiquitos_Computing_Project/quang/time_series_prediction/main_experiments/raw_embeddings/airbnb_raw_ver.csv"  # Replace with your input file name
df = pd.read_csv(input_file, header=None)

# Split the dataframe into 3 parts
df1 = df.iloc[:, :23]  # First 23 columns
df2 = df.iloc[:, 23:23+35]  # Next 35 columns
df3 = df.iloc[:, 23+35:23+35+692]  # Remaining 3072 columns

# Combine the required dataframes
df1_df2 = pd.concat([df1, df2], axis=1)
df1_df3 = pd.concat([df1, df3], axis=1)
df2_df3 = pd.concat([df2, df3], axis=1)

# Save the dataframes to CSV files
# df2.to_csv("hf_embeddings.csv", index=False, header=False)
df3.to_csv("/disk1/jupyter/hongju/Ubiquitos_Computing_Project/quang/time_series_prediction/ablation_experiments/embeddings/airbnb_raw_embeddings.csv", index=False, header=False)
# df1_df2.to_csv("road_hf_embeddings.csv", index=False, header=False)
df1_df3.to_csv("/disk1/jupyter/hongju/Ubiquitos_Computing_Project/quang/time_series_prediction/ablation_experiments/embeddings/road_airbnb_raw_embeddings.csv", index=False, header=False)
df2_df3.to_csv("/disk1/jupyter/hongju/Ubiquitos_Computing_Project/quang/time_series_prediction/ablation_experiments/embeddings/hf_airbnb_raw_embeddings.csv", index=False, header=False)

print("CSV files created successfully!")
