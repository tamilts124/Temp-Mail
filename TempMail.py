import cloudscraper, sys, os
from time import sleep
from ast import literal_eval
from subprocess import getoutput

temp_mail_tokens =[];temp_mail_messages =[]
userAgent ='Mozilla/5.0 (X11; Windows x86_64; rv:91.0) Gecko/20100402 Firefox/91.0'
scraper =cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})

def request_resourse(url, headers, method):
    if method=='POST':response =scraper.post(url, headers=headers)
    else:response =scraper.get(url, headers=headers)
    return response

def create_id():
    headers ={'User-Agent': userAgent,
        'Authorization': 'Bearer'}
    result =request_resourse('https://ext2.temp-mail.org/mailbox', headers, 'POST')
    result =result.json();temp_mail_tokens.append(result);return result

def view_mail(json_data, id):
    headers ={'User-Agent': userAgent,
        'Authorization': f'Bearer {json_data["token"]}'}
    result =request_resourse(f'https://ext2.temp-mail.org/messages/{id}', headers, 'GET')    
    result =result.json();return result

def get_mails(json_data):
    headers ={'User-Agent': userAgent,
        'Authorization': f'Bearer {json_data["token"]}'}
    result =request_resourse('https://ext2.temp-mail.org/messages', headers, 'GET')    
    result =result.json();return result

def clear():
    if sys.platform.lower().startswith('win'):os.system('cls')
    else:os.system('clear')

def create_mew_id():print();print(create_id()['mailbox']);print()

def total_messages(mess):
    count =0
    for messages in temp_mail_messages:
        for message in messages['messages']:
            count +=1
            if mess == message:return count

def show_all_ids():
    print()
    for id, token in enumerate(temp_mail_tokens):print(f'{id+1}. '+token['mailbox'])
    print()

def save_message(file_path, file_name, data):
    if not os.path.exists(file_path):os.makedirs(file_path)
    with open(file_path+file_name, 'w') as file:file.write(data)

def show_mail(index):
    global temp_mail_messages
    print();token =temp_mail_tokens[index]
    mess_info =get_mails(token)
    temp_mail_messages.append(mess_info)
    if mess_info.get('errorMessage'):print('Mail Id Expired!');print();return
    if not mess_info.get('messages'):return
    for mess in mess_info['messages']:
        message =view_mail(token, mess['_id'])
        print(f'{total_messages(mess)})')
        print('           From: ' + message['from'])
        print('             To: ' + message['mailbox'])
        print('     Created At: ' + message['createdAt'])
        if not message['subject']:print('        Subject: ' + '( no subject )')
        else:print('        Subject: ' + message['subject'])
        print('        Preview: ' + message['bodyPreview'])
        if sys.platform.lower().startswith('win'):path=f'{getoutput(r"echo %userprofile%")}\Documents\messages\\'
        else:path=f'{getoutput("echo $HOME")}/Documents/messages/'
        path =path.replace('\\', '/')
        print('        Message: ' + f'file:///{path}{mess["_id"]}.html')
        save_message(path,  f'{mess["_id"]}.html', message['bodyHtml']);print()
    print()

def view_mails():
    global temp_mail_messages
    if not len(temp_mail_tokens):print();print('Mail Id Not Found, create new one!');print();sleep(3);return
    clear();print('\n'*2)
    print('    Temp Mail Ids');show_all_ids()
    print(f'{len(temp_mail_tokens)+1}. View All Id\'s Mails')
    print(f'{len(temp_mail_tokens)+2}. Clear Screen')
    print(f'{len(temp_mail_tokens)+3}. Go Back');print()
    print('Select Above Mail Id For View Mails');print()
    while True:
        option =input('> ')
        try:option =int(option)
        except:continue
        if not 1<=option<=len(temp_mail_tokens)+3:continue
        if option==len(temp_mail_tokens)+3:break
        if option==len(temp_mail_tokens)+2:view_mails();break
        elif option==len(temp_mail_tokens)+1:
            temp_mail_messages=[]
            for i in range(0, len(temp_mail_tokens)):show_mail(i)
        else:temp_mail_messages=[];show_mail(option-1)

def remove_id(index):
    global temp_mail_tokens, temp_mail_messages
    token =temp_mail_tokens[index]
    for messages in temp_mail_messages:
        if token.get('mailbox')==messages.get('mailbox'):temp_mail_messages.remove(messages)
    temp_mail_tokens.remove(token)

def remove_mail_ids():
    if not len(temp_mail_tokens):print();print(' Mail Id Not Found, create new one!');print();sleep(3);return
    clear();print('\n'*2)
    print('    Temp Mail Ids');show_all_ids()
    print(f'{len(temp_mail_tokens)+1}. Remove All Mail Ids')
    print(f'{len(temp_mail_tokens)+2}. Go Back');print()
    print('Select Above Mail Id to Removes');print()
    while True:
        option =input('> ')
        try:option =int(option)
        except:continue
        if not 1<=option<=len(temp_mail_tokens)+2:continue
        if option==len(temp_mail_tokens)+2:break
        elif option==len(temp_mail_tokens)+1:
            for i in range(len(temp_mail_tokens), 0, -1):remove_id(i-1)
            remove_mail_ids();break
        else:remove_id(option-1);remove_mail_ids();break;

def save_mail_ids():
    if sys.platform.lower().startswith('win'):file=f'{getoutput(r"echo %userprofile%")}\Documents\mailids.id'
    else:file=f'{getoutput("echo $HOME")}/Documents/mailids.id'
    file =file.replace('\\', '/')
    file =open(file, 'w')
    file.write(str(temp_mail_tokens));file.close()
    print();print('Temp Mail Ids List stored! can Access Anytime!');print()

def load_mail_ids():
    global temp_mail_tokens
    if sys.platform.lower().startswith('win'):file=f'{getoutput(r"echo %userprofile%")}\Documents\mailids.id'
    else:file=f'{getoutput("echo $HOME")}/Documents/mailids.id'
    file =file.replace('\\', '/')
    if os.path.exists(file):
        try:
            if sys.platform.lower().startswith('win'):file =open(file, 'r')
            else:file =open(file, 'r')
            for item in literal_eval(file.read()):temp_mail_tokens.append(item)
            file.close()
        except Exception as e:print(e);exit(0)

def selection():
    while True:
        option =input('>> ')
        try:option =int(option)
        except:break
        if not 1<=option<=7:continue
        if option==1:create_mew_id()
        elif option==2:show_all_ids() 
        elif option==3:view_mails();break
        elif option==4:remove_mail_ids();break
        elif option==5:save_mail_ids()
        elif option==6:break
        elif option==7:Exit()

def Exit():
    clear();print('\n'*2)
    print(' <<< For More Follow Me @tamilts124 In Github >>>')
    print();sleep(5);sys.exit(0)

def Main():
    try:
        while True:
            clear();print();print()
            print('                Temp Mail Ids Generator');print()
            print('        1. Create New Mail Id')
            print('        2. Show Mail Ids')
            print('        3. View Mails')
            print('        4. Remove Mail Ids')
            print('        5. Save Mail Ids (Store)')
            print('        6. Clear Screen')
            print('        7. Exit');print()
            print('    Note: May be Mails Automatically Deletes After 10 Minutes');print()
            print();selection()
    except KeyboardInterrupt:Exit()

if __name__ =='__main__':
    load_mail_ids();Main()
