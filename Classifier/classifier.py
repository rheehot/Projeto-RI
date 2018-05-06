import json
from sklearn import svm
from stop_words import get_stop_words
import operator
from os.path import isfile, join
import os
from os import listdir
import re

stop_words = get_stop_words('en')

class Classifier:
    def __init__(self):
        self.features = []
        self.clf = self.train()
        
    
    def getIDF(self):
        with open('idf.json') as data_file:    
            data = json.load(data_file)
        return data
    
    
    def setFeatures(self, idf):
        idf_sorted = sorted(idf.items(), key=operator.itemgetter(1))
        
        cont = 0
        for x in idf_sorted:
            if x[1] > 0 and cont < 100:
                self.features.append(x[0])
                cont+=1
        
    def getTrainData(self):
        pos_path = "positive_docs/"
        neg_path = "negative_docs/"
        positive_files = [f for f in listdir(pos_path) if isfile(join(pos_path, f))]
        negative_files = [f for f in listdir(neg_path) if isfile(join(neg_path, f))]
        
        X = []
        y = []
        for file in positive_files:
            with open(pos_path+file) as data_file:    
                data = json.load(data_file)
            aux = []
            for feature in self.features:
                aux.append(data.get(feature, 0))
            
            y.append('positive')
            X.append(aux)
        
        
        for file in negative_files:
            with open(neg_path+file) as data_file:    
                data = json.load(data_file)
            aux = []
            for feature in self.features:
                aux.append(data.get(feature, 0))
            
            y.append('negative')
            X.append(aux)
        
        yield X
        yield y
        
    def train(self):
        idf = self.getIDF()
        self.setFeatures(idf)
        X, y = self.getTrainData()
        
        clf = svm.SVC()
        clf.fit(X, y)
        
        return clf
        
    def getPageTf(self, page):
        [s.extract() for s in page('script')]
        data = ""
        data += (page.get_text())
    
        tf = {}
        regex = r'\b[a-zA-Z]+\b'
        data=re.sub("[^\w]", " ",  data).split()
    
        for word in data:
            if word.lower() not in stop_words and len(word)>2:
                tf[word.lower()] = tf.get(word.lower(),0)+1
    
        return tf
    
    def classify(self, page):
        tf = self.getPageTf(page)
        
        inst = []
        for feature in self.features:
            inst.append(tf.get(feature, 0))
        
        return self.clf.predict([inst])[0]
        
    
    
    
    