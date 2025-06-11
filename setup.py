from setuptools import setup

setup(
    name="weekly-status-report",
    version="0.1.0",
    packages=["weekly_status_report"],
    install_requires=[
        "gitpython==3.1.42",
        "python-dateutil==2.8.2",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wsr=weekly_status_report.wsr:main",
        ],
    },
) 