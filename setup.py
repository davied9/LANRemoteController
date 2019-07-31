if '__main__' == __name__:
    import os, sys, setuptools
    src_root = os.path.dirname(sys.argv[0])
    os.chdir(src_root)

    from LRC.Common.info import version

    # get readme description
    with open(os.path.join("README.md"), "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="LRC",
        version=version,
        author="Davied Paul",
        author_email="wuwei_543333827@126.com",
        description="A lan remote controller to keyboard associated devices.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/davied9/LANRemoteController",
        packages=setuptools.find_packages(where='./LRC'),  # find all packages under ./LRC, like Client | Common | Server | Server.Commands
        package_dir={'':'LRC'},  # put all packages into folder LRC
        package_data={'collections':['*.json']}, # package collection has data *.json
        include_package_data=True, # pack data (e.g. *.json in collections) into setup package
        entry_points="""
        [console_scripts]
        lrcclient = LRC.client_main:main
        lrcserver = LRC.server_main:main
        """,
        classifiers=["Programming Language :: Python",],
        install_requires=['pypiwin32>=223;platform_system=="Windows"', 'PyUserInput>=0.1.9']
    )

