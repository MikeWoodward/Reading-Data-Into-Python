import urllib

url = ("https://www.marineband.marines.mil"
       "/Portals/175/Docs/Audio/Taps/"
       "Taps_Matt_Harding.mp3")

web_resource = (urllib
                .request
                .urlopen(url)
                )

mp3_data = web_resource.read()

with open("taps.mp3", 'wb') as f:
    f.write(mp3_data)
