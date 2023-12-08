"""

Intent classification modelling file:
Creates an Intent Classification model using TensorFlow and Keras for NLP tasks.

Consists of methods to:
- Initialize paths
- Train model
- Save Trained Model
- Load Trained Model
- Predict intent

"""

import pickle
import pandas as pd
import numpy as np
import tensorflow as tf
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.metrics import Precision, Recall
from tensorflow.keras import utils
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import json

class IntentModel:
    def __init__(self, model_save_path, tokenizer_save_path, label_encoder_save_path):
        """
        Initialize paths to models, tokenizers, label encoders
        Set additional attributes initialized to None

        Args:
        - model_save_path:
        - tokenizer_save_path:
        - label_encoder_save_path:
        """

        self.model_save_path = model_save_path
        self.tokenizer_save_path = tokenizer_save_path
        self.label_encoder_save_path = label_encoder_save_path
        self.model_lstm = None
        self.tokenizer = None
        self.intent_encoder = None
        self.max_seq_size = None

    def train_model(self, df):
        """
        Method used to prepare data for tokenization, encoding, training, fitting the model

        Args:
        - df (DataFrame): DataFrame derived from intent classification dataset

        Execution:
        - Uses dataframe as input, containing columns 'sentence' and 'intent'
        - Splits the data into training and testing sets - test set occupying 20% (test_split_size) set aside for testing, used for evaluating perfomance metrics, including precision
        - Tokenizes and pads the sequences using the Keras 'Tokenizer' and 'pad_sequences'
        - Train and test intents are combined for label encoding fitting
        - One hot encoding technique used to convert categorical labels into one-hot encoded representations of the train and test intent labels
        - Builds and trains an LSTM model using Keras Sequential - dealing with layering of neural network models
        - Evaluate the model on the test set
        - Convert one-hot encoded predictions to class labels
        - Decode labels back to original intent labels
        - Print classification report
        - Saves the trained model, tokenizer, label encoder
        """

        test_split_size = 0.2
        val_split_size = 0.1
        random_state_size = 10
        batch_size = 32
        e = 9
        embed_space = 16
        units_size = 16

        np.random.seed(random_state_size)
        tf.random.set_seed(random_state_size)

        sentences = df["sentence"]
        intents = df["intent"]

        train_s, test_s, train_i, test_i = train_test_split(sentences, intents, test_size=test_split_size, random_state=random_state_size)

        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(list(train_s))

        train_s_seq = tokenizer.texts_to_sequences(list(train_s))
        test_s_seq = tokenizer.texts_to_sequences(list(test_s))

        max_seq_size = max(max(len(seq) for seq in train_s_seq), max(len(seq) for seq in test_s_seq))
        train_s_padded = pad_sequences(train_s_seq, maxlen=max_seq_size, padding='post')
        test_s_padded = pad_sequences(test_s_seq, maxlen=max_seq_size, padding='post')

        combined_i = pd.concat([train_i, test_i], axis=0)

        i_enc = LabelEncoder()
        i_enc.fit(combined_i)

        train_i_encoded = utils.to_categorical(i_enc.transform(train_i))
        test_i_encoded = utils.to_categorical(i_enc.transform(test_i))

        vocab_size = len(tokenizer.word_index) + 1
        classes_size = len(intents.unique())

        model_lstm = Sequential()
        model_lstm.add(Embedding(input_dim=vocab_size, output_dim=embed_space, input_length=max_seq_size, mask_zero=True))
        model_lstm.add(LSTM(units_size, activation='relu'))
        model_lstm.add(Dense(classes_size, activation='softmax'))

        model_lstm.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[Precision()])

        model_lstm.summary()

        lstm_history = model_lstm.fit(train_s_padded, train_i_encoded, batch_size=batch_size, epochs=e, verbose=1, validation_split=val_split_size)

        predictions = model_lstm.predict(test_s_padded)

        predicted_labels = np.argmax(predictions, axis=1)
        true_labels = i_enc.transform(test_i)

        decoded_predicted_labels = i_enc.inverse_transform(predicted_labels)
        decoded_true_labels = i_enc.inverse_transform(true_labels)

        print(classification_report(decoded_true_labels, decoded_predicted_labels))

        self.model_lstm = model_lstm
        self.tokenizer = tokenizer
        self.intent_encoder = i_enc
        self.max_seq_size = max_seq_size

    def save_model_and_tokenizer(self):
        """
        Saves the trained LSTM model, tokenizers and label encoders to JSON files

        Execution:
        - Saves the trained LSTM using Keras's save_model method
        - Serializes the tokenizers word index to JSON file
        - Saves the labels encoder to JSON file
        """

        if self.model_lstm is not None and self.tokenizer is not None and self.intent_encoder is not None:
            self.model_lstm.save(self.model_save_path)

            model_config = {
                "max_seq_size": self.max_seq_size
            }
            
            path = os.path.join(os.path.dirname(__file__), "../json/config.json")
            with open(path, 'w') as config_file:
                    json.dump(model_config, config_file)

            with open(self.tokenizer_save_path, 'w') as json_file:
                tokenizer_config = self.tokenizer.word_index
                json.dump(tokenizer_config, json_file)

            with open(self.label_encoder_save_path, 'w') as label_encoder_file:
                label_encoder_file.write(json.dumps(self.intent_encoder.classes_.tolist()))
        else:
            print("Model, tokenizer, or label encoder not available. Train the model first.")

    def load_model_and_tokenizer(self):
        """
        Loads the trained LSTM model, tokenizers, encoder, additional configurations

        Execution:
        - Load the trained LSTM model using Keras's load_model method
        - Load the tokenizers word index from JSON file
        - Load the label encoder from JSON file
        - Load 'max_seq_size' from configuration file - sequences padded length

        Returns:
        - True/False (boolean): indicating loading of models, tokenizers successful or unsuccessful
        """
        try:
            self.model_lstm = load_model(self.model_save_path)

            with open(self.tokenizer_save_path, 'r') as json_file:
                tokenizer_config = json.load(json_file)
                self.tokenizer = Tokenizer()
                self.tokenizer.word_index = tokenizer_config

            with open(self.label_encoder_save_path, 'r') as label_encoder_file:
                label_classes = json.loads(label_encoder_file.read())
                self.intent_encoder = LabelEncoder()
                self.intent_encoder.classes_ = label_classes

            path1 = os.path.join(os.path.dirname(__file__), "../json/config.json")
            with open(path1, 'r') as config_file:
                    model_config = json.load(config_file)
                    self.max_seq_size = model_config.get("max_seq_size")

            return True
        except Exception as e:
            print("Error loading model and tokenizer:", str(e))
            return False

    def predict_intent(self, sentence):
        """
        Predicts the intent for the sentence passed using the trained model

        Execution:
        - Tokenize and pad the input sentence and use the model to predict the intent

        Args:
        - sentence (string): Sentence passed to predict intent

        Returns:
        - predicted_intent (string): Sentence's classified intent
        """

        if self.model_lstm is not None and self.tokenizer is not None and self.intent_encoder is not None:
            sentence_seq = self.tokenizer.texts_to_sequences([sentence])
            sentence_features = pad_sequences(sentence_seq, maxlen=self.max_seq_size, padding='post')
            predicted_i = int(self.model_lstm.predict(sentence_features).argmax(axis=-1))
            predicted_intent = self.intent_encoder.classes_[predicted_i]
            return predicted_intent
        else:
            print("Model, tokenizer, or label encoder not available. Train the model first.")
