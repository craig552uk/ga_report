# -*- coding: utf-8 -*-
#
# Run a simple report from GA and print the results

import sys
import ga_helper as GA
from apiclient.errors import HttpError
from optparse import OptionParser, OptionGroup

__author__  = "Craig Russell <craig@craig-russell.co.uk>"
__version__ = "0.1"

DESCRIPTION = """A command line tool for querying the Google Analytics Reporting API.
For more information about API options see: 
https://developers.google.com/analytics/devguides/reporting/core/v3/reference
https://developers.google.com/analytics/devguides/reporting/core/dimsmets"""

EPILOG = "Author: %s" % __author__

# Command line options
parser = OptionParser(usage="Usage: ga_report [options]", description=DESCRIPTION, epilog=EPILOG, version=__version__)
parser.add_option("-F",  "--field_seperator", dest="field_seperator", metavar="FIELD_SEPERATOR", default=",",   help="The field seperator in the output.")
parser.add_option("-H",  "--headings",        dest="headings",        action="store_true",       default=False, help="Show filed headings in the output")
parser.add_option("-L",  "--list_profiles",   dest="list_profiles",   action="store_true",       default=False, help="List all Profiles available to the authenticated user (rate limit permitting)")
parser.add_option("-P",  "--fetch_all_pages", dest="fetch_all_pages", action="store_true",       default=False, help="If there is more than one page of results, fetch them all")

group  = OptionGroup(parser, "Google Analytics Reporting Options")
group.add_option("-b",  "--start_date",      dest="start_date",      metavar="START_DATE",      default=None,  help="Beginning date to retrieve data in format YYYY-MM-DD.")
group.add_option("-d",  "--dimensions",      dest="dimensions",      metavar="DIMENSIONS",      default=None,  help="The dimension data to be retrieved from the API. A single request is limited to a maximum of 7 dimensions.")
group.add_option("-e",  "--end_date",        dest="end_date",        metavar="END_DATE",        default=None,  help="Final date to retrieve data in format YYYY-MM-DD.")
group.add_option("-f",  "--filters",         dest="filters",         metavar="FILTERS",         default=None,  help="Specifies a subset of all data matched in analytics.")
group.add_option("-g",  "--segment",         dest="segment",         metavar="SEGMENT",         default=None,  help="Specifies a subset of visits based on either an expression or a filter. The subset of visits matched happens before dimensions and metrics are calculated.")
group.add_option("-i",  "--start_index",     dest="start_index",     metavar="START_INDEX",     default=None,  help="Use this parameter to request more rows from the API. The index starts from 1 and the default is 1.")
group.add_option("-l",  "--sampling_level",  dest="sampling_level",  metavar="SAMPLING_LEVEL",  default=None,  help="Use this parameter to set the sampling level. One of DEFAULT, FASTER or HIGHER_PRECISION.")
group.add_option("-m",  "--metrics",         dest="metrics",         metavar="METRICS",         default=None,  help="The metrics data to be retrieved from the API. A single request is limited to a maximum of 10 metrics.")
group.add_option("-p",  "--profile_id",      dest="profile_id",      metavar="PROFILE_ID",      default=None,  help="The namespaced view (profile) ID of the view (profile) from which to request data.")
group.add_option("-r",  "--max_results",     dest="max_results",     metavar="MAX_RESULTS",     default=None,  help="Maximum number of results to retrieve from the API. The default is 1000 but can be set up to 10000.")
group.add_option("-s",  "--sort",            dest="sort",            metavar="SORT",            default=None,  help="The order and direction to retrieve the results. Can have multiple dimensions and metrics.")

parser.add_option_group(group)

def list_profiles():
    """Lists all Profiles available to the authenticated user (rate limit permitting)"""
    try:
        accounts = GA.get_accounts()
        if accounts.get('items'):
            for account in accounts.get('items'):
                print "%s" % account.get('name')

                web_properties = GA.get_web_properties(account.get('id'))
                if web_properties.get('items'):
                    for web_property in web_properties.get('items'):
                        print "  %s (%s)" % (web_property.get('name'), web_property.get('id'))

                        if web_property.get('profileCount') > 0:
                            profiles = GA.get_profiles(account.get('id'), web_property.get('id'))
                            for profile in profiles.get('items'):
                                print "    %s: %s" % (profile.get('id'), profile.get('name'))

    except HttpError as e:
        print >> sys.stderr, "ERROR: %s" % e._get_reason()

def run_report(options):
    """Run a GA Report using options on the command line"""
    try:

        query = {
            'profile_id':     options.profile_id,
            'start_date':     options.start_date,
            'end_date':       options.end_date,
            'dimensions':     options.dimensions,
            'metrics':        options.metrics,
            'segment':        options.segment,
            'filters':        options.filters,
            'sort':           options.sort,
            'max_results':    options.max_results,
            'sampling_level': options.sampling_level,
            'start_index':    options.start_index,
        }

        # Fetch data
        report = GA.get_report(**query)
        sum_results = len(report.get('rows'))

        # Print field headings
        if options.headings:
            if options.dimensions:
                print options.field_seperator.join((options.dimensions + "," + options.metrics).split(","))
            else:
                print options.field_seperator.join(options.metrics.split(","))

        # Print data
        for row in report.get('rows'):
            print options.field_seperator.join(row)

        while options.fetch_all_pages and report.get('nextLink'):
            
            # Fetch subsequent pages if there are any
            query['start_index'] = sum_results + 1
            report = GA.get_report(**query)
            sum_results += len(report.get('rows'))

            # Print data
            for row in report.get('rows'):
                print options.field_seperator.join(row)


    except TypeError as e:
        print >> sys.stderr, "ERROR: %s" % e

    except HttpError as e:
        print >> sys.stderr, "ERROR: %s" % e._get_reason()


if __name__ == "__main__":
    (options, args) = parser.parse_args()
    if options.list_profiles:
        list_profiles()
    else:
        run_report(options)
