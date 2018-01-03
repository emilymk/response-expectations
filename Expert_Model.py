#determines if an email expects a response
import re

def determine_response_expectation(emailBody, toHeader):

    """FORMATTING STYLES
    Gmail:
    On Thu, Mar 24, 2011 at 3:51 PM, <test@test.com> wrote:

    Gmail Forward:
    From: David Vandegrift <david@4degrees.ai>
    Date: Wed, Jan 3, 2018 at 8:15 AM
    Subject: Re: Advice - 2018 Chicago Industry4.0 Meetup
    To: Ty Findley <tfindley@pritzkergroup.com>
    
    Outlook:
    From: David Vandegrift [mailto:david@4degrees.ai] 
    Sent: Monday, December 18, 2017 12:27 PM
    To: Alyssa Jaffee <ajaffee@pritzkergroup.com>
    Subject: Willing to chat with an NVC aspirant?
    """

    #flag GMAIL thread
    emailBody = re.sub(r'On (Sun|Mon|Tue|Wed|Thu|Fri|Sat), (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4} at \d{1,2}:\d{2} [AP]M, <.*?@.*?> wrote:', 'XXXthread_flagXXX', emailBody)#, flags=re.IGNORECASE)
    #flag GMAIL FORWARD thread 
    emailBody = re.sub(r'From: .*? <.*?@.*?>.?\nDate: (Sun|Mon|Tue|Wed|Thu|Fri|Sat), (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4} at \d{1,2}:\d{2} [AP]M.?\nSubject:.*?\nTo:', 'XXXthread_flagXXX', emailBody)

    #flag OUTLOOK thread
    emailBody = re.sub(r'From: .*?mailto:.*?@.*?\n *?Sent: (Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday), (January|Febuary|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4} \d{1,2}:\d{2} [AP]M *?\nTo:.*?\n *?Subject:.*', 'XXXthread_flagXXX', emailBody)
    
    #flag IPHONE FORWARD thread 
    emailBody = re.sub(r'From: .*? <.*?@.*?>.?\n.*?Date: (January|Febuary|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4} at \d{1,2}:\d{2}:\d{2} [AP]M.*?\n.*?To:.*?\n.*?Subject:', 'XXXthread_flagXXX', emailBody)

    #flag some other type of thread
    emailBody = re.sub(r'On \d{1,2}/\d{1,2}/\d{4} \d{2}:\d{2} [AP]M, .*? wrote:', 'XXXthread_flagXXX', emailBody)

    #flag GCal invitations
    emailBody = re.sub(r'Content-Type: application/ics; name="invite.?ics".*?\nContent-Disposition: attachment; filename="invite.?ics".?','XXXinvitation_flagXXX', emailBody)
    
    ###
    ###
    #exclude thread after last email
    threadFlag_i = emailBody.find('XXXthread_flagXXX')

    if threadFlag_i != -1:
        emailBody = emailBody[:threadFlag_i]

    #look for invitations
    invitationFlag_i = emailBody.find('XXXinvitation_flagXXX')

    #if it there is an invitation
    if invitationFlag_i != -1:
        return False
        #A/N: if the invitation was a part of a thread, then it would have been cropped out already 

    #replace question marks and "anyone" typos
    emailBody = emailBody.replace('?', ' qMI')
    emailBody = emailBody.replace('any one', 'anyone')

    #if no qMI, then simply does NOT require a response
    if ' qMI' not in emailBody:
        return False

    #helper function for checking qMI exception. False = response expected
    def checking_qMI_exceptions(emailBody, exception):

        #create substring of email that starts at "anyone or "someone" and ends w qMI
        j = emailBody.lower().find(' qMI')
        i = emailBody[:j].lower().rfind(exception)
        
        #if ending punc between anyone/someone and qMI, then not same sentence
        if '\n' in emailBody[i:i+j] or '.' in emailBody[i:i+j] or '!' in emailBody[i:i+j] or ')' in emailBody[i:i+j] or ';' in emailBody[i:i+j]:
            return True

        # Check to see if the email was sent to 3+ people
        # If so, and someone/anyone is in the question, flag as False
        recipients = re.sub('".*?"', '', toHeader)
        recipCount = recipients.count(',') + 1
        if recipCount >= 3:
            return False

        return True #aka checked all exceptions and theyre all valid! 

    exceptions = ['anyone', 'someone']
    #if any of these exceptions are in the email body
    if any(x in emailBody.lower() for x in exceptions):
        for exception in exceptions:
            if exception in emailBody.lower():
                is_valid_exception = checking_qMI_exceptions(emailBody, exception)
                #if it not a valid exception aka response is expected
                if is_valid_exception is False:
                    return True

            #if went through all exceptions and all valid exceptions 
            return False

    return True
