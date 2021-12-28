import os
import re
import yaml
import glob
from textfsm import clitable
from textfsm.clitable import CliTableError


def command_from_index(attributes):
    """Use index file to get full command name.

    show ip int br -> show ip interface brief
    """
    template_dir = f"{os.getcwd()}{os.sep}ntc-templates{os.sep}ntc_templates{os.sep}templates"

    cli_table = clitable.CliTable("index", template_dir)
    row_idx = cli_table.index.GetRowMatch(attributes)
    if row_idx:
        template = cli_table.index.index[row_idx]['Template']
    else:
        raise CliTableError(f'No template and mock found for attributes: "{attributes}"')
    return re.search(rf"{attributes['Platform']}_(?P<command>.*?)\.", template).groupdict().get("command")


def mock_dir(attributes):
    """Returns mock directory from ntc-templates tests."""
    full_command = command_from_index(attributes)
    platform = attributes.get("Platform")
    return f"{os.getcwd()}{os.sep}ntc-templates{os.sep}tests{os.sep}{platform}{os.sep}{full_command}"


def command_output(attributes, use_textfsm=False):
    """Reads raw command output or structured data from mock files."""
    _dir = mock_dir(attributes)
    file_name = glob.glob(f"{_dir}{os.sep}*.yml")[0] if use_textfsm else glob.glob(f"{_dir}{os.sep}*.raw")[0]
    with open(file_name, "r") as f:
        return yaml.safe_load(f).get("parsed_sample") if use_textfsm else f.read()


class NetmikoMock:
    """Overwrites netmiko methods."""
    def __init__(self, **kwargs):
        self.platform = kwargs.get("device_type")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def open(self):
        pass

    def enable(self):
        pass

    def close(self):
        pass

    def disconnect(self):
        pass

    def send_command(self, command, use_textfsm=False, **kwargs):
        attrs = {"Command": command, "Platform": self.platform}
        return command_output(attrs, use_textfsm)
