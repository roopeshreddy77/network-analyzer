import dpkt
import socket
import pygeoip
import optparse

gi = pygeoip.GeoIP('GeoLiteCity.dat')

def printRecord(tgt):
    rec = gi.record_by_name(tgt)
    city = rec['city']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    return (lat, long)

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
    print "Unique Ips :"

    uniqueLatLong = set()
    for item in uniqueIP:
        print item;
        try:
            uniqueLatLong.add(printRecord(item))
        except:
            pass

    print "Unique Lat Long :"
    for item in uniqueLatLong:
        print 'Lat:' + str(item[0]) + ' Long:' + str(item[1])


def main():
    #parser = optparse.OptionParser('usage%prog -p <pcap file>')
    #parser.add_option('-p', dest='pcapFile', type='string', \
    #                  help='specify pcap filename')
    #(options, args) = parser.parse_args()
    #if options.pcapFile == None:
        # print parser.usage
        # exit(0)
    #pcapFile = options.pcapFile
    pcapFile = 'ex1.pcap'
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)

if __name__ == '__main__':
    main()