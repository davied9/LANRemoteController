import os, sys, subprocess, shutil
from LRC.Common.logger import logger
from LRC.Common.info import version
from LRC.Utilities.distribution import tar

def build_main():
    main_path = sys.argv[0]

    copy_to_history = False
    if '--copy-to-history' in sys.argv:
        copy_to_history = True

    src_root, main_name = os.path.split(main_path)
    src_root = os.path.dirname(src_root)

    logger.stream_id = os.path.join(src_root, 'build.log')
    if os.path.exists(logger.stream_id):
        os.remove(logger.stream_id)

    build_all(src_root, copy_to_history=copy_to_history)

    logger.info('')
    logger.info('for detailed build log, see : {}'.format(logger.stream_id))


def build_all(src_root, *, copy_to_history=False):
    logger.info('start build LRC ...')
    total = 0
    success = 0

    info = dict()

    err, package_path = build_server3(src_root, copy_to_history=copy_to_history)
    info['server 3'] = (err, package_path)
    total += 1

    err, package_path = build_server2(src_root, copy_to_history=copy_to_history)
    info['server 2'] = (err, package_path)
    total += 1

    err, package_path = build_server_source(src_root, copy_to_history=copy_to_history)
    info['server source'] = (err, package_path)
    total += 1

    err, package_path = build_client_android_source(src_root, copy_to_history=copy_to_history)
    info['client source android'] = (err, package_path)
    total += 1

    logger.info('')
    logger.info('build summery :')
    for k, v in info.items():
        if v[0]:
            logger.error('    build {} error:\n{}'.format(k, v[0].decode('utf-8')))
        else:
            logger.info('    build {} success, package : {}.'.format(k, v[1]))
            success += 1
    logger.info('')
    logger.info('build LRC done : total {}, success {}'.format(total, success))


def build_server3(src_root, *, copy_to_history=False):
    logger.info('start build server 3 ...')
    os.chdir(src_root)
    command = ['python3', '-m', 'setup', 'bdist_wheel']
    p = subprocess.Popen(command, shell=True, stdout=logger._stream, stderr=subprocess.PIPE)
    _, stderr = p.communicate()

    package_name = 'LRC-{}-py3-none-any.whl'.format(version)
    package_path = os.path.join(src_root, 'dist', package_name)

    if copy_to_history and not stderr:
        history_path = os.path.join(src_root, 'history_packages')
        shutil.copy(package_path, history_path)
        logger.info('copy package {} to history_packages'.format(package_name))

    return stderr, package_path


def build_server2(src_root, *, copy_to_history=False):
    logger.info('start build server 2 ...')
    os.chdir(src_root)
    command = ['python2', '-m', 'setup', 'bdist_wheel']
    p = subprocess.Popen(command, shell=True, stdout=logger._stream, stderr=subprocess.PIPE)
    _, stderr = p.communicate()

    package_name = 'LRC-{}-py2-none-any.whl'.format(version)
    package_path = os.path.join(src_root, 'dist', package_name)

    if copy_to_history and not stderr:
        history_path = os.path.join(src_root, 'history_packages')
        shutil.copy(package_path, history_path)
        logger.info('copy package {} to history_packages'.format(package_name))

    return stderr, package_path


def build_server_source(src_root, *, copy_to_history=False):
    logger.info('start build server source ...')
    os.chdir(src_root)
    command = ['python', '-m', 'setup', 'sdist']
    p = subprocess.Popen(command, shell=True, stdout=logger._stream, stderr=subprocess.PIPE)
    _, stderr = p.communicate()

    package_name = 'LRC-{}.tar.gz'.format(version)
    package_path = os.path.join(src_root, 'dist', package_name)

    if copy_to_history and not stderr:
        history_path = os.path.join(src_root, 'history_packages')
        shutil.copy(package_path, history_path)
        logger.info('copy package {} to history_packages'.format(package_name))

    return stderr, package_path


def build_client_android_source(src_root, *, copy_to_history=False):
    logger.info('start build client source for android ...')
    os.chdir(os.path.join(src_root, 'scripts'))
    command = ['python', '-m', 'build_android_client', '--log-file={}'.format(logger.stream_id)]
    p = subprocess.Popen(command, shell=True, stdout=logger._stream, stderr=subprocess.PIPE)
    _, stderr = p.communicate()

    package_base_name = 'LRCClient-{}-Android'.format(version)
    package_name = '{}.tar.gz'.format(package_base_name)
    package_path = os.path.join(src_root, 'dist', package_name)
    source_folder = os.path.join(src_root, 'dist', package_base_name)
    # move client sources to dist/client-version-android
    shutil.move(os.path.join(src_root,'dist','client', 'android'), source_folder)
    # compress client source into tar.gz
    tar(package_path, source_folder)
    shutil.rmtree(source_folder)

    if copy_to_history and not stderr:
        history_path = os.path.join(src_root, 'history_packages')
        shutil.copy(package_path, history_path)
        logger.info('copy package {} to history_packages'.format(package_name))

    return stderr, package_path


if '__main__' == __name__:
    build_main()