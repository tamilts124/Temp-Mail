import requests, os
from sys import platform as plfm
from bs4 import BeautifulSoup
from time import sleep
import pickle

class TempMail:

    def __init__(self) -> None:
        self.tokens ={}
        self.mails ={}
        self.messages ={}
        useragent ='Mozilla/5.0 (X11; Windows x86_64; rv:91.0) Gecko/20100402 Firefox/91.0'
        self.headers ={'User-Agent': useragent, 'Authorization': 'Bearer '}

    def createmailid(self):
        token =requests.post('https://ext2.temp-mail.org/mailbox', headers =self.headers).json()
        self.tokens[token['mailbox']] =token['token']
        return token['mailbox']
    
    def getmailid(self, token):
        headers =self.headers.copy()
        headers['Authorization'] =headers['Authorization']+token
        mails =requests.get('https://ext2.temp-mail.org/messages', headers =headers).json()    
        if mails.get('errorMessage'): return
        mailid =mails['mailbox']
        self.tokens[mailid] =token
        self.mails[mailid] =mails['messages']
        return mailid

    def getmails(self, mailid):
        headers =self.headers.copy()
        headers['Authorization'] =headers['Authorization']+self.tokens[mailid]
        mails =requests.get('https://ext2.temp-mail.org/messages', headers =headers).json()    
        if mails.get('errorMessage'): return
        self.mails[mailid] =mails['messages']
        return mails['messages']
    
    def getmessage(self, mailid, messageid):
        headers =self.headers.copy()
        headers['Authorization'] =headers['Authorization']+self.tokens[mailid]
        message =requests.get('https://ext2.temp-mail.org/messages/'+messageid, headers =headers).json()    
        self.messages[messageid] =message
        return message

