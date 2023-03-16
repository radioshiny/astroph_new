from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="astroph_new", # Replace with your own username
    version="0.1.8",
    author="Shinyoung Kim",
    author_email="radioshiny@gmail.com",
    description="python module to make summary of astro-ph based on user interests",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/radioshiny/astroph_new",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.7',
    install_requires=['bs4', 'markdown', 'numpy', 'selenium', 'whoswho']
)
