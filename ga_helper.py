# -*- coding: utf-8 -*-
#
# Author: Craig Russell <craig@craig-russell.co.uk>
# 
# A simple wrapper for querying the Google Analytics API

import os
import sys
import argparse
import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets, AccessTokenRefreshError
from oauth2client.file import Storage
from oauth2client.tools import run_flow


CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'ga_client_secrets.json')
ACCESS_TOKEN   = os.path.join(os.path.dirname(__file__), 'ga_access_token.json')


# Create flow from client secrets
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/analytics.readonly',
    message='ERROR: %s is missing' % CLIENT_SECRETS)

# Retrieve existing credendials
storage = Storage(ACCESS_TOKEN)
credentials = storage.get()

# If existing credentials are invalid and Run Auth flow
# the run method will store any new credentials in ACCESS_TOKEN
if credentials is None or credentials.invalid:

    # Spoof CLI flags for authentication flow
    flags = argparse.Namespace(auth_host_name='localhost', auth_host_port=[8080, 8090], logging_level='ERROR', noauth_local_webserver=True)
    
    # Run the authorisation flow
    credentials = run_flow(FLOW, storage, flags)
    print "Authenticated credentials saved in %s. Please re-run the program." % ACCESS_TOKEN
    sys.exit()

# Create an httplib2.Http object to handle our HTTP requests and authorize it with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Construct the service object for the interacting with the Google Analytics API.
service = build('analytics', 'v3', http=http)


def get_accounts():
    """Return a list of accounts"""
    try:
        return service.management().accounts().list().execute()
    
    except AccessTokenRefreshError:
        print >> sys.stderr, "ERROR: Access token refresh failed"


def get_web_properties(account_id=None):
    """Return a list of web properties in an account"""
    try:
        return service.management().webproperties().list(accountId=account_id).execute()
    
    except AccessTokenRefreshError:
        print >> sys.stderr, "ERROR: Access token refresh failed"


def get_profiles(account_id=None, web_property_id=None):
    """Retun a list of profiles in a web property"""
    try:
        return service.management().profiles().list(accountId=account_id, webPropertyId=web_property_id).execute()
    
    except AccessTokenRefreshError:
        print >> sys.stderr, "ERROR: Access token refresh failed"


def get_report(profile_id=None, start_date=None, end_date=None, dimensions=None, 
               metrics=None, segment=None, filters=None, sort=None, max_results=None,
               sampling_level=None, start_index=None, output=None):
    """Return the result of a reporting query"""
    try:

        if not profile_id:
            raise TypeError('Missing required parameter "profile_id"')

        return service.data().ga().get(
                    ids           ='ga:%s' % profile_id,
                    start_date    =start_date,
                    end_date      =end_date,
                    metrics       =metrics,
                    max_results   =max_results,
                    filters       =filters,
                    dimensions    =dimensions,
                    sort          =sort,
                    samplingLevel =sampling_level,
                    segment       =segment,
                    start_index   =start_index,
                    output        =output,
                ).execute()

    except AccessTokenRefreshError:
        print >> sys.stderr, "ERROR: Access token refresh failed"
