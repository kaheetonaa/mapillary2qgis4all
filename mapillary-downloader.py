import urllib.request, json 
import pandas as pd
from pyproj import Transformer

#check canvas

project_espg=str(QgsProject.instance().crs().authid())
destination_espg='EPSG:4326'
transformer = Transformer.from_crs(project_espg, destination_espg)
canvas = iface.mapCanvas()
original_extent=canvas.extent().toString().split(":")
transform_extent=[]
for coord in original_extent:
    coord=[float(i) for i in coord.split(",")]
    coord=transformer.transform(coord[0],coord[1])
    transform_extent=transform_extent+[i for i in coord]
print(transform_extent)

#download from Mapillary

limit_number=10
start_date="2015-01-11T00:00:00Z"
end_date="2015-12-31T23:59:59Z"
user=NULL #NULL
pano="false"

extent=str(transform_extent[1])+","+str(transform_extent[0])+","+str(transform_extent[3])+","+str(transform_extent[2])
if(user!=NULL):
    extent+=user

with urllib.request.urlopen("https://graph.mapillary.com/images?access_token=MLY|4463150933761310|5995ca3757fc4f9a9c8f5e96b2efaa03&fields=id&bbox="+extent+"&limit="+str(limit_number)+"&start_captured_at="+start_date+"&end_captured_at="+end_date+"&is_pano="+str(pano)) as url:
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

#add data to QGIS

uri = "point?crs=epsg:4326"

temp = QgsVectorLayer(uri,"Mapillary","memory")
temp_data = temp.dataProvider()
# Start of the edition 
temp.startEditing()

# Creation of my fields 
columns=['id','id_mapillary','angle','captured_at','thumb_256','url']
type=[QVariant.Double,QVariant.Double,QVariant.Double,QVariant.String,QVariant.String,QVariant.String]

for i in range(len(type)) : 
    myField = QgsField(columns[i] ,type[i])
    temp.addAttribute(myField)
# Update     
temp.updateFields()

# Addition of features
# [1] because i don't want the indexes 
for row in df.itertuples():
    print(row)
    f = QgsFeature()
    f.setAttributes([row[i] for i in range(0,6)])
    f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(row[6], row[7])))
    temp.addFeature(f)
    
# saving changes and adding the layer
temp.loadNamedStyle('https://raw.githubusercontent.com/kaheetonaa/mapillary2qgis4all/refs/heads/main/style.qml')
temp.commitChanges()
QgsProject.instance().addMapLayer(temp)
