import smtplib
from email.mime.text import MIMEText

def send_email(contact, text):
    gmail_user = contact['User'];
    phone_number = contact['PhoneNumber'];
    gmail_pwd = contact['Password'];
    recipient = phone_number + contact['TextEmailServer'];

    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo();
    smtpserver.starttls();
    smtpserver.ehlo;
    smtpserver.login(gmail_user, gmail_pwd);
    msg = MIMEText(text);
    msg['Subject'] = "PAX TIX";
    msg['From'] = gmail_user;
    msg['To'] = recipient;
    try:
        smtpserver.sendmail(gmail_user, recipient, msg.as_string());
        print('Sent email');
        smtpserver.close();
        return 0;
    except:
        print("ERROR, failed to email this cycle!");
        return -1
