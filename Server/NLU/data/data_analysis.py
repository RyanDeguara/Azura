"""
Data analysis file, reads dataset as json, filter to optimise for desired intents, optimize distribution of dataset
Filter the DataFrames of slurp's train and train_synthetic datasets based on the list of allowed words
Replace 'qa_factoid' intents and associated sentences from train dataset and replace with those of train synthetic dataset for optimal distribution
Replace 'qa_factoid' with 'search_query' in the 'intent' column for better naming conventions
Save the result to SLURP.csv

To note:
Filtered out intents to be implemented in future, for now optimizing to work on the desired intents
"""

import pandas as pd

file_path = "slurp/train.jsonl"
file_path2 = "slurp/train_synthetic.jsonl"

df_train = pd.read_json(file_path, lines=True)
df_train.columns = ["slurp_id", "sentence", "sentence_annotation", "intent", "action", "tokens", "scenario", "recordings", "entities"]
df_train = df_train.drop(columns=['action', "tokens", "recordings", "entities"])
df_syn = pd.read_json(file_path2, lines=True)
df_syn.columns = ["slurp_id", "sentence", "sentence_annotation", "intent", "action", "tokens", "scenario", "recordings", "entities"]
df_syn = df_syn.drop(columns=['sentence_annotation','action','scenario', 'entities'])

allowed_intents = ["weather_query", "qa_factoid", "play_music", "datetime_query", "news_query", "email_sendemail", "calendar_set"]
allowed_intents2 = ["qa_factoid"]

filtered_df = df_train[df_train['intent'].isin(allowed_intents)]
filtered_df2 = df_syn[df_syn['intent'].isin(allowed_intents2)]

filtered_df = filtered_df[filtered_df['intent'] != 'qa_factoid']
filtered_df = filtered_df.append(filtered_df2[filtered_df2['intent'] == 'qa_factoid'], ignore_index=True)
filtered_df['intent'] = filtered_df['intent'].replace('qa_factoid', 'search_query')

filtered_df.to_csv('SLURP.csv', index=False)
