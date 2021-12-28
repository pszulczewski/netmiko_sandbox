# Netmiko Sandbox

## What is it?
This is an implementation of a Fake Device to create development sandbox to allow network engineers and developers 
to work with different vendor device types in a netmiko-like style, to retrieve raw or structured command outputs, 
without the requirement of running physical or virtual devices.

## How does it work?
`NetmikoMock` overwrites all major netmiko methods used to make connection to a device and retrieve a command output. 
It's coupled with `ntc-templates` repository (sub-repository) which has many `textFSM` templates and mock data for tests 
containing many raw & structured command outputs from multiple devices of different vendors.
This fake device leverages these mock files to return command output like netmiko does, but this time without the need
of running real or virtual devices.

## Key features
It reads textFSM CliTable index file available in ntc-templates directory, so it's able to "auto-complete" commands.

## Caveats
When a directory with mock files for a specific textFSM template is detected the first .raw or .yml file is returned. 
When many mock files are present under mock files, always the first one is returned.

Supported commands are limited to those having textFSM template and mock files in `ntc-templates` repository.

## Use Cases
* Easy access command outputs for many devices of different vendor types.
* Facilitate local development of netmiko scripts when device(s) are not available.
* Facilitate collecting raw or structured command outputs when developing network tests and mocking netmiko responses.

## Cloning repositories
```
git clone https://github.com/pszulczewski/netmiko_sandbox.git
cd netmiko_sandbox
# clone ntc-templates as sub-repository
git clone https://github.com/networktocode/ntc-templates.git
```

## Create environment
`poetry install`

`poetry shell` and you're good to go!

## Developing netmiko scripts with NetmikoMock
Connecting do devices over and over when developing a script can be slow, you can greatly speed it up by using Mock in 
similar way as using mocks for tests.

Let's consider the following scenarios:
1. import `NetmikoMock` as `ConnectHandler` the same way as you usually import `ConnectHandler` from netmiko and then 
work on your development locally. You can switch back to netmiko just by removing that extra import statement whenever 
you're ready to use your script on real devices.
2. Use `NetmikoMock` for a device or group of devices which you can't connect to.

See `main.py` for some examples. Keep in mind that commands are limited to what's available in `ntc-templates` 
repository.

## Using CLI tool to collect command outputs when writing network tests.

```
$ ./cli.py -h
usage: cli.py [-h] -d DEVICE_TYPE -c COMMAND [-u] [-p] [-j]

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE_TYPE, --device-type DEVICE_TYPE
                        Netmiko device driver i.e 'cisco_ios'.
  -c COMMAND, --command COMMAND
                        Command to run.
  -u, --use-textfsm     Use textFSM to transform command output.
  -p, --pprint          Use pretty print to display command output.
  -j, --json            Display as json.
```
Json output option should be used together with -u option structured output.

Imagine that you need structured command output to prepare mock files.

```
$ ./cli.py -d cisco_ios -c "show ip int br" -u -j
[
    {
        "intf": "Ethernet0/0",
        "ipaddr": "unassigned",
        "proto": "up",
        "status": "up"
    },
    {
        "intf": "Ethernet0/0.11",
        "ipaddr": "10.0.1.38",
        "proto": "up",
        "status": "up"
    },
    {
        "intf": "Ethernet0/1",
        "ipaddr": "1.1.1.1",
        "proto": "up",
        "status": "up"
    },
    {
        "intf": "Ethernet0/2",
        "ipaddr": "unassigned",
        "proto": "down",
        "status": "administratively down"
    },
    {
        "intf": "Ethernet0/3",
        "ipaddr": "unassigned",
        "proto": "down",
        "status": "administratively down"
    },
    {
        "intf": "Loopback0",
        "ipaddr": "10.0.1.2",
        "proto": "up",
        "status": "up"
    }
]
```
You can save this output as `show_ip_interface_brief.json` and use it to mock up netmiko output in your tests.
