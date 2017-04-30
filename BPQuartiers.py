# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# def
import requests
import json
from StringIO import StringIO

FILE_USERPWD = 'userpwd.txt'
FILE_COUNTER = 'counter.txt'
FILE_DISTRICTLIST = 'districtList.json'

def fetchJson(district):
  if district:
    address = 'http://www.battleparis.com/api/zones/%s/' % district
  else:
    return

  auth = readFile(FILE_USERPWD)[:-1].split(':')

  headers = {'Content-type': 'application/json'}
  
  r = requests.get(address, auth=(auth[0], auth[1]), headers = headers)

  body = r.json()
  #print(body)


def readFile(file):
  # open / read / close / return
  openedFile = open(file)
  fileContent = openedFile.readline()
  openedFile.close()
  return fileContent

def writeCounter(newCount):
  # open / truncate / write / close
  currentCounterFile = open(FILE_COUNTER, 'w')
  currentCounterFile.truncate()
  currentCounterFile.write(str(newCount))
  currentCounterFile.close()

def getCurrentDistrict():
  # read districts list
  with open(FILE_DISTRICTLIST, 'r') as f:
    districtList = json.load(f)

  # read the counter
  currentCounter = int(readFile(FILE_COUNTER))
  # identify the current district
  districtUrl = districtList[currentCounter]['url']
  # fetch the json of the current district
  districtJson = fetchJson(districtUrl)
  
  return districtJson, districtUrl, currentCounter, len(districtList)

def getDistrict(district):
  # read districts list
  with open(FILE_DISTRICTLIST, 'r') as f:
    districtList = json.load(f)

  # identify the current district
  districtUrl = districtList[district]['url']
  # fetch the json of the current district
  districtJson = fetchJson(districtUrl)
  
  return districtJson, districtUrl

def getFormattedText(district = False):
  if district:
    district, districtUrl = getDistrict(district)
  else:
    district, districtUrl, districtID, totalDistricts = getCurrentDistrict()

  districtName = district['name']
  districtOrigin = district['origin']
  districtOwner = district['owner']
  districtDesc = district['description']
  districtUrl = "\n\nhttp://battle.paris/districts/" + districtUrl

  # sort scores by score number
  scoresList = sorted(district['scores'], key=lambda k: k['score'], reverse=True)
  # take next up
  nextTeam = scoresList[1]['name']
  nextTeamScore = scoresList[1]['score']

  # formatter depends on the score
  if nextTeamScore > 95:
    formatter = "Allerte rouge ! %s est très proche, à %d%% !"
  elif nextTeamScore > 80 and nextTeamScore <= 95:
    formatter = "Attention, %s remonte, ils sont quand même à %d%%"
  elif nextTeamScore > 60 and nextTeamScore <= 80:
    formatter = "%s est à %d%%, c'est une bonne avance"
  elif nextTeamScore > 30 and nextTeamScore <= 60:
    formatter = "%s est à %d%%, c'est super confortable"
  elif nextTeamScore > 10 and nextTeamScore <= 30:
    formatter = "On est super large, %s n’est qu’à %d%%"
  else:
    formatter = "Aucun souci. %s est à %d%% et ça ne changera pas de sitôt !"

  # building all the text
  startOutputText = '%s\n\n' % districtName
  endOutputText = '\n\nAppartient à %s (origine: %s)\n' % (districtOrigin, districtOwner)
  endOutputText += formatter % (nextTeam, nextTeamScore)

  descCutoffPoint = 499 - ( len(startOutputText) + len(endOutputText) + len(districtUrl) )

  districtDesc = districtDesc[:descCutoffPoint]
  districtDesc = ' '.join(districtDesc.split(' ')[:-1])

  outputText = startOutputText + districtDesc + "…" + endOutputText + districtUrl

  try:
    districtID
  except NameError:
    return outputText
  else:
    if outputText != False and len(outputText) <= 500:
      districtID += 1
      if districtID == totalDistricts:
        districtID = 0
      writeCounter(districtID)
    return outputText
