import json
import requests

with open('./config.json', 'r+') as outfile:
    config = json.loads(outfile.read())

myuuid = 'b4965441e34b477981d5e37976e7b6a2'
key = config["api"]["mainkey"]


data = requests.get("https://api.hypixel.net/player?key={}&name={}".format(key, "ramenling")).json()

XPLevel = data["player"]["stats"]["Bedwars"]["Experience"]
Star = 1
XPLevelModified = XPLevel
while True:
  if XPLevelModified > 487000: # Reduce Prestige
    XPLevelModified -= 487000
    Star += 100 # add to stars
  else: # now we have their prestige
    if XPLevelModified > 5000: # Reduce the 5th star and beyond
      XPLevelModified -= 5000
      Star += 1 # add to stars
    else: # now we have their 4-5th star
      if XPLevelModified > 3500: # Reduce the 4th star of the prestige
        XPLevelModified -= 3500
        Star += 1 # add to stars
      else: # now we have their 3-4th star
        if XPLevelModified > 2000: # Reduce the 3rd star of the prestige
          XPLevelModified -= 2000 
          Star += 1 # add to stars
        else:
          if XPLevelModified > 1000: # Reduce the 2nd star of the prestige
             XPLevelModified -= 1000
             Star += 1 # add to stars
          else:
            if XPLevelModified > 500: # Reduce the 1st star of the prestige
              XPLevelModified -= 500
              Star += 1 # add to stars
            else:
              break

print(Star)

