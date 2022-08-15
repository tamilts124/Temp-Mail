import cloudscraper, sys, os
from time import sleep
from ast import literal_eval
from subprocess import getoutput

temp_mail_tokens =[];temp_mail_messages =[]
userAgent ='Mozilla/5.0 (X11; Windows x86_64; rv:91.0) Gecko/20100402 Firefox/91.0'

def request_resourse(url, headers, method):
    try:
        scraper =cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})
        if method=='POST':response =scraper.post(url, headers=headers)
        else:response =scraper.get(url, headers=headers)
    except Exception as e:excepted(e)
    return response

def excepted(e):clear();print();print(e);sys.exit()

def create_id():
    try:
        headers ={'User-Agent': userAgent,
            'Authorization': 'Bearer'}
        result =request_resourse('https://ext2.temp-mail.org/mailbox', headers, 'POST')
        result =result.json();temp_mail_tokens.append(result);return result
    except Exception as e:excepted(e)

def view_mail(json_data, id):
    try:
        headers ={'User-Agent': userAgent,
            'Authorization': f'Bearer {json_data["token"]}'}
        result =request_resourse(f'https://ext2.temp-mail.org/messages/{id}', headers, 'GET')    
        result =result.json();return result
    except Exception as e:excepted(e)

def get_mails(json_data):
    try:
        headers ={'User-Agent': userAgent,
            'Authorization': f'Bearer {json_data["token"]}'}
        result =request_resourse('https://ext2.temp-mail.org/messages', headers, 'GET')    
        result =result.json();return result
    except Exception as e:excepted(e)

def sprint(text, ndelay=None):
    temp =''
    for i in text:
        if ndelay:sleep(ndelay)
        else:sleep(delay)
        temp+=i;print(temp, end='\r')
    print()

def clear():
    if sys.platform.lower().startswith('win'):os.system('cls')
    else:os.system('clear')

def create_mew_id():
    print();sprint(create_id()['mailbox']);print()

def total_messages(mess):
    count =0
    for messages in temp_mail_messages:
        for message in messages['messages']:
            count +=1
            if mess == message:return count

def show_all_ids():
    print()
    for id, token in enumerate(temp_mail_tokens):sprint(f'{id+1}. '+token['mailbox'])
    print()

def save_message(file_path, file_name, data):
    if not os.path.exists(file_path):os.makedirs(file_path)
    with open(file_path+file_name, 'w') as file:file.write(data)

def show_mail(index):
    global temp_mail_messages
    print();token =temp_mail_tokens[index]
    mess_info =get_mails(token)
    temp_mail_messages.append(mess_info)
    if not mess_info['messages']:sprint(f'No Temp Mails In {mess_info["mailbox"]}!');print();return
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

def show_mails():
    global temp_mail_messages
    if not len(temp_mail_tokens):print();sprint('Temp Mail Id Not Found, create new one!');print();sleep(edelay);return
    clear();print()
    sprint('                      Github @tamilts124', mdelay)
    print()
    sprint('    Temp Mail Ids List');show_all_ids()
    sprint(f'{len(temp_mail_tokens)+1}. View All Temp Mails')
    sprint(f'{len(temp_mail_tokens)+2}. Clear Screen')
    sprint(f'{len(temp_mail_tokens)+3}. Go Back');print()
    sprint('Select Above Temp Mail Id For View Mails');print()
    while True:
        option =input('> ')
        try:option =int(option)
        except:continue
        if not 1<=option<=len(temp_mail_tokens)+3:continue
        if option==len(temp_mail_tokens)+3:break
        if option==len(temp_mail_tokens)+2:show_mails();break
        elif option==len(temp_mail_tokens)+1:
            temp_mail_messages=[]
            for i in range(0, len(temp_mail_tokens)):show_mail(i)
        else:temp_mail_messages=[];show_mail(option-1)

def remove_id(index):
    global temp_mail_tokens, temp_mail_messages
    print();token =temp_mail_tokens[index]
    for messages in temp_mail_messages:
        if token['mailbox']==messages['mailbox']:temp_mail_messages.remove(messages)
    sprint(f'Mail Id {token["mailbox"]} removed!')
    temp_mail_tokens.remove(token);print()

