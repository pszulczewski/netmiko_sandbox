#!/usr/bin/env python3
import argparse
import json
from pprint import pprint
from netmiko_mock import NetmikoMock


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--device-type", help="Netmiko device driver i.e 'cisco_ios'.", required=True)
parser.add_argument("-c", "--command", help="Command to run.", required=True)
parser.add_argument("-u", "--use-textfsm", help="Use textFSM to transform command output.", action="store_true")
parser.add_argument("-p", "--pprint", help="Use pretty print to display command output.", action="store_true")
parser.add_argument("-j", "--json", help="Display as json.", action="store_true")
args = parser.parse_args()

with NetmikoMock(device_type=args.device_type) as device:
    cmd = device.send_command(args.command, use_textfsm=args.use_textfsm)

if args.json:
    if args.use_textfsm:
        print(json.dumps(cmd, indent=4))
    else:
        print("WARNING: use -ju for json output.")
elif args.pprint:
    pprint(cmd)
else:
    print(cmd)
