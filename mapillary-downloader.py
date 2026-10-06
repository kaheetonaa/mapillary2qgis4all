import urllib.request, json 
import pandas as pd
from pyproj import Transformer
import urllib.request

#download from Mapillary

limit_number=100
start_date="2006-01-11T00:00:00Z"
end_date="2026-12-31T23:59:59Z"
user="Francesco_Brs" #NULL
pano="true"

extent="9.684541257339498,44.898310695762866,9.820800861583075,45.0395098618434"
url="https://graph.mapillary.com/images?access_token=MLY|4463150933761310|5995ca3757fc4f9a9c8f5e96b2efaa03&fields=id&bbox="+extent+"&creator_username=i"+user+"&limit="+str(limit_number)+"&start_captured_at="+start_date+"&end_captured_at="+end_date+"&is_pano="+str(pano)
print(url)

with urllib.request.urlopen(url) as url:
    data = json.load(url)['data']

collection=[]

print(len(data))
progress=0

for i in data:
    print(str(int(progress/len(data)*100))+"%")
    progress=progress+1
    with urllib.request.urlopen("https://graph.mapillary.com/"+i['id']+"?access_token=MLY|4463150933761310|5995ca3757fc4f9a9c8f5e96b2efaa03&fields=id,computed_geometry,compass_angle,captured_at,thumb_256_url,thumb_original_url") as url:
        input = json.load(url)
        photo={}
        try:
            photo['id']=input['id']
            photo['angle']=input['compass_angle']
            photo['captured_at']=input['captured_at']
            photo['thumb_256_url']=input['thumb_256_url']
            photo['thumb_original_url']=input['thumb_original_url']
            photo['x']=input['computed_geometry']['coordinates'][0]
            photo['y']=input['computed_geometry']['coordinates'][1]
            collection+=[photo]
        except:
            print('missing data for '+i['id'])

df=pd.DataFrame(collection)

