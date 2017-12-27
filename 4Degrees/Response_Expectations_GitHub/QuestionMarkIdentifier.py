#EXPERT/HEURISTIC MODEL

import csv
import string #for punctuation and counting commas
import re #getting rid of names in recipients


def run_model():
    emails_list = []
    outcomes_list = []

    allData = []

    with open('Email_Resp_Expt_Data - Sheet1.csv') as emails:
         reader = csv.reader(emails) 
         for row in reader:

            newItem = {}
            newItem['outcome'] = row[0]
            newItem['data'] = row[1].replace('?', ' qMI')
            newItem['data'] = newItem['data'].replace('any one', 'anyone')
            #newItem['recipients'] = row[2]
            allData.append(newItem)

    falsePositives = 0
    falsePositives_list = []
    predicted = []


    for x in allData:
        email_body = x['data']

        
        if 'qMI' in email_body:

            #create substring of email that starts at anyone and ends w qMI
            #check if it contains \n, '.', '!', ')', or ';'
            if 'anyone' in email_body.lower():# or 'someone' in x['data']:
                anyone_i = email_body.find('anyone')
                qMI_i = email_body[anyone_i:].find('qMI')
                
                #if anyone not in a question
                if '\n' in email_body[anyone_i:qMI_i] or '.' in email_body[anyone_i:qMI_i] or '!' in email_body[anyone_i:qMI_i] or ')' in email_body[anyone_i:qMI_i] or ';' in email_body[anyone_i:qMI_i]:
                    predicted.append('Yes')
                    #print('its a valid question!')

                else: 
                    predicted.append('No')

            elif 'someone' in email_body.lower():
                someone_i = email_body.find('someone')
                qMI_i = email_body[someone_i:].find('qMI')

                #if someone not in a question
                if '\n' in email_body[someone_i:qMI_i] or '.' in email_body[someone_i:qMI_i] or '!' in email_body[someone_i:qMI_i] or ')' in email_body[someone_i:qMI_i] or ';' in email_body[someone_i:qMI_i]:
                    predicted.append('Yes')
                    #print('its a valid question!')

                #if someone is in the question
                else: 
        #       x['recipients'] = re.sub('".*?"', '', x['recipients'])
        #       recipCount = x['recipients'].count(',') + 1
        #       if recipCount > 2:
                    predicted.append('No')
        #       else:  
        #           predicted.append('Yes') 
                    
            else:
                predicted.append('Yes')
        # if qCount/wordCount >= .001:
        #    predicted.append('Yes')

        else:
            predicted.append('No')

        ####seeing if any No's have question marks
        # if 'qMI' in x['data'] and x['outcome'] == 'No':
        #     falsePositives += 1
        #     falsePositives_list.append(x['data'])

    totalCount = len(predicted)
    falseNo_list = []
    falseYes_list = []
    truePositiveCount = 0
    falsePositiveCount = 0

    for i in range(totalCount):
        #correct prediction
        if predicted[i] == allData[i]['outcome']:
            if allData[i]['outcome'] == 'Yes':
                truePositiveCount += 1


        #wrong prediction
        else:
            #was supposed to be no but came out as Yes
            if allData[i]['outcome'] == 'No':
                falseYes_list.append(allData[i]['data']) 
                falsePositiveCount += 1

            #was supposed to be yes but came out as No, aka false negative
            elif allData[i]['outcome'] == 'Yes':
                falseNo_list.append(allData[i]['data'])

    truePositiveAccuracy = truePositiveCount/(truePositiveCount + falsePositiveCount)

    return falseYes_list, truePositiveAccuracy


print(run_model())



"""
False Yes's are: 
'any one' and 'someone'

False No's are: (false negatives)
please help!', 'i was wondering', 'let me know', 'if that still works', 
'maybe you can help me', 'please select', 'please confirm', 'let us know', 
'please complete/look forward to hearing from you', 'looking forward to hearing back', 
'I have a question/double check','if you are interested', 
'I would be happy to speak to you then or schedule some time on the phone', 
'friendly reminder to send me', 'Curious if you have been able to...'
"""

"""
False negatives OK (say u dont need to respond, even when u do)
"""

"""
hypothesis: if there are >2 recipients that the email is being sent to
and it contains both a question and 'someone', then it doesn't necessarily have to
be responded to. 
"""
