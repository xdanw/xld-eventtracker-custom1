
import json;
import datetime;
import requests;
import requests.utils;
# Fixes some issues with TLS
import os;

# This file is required for Requests.py TLS connections
os.environ['REQUESTS_CA_BUNDLE'] = 'ca.pem';

task = context.getTask();
repository = context.getRepository();

appName = str(task.getMetadata()['application']);
appVersion = str(task.getMetadata()['version']);
envName = str(task.getMetadata()['environment']);

deploymentPackage = repository.read("Applications/" + appName + "/" + appVersion);
deploymentEnv = repository.read("Environments/" + envName);
ticketRequired = "";
startTime = "unavailable";
if (context.getAttribute("start_time")) :
    startTime = context.getAttribute("start_time");

# Hardcoded parameter for Voya - to be changed
if (deploymentEnv.getProperty("requiresTicketNumber")) :
    ticketRequired = "true";
    ticketNumber = deploymentPackage.getProperty("satisfiesTicketNumber");
else : 
    ticketRequired = "false";
    ticketNumber = "not_required";

# DUMMY TEST
appCmdbId = "DUMMY_CMDB_ID";
# appCi = repository.read("Applications/" + appName);
# appCmdbId = appCi.getAttribute("Put_Cmdb_Property_Here");

# TImestamp
timeStamp = str(datetime.datetime.now());

# Hardcoded test URL - replace with your data bucket e.g. Splunk or Google Docs
url = 'http://127.0.0.1:8080/example?';

dataJSON = "{'appName': '" + appName + "', 'appCMDB': '" + appCmdbId + "', 'version': '" + appVersion + \
    "', 'ticket': '" + ticketNumber + "', 'start_time': '" + startTime + "', 'end_time': '" + timeStamp + "'}";

dataCSV = appName + "," + appCmdbId + "," + appVersion + \
    "," + ticketNumber + "," + startTime + "," + timeStamp + "\r\n";

print "XLDEventTracker: message - " + dataJSON;

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"};

# Filesystem write
outputFile = open("XLDEvents.csv", "a");
outputFile.write(dataCSV);
outputFile.close();

# Do the HTTP request
# response = requests.post(url, headers=headers ,data=data);

# Check for HTTP codes other than 200 and 201
# if response.status_code != 200 and response.status_code != 201:
#     print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
#     raise exception;

# Decode the JSON response into a dictionary
# data = response.json();

# --- End API ---

print "XLDEventTracker: data sent.";

