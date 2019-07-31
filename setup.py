if '__main__' == __name__:
    import os, sys, setuptools
    src_root = os.path.dirname(sys.argv[0])
    os.chdir(src_root)

    from LRC.Common.info import version, url, server_entry, client_entry

    # get readme description
    with open(os.path.join("README.md"), "r") as fh:
        long_description = fh.read()

    # find all packages under ./LRC, like LRC.Client | LRC.Common | LRC.Server | LRC.Server.Commands
    packages = [p for p in setuptools.find_packages(where='.') if p.startswith('LRC')]
    print('packages :')
    for p in packages:
        print('    {}'.format(p))

    setuptools.setup(
        name="LRC",
        version=version,
        author="Davied Paul",
        author_email="wuwei_543333827@126.com",
        description="A lan remote controller to keyboard associated devices.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=url,
        packages=packages,
        # package_dir={'':'LRC'},  # put all packages into folder LRC
        package_data={'LRC.lrccollections':['*.json']}, # package collection has data *.json
        include_package_data=True, # pack data (e.g. *.json in collections) into setup package
        entry_points="""
        [console_scripts]
        {} = LRC.client_main:main
        {} = LRC.server_main:main
        """.format(client_entry, server_entry),
        classifiers=["Programming Language :: Python",],
        install_requires=['pypiwin32>=223;platform_system=="Windows"', 'PyUserInput>=0.1.9']
    )

