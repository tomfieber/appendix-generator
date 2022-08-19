#!/usr/bin/env python3

from libnmap.parser import NmapParser
from Modules.KeyFunctions import check_abnormal, check_open


class NmapParse(object):

    def __init__(self, file, options):
        self.file = file
        self.options = options

    def parse_xml(self, ips, pd, pc):
        af = self.options.exclude
        nmap_parse = NmapParser.parse_fromfile(self.file)
        for host in nmap_parse.hosts:
            ip = str(host.address)
            if not check_abnormal(ip, af):
                if host.hostnames:
                    hostname = host.hostnames[0]
                else:
                    hostname = ""
                if ip not in ips.keys():
                    ips[ip] = [hostname + '\n']
                else:
                    ips[ip].append(hostname + '\n')

                # Get a dictionary object of all service details
                for service in host.services:

                    svcDetails = service.get_dict()
                    port = svcDetails['port']
                    svcState = svcDetails['state']
                    svcProtocol = svcDetails['protocol'].upper()

                    port_is_open = check_open(svcState)

                    if port_is_open:

                        # Get a count of all ports across hosts
                        if port not in pc.keys():
                            pc[port] = {'protocol': svcProtocol, 'count': 1}
                        else:
                            pc[port]['count'] += 1

                        #self.generate_port_dataset(pd, ip, svcDetails)
                        if ip not in pd.keys():
                            pd[ip] = [svcDetails]
                        elif ip in pd.keys() and svcDetails not in pd[ip]:
                            pd[ip].append(svcDetails)
                        else:
                            continue
