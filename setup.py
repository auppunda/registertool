from setuptools import setup

setup(name='registertool',
      version='0.3',
      description='Using docx, I take the register tables from a docx file and write into text file',
      url='http://github.com/auppunda/registertool',
      author='Ankith Uppunda',
      author_email='auppunda@gmail.com',
      license='Ankith Uppunda',
      packages=['registertool'],
      install_requires=[
          'docx',
      ],
      zip_safe=False)
