def entry_00():
    import os
    import argparse
    parser = argparse.ArgumentParser(prog="parse_arguments", description='a test parser')
    parser.add_argument( '--work-dir', '-w', type=str, help='working directory')
    parser.add_argument( '-srvaddr', '-s', '--server-address', dest='srv_addr', type=str, help='server address')
    parser.add_argument( '--no-ui', '-u', dest='enable_ui', default=True, action="store_false", help='do not use ui')
    parser.add_argument( 'commands', type=str, nargs="*", help='commands to execute on server') # nargs : * or + or ?

    def print_args(args, keyword=None):
        print('########################## {} ##################################'.format(keyword))
        print('args : ', args)
        print('working directory : ', args.work_dir)
        print('server address    : ', args.srv_addr)
        print('enable_ui         : ', args.enable_ui)
        print('commands          : ', args.commands)

    sim_args = []
    sim_args.append('--work-dir')
    sim_args.append(os.path.split(__file__)[0])
    sim_args.append('--server-address')
    sim_args.append('("127.0.0.1",31730)')
    sim_args.append('start_lrc_server')
    sim_args.append('start_lrc_waiter')
    args = parser.parse_args(sim_args)
    print_args(args, '1')

    sim_args = []
    sim_args.append('--work-dir')
    sim_args.append(os.path.split(__file__)[0])
    sim_args.append('--no-ui')
    sim_args.append('start_lrc_server')
    args = parser.parse_args(sim_args)
    print_args(args, '2')

    sim_args = []
    sim_args.append('--work-dir')
    sim_args.append(os.path.split(__file__)[0])
    sim_args.append('-srvaddr')
    sim_args.append('("127.0.0.1",51110)')
    args = parser.parse_args(sim_args)
    print_args(args, '3')

    class AP: pass
    nn = AP()
    parser.parse_args(sim_args, namespace=nn)
    print_args(nn, '4')

    print('######################## help ####################################')
    parser.print_help()



def entry_01(): # usage
    import argparse
    parser = argparse.ArgumentParser(prog="parse_arguments", description='a test parser', usage='%(prog)s [options]')
    sim_args = []
    sim_args.append('--help')
    args = parser.parse_args(sim_args)
    print('args : ', args)

def entry_02(): # version
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action="version", version='parse arg 0.1.4', help='show version and exit')
    sim_args = []
    sim_args.append('--version')
    parser.parse_args(sim_args)

def entry_03(): # too many arguments
    import argparse
    parser = argparse.ArgumentParser()
    sim_args = []
    sim_args.append('--this-is-too-much-to-take')
    parser.add_argument('--version', '-v', action="version", version='parse arg 0.1.4', help='show version and exit')
    parser.parse_args(sim_args)

if '__main__' == __name__:
    entry_00()
    # entry_01()
    # entry_02()
    # entry_03()