__all__ = ['version', 'common_path', 'collection_path', 'lrc_root']

version = '0.1.4'
url = 'https://github.com/davied9/LANRemoteController'
repo = 'https://github.com/davied9/LANRemoteController.git'

server_entry = 'lrcserver'
client_entry = 'lrcclient'

import os
common_path = os.path.split(__file__)[0]
lrc_root = os.path.split(common_path)[0]
collection_path = os.path.join(os.path.split(common_path)[0], 'lrccollections')
