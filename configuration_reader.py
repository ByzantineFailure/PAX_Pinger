import os
from xml.etree.ElementTree import ElementTree

CONFIGURATION_PATH="configuration.xml"

def getConfiguration(configurationPath):
        tree = ElementTree();
        tree.parse(configurationPath);
        root = tree.getroot();

        authData = root.find('TwitterAuthDetails');
        contactData = root.find('ContactDetails');

        authOutput = dict();
        contactOutput = dict();

        for child in authData:
                authOutput[child.tag] = child.text;

        for child in contactData:
                contactOutput[child.tag] = child.text;

        return dict(auth=authOutput, contact=contactOutput);

def writeOAuthDanceValues(configurationPath, OAuth_Token, OAuth_Secret):
        tree = ElementTree();
        tree.parse(configurationPath);
        root = tree.getroot();

        authData = root.find('TwitterAuthDetails');
        authData.find('OAuthToken').text = OAuth_Token;
        authData.find('OAuthSecret').text = OAuth_Secret;
        tree.write(configurationPath);
