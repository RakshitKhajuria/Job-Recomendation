from setuptools import find_packages,setup
from typing import List

REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements()->List[str]:
    # this arrow give the info to the user
    # here the  arrow showing that this function is going to return list wgich will conatin str 

    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]

    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list



setup(
    name="JobRecommendation",
    version="0.0.2",
    packages = find_packages(),
    install_requires=get_requirements(),
)