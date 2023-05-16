from setuptools import setup, find_packages


setup(
    name="absquant",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.R"]},
    entry_points={
        "qiime2.plugins": ["q2-absquant=absquant.q2.plugin_setup:plugin"]
    }
)
