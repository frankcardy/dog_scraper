from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import time
import random
import os
import smtplib



#pages = np.arange(1,2)
#for page in pages:

page = requests.get('https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals.aspx?species=Dog&gender=A&agegroup=UnderYear&location=&site=&onhold=A&orderby=name&colnum=3&css=http://ws.petango.com/WebServices/adoptablesearch/css/styles.css&authkey=io53xfw8b0k2ocet3yb83666507n2168taf513lkxrqe681kf8&recAmount=&detailsInPopup=No&featuredPet=Include&stageID=&wmode=opaque')
source = page.content
soup = BeautifulSoup(source, 'lxml')
images = soup.find_all('div', class_= 'list-animal-photo-block')
postings = soup.find_all('td', class_='list-item')  #list-animal-info-block

print(postings)

def extract_dogs():

    for item in postings:
        try:
            atag = item.div.a
            url = "ws.petango.com/webservices/adoptablesearch/" + atag.get('href')
        except AttributeError:
            return
        name = item.find('div', class_='list-animal-name').text
        id = item.find('div', class_='list-animal-id').text
        breed = item.find('div', class_='list-animal-breed').text
        age = item.find('div', class_='list-animal-age').text
        gender = item.find('div', class_='list-animal-sexSN').text

        bad_chars = ' months'
        fixed_age_1 = age.strip(bad_chars)
        fixed_age_2 = int(fixed_age_1 or 0)

        result = (url, name, id, breed, fixed_age_2, gender)
        #print(result)



        records = []
        elements = []
        if fixed_age_2 < 3 and 'Australian Shepherd' in breed and gender == 'Male':
            records.append(result)
        elif len(result) > 5:
            send_mail()
        else:
            pass
        #print(records)
'''

        for record in records:
            elements.append(record)
        print(elements)
'''

def send_mail():

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('cardyf123@gmail.com', 'lsqohtmzdmrobwai')

    subject = 'Here are some doges you may be interested in:'
    body = f'Check out the following links\n{records}'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(
        'franksdogs@gmail.com',
        'cardyf123@gmail.com',
        msg
    )

    print('Email has been sent')

    server.quit()



#extract_dogs()
