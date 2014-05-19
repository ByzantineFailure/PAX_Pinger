from twitter import *
import urllib
import time
import smtplib
import re
from email.mime.text import MIMEText
 
#Do Oauth Dance to get this rather than hardcode
OAUTH_TOKEN="OAUTH_TOKEN";
OAUTH_SECRET="OAUTH_SECRET";
 
CONSUMER_KEY="API_KEY";
CONSUMER_SECRET="API_SECRET";
 
t_obj = Twitter( auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                              CONSUMER_KEY, CONSUMER_SECRET));
 
Last_Tweet_ID = 467354116139020288;
gmail_user = 'EMAIL'
phone_number = 'PHONE_NUMBER'
gmail_pwd = 'GMAIL_PASSWORD'
recip2 = phone_number + 'PHONE_PROVIDER_TEXT_EMAIL'
news = 'PAX Prime registration isn\'t yet available...follow our '
soon = '<li class="soon"><h3>Soon</h3></li>'
 
def email(to, text):
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo();
    smtpserver.starttls();
    smtpserver.ehlo;
    smtpserver.login(gmail_user, gmail_pwd);
    msg = MIMEText(text);
    msg['Subject'] = "PAX TIX MAY BE AVAILABLE";
    msg['From'] = gmail_user;
    msg['To'] = to;
    try:
        smtpserver.sendmail(gmail_user, to, msg.as_string());
        print('done');
        smtpserver.close();
        return 0;
    except:
        print("ERROR, failed to email this cycle!");
        return -1;
 
def checkTweets(t_obj):
    try:
        tweets = t_obj.statuses.user_timeline(screen_name="Official_PAX");
    except:
        print("Tweet checking failed for some reason!");
        return -1;
   
    if(tweets[0]['id'] != Last_Tweet_ID):
        email(recip2, 'NEW TWEET FROM PAX!');
        print('New Tweet!');
        return tweets[0]['id'];
    else:
        print('No new Tweet');
        return -1;
 
while 1:
    try:
        aResp = urllib.request.urlopen('http://prime.paxsite.com/');
        web_pg = aResp.read().decode('utf-8');
 
        newsmatches = re.findall(news, web_pg);
        soonmatches = re.findall(soon, web_pg);
        if len(newsmatches) == 0:
            print('News Changed!');
            email(recip2, 'News Changed!');
            break;
        elif len(soonmatches) == 0:
            print('Soon Changed!');
            email(recip2, 'Soon Changed!');
            break;
        else:
            print("No Site changes");
 
        tweetResult = checkTweets(t_obj);
        if(tweetResult != -1):
            Last_Tweet_ID = tweetResult;
    except:
        print("Shit fucked up, going back to bed.");
       
    time.sleep(60);