def main():
    if os.path.exists('./TempMail.pkl'):
        with open('./TempMail.pkl', 'rb') as pf:
            tempmail =pickle.loads(pf.read())
    else: tempmail =TempMail()

    def viewmail(message):
        soup =BeautifulSoup(message, 'html.parser')
        print('\n > TEXTS: \n')
        for mess in soup.text.split('\n'):
            mess =mess.strip('\t ')
            if mess: print(mess)
        messagesplits =message.split('"')
        links =[]
        for link in messagesplits:
            if link.lower().startswith('http'): links.append(link+'\n')
        if links:
            print('\n > LINKS: \n')
            print('', *links, '\n')
        print('  01. Open With Browser')
        print('  02. Go Back\n')

        while True:
            choice =int(input(' >> '))
            if choice==1:
                with open('./message.html', 'wt') as m: m.write(message)
                if plfm.startswith('win'): os.system('start message.html')
                else: os.system('open message.html 2>/dev/null')
            elif choice==2: break

    def managemails():

        def viewmails(mailid):
            
            while True:
                os.system('cls') if plfm.startswith('win') else os.system('clear')
                mails =tempmail.getmails(mailid)
                print(f'''\n{' '*8}Mails\n''')
                print(' >', mailid, '\n')
                if mails==None:
                    print(' > Mail Id Expired!')
                    sleep(3); return
                for no, mail in enumerate(mails, start=1):
                    no ='0'+str(no) if no <10 else str(no)
                    print(' '+no+')','From: '+mail['from'])
                    print('  Subject: '+mail['subject'])
                    print('  Preview: '+mail['bodyPreview'], '\n')
                tmail =len(mails)
                print('', ['0'+str(tmail+1) if tmail+1 <10 else str(tmail+1)][0]+'. '+'Refresh')
                print('', ['0'+str(tmail+2) if tmail+2 <10 else str(tmail+2)][0]+'. '+'View Cookie')
                print('', ['0'+str(tmail+3) if tmail+3 <10 else str(tmail+3)][0]+'. '+'Go Back\n')
                while True:
                    choice =int(input(' >> '))
                    if choice==tmail+1: break
                    elif choice==tmail+2:
                        print('\n', 'token: '+tempmail.tokens[mailid], '\n')
                    elif choice==tmail+3: return
                    elif 0<choice<=tmail:
                        os.system('cls') if plfm.startswith('win') else os.system('clear')
                        if tempmail.messages.get(mails[choice-1]['_id']):
                            message =tempmail.messages[mails[choice-1]['_id']]['bodyHtml']
                        else: message =tempmail.getmessage(mailid, mails[choice-1]['_id'])['bodyHtml']
                        viewmail(message)
                        break
                
        while True:
            os.system('cls') if plfm.startswith('win') else os.system('clear')
            print('''
            Manage Mail Ids\n''')
            for no, mailid in enumerate(tempmail.tokens, start=1):
                no ='0'+str(no) if no <10 else str(no)
                print('\t'+no+'. '+mailid)
            tmailid =len(tempmail.tokens)
            print('\n   ', ['0'+str(tmailid+1) if tmailid+1 <10 else str(tmailid+1)][0]+'. '+'Create Mail Ids')
            print('   ', ['0'+str(tmailid+2) if tmailid+2 <10 else str(tmailid+2)][0]+'. '+'Delete Mail Ids')
            print('   ', ['0'+str(tmailid+3) if tmailid+3 <10 else str(tmailid+3)][0]+'. '+'Add Mail Id')
            print('   ', ['0'+str(tmailid+4) if tmailid+4 <10 else str(tmailid+4)][0]+'. '+'Go Back\n')

            while True:
                choice =int(input(' >> '))
                if choice==tmailid+1:
                    number =int(input('\n > How Many Mail Ids To Create: '))
                    for num in range(number):
                        print('  ',num+1, '\t', end='\r')
                        tempmail.createmailid()
                    break
                elif choice==tmailid+2:
                    numbers =input('\n > Which Are The Mail Ids To Delete: ')
                    numbers =numbers.split()
                    numbers =list(map(lambda n: int(n), numbers))
                    numbers.sort(reverse =True)
                    mailids =list(tempmail.tokens.keys())
                    for num in numbers:
                        mailid =mailids[num-1]
                        tempmail.tokens.pop(mailid)
                        if tempmail.mails.get(mailid):
                            tempmail.mails.pop(mailid)
                    break
                elif choice==tmailid+3:
                    token =input('\n > Enter Token Of Mail Id: ').strip('\n\t ')
                    if not token: break
                    mailid =tempmail.getmailid(token)
                    if mailid==None:
                        print('\n > Mail Id Expired!')
                        sleep(3)
                    break
                elif choice==tmailid+4: return
                elif 0<choice<=tmailid:
                    mailid =list(tempmail.tokens.keys())[choice-1]
                    viewmails(mailid)
                    break

    def offlinemails():

        while True:
            os.system('cls') if plfm.startswith('win') else os.system('clear')
            print('''
            Offline Mails
            ''')
            ids =list(tempmail.messages.keys())
            mails =list(tempmail.messages.values())
            for no, mail in enumerate(mails, start=1):
                no ='0'+str(no) if no <10 else str(no)
                print(' '+no+')','From: '+mail['from'])
                print('       To: '+mail['mailbox'])
                print('  Subject: '+mail['subject'])
                print('  Preview: '+mail['bodyPreview'], '\n')
            tmail =len(tempmail.messages)
            print('', ['0'+str(tmail+1) if tmail+1 <10 else str(tmail+1)][0]+'. '+'Go Back\n')
            while True:
                choice =int(input(' >> '))
                if choice==tmail+1: return
                elif 0<choice<=tmail:
                    os.system('cls') if plfm.startswith('win') else os.system('clear')
                    message =tempmail.messages[ids[choice-1]]['bodyHtml']
                    viewmail(message)
                    break

    def savestatus():
        with open('./TempMail.pkl', 'wb') as pf:
            pf.write(pickle.dumps(tempmail))
        return True

    while True:
        os.system('cls') if plfm.startswith('win') else os.system('clear')
        print('''
            Temp-Mail.org
        
        01. Manage Mail Ids
        02. Offline Messages
        03. Save Status & Exit
        ''')

        try:
            while True:
                choice =int(input(' >> '))
                if choice==1: managemails(); break
                elif choice==2: offlinemails(); break
                elif choice==3: savestatus() and exit()
        except Exception: pass
        except KeyboardInterrupt: break

if __name__ == '__main__':
    main()
