from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="AnsibleDependenciesGraph",
    version="0.1",
    packages=find_packages(),
    scripts=["dependency-graph.py"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["graphviz>=0.14", "PyYAML>=5.3.1"],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"],
    },

    # metadata to display on PyPI
    author="Yohan Lascombe",
    author_email="yohan.lascombe@gmail.com",
    description="Browse ansible roles directory to build roles dependency graph",
    keywords="ansible dependencies graph",
    project_urls={
        "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://code.example.com/HelloWorld/",
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

    # could also include long_description, download_url, etc.
)
