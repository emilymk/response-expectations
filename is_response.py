import re
import base64

#input the appropriate file names
encResponseNeeded = open("enciPhoneGmailRN.txt").read()
encPotentialResponse = open("encGmailiPhonePR.txt").read()

decodedRN = str(base64.urlsafe_b64decode(encResponseNeeded.replace('-_', '+/').encode('utf-8')))
decodedPR = str(base64.urlsafe_b64decode(encPotentialResponse.replace('-_', '+/').encode('utf-8')))

def is_response(responseNeeded,potentialResponse):
    needOmit = ['\\r','\r','\\n','\n','>','<','*','-','_',' ']

    RN_PR = []
    for email in [responseNeeded, potentialResponse]:
        email = email[2:-1] #get rid of the b'' that is left over from decoding
        
        #getting rid of formatting
        for omitThis in needOmit:
            email = email.replace(omitThis,'')

        #for Outlook :'///// 
        email = re.sub(r'mailto:.*?@.*?w', '', email)
        email = email.replace('w','')

        #bc changing email will not change the actual respNeed and potResp, make new list of values
        RN_PR.append(email)

    #if the respNeed email is found in potResp email, then flag as a response found in thread
    RN_PR[1] = RN_PR[1].replace(RN_PR[0],'XXXresponse_flagXXX')
    
    if 'XXXresponse_flagXXX' in RN_PR[1]:
        return True
    
    return False

print(is_response(decodedRN,decodedPR))
