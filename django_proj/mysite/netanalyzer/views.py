from django.shortcuts import render
import dpkt
import socket
import pygeoip
from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponse
import json

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

def printRecord(tgt):
      rec = gi.record_by_name(tgt)
      city= rec['city']
      country= rec['country_name']
      long= rec['longitude']
      lat= rec['latitude']
      return (tgt, lat, long, city, country)
   
def printPcap(pcap):
   uniqueIP = set()
   for (ts, buf) in pcap:
      try:
         eth = dpkt.ethernet.Ethernet(buf)
         ip = eth.data
         src = socket.inet_ntoa(ip.src)
         dst = socket.inet_ntoa(ip.dst)
         uniqueIP.add(src)	  
      except:
         pass

   
   uniqueLatLong = set()
   for item in uniqueIP:
      

      try:
         uniqueLatLong.add(printRecord(item))
      except:
         pass
   return uniqueLatLong
   print "Unique Lat Long :"
   

def index(request):
    return render(request, 'netanalyzer/home.html')
def search(request):
    pcapFile = '/home/roopeshreddy77/'+request.GET['file_upload']
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    unique = printPcap(pcap)
    print unique
    js = []
    for item in unique:
    
      obj={"IP": str(item[0]), "Lat": str(item[1]), "Long": str(item[2]), "City": str(item[3]), "Country": str(item[4])}
      js.append(obj)
      lat=str(item[1])
      lng=str(item[2])
      ip=str(item[0])
      city=str(item[3])
      country=str(item[4])
    print js
   
    fp=open('/home/roopeshreddy77/django_proj/mysite/netanalyzer/templates/netanalyzer/result.html')

    t=Template(fp.read())
    fp.close()
    html=t.render(Context({'data' : js}))
    return HttpResponse(html)
    








