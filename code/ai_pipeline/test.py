import requests

req = requests.request( "GET", "http://10.243.248.146:5000/points", timeout = None )

print( req.data )