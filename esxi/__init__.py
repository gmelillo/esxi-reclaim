__author__ = 'gabriel'
from paramiko import SSHClient, AutoAddPolicy
from socket import error as socket_error
from re import search
from storage import ISCSIStorage
import logging


class ESXiConnectionError(Exception):
    pass


class ESXi(object):
    def __init__(self, **kwargs):
        self._host = kwargs.get('hostname', 'localhost')
        self._user = kwargs.get('username', 'root')
        self._pass = kwargs.get('password', None)

        self._device_list = []

        self._connection = SSHClient()
        self._connection.set_missing_host_key_policy(AutoAddPolicy())

    def is_connected(self):
        transport = self._connection.get_transport() if self._connection else None
        return transport and transport.is_active()

    def connect(self):
        if not self.is_connected():
            try:
                if self._pass is None:
                    self._connection.connect(self._host, username=self._user)
                else:
                    self._connection.connect(self._host, username=self._user, password=self._pass)
            except socket_error as e:
                logging.critical(e.__str__())
                raise ESXiConnectionError(e.__str__())

    def get_storage_list(self):
        self._device_list = []
        stdin, stdout, stderr = self._connection.exec_command('esxcli storage vmfs extent list')
        for l in stdout:
            m = search(
                '([a-zA-Z\-0-9]+) +([0-9a-zA-Z]{8}-[0-9a-zA-Z]{8}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{12}).*(naa\.[0-9a-z]{32})',
                l.strip()
            )
            if m is not None:
                self._device_list.append(ISCSIStorage(
                    Name=m.group(1),
                    UUID=m.group(2),
                    DName=m.group(3)
                ))
                self._device_list[-1].thin_provision_status = self.get_param(
                    'esxcli storage core device list -d {0}'.format(self._device_list[-1].DName),
                    'Thin Provisioning Status: ([a-z]*)',
                    1
                )
                self._device_list[-1].delete_status = self.get_param(
                    'esxcli storage core device vaai status get -d {0}'.format(self._device_list[-1].DName),
                    'Delete Status: ([a-z]*)',
                    1
                )
                if self._device_list[-1].delete_status.lower() == 'supported' \
                        and self._device_list[-1].thin_provision_status.lower() == 'yes':
                    self._device_list[-1].reclaim_supported = True
                else:
                    self._device_list[-1].reclaim_supported = False

        return self._device_list

    def get_param(self, command, pattern, position=1):
        stdin, stdout, stderr = self._connection.exec_command(command)
        for l in stdout:
            m = search(pattern, l.strip())
            if m is not None:
                return m.group(position)
        return "N/A"

    def reclaim_iscsi_space(self, iscsi_target):
        if not isinstance(iscsi_target, ISCSIStorage):
            raise ValueError('ISCSIStorage instance required')

        return self._connection.exec_command('esxcli storage vmfs unmap -volume-label={}'.format(iscsi_target.Name))