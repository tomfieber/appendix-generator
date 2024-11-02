#!/usr/bin/env python3


def check_abnormal(ip, d, max_limit=30):
    return len(d[ip]['svcDetails']) > max_limit


def join_values(l):
    return " ".join(l)


def split_banner(b):
    headings = {'test': 'test'}
    banner = b.split()
    heading_word = ""
    value = ""
    for i in range(len(banner)):

        word = banner[i]
        last_word = banner[-1]
        if word.endswith(':') and word is not last_word:
            heading_word = word.strip(':')
            value = banner[i + 1]
            headings[heading_word] = [value]
        elif word is not value:
            try:
                headings[heading_word].append(word)
            except KeyError:
                continue

    try:
        product = headings['product']
        full_product = join_values(product)
    except KeyError:
        full_product = 'Unknown'

    try:
        version = headings['version']
        full_version = join_values(version)
    except KeyError:
        full_version = 'Unknown'
    return full_product, full_version


def get_port_details(dict):
    port = dict['port']
    protocol = dict['protocol']
    service = dict['service']
    banner = dict['banner']
    product, version = split_banner(banner)
    return port, protocol, service, product, version


def check_open(state):
    return state == "open"


def exportCsv(dict):
    with open('./output/listening-services.csv', 'w') as csvfile:
        csvfile.write(f"Port, Listening Services\n")
        for key in dict.keys():
            csvfile.write(
                f"{key} - {dict[key]['protocol']}, {dict[key]['count']}\n")


def export_cred_stuffing(lst):
    with open('./output/cs-usernames.txt', 'w') as file:
        for tuple in lst:
            file.write(f"{tuple[0]}\n")
        file.write(f"\n\n")
    with open('./output/cs-passwords.txt', 'w') as file:
        for tuple in lst:
            file.write(f"{tuple[1]}\n")


def export_usernames(lst):
    with open('./output/password-spray.txt', 'w') as file:
        for name in lst:
            name = name.strip()
            file.write(f"{name}\n")


def export_ip_hostnames(dict):
    with open('./output/ip-hostnames.txt', 'w') as file:
        for ip in dict.keys():
            file.write(f"{ip}\n")
        for ip in dict.keys():
            for hostname in dict[ip]['hostnames']:
                if len(hostname) > 1:
                    file.write(f"{hostname}\n")


def export_open_ports(dict):
    with open('./output/open-ports.txt', 'w') as file:
        for port in dict.keys():
            file.write(f"{port}\n")


def export_nuclei_scope(dict):
    with open('./output/nuclei-scope.txt', 'w') as nuclei:
        for prot in ['http', 'https']:
            for ip in dict.keys():
                if not check_abnormal(ip, dict):
                    for svc in dict[ip]['svcDetails']:
                        port = svc['port']
                        nuclei.write(f"{prot}://{ip}:{port}\n")
                        for hostname in dict[ip]['hostnames']:
                            if hostname != '-':
                                nuclei.write(f"{prot}://{hostname}:{port}\n")


# def export_port_hosts(dict, check_dict):
#     if not os.path.exists('./output/'):
#         os.mkdir('./output/')
#     with open(f'./output/hosts-by-port.txt', 'w') as file:
#         for port in dict.keys():
#             file.write(f"Port {port}\n\n")
#             for ip in dict[port]['ips']:
#                 if not check_abnormal(ip, check_dict):
#                     file.write(f"{ip}\n")
#                     for hostname in dict[port]['hostnames']:
#                             if hostname != '-':
#                                 file.write(f"{hostname}\n")
#             file.write("\n")


def parse_hostname_enumerator(file, dict):
    with open(file, 'r') as hostenum:
        data = hostenum.readlines()
        lines = [line.split('[') for line in data]
        for line in lines:
            hostname = line[0].strip()
            try:
                ip = line[1].strip(']\n')
            except IndexError:
                hostname = "***"
            if ip not in dict.keys():
                dict[ip] = {'hostnames': [hostname], 'svcDetails': []}
            else:
                if hostname not in dict[ip]['hostnames']:
                    # print(hostname, len(hostname))
                    dict[ip]['hostnames'].append(hostname)
