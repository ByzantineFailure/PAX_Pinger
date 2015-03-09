from twitter_thread import *
from send_operations import *
from configuration_reader import *
import urllib
import time
import sys
import re

#Set hardcoded parameters
CONFIG_LOCATION = "configuration.xml";
OAUTH_LOCATION = "oauth.dat";

configuration = getConfiguration(CONFIG_LOCATION);

news = 'PAX Prime registration isn\'t yet available...follow our ' 
soon = '<li class="soon"><h3>Soon</h3></li>'

tw_thread = TwitterThread(OAUTH_LOCATION, CONFIG_LOCATION, configuration);
#HTML Scraping incoming.  Poke thejbw?
scrape_thread = None;

threads = [tw_thread, scrape_thread];

try:
        tw_thread.start();
        #scrape_thread.start();
        
        #Because threaded python applications don't respond to exceptions well
        #we have to get creative to handle it.  Iterate while we have threads.
        #Long-run we need a better way to do this
        while len(threads) > 0:
                try:
                        #Join with a timeout and set those that return to the new list of threads
                        #This is pretty sloppy but we only have 2 threads so w/e
                        for thread in threads:
                                if(thread is not None):
                                        if (thread.stop):
                                                #Ew, exception-based control flow.  Fix.
                                                raise Exception("Stop in child thread");
                                        threads.append(thread);
                                        thread.join(3);
                #This except block will only fire on the timeout, so there may be lag time between thread
                #failure/overall failure and exception handling and user notification
                except:
                        sys.stdout.write(traceback.format_exc() + '\n');
                        #send_email(configuration['contact'], "PAX_Pinger failed!");
                        sys.exit("Exited due to exception.");
#Only fires if the threads fail to start
except:
        sys.stdout.write(traceback.format_exc() + '\n');

