import requests


data = requests.request( url = "http://192.168.8.122:40324/image", method = "get" )

print( data.json() )


data = requests.request( url = "http://192.168.8.114:40325/points", method = "get" )

print( data.json() )


