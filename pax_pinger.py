from twitter import *
from configuration_reader import *
import urllib
import time
import smtplib
import re
from email.mime.text import MIMEText

#Set hardcoded parameters
CONFIG_LOCATION = "configuration.xml";
OAUTH_LOCATION = "oauth.dat";
APP_NAME = "PAX_Pinger";
Last_Tweet_ID = 467354116139020288;

#Get configuration
config = getConfiguration(CONFIG_LOCATION);
auth = config['auth'];
contact = config['contact'];

#Perform OAuth dance and store result if oauth keys not already present

if(not auth['OAuthToken'] or not auth['OAuthSecret']):
        oauth_dance(APP_NAME, auth['API_Key'], auth['API_Secret'],
                    OAUTH_LOCATION);
        auth['OAuthToken'], auth['OAuthSecret'] = read_token_file(OAUTH_LOCATION);
        writeOAuthDanceValues(CONFIG_LOCATION, auth['OAuthToken'], auth['OAuthSecret']);
        #Clean up after ourselves
        os.remove(OAUTH_LOCATION);

#Create our twitter object
t_obj = Twitter( auth=OAuth(auth['OAuthToken'], auth['OAuthSecret'],
                               auth['API_Key'], auth['API_Secret']));

#Set values from config
gmail_user = contact['User']
phone_number = contact['PhoneNumber']
gmail_pwd = contact['Password']
recip2 = phone_number + contact['TextEmailServer']
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
