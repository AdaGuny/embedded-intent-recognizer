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