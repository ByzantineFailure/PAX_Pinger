from twitter import *
from configuration_reader import *
from send_operations import *
import threading
import pprint
import traceback
import sys
import os

#PAX_TWITTER_ACCOUNT = "official_pax"
PAX_TWITTER_ACCOUNT = "TweetSqlAtMeTes"

class TwitterThread(threading.Thread):
        def __init__(self, oauth_location, config_location, config):
                #Retreive configuration values
                self.auth = config['auth'];
                self.contact = config['contact'];

                self.stop = False;

                #Do the OAuth dance if we don't have these values already
                if(not self.auth['OAuthToken'] or not self.auth['OAuthSecret']):
                        self.perform_and_store_oauth_dance(self.auth, config['auth']['AppName'], oauth_location, config_location);

                #Create twitter objects and get id to stream from
                self.create_twitter_objects();
                self.pax_id = self.rest_obj.users.lookup(screen_name=PAX_TWITTER_ACCOUNT)[0]['id'];
                threading.Thread.__init__(self);

        def perform_and_store_oauth_dance(self, auth, app_name, oauth_location, config_location):
                oauth_dance(app_name, auth['API_Key'], auth['API_Secret'],
                            oauth_location);
                auth['OAuthToken'], auth['OAuthSecret'] = read_token_file(oauth_location);
                writeOAuthDanceValues(config_location, auth['OAuthToken'], auth['OAuthSecret']);
                #Clean up after ourselves
                os.remove(oauth_location);

        def start_stream(self):
                for msg in self.stream_obj.statuses.filter(follow=self.pax_id):
                        if (self.stop):
                                raise Exception("Stopping from sentinel!");
                        
                        #Twitter stream hangup
                        if('hangup' in msg and msg['hangup']):
                                raise StopIteration("Found Hangup in twitter stream!");

                        if('text' not in msg):
                                sys.stdout.write("text not found in tweet!  Tweet was:\n");
                                pprint.pprint(msg);
                                continue;
                        
                        printableMessage = msg['text'].encode('utf-8');

                        sys.stdout.write("NEW TWEET: {0}\n".format(printableMessage));
                        if(msg['user']['screen_name'].lower() != PAX_TWITTER_ACCOUNT.lower()):
                                sys.stdout.write("Continuing -- not a tweet from official_pax\n");
                                sys.stdout.flush();
                                continue;
                        tries = 0
                        #Try sending the email until we succeed or until we've tried 5 times
                        while send_email(self.contact, 'NEW TWEET: {0}'.format(printableMessage)) < 0:
                                if(tries > 4):
                                        break;
                                tries = tries + 1;
                                continue;
                        
        
        def create_twitter_objects(self):
                self.rest_obj = Twitter( auth=OAuth(self.auth['OAuthToken'], self.auth['OAuthSecret'],
                               self.auth['API_Key'], self.auth['API_Secret']));
                self.stream_obj = TwitterStream(auth=OAuth(self.auth['OAuthToken'], self.auth['OAuthSecret'],
                                                           self.auth['API_Key'], self.auth['API_Secret']),
                                                domain='stream.twitter.com');
        
        def stop(self):
                sys.stdout.write("Received stop!\n");
                self.stop = True;

        def isAlive(self):
                return (not self.stop);

        def run(self):
                while(not self.stop):
                        try:
                               self.start_stream();
                        #Twitter Stream has failed in some way.  Respawn.
                        except StopIteration:
                               sys.stdout.write("StopIteration found (probably a hangup.  Respawning...\n");
                               self.create_twitter_objects();
                        #Some other failure.  Notify the user and rethrow.
                        #The email may be factored up to the parent thread in the future.
                        except:
                               sys.stdout.write(traceback.format_exc() + '\n');
                               self.stop = True;
                               raise;
