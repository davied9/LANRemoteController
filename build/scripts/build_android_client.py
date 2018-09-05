from __future__ import print_function

if '__main__' == __name__ :
    import shutil
    import os, sys

    # define utilities
    def empty(*args, **kwargs): pass

    # copy = empty
    copy = shutil.copy

    # -------------------------------------------------------------------------------------------------------------
    # configurations
    dirs_to_copy = ['Controller', 'Common', 'collections', 'Client']
    skip_dirs = ['logs', '__pycache__']
    skip_files = ['android.txt', 'android.ini']

    # initialize
    script_file = sys.argv[0]
    working_dir, _ = os.path.split(script_file)
    working_dir, _ = os.path.split(working_dir)
    working_dir, _ = os.path.split(working_dir)
    os.chdir(working_dir)
    print('[info] working directory : {}'.format(working_dir))
    sys.path.append(working_dir)
    sys.path.append(os.path.dirname(sys.argv[0]))

    from Common.logger import logger

    # start the dirty work
    build_root = os.path.join(working_dir,'build','client','android')
    logger.info('copy files for android pydroid3 into {}.'.format(build_root))
    if os.path.exists(build_root):
        shutil.rmtree(build_root)

    # copy files into build/client/android
    logger.info('start basic copy ...')
    for dir in dirs_to_copy:
        for r, ds, fs in os.walk(os.path.join(working_dir, dir)):
            dir_name = os.path.basename(r)
            if dir_name in skip_dirs:
                logger.info('skipping directory : {}'.format(r))
                continue
            dir_to_root = os.path.relpath(r, working_dir)
            target_dir = os.path.join(build_root, dir_to_root)
            source_dir = os.path.join(working_dir, dir_to_root)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            for src in fs:
                this_src = os.path.join(source_dir, src)
                this_target = os.path.join(target_dir, src)
                if src in skip_files:
                    logger.info('skipping file : {}'.format(this_src))
                    continue
                logger.info('copying {}'.format(this_src))
                logger.info('     to {}'.format(this_target))
                copy(this_src, this_target)
    logger.info('done basic copy.')

    # rename server_main.py into main.py
    logger.info('start copy main.py ...')
    this_src = os.path.join(working_dir, 'client_main.py')
    this_target =  os.path.join(build_root, 'main.py')
    logger.info('copying {}'.format(this_src))
    logger.info('     to {}'.format(this_target))
    copy(this_src, this_target)
    logger.info('done copy main.py.')

    # copy android.ini and android.txt
    logger.info('start copy android.txt/android.ini ...')
    this_src = os.path.join(working_dir, 'Client', 'android.ini')
    this_target = os.path.join(build_root, 'android.ini')
    logger.info('copying {}'.format(this_src))
    logger.info('    into {}'.format(this_target))
    copy(this_src, this_target)

    this_src = os.path.join(working_dir, 'Client', 'android.txt')
    this_target = os.path.join(build_root, 'android.txt')
    logger.info('copying {}'.format(this_src))
    logger.info('    into {}'.format(this_target))
    copy(this_src, this_target)
    logger.info('done copy android.txt/android.ini.')

    logger.info('done copy files for android pydroid3.')
    logger.info('copy directory {} to /sdcard/kivy,'.format(build_root))
    logger.info('then start main.py in pydroid3 to make things work.'.format(build_root))
