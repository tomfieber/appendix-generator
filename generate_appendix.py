#!/usr/bin/env python3

# Usage: python3 generate_appendix.py --nmap nmap.xml --dehashed dehashed.json \
# --template template.docx --output outputfile.docx

# This will create a new docx file in an 'output' directory in the directory
# from which this tool is called.

from Modules.GenerateAppendix import AppendixGenerator
import argparse
from docx import Document
from Modules.KeyFunctions import exportCsv, export_cred_stuffing, export_usernames
from Modules.ParseNmap import NmapParse
from Modules.ParseDehashed import ParseDehashed


def run():
    parser = argparse.ArgumentParser(
        description='Make constructing the IP table easy')
    parser.add_argument('-n', '--nmap', dest='nmaps',
                        nargs='+', help='The nmap file(s) to parse')
    parser.add_argument('-d', '--dehashed', dest='dehashed',
                        nargs='+', help='The dehashed JSON file(s) to parse')
    parser.add_argument('-o', '--output', dest='output',
                        help='The name of the output file')
    parser.add_argument('-t', '--template', dest='template',
                        required=True, help='The path to the template file')
    parser.add_argument('-x', '--exclude', dest='exclude',
                        help='The list (file) of hosts to exclude from the report')

    options = parser.parse_args()

    nmap_files = options.nmaps
    dehashed_files = options.dehashed
    if not options.output:
        output_file = 'appendix_output.docx'
    else:
        output_file = options.output
    template_file = options.template

    breached_creds = {}
    ips = {}
    ports = {}
    port_count = {}
    cred_stuffing = []
    password_spray = []

    if nmap_files:
        print("[+] Parsing Nmap file(s)")
        for nmap_file in nmap_files:
            parsed_nmap = NmapParse(nmap_file, options=options)
            parsed_nmap.parse_xml(ips, ports, port_count)

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
    appendix.export_doc(breached_creds, ips, ports, document, output_file)
    print("[+] Export complete")
    print("-----")
    print("[+] Exporting port count to CSV file")
    exportCsv(port_count)
    print("[+] Exporting list for credential stuffing")
    export_cred_stuffing(cred_stuffing)
    print("[+] Exporting username list for password spraying")
    export_usernames(password_spray)
    print("[+] Done!")


if __name__ == "__main__":
    run()
