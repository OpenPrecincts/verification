import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="op_verification",
    version="0.0.2",
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
    install_requires=[
        'geopandas>=0.8.1',
        'pandas>=1.1.4',
        'shapely',
        'statistics',
        'gerrychain',
        'maup',
    ],
    include_package_data=True,
    package_data={
        'op_verification': [
            'data/election_results/countypres_2000-2016.csv',
            'data/county_shapefiles/cb_2016_us_county_500k',
            'data/county_shapefiles/cb_2016_us_county_500k/*',
            'data/county_shapefiles/2013-HD-ProclamationPlan',
            'data/county_shapefiles/2013-HD-ProclamationPlan/*',
        ],
    },
)