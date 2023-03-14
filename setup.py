from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="astroph_new", # Replace with your own username
    version="0.1.2",
    author="Shinyoung Kim",
    author_email="radioshiny@gmail.com",
    description="astroph_new",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/radioshiny/astroph_new",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.7', install_requires=['bs4', 'markdown', 'numpy', 'selenium', 'whoswho'])
