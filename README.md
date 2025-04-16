# mapillary2qgis4all

This piece of python code will download Mapillary data in QGIS canvas as a Point Vector layer.

## Usage

1. Copy all code inside mapillary-downloader.py into * Python console editor* in QGIS (Plugins/Python Console/Show editor)
2. Modify parameters to fit the need.
3. Click "Run Script" to run

### Parameters

1. * limit_number*: number of maximum mapillary images downloaded (current:10)
2. * start_date*: the start of time range filter (current: "2025-01-11T00:00:00Z")
3. * end_date*:the end of time range filter (current:"2025-12-31T23:59:59Z")
4. * user*: user filter, leave * NULL* in case does not limit to any users (current: NULL)
5. * pano*: including panoramic photo (current:"false")