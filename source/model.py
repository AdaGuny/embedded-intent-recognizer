import numpy
from sklearn.ensemble import RandomForestClassifier
import torch
import transformers as ppb
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer


def find_intent(input_text):
    
    # Create tokenizer
    tokenizer = ppb.AutoTokenizer.from_pretrained('distilbert-base-cased')
    
    # Create model
    model = ppb.DistilBertModel.from_pretrained('distilbert-base-cased')
    
    # Create binarizer for multilabel data
    binarizer = MultiLabelBinarizer()

    # Create multioutput random forest classifier
    mt_forest = MultiOutputClassifier(RandomForestClassifier())
    
    # Create train dataset 
    X = ['What is the weather like today?',
         'Tell me the weather?',
         'What is the weather like in Paris today?',
         'Tell me an interesting fact.',
         'Tell me a fact.',
         'What is the weather like in Berlin today?',
         'What is the weather like in Istanbul today?']
    # Create labels for data-set
    y = [['Weather'], 
              ['Weather'], 
              ['Weather', 'City'], 
              ['Fact'], 
              ['Fact'],  
              ['Weather', 'City'], 
              ['Weather', 'City']]

    return intent

    # At later stages we can get the information from a csv file
    # In order to do that we have to also copy the data to the working directory
    # Copying data could easily implementable with cmake

    # Tokenize, pad and create data for 
    encoded_input = tokenizer(X, padding=True, truncation=True, return_tensors="pt")
    
    # Run tokenized training data in distillBERT
    with torch.no_grad():
        last_hidden_states = model(encoded_input['input_ids'], attention_mask=encoded_input['attention_mask'])
    print("torch")

    # Save features of sentences
    features = last_hidden_states[0][:,0,:].numpy()

    # Create a numpy array for labels
    y = numpy.array(y, dtype=object)

    # Run labels through binarizer
    b_y = binarizer.fit_transform(y)

    # For multioutput random forest classifier
    # Send cls tokens and binarized labels to train
    mt_forest.fit(features, b_y)

    # User input is tokenized
    encoded_input = tokenizer(input_text, padding=True, truncation=True, return_tensors="pt")

    # Send user input to extract cls tokens
    with torch.no_grad():
        last_hidden_states = model(encoded_input['input_ids'], attention_mask=encoded_input['attention_mask'])

    # Extract cls tokens from user input        
    features = last_hidden_states[0][:,0,:].numpy()

    # Predict labels using already trained multi out random forest classifier
    prediction = mt_forest.predict(features)[0]

    # Turn labels from binary values to actual labels
    intent = list(binarizer.inverse_transform(prediction.reshape(1, -1)))

    return intent