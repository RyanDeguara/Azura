"""

Query Classification file:
Consists of IntentClassifier class containing initialize_model and intent and entity classification methods

"""

import os
import pandas as pd
import spacy
from .models.model import IntentModel

class IntentClassifier:
    def __init__(self):
        """
        Initialize configuration files including models, tokenizers, encoders
        Model, tokenizer, encoder relative paths passed in instantiation of IntentModel - intent classification model
        spaCy's medium model loaded for entity extraction
        """
        self.model_path = os.path.join(os.path.dirname(__file__), "models/lstm_model.h5")
        self.tokenizer_path = os.path.join(os.path.dirname(__file__), "json/tokenizer.json")
        self.label_encoder_path = os.path.join(os.path.dirname(__file__), "json/label_encoder.json")
        self.data_path = os.path.join(os.path.dirname(__file__), "data/SLURP.csv")
        self.slurp_model = IntentModel(self.model_path, self.tokenizer_path, self.label_encoder_path)
        self.entity_extract = spacy.load("en_core_web_md")

    def initialize_model(self):
        """
        Initialization method to check if model_path containing intent classification model exists

        Execution:
        If doesnt exist:
        - Reads SLURP dataset from path into a pandas dataframe
        - Calls to train model passing dataframe
        - Call to save the trained model and tokenizer
        Call to load existing model and tokenizer from IntentModel instance, if True returned from method (indicating
        model loaded successfully) then:
        - Print messaging indicating successful model loading
        """

        if not os.path.exists(self.model_path):
            print("Creating the model as it does not exist in the path.")
            slurp_df = pd.read_csv(self.data_path)
            self.slurp_model.train_model(slurp_df)
            self.slurp_model.save_model_and_tokenizer()

        if self.slurp_model.load_model_and_tokenizer():
            print("Model and tokenizer loaded successfully.")

    def classify_intent_and_entities(self, sentence):
        """
        Method used to classify sentence into its intent and entities/labels.

        Args:
        - sentence (string): Sentence passed to predict intent, entities

        Execution:
        - Call to predict_intent method passing sentence from IntentModel instance, returns predicted_intent (string)
        - Call to spaCy's 'medium' entity extraction model passing sentence, returns doc (spacy.tokens.Doc class) containing tokens, tagging, NER (entities)
        - Iterate over entities found in the 'doc' object, returning a list of tuples each containing the text of named entities 'ent.text' and associated entity label 'ent.label_'
        - Create list of entity labels by extracting second element of each tuple
        - Create list of entity texts by extracting first element of each tuple

        Returns:
        - predicted_intent (string): Sentence's classified intent type
        - entity_labels (list): List of entity labels
        - entities (list): List of entity texts
        """

        predicted_intent = self.slurp_model.predict_intent(sentence)
        doc = self.entity_extract(sentence)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        entity_labels = [label for (_, label) in entities]
        entity_texts = [text for (text, _) in entities]
        return predicted_intent, entity_labels, entity_texts

