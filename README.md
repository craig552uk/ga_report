
# GA Report

A command line tool for querying the Google Analytics Reporting API.

For more information about API options see: 
https://developers.google.com/analytics/devguides/reporting/core/v3/reference
https://developers.google.com/analytics/devguides/reporting/core/dimsmets

Author: Craig russell <craig@craig-russell.co.uk>    
Version: 0.1

## Installation

Install Google API Python client libraries

    pip install --upgrade google-api-python-client

Register a project in the Google Developers Console and create a `ga_client_secrets.json` file in the project root. https://developers.google.com/analytics/solutions/articles/hello-analytics-api#register_project

## Usage
     Usage: ga_report [options]

     Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -F FIELD_SEPERATOR, --field_seperator=FIELD_SEPERATOR
                        The field seperator in the output.
     -H, --headings        Show filed headings in the output
     -L, --list_profiles   List all Profiles available to the authenticated user
                        (rate limit permitting)

     Google Analytics Reporting Options:
     -b START_DATE, --start_date=START_DATE
                        Beginning date to retrieve data in format YYYY-MM-DD.
     -d DIMENSIONS, --dimensions=DIMENSIONS
                        The dimension data to be retrieved from the API. A
                        single request is limited to a maximum of 7
                        dimensions.
     -e END_DATE, --end_date=END_DATE
                        Final date to retrieve data in format YYYY-MM-DD.
     -f FILTERS, --filters=FILTERS
                        Specifies a subset of all data matched in analytics.
     -g SEGMENT, --segment=SEGMENT
                        Specifies a subset of visits based on either an
                        expression or a filter. The subset of visits matched
                        happens before dimensions and metrics are calculated.
     -i START_INDEX, --start_index=START_INDEX
                        Use this parameter to request more rows from the API.
                        The index starts from 1 and the default is 1.
     -l SAMPLING_LEVEL, --sampling_level=SAMPLING_LEVEL
                        Use this parameter to set the sampling level. One of
                        DEFAULT, FASTER or HIGHER_PRECISION.
     -m METRICS, --metrics=METRICS
                        The metrics data to be retrieved from the API. A
                        single request is limited to a maximum of 10 metrics.
     -p PROFILE_ID, --profile_id=PROFILE_ID
                        The namespaced view (profile) ID of the view (profile)
                        from which to request data.
     -r MAX_RESULTS, --max_results=MAX_RESULTS
                        Maximum number of results to retrieve from the API.
                        The default is 1000 but can be set up to 10000.
     -s SORT, --sort=SORT
                        The order and direction to retrieve the results. Can
                        have multiple dimensions and metrics.