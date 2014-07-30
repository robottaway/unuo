from setuptools import setup, find_packages
setup(
    name = "unuo",
    version = "0.1.0",
    author = "Rob Ottaway",
    author_email = "robottaway@gmail.com",
    description = "A simple tool for building Docker containers",
    packages = find_packages(exclude='tests'),
    test_suite = "tests",
)
