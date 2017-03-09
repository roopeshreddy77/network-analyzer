from django.shortcuts import render
import dpkt
import socket
import pygeoip
import optparse

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

def printRecord(tgt):
      rec = gi.record_by_name(tgt)
      city= rec['city']
      country= rec['country_name']
      long= rec['longitude']
      lat= rec['latitude']
      return (tgt, lat, long, city, country)
      #print '[*] Target: '+tgt+' Geo-located. '
      #print '[+] '+str(city)+','+str(country)
      #print '[+] Latitude: '+str(lat)+ ', Longitude : '+ str(long)
def printPcap(pcap):
   uniqueIP = set()
   for (ts, buf) in pcap:
      try:
         eth = dpkt.ethernet.Ethernet(buf)
         ip = eth.data
         src = socket.inet_ntoa(ip.src)
         dst = socket.inet_ntoa(ip.dst)
         uniqueIP.add(src)	 
         
         #print '[+] Src: ' + src 
         #print '[+] Src: ' + printRecord(src) 
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
    for item in unique:
    
      print 'IP:' + str(item[0]) + ' Lat:' + str(item[1]) + ' Long:' + str(item[2]) + ' City:' + str(item[3]) + ' Country:' + str   (item[4])
    return render(request, 'netanalyzer/result.html')








