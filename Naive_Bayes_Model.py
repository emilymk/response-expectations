#NAIVE BAYES MODEL 

import math
import random
import csv 
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
import string #for punctuation
import collections #for ordered dictionary


def run_model():
    #CREATE LIST OF DICTIONARIES FOR THE EMAILS!!!!!
    emails_list = []
    outcomes_list = []

    allData = []

    with open('Email_Resp_Expt_Data - Sheet1.csv') as emails:
        reader = csv.reader(emails)
        for row in reader:
            """ Here I lemmatized the text but then realized the CountVectorizer already does that!!!

            email_body = row[1]

            #lemmatizing by verb and noun
            for punc in string.punctuation:
                email_body = email_body.replace(punc,'')
            split_into_words = email_body.split()
            for word in split_into_words:
                email_body = email_body.replace(word,lmtzr.lemmatize(word,'v'))
                email_body = email_body.replace(word,lmtzr.lemmatize(word,'n'))
            #emails_orderedDict[email_body] = row[0]
            """

            ##Make a list of dictionaries
            newItem = {}
            newItem['outcome'] = row[0]
            newItem['data'] = row[1].replace('?', ' qMI') #replacing the question marks with idenitifiers
            allData.append(newItem)

    random.shuffle(allData)
    trainingData = allData[:int(math.floor(len(allData)*.9))]
    testData = allData[int(-1*(math.ceil(len(allData)*.1))):]


    # Words to be ignored by the classifier
    stopwords = ['a','above','an','and','any', 'as','be','because','truly','lol','haha','hah','rly','really',
        'before','being','below','down','laptop','computer','screen','organization','club','loll',
        'each','few','for','further','he','her','here','hers','herself', 'hey','hello','year','u','you','me',
        'him','himself','his','i','in','into','it','its','itself','me','more','most','celebrate','hi','bye','goodbye',
        'my','myself','of','off','office','on','our','ours', 'from','sincerely','regards','undergraduate',
        'ourselves','out','over','own','same','she','student','the', 'tomorrow','yesterday','today','week','day','month',
        'their','theirs','them','themselves','they','this','those','through', 'thanks','thank','appreciate',
        'to','under','up','very','was','we','were','with','tree','holiday','holidays','generally']


    #TOKENIZE TEXT!!!!!
    #found that including bigrams results in lower accuracy of predictions
    #instead of strip_punctuation = False --> use qMI
    vect_init = CountVectorizer(stop_words=stopwords, lowercase=True, ngram_range=(1,1))
    occurrence_vect = vect_init.fit_transform([x['data'] for x in trainingData])

    #CONVERT TO FREQUENCIES!!!!!
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(occurrence_vect)

    #TRAIN NAIVE BAYES MODEL!!!!! 
    #the second argument of fit is outcome, not body
    clf = MultinomialNB().fit(X_train_tfidf, [x['outcome'] for x in trainingData])

    #TEST THE DATA!!!!!
    x_test_counts = vect_init.transform([x['data'] for x in testData])
    x_test_tfidf = tfidf_transformer.fit_transform(x_test_counts)
    predicted = clf.predict(x_test_tfidf)


    #for calculating prediction accuracy
    totalCount = len(predicted)
    correctCount = 0
    for i in range(totalCount):
        if predicted[i] == testData[i]['outcome']:
            correctCount += 1
    accuracy = correctCount/totalCount

    return accuracy

#how many times the program should run, then find average accuracy
results = []
for i in range(50):
    results.append(run_model())

print(float(sum(results)/len(results)))

