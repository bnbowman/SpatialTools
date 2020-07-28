try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name="SpatialTools",
    version="0.0.1",
    description="Tools for spatial analysis bioinformatics",
    author="Brett Bowman",
    author_email="bbowman@illumina.com",
    url="https://github.com/bnbowman/SpatialTools",
    packages=find_packages(),
    package_dir={"spatial_analysis": "spatial_analysis"},
    include_package_data=True,
    install_requires=["requests", "distro"],
    zip_safe=False,
    keywords=["spatial_analysis"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={"console_scripts": ["spatial_analysis=spatial_analysis:main",]},
)
