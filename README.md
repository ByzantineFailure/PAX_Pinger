PAX_Pinger
==========

An application for watching the Official_PAX twitter account and sending a text notifcation more reliably than twitter's app will.  It leverages Twitter's streaming API.  It also will eventually contain an HTML scraper for polling the website and updating on change, but this will be noticeably less immediate and up-to-date than the twitter stream.

It will text the user if the service fails.

Uses <a href="https://pypi.python.org/pypi/twitter#downloads">this twitter library.</a>

Initial version done last year over a few days of waiting and mutual boredom in collaboration with <a href="https://github.com/thejbw">the_jbw</a> and <a href="https://github.com/Barril">Barril</a>.  Went through a lot of iterations, from a simple scraper for the PAX site, to that plus a twitter HTML scraper, to actually using the twitter API, to using a configuration xml.  It now is kinda complex.  Nifty.

You'll need your own twitter API key.  And stuff.

#TODOs for Next Year
Ensure the application will continue to try to respawn in the event of a network failure.  This almost caused me to miss 2015's tickets!

#Configuration Details
APIKey:  The API Key you will use to run this application.  Not provided.

APISecret:  The API Secret.  Not provided.

AppName:  Whatever the name you registered this app under with twitter is.  Provided, but you can modify.


OAuthKey:  Will be automatically populated by the OAUTH dance.  Do not fill in this value.

OAuthSecret:  Will be automatically populated by the OAUTH dance.  Do not fill in this value.


User:  The email address you will be sending the text notifications from.  This application assumes GMail and is not guaranteed to work with other email providers.

Password:  The password for the account, plaintext.  This is not secure, but I'm lazy and don't want to figure out how to do it right.


PhoneNumber:  The phone number you are sending the text to.

TextEmailServer: The email address ending, including "@" that your provider uses.


Phone Number and TextEmailServer are dependent upon your provider, but are concatenated together to create a single email address to send the email to.
