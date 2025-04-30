# ------------------------------------------------------------------------------
# Name:         SecMark DDoSsia Monitor
# Description:  Tool to monitor if specific URLs, TLDs or IP addresses
#               have ended up on the NoName057(16) DDoSsia projects target list
# 
# Author:       markus@secmark.fyi
# 
# Created:      30.04.2025
# License:      MIT
# ------------------------------------------------------------------------------

import requests
import json
import argparse
import string
import pprint

def main():
    try:
        # Get raw target data
        url = r"https://www.witha.name/data/last.json"
        response = requests.get(url=url)
        data = json.loads(response.content)

        # User Defined Targets
        targets = []
        # DDoSsia Targets
        ddostarget = []

        # This list stores any actual hits
        alerts = []
        fullalerts = []

        # Build list of target hosts and IP addresses
        for target in data["targets"]:
            if (target["host"], target["ip"]) in ddostarget:
                continue
            else:
                ddostarget.append((target["host"], target["ip"]))

        # Parse input arguments
        parser = argparse.ArgumentParser(
            prog="DDoSsia_monitor.py", 
            description="'SecMark DDoSsia Monitor' is a tool to monitor if specific URLs, TLDs or IP addresses have ended up on the NoName057(16) DDoSsia projects target list.", 
            epilog=".")
        options =parser.add_mutually_exclusive_group()
        options.add_argument("-t", "--target", metavar="", help="Comma separated list of targets ip1,ip2,url1,tld1")
        options.add_argument("-tf", "--target-file", metavar="", help="Wordlist of targets")
        parser.add_argument("-v", "--verbose", help="Increase verbosity of output", action="store_true")
        parser.add_argument("IP", help="IP Address (ex. 192.168.1.1)", action="store_true")
        parser.add_argument("Domain", help="Domain without protocol (ex. 'example.com')", action="store_true")
        parser.add_argument("TLD", help="Top level domain (ex. '.com', '.co.uk', '.org')(", action="store_true")
        parser.add_argument("CIDR", help="CIDR/24 leave the last number out (ex. '1.2.3.')", action="store_true")
        args = parser.parse_args()

        # Put user input targets list into targets list
        if args.target is not None:
            if "," in args.target:
                for i in args.target.split(","):
                    targets.append(i)
            elif ";" in args.target:        
                for i in args.target.split(";"):
                    targets.append(i)
            else:
                targets.append(args.target)

        elif args.target_file is not None:
            with open(args.target_file, "r") as targetfile:
                while True:
                    line = targetfile.readline()
                    if not line:
                        break
                    print(line.strip())  # Remember to strip newline
                    targets.append(line.strip())

        # TLD check
        def tldcheck(tld):
            for i in ddostarget:
                if tld.count(".") == 1:
                    if i[0].split(".")[-1] == tld[1:]:
                        alerts.append(i[0])
                    else:
                        pass
                else:
                    if i[0].split(".")[-2] == tld.split(".")[-2]:
                        alerts.append(i[0])
                    else:
                        pass
            return 0

        # IP/CIDR address check
        def ipcheck(ip):
            for i in ddostarget:
                if ip in i[1]:
                    alerts.append(i[1])
                else:
                    pass
            return 0

        # Domain
        def domaincheck(domain):
            for i in ddostarget:
                if domain in i[0]:
                    alerts.append(i[0])
                else:
                    pass
            return 0


        for item in targets:
            if item[0] == ".":  # TLD check
                tldcheck(item)
            elif item[0] in string.digits:  # IP/CIDR address check
                ipcheck(item)
            else:  # Domain
                domaincheck(item)


        print(args.verbose)
        if args.verbose is True:
            for alert in alerts:
                for dt in data["targets"]:
                    if alert in dt["host"] or alert in dt["ip"]:
                        fullalerts.append(dt)
                    else:
                        pass
            pprint.pprint(fullalerts, sort_dicts=False)
        else:
            pprint.pprint(alerts, sort_dicts=False)
    except Exception as e:
        print("An error occurred, you are using it wrong.")
    finally:
        return 1

if __name__ == "__main__":
    main()