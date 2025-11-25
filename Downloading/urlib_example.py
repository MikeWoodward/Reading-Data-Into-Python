import urllib

url = ("""http://www.marseillaise.org"""
       """/audio/mireille_mathieu_-_"""
       """la_marseillaise.mp3""")

web_resource = (urllib
                .request
                .urlopen(url)
                )

mp3_data = web_resource.read()

with open("La Marseillaise.mp3", 'wb') as f:
    f.write(mp3_data)
