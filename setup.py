import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goecharger",
    version="0.0.11",
    author="Carsten Thiele",
    author_email="software@carsten-thiele.de",
    description="A Python API for accessing the go-eCharger EV-Charger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cathiele/goecharger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    provides=[
        "goecharger"
    ],
    install_requires=[
        'requests'
    ],
    setup_requires=['wheel']
)