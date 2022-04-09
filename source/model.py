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
    
    # At later stages we can get the information from a csv file
    # In order to do that we have to also copy the data to the working directory
    # Copying data could easily implementable with cmake

    # Tokenize, pad and create data for 
    encoded_input = tokenizer(X, padding=True, truncation=True, return_tensors="pt")
    
    # Run train data through distillBERT model
    with torch.no_grad():
        last_hidden_states = model(encoded_input['input_ids'], attention_mask=encoded_input['attention_mask'])
    
    # Save cls tokens of training sentences
    features = last_hidden_states[0][:,0,:].numpy()
    
    # Save training labels as numpy array 
    y = numpy.array(y, dtype=object)
    
    # Binarize labels 
    b_y = binarizer.fit_transform(y)
    
    # Fit the multi output random forest model 
    mt_forest.fit(features, b_y)
    
    # Encode user input 
    encoded_input = tokenizer(input_text, padding=True, truncation=True, return_tensors="pt")
    
    # Run user input through distillBERT model
    with torch.no_grad():
        last_hidden_states = model(encoded_input['input_ids'], attention_mask=encoded_input['attention_mask'])    

    # Save features of input word embeddings
    features = last_hidden_states[0][:,0,:].numpy()
    
    # Predict intent
    prediction = mt_forest.predict(features)[0]
    print("prediction")
    
    intent = list(binarizer.inverse_transform(prediction.reshape(1, -1)))
    print("intent")

    return intent