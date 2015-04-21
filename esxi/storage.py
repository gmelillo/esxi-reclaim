__author__ = 'gabriel'


class ISCSIStorage(object):
    def __init__(self, **kwargs):
        self.Name = kwargs.get('Name', 'Unknown')
        self.UUID = kwargs.get('UUID', '00000000-00000000-0000-000000000000')
        self.DName = kwargs.get('DName', 'Unknown')

    def __repr__(self):
        return '<ISCSIStorage {name}({uuid})>'.format(
            name=self.Name,
            uuid=self.UUID
        )