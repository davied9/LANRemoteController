__all__ = ['version', 'common_path', 'collection_path', 'lrc_root']

version='0.1.4'

import os
common_path = os.path.split(__file__)[0]
lrc_root = os.path.split(common_path)[0]
collection_path = os.path.join(os.path.split(common_path)[0], 'collections')
