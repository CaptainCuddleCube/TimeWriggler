import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timewriggler",
    version="2.0.1",
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
        "google-api-python-client==1.8.2",
        "google-auth-oauthlib==0.4.1",
        "typer==0.3.2",
        "toml==0.10.0",
    ],
    tests_requires=["pytest==6.1.2", "mypy==0.770"],
    entry_points={"console_scripts": ["timewriggler = timewriggler.__main__:app"]},
)
