#!/usr/bin/env python3

from libnmap.parser import NmapParser

from Modules.KeyFunctions import check_abnormal, check_open, get_port_details


class NmapParse(object):

    def __init__(self, file, options):
        self.file = file
        self.options = options
        self.MAX_LIMIT = 30

    def parse_xml(self, ips, pc):
        if self.options.max:
            self.MAX_LIMIT = int(self.options.max)
        nmap_parse = NmapParser.parse_fromfile(self.file)
        for host in nmap_parse.hosts:
            ip = str(host.address)
            # if not check_abnormal(ip, abnormal):
            if host.hostnames:
                hostname = host.hostnames[0]
            else:
                hostname = "-"
            if ip not in ips.keys():
                ips[ip] = {'hostnames': [hostname], 'svcDetails': []}
            elif hostname not in ips[ip]['hostnames'] and hostname != '-':
                ips[ip]['hostnames'].append(hostname)
            elif hostname == '-':
                continue

            # Get a dictionary object of all service details
            for service in host.services:

                svcDetails = service.get_dict()
                port, protocol, service, product, version = get_port_details(
                    svcDetails)
                svcState = svcDetails['state']
                svcProtocol = protocol.upper()

                port_is_open = check_open(svcState)

                if port_is_open:

                    # Get a count of all ports across hosts
                    if not check_abnormal(ip, ips, self.MAX_LIMIT):
                        if port not in pc.keys():
                            pc[port] = {'protocol': svcProtocol, 'count': 1}
                        else:
                            pc[port]['count'] += 1

                    if ip not in ips.keys():
                        ips[ip]['svcDetails'] = [svcDetails]
                        # print(ips[ip]['svcDetails'])
                    elif ip in ips.keys() and svcDetails not in ips[ip]['svcDetails']:
                        ips[ip]['svcDetails'].append(svcDetails)
                    else:
                        continue
