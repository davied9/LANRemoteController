import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LRC",
    version="0.0.1",
    author="Davied Paul",
    author_email="wuwei_543333827@126.com",
    description="A lan remote controller to keyboard associated devices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davied9/LANRemoteController",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
    ],
)
