# Arlo Video Backup Script #

## What it does

This script is a helper script to download Arlo videos. There are still some problems, but I think it is acceptable to use.

### Problems
* Splinter is using forground Web browser access: Which means, it might not work if you are manipulating your machine when this script is running.
* No strict login checking: Login might not work, but you wouldn't know.
* No checking for completing downloads: It just waits for 5 seconds and hope it has done in time.

If you have good idea to improve these things, please contact me. I would greatly appreciate.

## Requirement

* Python 2.7
* Splinter (http://splinter.readthedocs.org/en/latest/install.html)
* Chromedriver (https://devblog.supportbee.com/2014/10/27/setting-up-cucumber-to-run-with-Chrome-on-Linux/
* webdriver (http://stackoverflow.com/questions/8255929/running-webdriver-chrome-with-selenium)

## How to use

Prepare a cloud storage service. I used Google Photos here.

    python arloBackup.py {userId} {password} -d {download folder} -u {upload folder}

    # Sample
    python arloBackup.py your@email.com yourpassword -d ~Downloads -u "~/Google Photos"

This basically says "Hey script. Download all yesterday's Videos with my credential. You can find them in '~Downloads' folder. Move them to '~/Google Photos' folder."

## Comments

I couldn't find an easy way for doing this BACKGROUND yet. If I could, I would be happy. I tried to pass their authentication system with urllib2. Apparently there are some tricks for their authentication system, I keep getting BAD REQUEST errors. I felt like that I'm wasting time, so I would go for easier solution.

Thank you.