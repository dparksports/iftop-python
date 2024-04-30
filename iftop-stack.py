import psutil
import time
import socket
import os
import sys
print(os.path.dirname(sys.executable))
from collections import defaultdict
from ipwhois import IPWhois
import ipaddress
import datetime
import socket
import ssl
import pprint

def isIpAddress(ip):
   try:
       ip_object = ipaddress.ip_address(ip)
       return True
   except ValueError:
       return False

def print_addresses(connection, process_name):
    addr_to = connection[4]
    print(addr_to.ip, addr_to.port, process_name)

def get_process_name(pid):
    try:
        process_name = psutil.Process(pid).name()
    except:
        process_name = connection.pid
    return process_name        

def get_hostname(ip):
    try:
        hostname = socket.getfqdn(ip)
    except:
        try:
            hostname = socket.gethostbyaddr(ip)
        except:
            print("not hostname", ip)
            hostname = ip        

    if isIpAddress(hostname):
        hostname = whois(ip)
    return hostname        

def whois(ip):
    try:
        obj = IPWhois(ip)
        results = obj.lookup_rdap(depth=1)    
        hostname = results['entities'][0]
    except:
        hostname = ""
    return hostname        

def get_subject(ip):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.load_default_certs()
    conn = context.wrap_socket(socket.socket(socket.AF_INET),
                               server_hostname=ip)
    conn.connect((ip, 443))
    cert = conn.getpeercert()
    # pprint.pprint(cert)
    return cert['subject']

def get_subject_dns(ip):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.load_default_certs()
    conn = context.wrap_socket(socket.socket(socket.AF_INET),
                               server_hostname=ip)
    conn.connect((ip, 443))
    cert = conn.getpeercert()
    # pprint.pprint(cert)
    return cert['subjectAltName']

def get_common_name(ip, port):
    # print(ip, port)
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.load_default_certs()
        conn = context.wrap_socket(socket.socket(socket.AF_INET),
                                server_hostname=ip)
        conn.connect((ip, port))
    except:
        context = ssl._create_unverified_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE        
        context.load_default_certs()
        conn = context.wrap_socket(socket.socket(socket.AF_INET),
                                server_hostname=ip)
        try:
            conn.connect((ip, port))
        except:
            return "Handshake"
            
    cert = conn.getpeercert()
    if len(cert) == 0:
        return "None"
        
    subject = cert.get('subject', None)
    if subject is None:
        subject = cert.get('subjectAltName', None)
    if len(subject) > 1:
        return subject[-1][0][-1] + ' ' + subject[-2][0][-1]
    else:
        return subject[0][0][-1]


connected_list = defaultdict(list)
previous_count = 0
hostnames = {}
common_names = {}
process_names = {}
while True:
    current = psutil.net_connections(kind='tcp')
    for connection in current:
        addr_from = connection[3]
        addr_to = connection[4]
        if len(addr_to) == 0:
            continue
        if "127.0.0.1" == addr_to.ip:
            continue
        if "ESTABLISHED" != connection.status:
            continue

        process_name = get_process_name(connection.pid)
        process_names[connection.pid] = process_name
        connected_list[addr_to.ip].append((addr_to.port, process_name))
        connected_list[addr_to.ip] = sorted(set(connected_list[addr_to.ip]))

    if previous_count == len(process_names.keys()):
        time.sleep(1)
        continue
    else:
        previous_count = len(process_names.keys())

    print(datetime.datetime.now()) 
    for item in connected_list.items():
        ip = item[0]
        port = item[1][0][0]
        name = item[1][0][1]
        common_name = common_names.get(ip, "")
        if len(common_name) == 0:
            common_name = get_common_name(ip, port)
            common_names[ip] = common_name

        hostname = hostnames.get(ip, "")
        if len(hostname) == 0:
            hostname = get_hostname(ip)
            hostnames[ip] = hostname

        print(ip, port, hostname, common_name, name)
