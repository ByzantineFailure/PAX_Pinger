from twitter import *
from configuration_reader import *
from send_operations import *
import threading
import traceback
import sys
import os

PAX_TWITTER_ACCOUNT = "TweetSQLAtMeTes"

class TwitterThread(threading.Thread):
        def __init__(self, oauth_location, config_location):
                config = getConfiguration(config_location);
                self.auth = config['auth'];
                self.contact = config['contact'];
                if(not self.auth['OAuthToken'] or not self.auth['OAuthSecret']):
                        self.perform_and_store_oauth_dance(self.auth, config['auth']['AppName'], oauth_location, config_location);
                self.create_twitter_object();
                self.pax_id = self.rest_obj.users.lookup(screen_name=PAX_TWITTER_ACCOUNT)[0]['id'];

        def perform_and_store_oauth_dance(self, auth, app_name, oauth_location, config_location):
                oauth_dance(app_name, auth['API_Key'], auth['API_Secret'],
                            oauth_location);
                auth['OAuthToken'], auth['OAuthSecret'] = read_token_file(oauth_location);
                writeOAuthDanceValues(config_location, auth['OAuthToken'], auth['OAuthSecret']);
                #Clean up after ourselves
                os.remove(oauth_location);

        def start_stream(self):
                for msg in self.stream_obj.statuses.filter(follow=self.pax_id):
                        sys.stdout.write("NEW TWEET: {0}".format(msg['text']));
                        tries = 0
                        #Try sending the email until we succeed or until we've tried 5 times
                        while send_email(self.contact, 'NEW TWEET: {0}'.format(msg['text'])) < 0:
                                if(tries > 4):
                                        break;
                                tries = tries + 1;
                                continue;
                        
        
        def create_twitter_object(self):
                self.rest_obj = Twitter( auth=OAuth(self.auth['OAuthToken'], self.auth['OAuthSecret'],
                               self.auth['API_Key'], self.auth['API_Secret']));
                self.stream_obj = TwitterStream(auth=OAuth(self.auth['OAuthToken'], self.auth['OAuthSecret'],
                                                           self.auth['API_Key'], self.auth['API_Secret']),
                                                domain='stream.twitter.com');

        def run(self):
                while(True):
                        try:
                               self.start_stream();
                        except:
                               sys.stdout.write(traceback.format_exc() + '\n');
                               self.create_twitter_object();
