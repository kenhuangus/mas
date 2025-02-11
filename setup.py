from setuptools import setup, find_packages

setup(
    name="mas",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "python-json-logger>=2.0.0",
        "jsonschema>=4.0.0",
        "anthropic>=0.3.0",
        "python-dateutil>=2.8.2",
        "uuid>=1.30"
    ],
    author="Ken Huang",
    author_email="ken@distributedapps.ai",
    description="A Multi-Agent System framework for distributed applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://distributedapps.ai",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8"
)
