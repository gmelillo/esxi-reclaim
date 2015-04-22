from distutils.core import setup
from pip.req import parse_requirements
from setuptools.command.develop import develop

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Information Technology',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='ESXi-Reclaim',
    version='0.1.1',
    author="Gabriel Melillo",
    author_email="gabriel@melillo.me",
    maintainer="Gabriel Melillo",
    maintainer_email="gabriel@melillo.me",
    description="Reclaim storage on thin on thin lun for vmware ESXi 5.X",
    url="https://github.com/gmelillo/esxi-reclaim",
    install_requires=[
        "argparse==1.2.1",
        "configparser==3.3.0r2",
        "ecdsa==0.13",
        "paramiko==1.15.2",
        "pycrypto==2.6.1",
        "wsgiref==0.1.2"
    ],
    classifiers=CLASSIFIERS,
    platforms=['OS Independent'],
    data_files=[
        ('esxi-backup', ['requirements.txt']),
        ('esxi-backup', ['esxi.ini.sample'])
    ],
    include_package_data=True,
    packages=[
        'esxireclaim',
    ],
    license="GNU GENERAL PUBLIC LICENSE",
    long_description='Reclaim storage on thin on thin lun for vmware ESXi 5.X'
                     '\n\n',
    entry_points={'console_scripts': 'esxi-reclaim = esxireclaim.cmd:run'}
)
