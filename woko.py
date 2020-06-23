

import urllib.request
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import datetime
import time

rows_prev = None

def main():
    with urllib.request.urlopen('http://www.woko.ch/en/nachmieter-gesucht') as response:
        html = response.read()
    
    soup = BeautifulSoup(html, features="lxml")
    # housing_div = soup.find(id="GruppeID_99")
    housing_div = soup.find(id="GruppeID_98")
    rows = housing_div.find_all(class_='row')

    msg_str = ''
    for row in rows:
        data = row.find_all('td')
        rent_from = data[1].string[8:]
        address = data[3].string
        price = row.find(class_='preis').string[:-3]
        msg_str += 'rent from: {0}\n'.format(rent_from)
        msg_str += 'address: {0}\n'.format(address)
        msg_str += 'price: {0}\n'.format(price)
        msg_str += '---------------------\n'

    msg_str += '{1}: {0} entries found\n'.format(len(rows), datetime.datetime.today()) 
    print(msg_str)

    # don't send email, if there's no change
    global rows_prev
    if rows == rows_prev:
        return
    rows_prev = rows

    email_msg = EmailMessage()
    email_msg.set_content(msg_str)
    email_msg['Subject'] = 'WOKO HOUSING REMINDER'
    email_msg['From'] = 'your-email@address'
    email_msg['To'] = ', '.join(['receiver1@address', 'receiver2@address'])
    

    smtpObj = smtplib.SMTP('smtp.your.server') # your smtp address
    smtpObj.login('username','password') # your username and your password
    smtpObj.send_message(email_msg)
    smtpObj.quit()


if __name__ == '__main__':

    while True:
        try:
            main()
            time.sleep(60)
        except Exception as e:
            print(e)
        