def remove_mail_ids():
    if not len(temp_mail_tokens):print();sprint(' Temp Mail Id Not Found, create new one!');print();sleep(edelay);return
    clear();print()
    sprint('                   Github @tamilts124', mdelay)
    print()
    sprint('    Temp Mail Ids List');show_all_ids()
    sprint(f'{len(temp_mail_tokens)+1}. Remove All Temp Mail Ids')
    sprint(f'{len(temp_mail_tokens)+2}. Go Back');print()
    sprint('Select Above Temp Mail Id For Removes');print()
    while True:
        option =input('> ')
        try:option =int(option)
        except:continue
        if not 1<=option<=len(temp_mail_tokens)+2:continue
        if option==len(temp_mail_tokens)+2:break
        elif option==len(temp_mail_tokens)+1:
            for i in range(len(temp_mail_tokens), 0, -1):remove_id(i-1)
            sleep(edelay);remove_mail_ids();break
        else:remove_id(option-1);sleep(edelay);remove_mail_ids();break;

def save_mail_ids():
    if sys.platform.lower().startswith('win'):file=f'{getoutput(r"echo %userprofile%")}\Documents\.mail-ids.hid'
    else:file=f'{getoutput("echo $HOME")}/Documents/.mail-ids.hid'
    file =file.replace('\\', '/')
    file =open(file, 'w')
    file.write(str(temp_mail_tokens));file.close()
    print();sprint('Temp Mail Ids List stored! can Access Anytime!');print()

def load_mail_ids():
    global temp_mail_tokens
    if sys.platform.lower().startswith('win'):file=f'{getoutput(r"echo %userprofile%")}\Documents\.mail-ids.hid'
    else:file=f'{getoutput("echo $HOME")}/Documents/.mail-ids.hid'
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
        if not 1<=option<=8:continue
        if option==1:create_mew_id()
        elif option==2:show_all_ids() 
        elif option==3:show_mails();break
        elif option==4:remove_mail_ids();break
        elif option==5:save_mail_ids()
        elif option==6:break
        elif option==7:About();break
        elif option==8:stoped();break
        else:stoped()

def About():
    clear();print()
    sprint('                                        Github @tamilts124', mdelay);print()
    sprint('    //////////////////////////////////////////////////////')
    sprint('    //////////////////     FEATURES     //////////////////')
    sprint('    //////////////////////////////////////////////////////');print()
    sprint('    //////////////////////////////////////////////////////')
    sprint('    //////  1. Unlimited Mail Ids  ///////////////////////')
    sprint('    //////  2. Mail Ids Can Use Long Time  ///////////////')
    sprint('    //////  3. View All Mails At a Time  /////////////////')
    sprint('    //////  4. Can View Subject Of Mail  /////////////////')
    sprint('    //////  5. Message Preview Available  ////////////////')
    sprint('    //////  6. View Main Message From Browser Via Link  //')
    sprint('    //////  7. Remove All Unwanted Mail Id  //////////////')
    sprint('    //////////////////////////////////////////////////////');print()
    print('    NOTE: Temp Mail Ids, it\'s Only Storing Localy')
    if sys.platform.lower().startswith('win'):file=f'{getoutput(r"echo %userprofile%")}\Documents\.mail-ids.hid'
    else:file=f'{getoutput("echo $HOME")}/Documents/.mail-ids.hid'
    file =file.replace('\\', '/')
    print(f'    Storing Location: {file}')
    print('    Please Don\'t Change Information From The Stored File, May Can\'t be Receive Mails');sleep(10)

def Thank():
    clear();print()
    sprint('    //////////////////////////////////////////////////////')
    sprint('    //////////  For More Follow Me @tamilts124  //////////')
    sprint('    //////////////////////////////////////////////////////')
    print();sleep(5)

def stoped():
    Thank();clear();sys.exit(0)

def Main():
    global delay, edelay, mdelay
    delay =0.001;edelay =2;mdelay =0.03
    try:
        while True:
            clear();print();print()
            sprint('                                         Github @tamilts124', mdelay);print()
            sprint('                Temp Mail Ids Generator');print()
            sprint('        1. Create New Temp Mail Id')
            sprint('        2. Show Temp Mail Ids')
            sprint('        3. Show Temp Mails')
            sprint('        4. Remove Temp Mail Ids')
            sprint('        5. Save Temp Mail Ids (Store)')
            sprint('        6. Clear Screen')
            sprint('        7. About The Features')
            sprint('        8. Exit');print()
            sprint('    Note: Temp Mails Automatically Deletes After 10 Minutes');print()
            print();selection()
    except KeyboardInterrupt:stoped()

if __name__ =='__main__':
    load_mail_ids();Main()