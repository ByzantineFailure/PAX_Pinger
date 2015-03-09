from twitter import *
from configuration_reader import *
from send_operations import *
import threading
import traceback
import sys
import os

PAX_TWITTER_ACCOUNT = "Official_PAX"

class TwitterThread(threading.Thread):
	def __init__(self, config, app_name, oauth_location):
		self.auth = config['auth'];
		self.contact = config['contact'];
		if(not self.auth['OAuthToken'] or not self.auth['OAuthSecret']):
			self.perform_and_store_oauth_dance(self.auth, app_name, oauth_location);
		self.create_twitter_object();

	def perform_and_store_oauth_dance(self, auth, app_name, oauth_location):
		oauth_dance(app_name, auth['API_Key'], auth['API_Secret'],
			    oauth_location);
		auth['OAuthToken'], auth['OAuthSecret'] = read_token_file(oauth_location);
		writeOAuthDanceValues(config_location, auth['OAuthToken'], auth['OAuthSecret']);
		#Clean up after ourselves
		os.remove(oauth_location);

	def start_stream(self):
		for msg in self.t_obj.getStreamIterator():
			tries = 0
			#Try sending the email until we succeed or until we've tried 5 times
			while send_email(contact, msg['text']) < 0:
				if(tries > 4):
					break;
				tries++;
				continue;
	
	def create_twitter_object(self):
		self.t_obj = Twitter( auth=OAuth(self.auth['OAuthToken'], self.auth['OAuthSecret'],
                               self.auth['API_Key'], self.auth['API_Secret']));

	def run(self):
		while(True):
			self.start_stream();
		except:
			sys.stdout.write(traceback.format_exc() + '\n');
			self.create_twitter_object();
