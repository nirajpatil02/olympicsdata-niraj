import pandas as pd

df=pd.read_csv(r'https://drive.google.com/file/d/1k8zhTyDeY_O9R9GF7uPhsETTs6wRcFll/view?usp=drive_link')
region_df=pd.read_csv(r'https://drive.google.com/file/d/13epMolX7mrWfTqpwWNKAmUYrjYShaExN/view?usp=drive_link')

def preprocess(df,region_df):

    df = df[df['Season'] == 'Summer']

    df = df.merge(region_df, on='NOC', how='left')

    df.drop_duplicates(inplace=True)
    #one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df
