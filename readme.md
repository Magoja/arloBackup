# Arlo Video Backup Script #

## Requirement

* Python 2.7
* Splinter (http://splinter.readthedocs.org/en/latest/install.html)
* Chromedriver (https://devblog.supportbee.com/2014/10/27/setting-up-cucumber-to-run-with-Chrome-on-Linux/
* webdriver (http://stackoverflow.com/questions/8255929/running-webdriver-chrome-with-selenium)

## How to use

Prepare a cloud storage service. I used Google Photos here.

    python arloBackup.py {userId} {password} -d {download folder} -u {upload folder}

    # Sample
    python arloBackup.py magoja@gmail.com 1234 -d ~Downloads -u "~/Google Photos"
