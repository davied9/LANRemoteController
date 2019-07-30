if '__main__' == __name__:
    import os, sys, setuptools
    src_root = os.path.dirname(sys.argv[0])
    os.chdir(src_root)

    from LRC.Common.info import version
    from LRC.Common.logger import logger

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
        packages=[p for p in setuptools.find_packages(where='.') if p.startswith('LRC')],
        package_data={'':'*.json'},
        entry_points="""
        [console_scripts]
        lrcclient = LRC.client_main:main
        lrcserver = LRC.server_main:main
        """,
        classifiers=["Programming Language :: Python",],
        setup_requires=['kivy>=1.10.1', 'PyUserInput>=0.1.9']
    )

