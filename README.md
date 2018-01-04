# response-expectations

The Naive Bayes algorithm predicts, trains, and categorizes email data into whether the sender of the email would expect a response or not. The Expert Model runs a series of checks to determine whether the sender of the email would expect a response or not. 

The accuracy is defined as (True Positives)/(True Positives + False Positives). The Naive Bayes Model has an accuracy of ~76%, and the Expert Model has an accuracy of 96%. A False Positive means that an email is tagged as expecting a response, but does not actually need one. 

The is_response.py file detects when a response to a responseNeeded email is received, allowing the latter to update its expectation status real-time. 
