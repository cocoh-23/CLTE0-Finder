#! /usr/bin/env python3
import sys
from unittest import result
import requests
import argparse
import logging
requests.packages.urllib3.disable_warnings()

parser = argparse.ArgumentParser()
parser.add_argument('-u','--urlFile', help='file with urls to test response codes', required=True)
parser.add_argument('-o','--outputFile', help='file to save urls with 30X and 400 response codes', required=True)
args = parser.parse_args()

#CL0Host = args.target.strip()
URLFilePath = args.urlFile.strip()
ResultsFilePath = args.outputFile.strip()

#Session config
session = requests.Session()
session.allow_redirects = False
session.stream = False

URLs = open(URLFilePath, "r")
results = open(ResultsFilePath, "a")
for url in URLs:
    url = url.rstrip()
    GetResponseCodeTest = session.get(url, allow_redirects=False).status_code
    PostResponseCodeTest = session.post(url, allow_redirects=False).status_code
    PutResponseCodeTest = session.put(url, allow_redirects=False).status_code
    requestQualifiesForCL0 = ((GetResponseCodeTest > 300 and GetResponseCodeTest < 404) or GetResponseCodeTest == 422) or ((PostResponseCodeTest > 300 and PostResponseCodeTest < 404) or PostResponseCodeTest == 422) or ((PutResponseCodeTest > 300 and PutResponseCodeTest < 404) or PutResponseCodeTest == 422)
    if(requestQualifiesForCL0):
        if((GetResponseCodeTest > 300 and GetResponseCodeTest < 404) or GetResponseCodeTest == 422 ):
            results.write(url + "---GET---" + str(GetResponseCodeTest) + "\n")
        if((PostResponseCodeTest > 300 and PostResponseCodeTest < 404) or PostResponseCodeTest == 422 ):
            results.write(url + "---POST---" + str(PostResponseCodeTest) + "\n")
        if((PutResponseCodeTest > 300 and PutResponseCodeTest < 404) or PutResponseCodeTest == 422 ):
            results.write(url + "---PUT---" + str(PutResponseCodeTest) + "\n")
results.close()
URLs.close()
