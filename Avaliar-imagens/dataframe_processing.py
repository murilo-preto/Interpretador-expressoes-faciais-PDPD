import pandas as pd

df_1 = pd.read_csv("0-199_dataframe.csv")
df_2 = pd.read_csv("200-399_dataframe.csv")
df_3 = pd.read_csv("400-599_dataframe.csv")
df_4 = pd.read_csv("600-799_dataframe.csv")
df_5 = pd.read_csv("800-999_dataframe.csv")

df = pd.concat([df_1, df_2, df_3, df_4, df_5], ignore_index=True)
df.drop(["Unnamed: 0"], axis=1, inplace=True)

print(df)
df.to_csv("dataset_status.csv")