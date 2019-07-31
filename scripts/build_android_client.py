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
    dirs_to_copy = ['Controller', 'Common', 'Client', 'Protocol']
    ext_to_copy = ['.py']
    skip_dirs = ['logs', '__pycache__']
    skip_files = ['android.txt']
    example_collections_directory = os.path.join('..', 'collections')

    # initialize
    script_file = sys.argv[0]
    project_root = os.path.dirname(script_file)
    project_root = os.path.dirname(project_root)
    package_dir = os.path.join(project_root, 'LRC')
    os.chdir(project_root)

    sys.path.append(package_dir)
    sys.path.append(os.path.dirname(sys.argv[0]))

    from LRC.Common.logger import logger # directly import from working directory to avoid not installed problem
    for arg in sys.argv[1:]:
        if arg.startswith('--log-file='):
            logger.stream_id = arg[len('--log-file='):]

    # start the dirty work
    build_root = os.path.join(project_root,'dist','client','android')
    logger.info('copy files for android pydroid3 into {}.'.format(build_root))
    if os.path.exists(build_root):
        shutil.rmtree(build_root)

    # make LRC directory
    os.makedirs(os.path.join(build_root, 'LRC'))
    copy(os.path.join(package_dir, '__init__.py'), os.path.join(build_root, 'LRC', '__init__.py'))

    # copy files into dist/client/android
    logger.info('start basic copy ...')
    for dir in dirs_to_copy:
        for r, ds, fs in os.walk(os.path.join(package_dir, dir)):
            dir_name = os.path.basename(r)
            if dir_name in skip_dirs:
                logger.info('skipping directory : {}'.format(r))
                continue
            dir_to_root = os.path.relpath(r, package_dir)
            target_dir = os.path.join(build_root, 'LRC', dir_to_root)
            source_dir = os.path.join(package_dir, dir_to_root)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            for src in fs:
                _, ext = os.path.splitext(src)
                if ext not in ext_to_copy:
                    continue
                this_src = os.path.join(source_dir, src)
                this_target = os.path.join(target_dir, src)
                if src in skip_files:
                    logger.info('skipping file : {}'.format(this_src))
                    continue
                logger.info('copying {}'.format(this_src))
                logger.info('     to {}'.format(this_target))
                copy(this_src, this_target)
    logger.info('done basic copy.')

    # copy example collections
    logger.info('start copy example collections ...')
    example_collections_directory = os.path.join(package_dir, example_collections_directory) # source dir
    example_collections_build_dir = os.path.join(build_root, 'collections') # target dir
    if not os.path.exists(example_collections_build_dir):
        os.makedirs(example_collections_build_dir)
    print('build collections from {} to {}'.format(example_collections_directory, example_collections_build_dir))
    for r, ds, fs in os.walk(example_collections_directory):
        for src in fs:
            if src.endswith('.json'):
                this_src = os.path.join(example_collections_directory, src)
                this_target = os.path.join(example_collections_build_dir, src)
                logger.info('copying {}'.format(this_src))
                logger.info('     to {}'.format(this_target))
                copy(this_src, this_target)
        break
    logger.info('done copy example collections  ...')

    # rename server_main.py into main.py
    logger.info('start copy main.py ...')
    this_src = os.path.join(package_dir, 'client_main.py')
    this_target =  os.path.join(build_root, 'main.py')
    logger.info('copying {}'.format(this_src))
    logger.info('     to {}'.format(this_target))
    copy(this_src, this_target)
    logger.info('done copy main.py.')

    # copy android.txt
    this_src = os.path.join(package_dir, 'Client', 'android.txt')
    this_target = os.path.join(build_root, 'android.txt')
    logger.info('copying {}'.format(this_src))
    logger.info('    into {}'.format(this_target))
    copy(this_src, this_target)
    logger.info('done copy android.txt/android.ini.')

    logger.info('done copy files for android pydroid3.')
    logger.info('copy directory {} to /sdcard/kivy,'.format(build_root))
    logger.info('then start main.py in pydroid3 to make things work.'.format(build_root))
