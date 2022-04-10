#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy
from sklearn.ensemble import RandomForestClassifier
import torch
import transformers as ppb
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer


class Model:
    
    def __init__(self, pre_trained_weights):
        
        self.tokenizer = ppb.AutoTokenizer.from_pretrained(pre_trained_weights)
        self.model = ppb.DistilBertModel.from_pretrained(pre_trained_weights)
        self.binarizer = MultiLabelBinarizer()
        self.rf = MultiOutputClassifier(RandomForestClassifier())
                                                    
        self.X= ['What is the weather like today?',
         'Tell me the weather?',
         'What is the weather like in Paris today?',
         'Tell me an interesting fact.',
         'Tell me a fact.',
         'What is the weather like in Berlin today?',
         'What is the weather like in Istanbul today?']
                                                    
        self.y=  [['Weather'], 
              ['Weather'], 
              ['Weather', 'City'], 
              ['Fact'], 
              ['Fact'],  
              ['Weather', 'City'], 
              ['Weather', 'City']]
                                                
    def train_rf(self):
                                                    
        encoded_input = self.tokenizer(self.X, padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():
            last_hidden_states = self.model(encoded_input['input_ids'], attention_mask=encoded_input['attention_mask'])

        features = last_hidden_states[0][:,0,:].numpy()
        
        y = numpy.array(self.y, dtype=object)
    
        b_y = self.binarizer.fit_transform(y)
        
        self.rf.fit(features, b_y)
        
        return 
            
                                                    
    def find_intent(self, input_text):
                                                    
        encoded_input = self.tokenizer(input_text, padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():
            last_hidden_states = self.model(encoded_input['input_ids'], attention_mask=encoded_input['attention_mask'])    

        features = last_hidden_states[0][:,0,:].numpy()
    
        prediction = self.rf.predict(features)[0]
    
        intent = list(self.binarizer.inverse_transform(prediction.reshape(1, -1)))

        return intent
        
                                                


# In[14]:


model = Model('distilbert-base-cased')
model.train_rf()
model.find_intent("Tell me the weather for today")


# In[ ]:




