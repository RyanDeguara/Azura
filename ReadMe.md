# Azura - A Raspberry Pi powered virtual assistant

Student Name: Ryan Deguara

Student Number: C20309873

## Execution:
1. Server -> server-engine.py (trains model upon first time execution)
2. Client -> client-engine.py

## User interaction:
1. Invoke Azura by saying "Hey Azura"
2. Prompt a query to Azura, for example: "What is the weather in Ireland?"
3. A response is then outputted

## Description:
Employs a client-server paradigm, server should be booted up to do classification processing
in the back.
Client engine can then be ran, 

## Structure:
Consists of four main modules: 
1. Wake Word - Prompting Azura with wake word - "Hey Azura"
2. Speech Recognition - Prompting Azura with user query - "What's the weather in Ireland"
3. NLU:
   - Server Side: Processing of user query, broken down into an intent and entities
   - Client Side: Returned intent used to call action to call associated APIs passing entities, 
                  returned data parsed to form a sentence in response to user query.
4. Speech Synthesis - sentence formed is outputted to user in audio form - "Ireland will have temperature of 2.07 Degrees Celsius with some overcast clouds"

```
Client
- client-engine.py (root engine file)
- WakeWord
   - wake_detector.py
   - models
    - hey-azura_en_raspberry-pi_v3_0_0.ppn
- SpeechRecognition
   - audio_transcribe.py
- NLU
   - action_handler.py
   - Actions
    - datetime_query_action.py
    - weather_query_action.py
    - ....
- Speech Synthesis
    - speech_synthesizer.py

Server
- svr.py (root engine file)
- NLU
 - intentclassifier.py
 - data
   - data_analysis.py
   - SLURP.csv
   - slurp
    - devel.jsonl
    - metadata.json
    - test.jsonl
    - train.jsonl
    - train_synthetic.jsonl
 - json
   - config.json
   - label_encoder.json
   - tokenizer.json
 - models
   - model.py
   - lstm_model.h5
```
   
## Requirements:

```
- python3
- pandas
- spacy 3.7.2
- requests 2.31.0
- spacy download en_core_web_md
- numpy 1.25.2
- openai 0.28.1
- openai-whisper 20230918
- pandas 2.1.1
- pyaudio 0.2.11
- scikit-learn 1.3.1
- scipy 1.11.2
- spacy 3.7.2
- tensorflow 2.14.0
- pvporcupine 3.0.0
- playsound 1.3.0
- gTTS 2.4.0
- Flask 1.1.2
```

## References

pswietojanski/slurp: Repository for SLURP [Internet]. [cited 2023 Dec 1]. Available from: https://github.com/pswietojanski/slurp/tree/master


