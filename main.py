#!/usr/bin/env python3
import argparse
import os.path

from docx import Document

from Modules.GenerateAppendix import AppendixGenerator
from Modules.KeyFunctions import exportCsv, export_cred_stuffing, export_usernames, export_ip_hostnames, \
    export_open_ports, export_nuclei_scope, parse_hostname_enumerator
from Modules.ParseDehashed import ParseDehashed
from Modules.ParseNmap import NmapParse


# Usage: python3 generate_appendix.py --nmap nmap.xml --dehashed dehashed.json \
# --template template.docx --output outputfile.docx
# This will create a new docx file in an 'output' directory in the directory
# from which this tool is called.


def run():
    parser = argparse.ArgumentParser(
        description='Make constructing the IP table easy')
    parser.add_argument('-n', '--nmap', dest='nmaps',
                        nargs='+', help='The nmap file(s) to parse')
    parser.add_argument('-d', '--dehashed', dest='dehashed',
                        nargs='+', help='The dehashed JSON file(s) to parse')
    parser.add_argument('-o', '--output', dest='output',
                        help='The name of the output file')
    # parser.add_argument('-t', '--template', dest='template',
    #                     required=True, help='The path to the template file')
    parser.add_argument('-m', '--max', dest='max',
                        help='Exclude hosts with more than X open ports from the listening services table')
    parser.add_argument('-he', '--hostname-enumerator', dest='hostname_enumerator',
                        help='Hostname-Enumerator file')

    options = parser.parse_args()

    base_dir = os.path.dirname(__file__)
    template_file = base_dir + "/Template/appendix.docx"

    nmap_files = options.nmaps
    dehashed_files = options.dehashed
    if not options.output:
        output_file = 'appendix_output.docx'
    else:
        output_file = options.output
    hostname_enumerator = options.hostname_enumerator

    breached_creds = {}
    ips = {}
    port_count = {}
    cred_stuffing = []
    password_spray = []

    if not os.path.exists("./output/"):
        os.mkdir("./output/")

    parse_hostname_enumerator(hostname_enumerator, ips)

    if nmap_files:
        print("[+] Parsing Nmap file(s)")
        for nmap_file in nmap_files:
            parsed_nmap = NmapParse(nmap_file, options=options)
            parsed_nmap.parse_xml(ips, port_count)

    if dehashed_files:
        print("[+] Parsing Dehashed file(s)")
        for dehashed_file in dehashed_files:
            parsed_dehashed = ParseDehashed(
                dehashed_file, options=options)
            parsed_dehashed.parse_dehashed_json(
                breached_creds, password_spray, cred_stuffing)

    print("[+] Preparing to export the appendix")
    document = Document(template_file)
    appendix = AppendixGenerator(options)
    print("[+] Exporting the appendix")
    appendix.export_doc(breached_creds, ips, document, output_file)
    print("[+] Export complete")
    print("-----")
    print("[+] Exporting port count to CSV file")
    exportCsv(port_count)
    print("[+] Exporting list for credential stuffing")
    export_cred_stuffing(cred_stuffing)
    print("[+] Exporting username list for password spraying")
    export_usernames(password_spray)
    print("[+] Exporting IP and hostnames")
    export_ip_hostnames(ips)
    print("[+] Exporting open ports")
    export_open_ports(port_count)
    print("[+] Exporting Nuclei scope list")
    export_nuclei_scope(ips)
    print("[+] Done!")


if __name__ == "__main__":
    run()
