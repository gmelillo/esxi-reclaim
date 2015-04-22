__author__ = 'gabriel'

from argparse import ArgumentParser
from sys import exit
from os.path import isfile
from config import ConfigurationINI
from __init__ import ESXi, ESXiConnectionError
import logging
import logging.config

CONFIG_FILE = '/etc/esxi.ini'
DATABASE = '/tmp/esxi.db'


def run():
    global CONFIG_FILE, DATABASE
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
    logging.config.fileConfig(CONFIG_FILE)

    if conf['vmware']['hostname'] is None:
        print ('Invalid hostname')
        exit()
    if conf['vmware']['username'] is None:
        print ('Invalid username')
        exit()
    if conf['vmware']['password'] is None:
        print ('Invalid hostname')
        exit()
    if conf['db']['path'] is not None:
        DATABASE = conf['db']['path']

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

    storage_list = esxi.get_storage_list()

    if args.scan:
        for iscsi in storage_list:
            logging.info('- {0}'.format(iscsi.Name))

    if args.reclaim and len(storage_list) > 0:
        for iscsi in storage_list:
            if iscsi.reclaim_supported:
                logging.info("Reclaim space for {0}".format(iscsi.Name))
                esxi.reclaim_iscsi_space(iscsi)
            else:
                logging.info("Skip reclaim for {0}".format(iscsi.Name))
    elif args.reclaim and len(storage_list) == 0:
        logging.info("No iscsi target elegible for reclaim")

    return 0

if __name__ == '__main__':
    run()