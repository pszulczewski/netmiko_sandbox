from netmiko import ConnectHandler
from netmiko_mock import NetmikoMock  # import for direct use
from netmiko_mock import NetmikoMock as ConnectHandler  # temporary overwrite import to use NetmikoMock as ConnectHandler


# Use device object to retrive command output.
device = ConnectHandler(
    device_type="cisco_wlc_ssh",
    host="10.10.10.1",
    username="admin",
    password="admin"
)
device.open()
command = "show red det"
output = device.send_command(command, use_textfsm=True)
device.disconnect()

print("=" * 50 + device.platform + "=" * 50)
print(output)
print("=" * (100 + len(device.platform)))


# Or use context manager, so you don't need to worry about opening and closing connection.
with ConnectHandler(
    device_type="alcatel_sros",
    host="10.10.10.2",
    username="admin",
    password="admin"
) as device:
    command = "show router interfaces"
    output = device.send_command(command, use_textfsm=True)

    print("=" * 50 + device.platform + "=" * 50)
    print(output)
    print("=" * (100 + len(device.platform)))


with ConnectHandler(
    device_type="cisco_ios",
    host="10.10.10.3",
    username="admin",
    password="admin"
) as device:
    command = "show ver"
    output = device.send_command(command)  # raw command

    print("=" * 50 + device.platform + "=" * 50)
    print(output.splitlines()[0])  # just first line
    print("=" * (100 + len(device.platform)))


with ConnectHandler(
    device_type="juniper_junos",
    host="10.10.10.4",
    username="admin",
    password="admin"
) as device:
    command = "show interfaces"
    output = device.send_command(command, use_textfsm=True)

    print("=" * 50 + device.platform + "=" * 50)
    print(output)
    print("=" * (100 + len(device.platform)))


# Use NetmikoMock directly, you can change later for ConnectHandler
with NetmikoMock(
    device_type="arista_eos",
    host="10.10.10.5",
    username="admin",
    password="admin"
) as device:
    command = "show int desc"
    output = device.send_command(command, use_textfsm=True)

    print("=" * 50 + device.platform + "=" * 50)
    print(output)
    print("=" * (100 + len(device.platform)))
