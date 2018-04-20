import sqlite3
import imapclient
import pyzmail
import re

#Dictionary of emails and corresponding passwords
EMAILS = ['matt.thomas1202@yahoo.com', 'matt.thomas1202@gmail.com', 'mrthomas@syr.edu']
PASSWORDS = {'yahoo': '2lnhm82vo9x626883', 'gmail': '1g6kd57y28u124428', 'syr': 'MRt__1994!'}

def check_emails():
    #connect to applications database
    conn = sqlite3.connect('applications.sqlite')
    c = conn.cursor()

    #for every email in EMAILS, collect all company names where that email was used to apply
    for email in EMAILS:
        email_to_check = "\'" + email + "\'"
        c.execute('select distinct name from application, company where application.cid = company.cid and status is not "No" and email = %s' % email_to_check)
        companies = c.fetchall()
        #log in to correct email address
        if 'yahoo' in email:
            imapObj = imapclient.IMAPClient('imap.mail.yahoo.com', ssl=True)
            imapObj.login(email, PASSWORDS['yahoo'])
        elif 'gmail' in email:
            imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
            imapObj.login(email, PASSWORDS['gmail'])
        else:
            imapObj = imapclient.IMAPClient('imap-mail.outlook.com', ssl=True)
            imapObj.login(email, PASSWORDS['syr'])


        print('Checking %s...' % email)

        #select email inbox
        imapObj.select_folder('INBOX', readonly=True)
        for company in companies:
            if "Inc" in company[0]:
                com_to_search = re.sub('(, Inc| Inc)', '', company[0])
                print(com_to_search)
                sub_search = 'SUBJECT ' + '"' + com_to_search + '"'
                body_search = 'BODY ' + '"' + com_to_search+ '"'
                text_search = 'TEXT ' + '"' + com_to_search + '"'
            #search subject, body and text for company name
            else:
                sub_search  = 'SUBJECT ' + '"' + company[0] + '"'
                body_search = 'BODY ' + '"' + company[0] + '"'
                text_search = 'TEXT ' + '"' + company[0] + '"'
            #try to collect UIDs where company name shows up
            try:
                UIDs = imapObj.search((sub_search + ' ' + body_search + ' '+ text_search))
                if UIDs:
                    #go through UIDs to see if any words indicating a rejection show up
                    for UID in UIDs:
                        noBuzz = ['regret', 'unfortunately', 'other candidates', 'despite', 'won\'t be able to', 'However', 'Despite', 'experience level', 'quite', 'reflection', 'number of candidates', 'not move', 'filled']
                        intBuzz = ['interview', 'congratulations', 'talk']
                        rawMessage = imapObj.fetch(UID, ['BODY[]'])
                        message = pyzmail.PyzMessage.factory(rawMessage[UID][b'BODY[]'])
                        if message.text_part != None:
                            try:
                                text = message.text_part.get_payload().decode(message.text_part.charset)
                            #catch none typerrors
                            except TypeError:
                                pass
                        else:
                            try:
                                text = message.html_part.get_payload().decode(message.html_part.charset)
                            except TypeError:
                                pass
                        #if emails contain the word interview, set status to "Interviewing"
                        c.execute('''SELECT status from application, company where application.cid = company.cid and name = "Mintel"''')
                        status = c.fetchone()
                        if any (buzz in text for buzz in intBuzz) and status[0] != "No":
                            c.execute('UPDATE application SET status = "Interviewing" WHERE application.aid in (select application.aid from application, company where application.cid = company.cid and name = ?)',[company[0]])
                            c.execute(
                                'SELECT status FROM application, company where application.cid = company.cid and name = ?',
                                [company[0]])
                            status = c.fetchone()
                            print("Application for ", company[0], "updated to", status[0])
                        #if rejection words found, update status of application to company to "No"
                        if any (buzz in text for buzz in noBuzz):
                            c.execute('UPDATE application SET status = "No" WHERE application.aid in (select application.aid from application, company where application.cid = company.cid and name = ?)', [company[0]])
                            c.execute('SELECT status FROM application, company where application.cid = company.cid and name = ?', [company[0]])
                            status = c.fetchone()
                            print("Application for ", company[0], "updated to", status[0])
            except UnicodeEncodeError:
                pass




    c.close()
    conn.commit() #commit changes
    conn.close()