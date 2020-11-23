import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timewriggler",
    version="2.0.0",
    author="Ashton Hudson",
    author_email="ashton@dataprophet.com",
    description="Let's wriggle them timesheets into Google Sheets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "cachetools==4.1.0",
        "certifi==2020.4.5.1",
        "chardet==3.0.4",
        "google-api-core==1.17.0",
        "google-api-python-client==1.8.2",
        "google-auth==1.14.1",
        "google-auth-httplib2==0.0.3",
        "google-auth-oauthlib==0.4.1",
        "googleapis-common-protos==1.51.0",
        "httplib2==0.18.0",
        "idna==2.9",
        "oauthlib==3.1.0",
        "protobuf==3.11.3",
        "pyasn1==0.4.8",
        "pyasn1-modules==0.2.8",
        "pytz==2020.1",
        "requests==2.23.0",
        "requests-oauthlib==1.3.0",
        "rsa==4.0",
        "six==1.14.0",
        "toml==0.10.0",
        "uritemplate==3.0.1",
        "urllib3==1.25.9",
    ],
    tests_requires=["pytest==6.1.2", "mypy==0.770", "mypy-extensions==0.4.3"],
)
