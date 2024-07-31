from setuptools import setup , find_packages
import logging

setup(name="GenAI_practice",
      author="Anhtt9x",
      author_email="anhtt454598@gmail.com",
      packages=find_packages(where=["*","src"]),
      version="0.0.0"
      )


logging.info("Making package")