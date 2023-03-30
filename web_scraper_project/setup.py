import glob

from setuptools import find_packages, setup

setup(
    name="web_scraper_project",
    packages=find_packages(exclude=["web_scraper_project_tests"]),
    # package data paths are relative to the package key
    package_data={
        "web_scraper_project": ["../" + path for path in glob.glob("bigquery_scraper/**", recursive=True)]
    },
    install_requires=[
        "dagster",
        "dagster-dbt",
        "pandas",
        "dbt-core",
        "dbt-bigquery",
        # packaging v22 has build compatibility issues with dbt as of 2022-12-07
        "packaging<22.0",
        "pandas-gbq",
        "selenium"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
