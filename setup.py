from setuptools import setup

install_requires = [
    # "gurobipy",  # install this manually
    # "alib3",
    # "basemap",  # install this manually
    "click",
    "matplotlib",
    "numpy"
]

setup(
    name="vnep-approx3",
    # version="0.1",
    packages=["vnep_approx3"],
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "vnep-approx3 = vnep_approx3.cli:cli",
        ]
    }
)
