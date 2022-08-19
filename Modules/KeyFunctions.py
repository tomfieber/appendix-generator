#!/usr/bin/env python3

def check_abnormal(ip, af=None):
    abnormal = []
    if af:
        with open(af, 'r') as ab:
            for line in ab:
                clean_line = line.strip()
                abnormal.append(clean_line)
    return ip in abnormal


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
            value = banner[i+1]
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
    with open('./output/credential-stuffing.txt', 'w') as file:
        file.write(f"Credential Stuffing Lists\n")
        file.write(f"-----\n\n")
        file.write(f"Usernames\n\n")
        for tuple in lst:
            file.write(f"{tuple[0]}\n")
        file.write(f"\n\n")
        file.write(f"Passwords\n\n")
        for tuple in lst:
            file.write(f"{tuple[1]}\n")


def export_usernames(lst):
    with open('./output/password-spray.txt', 'w') as file:
        file.write(f"Password Spray List\n")
        file.write(f"-----\n\n")
        for name in lst:
            name = name.strip()
            file.write(f"{name}\n")
