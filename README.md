# scrap-jobs

Simple scraper that uses [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) to scrap some job searching websites,
and save the scrapped result as `csv` and `xlsx` file into local system.

## Prerequisite
This project requires the following packages to work well:
```
python >= 3.7
beautifulsoup4 == 4.6.3
fake_useragent == 0.1.11
lxml == 4.2.5
pandas == 0.23.4
requests == 2.19.1
```

A simple shortcut to install all the packages above in one line:
```
pip install -r requirements.txt
```

You might also want packages below for linting and compile-time type checking:
```
flake8 == 3.7.8
flake8-comprehensions == 2.1.0
flake8-mypy == 17.8.0
pylint == 2.3.1
```

## Get Started
To run the scraper, execute the command below on your terminal:
```
git clone git@github.com:andytan0727/scrap-jobs.git
cd scrap_jobs
python -m scrap_jobs
```

This will execute the `__main__.py` file in scrap_jobs directory. The `-m` switch is needed due to python module system.

## Further Note
Since this project uses python [typings](https://docs.python.org/3/library/typing.html), which is introduced in python version 3.5.
This means that this project might breaks if your python version is not supporting typings, with typing module included out
of the box.
