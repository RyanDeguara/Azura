"""
Server Root executed file, culmination of server side NLU functionality
- Flask server application booted
- Loads classifier models
- Method classify_intent called upon server application routed with '/classify-intent' of POST REST API method

To note:
- Temporary Flask server application method, migration to running on cloud server to be done
"""

from flask import Flask, jsonify, request
from NLU.intentclassifier import IntentClassifier

app = Flask(__name__)
classifier = IntentClassifier()
classifier.initialize_model()

@app.route('/classify-intent', methods=['POST'])
def classify_intent():
    """
    classify_intent called to grab text passed through POST request
    Uses loaded models returned from IntentClassifier's initialize_model method to classify text's intent and entities

    Returns:
    - intent: classification of query request type
    - entities: important pieces of information residing in sentence
    - labels: labels associated to entities
    """
    text = request.json['text']
    intent, entities, labels = classifier.classify_intent_and_entities(text)
    return jsonify({"intent": intent, "entities": entities, "labels": labels})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
