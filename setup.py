import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="op-verification",
    version="0.0.1",
    author="Baxter Demers",
    author_email="baxter.demers@gmail.com",
    description="Compares a Precinct-Level Election Shapefile with expected election results and geometries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenPrecincts/verification",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)