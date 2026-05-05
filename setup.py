from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT='-e .'

def get_requirements(file_path:str) -> List[str]:
    """
        this function will reture a list of requirements
    """
    requirements=[]

    
    #get file path from argument and open read line
    with open(file_path) as file_obj:        
        requirements = file_obj.readlines()
        #and remove newline "\n, 
        requirements = [req.replace("\n","") for req in requirements]
        #remove -e . from requirementa list"
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
        return requirements



setup(
    name='ml_project',
    version='0.0.1',
    author='Noel Kuasmapa',
    author_email='noeljackkuasmapa@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)