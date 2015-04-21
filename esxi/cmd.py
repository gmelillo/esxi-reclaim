__author__ = 'gabriel'

from argparse import ArgumentParser
from sys import exit
from os.path import isfile
from config import ConfigurationINI
from __init__ import ESXi, ESXiConnectionError

CONFIG_FILE = '/etc/esxi.ini'


def run():
    global CONFIG_FILE
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', help='Configuration file', type=str)
    parser.add_argument('-s', '--scan', help='Scan esxi for new ISCSI targets.', action='store_true')
    parser.add_argument('-r', '--reclaim', help='Reclaim space on cached ISCSI targets', action='store_true')
    args = parser.parse_args()

    if args.config is not None:
        CONFIG_FILE = args.config

    if not args.reclaim and not args.scan:
        parser.print_usage()
        exit()

    if not isfile(CONFIG_FILE):
        print("File {0} not found.".format(CONFIG_FILE))
        exit()

    conf = ConfigurationINI(CONFIG_FILE)

    if conf['vmware']['hostname'] is None:
        print ('Invalid hostname')
        exit()
    if conf['vmware']['username'] is None:
        print ('Invalid username')
        exit()
    if conf['vmware']['password'] is None:
        print ('Invalid hostname')
        exit()

    esxi = ESXi(
        hostname=conf['vmware']['hostname'],
        username=conf['vmware']['username'],
        password=conf['vmware']['password']
    )

    try:
        esxi.connect()
    except ESXiConnectionError as e:
        print(e.message)
        exit(0)

    if args.scan:
        for iscsi in esxi.get_storage_list():
            print('- {0}'.format(iscsi.Name))

    return 0

if __name__ == '__main__':
    run()