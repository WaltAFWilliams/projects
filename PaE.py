import re
import pyperclip

#Regexes for Emails and Phone Numbers

PhoneNumRE = re.compile(r'''(
    (\d{3}|\(\d{3}\)?)
    (\s|-|\.)?
    (\d{3})
    (\s|-|\.)
    (\d{4}))''', re.VERBOSE)

EmailRE = re.compile(r'''(
                    \w+
                     @\w+
                     \.\w+
                     )''',re.VERBOSE)

doc = str(pyperclip.paste())
PhoneNumbers = PhoneNumRE.findall(doc)
Emails = EmailRE.findall(doc)
matches = []
for group in PhoneNumbers:
    phNum = '-'.join([group[1],group[3],group[5]])
    matches.append(phNum)
for group in Emails:
    matches.append(group)


if len(matches) > 0:
    print('Here are all the emails and phone numbers found: ' + '\n')
    for match in matches:
        print(match+'\n')
        
else:
    print('There were no recognized emails or phone numbers.')




    
    
