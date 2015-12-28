# ArloBackup Script
# Author: Jake Jung
import argparse
import os
import time
import datetime

cVersion = "0.1a"
cWaitingTimeForPageUpdate = 20 # seconds
cWaitingTimeForDownloadingToComplete = 10 # seconds

def main():
  ShowApplicationTitle()
  inputs = ProcessCommandLineInputs()

  print "Accessing Arlo webpage.."
  result = DownloadAllTodaysVideo(inputs.account, inputs.password, inputs.verbose)

  if result:
    print "Processing Video.."
    MoveFilesToUploadFolder(inputs.download_path, inputs.upload_path)
  else:
    print "Download failed"
    return 1

  print "Done"
  return 0

def ShowApplicationTitle():
  print "-----------------------------------------"
  print "  ArloBackup %s" % cVersion
  print "-----------------------------------------"
  print

def ProcessCommandLineInputs():
  parser = argparse.ArgumentParser(
    description="""This is a helper script to download Arlo videos from your account, and put them into
a cloud storage. So that you can keep them forever without losing after certain time.""")

  parser.add_argument("account", help="Arlo site account id for login. ex> magoja@gmail.com")
  parser.add_argument("password", help="Arlo site password for login.")

  parser.add_argument(
    "-d", "--download_path",
    default="~/Downloads",
    help="Default download folder. This script will move all *.mp4 files from there.")
  parser.add_argument(
    "-u", "--upload_path",
    default="~/Uploads",
    help="Upload folder for cloud storage. I recommend you to use Dropbox, Google Photos or a similar service.")

  parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity for debug.")

  return parser.parse_args()

def DownloadAllTodaysVideo(account, password, verbose):
  downloader = ArloVideoDownloader(verbose)
  if not downloader.Login(account, password):
    print "Error) Login Failed. Please check your account."
    # This might break if they change the login system.
    return False
  downloader.DownloadTodaysVideo()

  return True

class ArloVideoDownloader:
  def __init__(self, verbose):
    from splinter import Browser
    self.browser = Browser("chrome")
    self.verbose = verbose

  def __del__(self):
    if self.verbose:
      return

    # Leave the browser open if this is running with Verbose option.
    if self.browser != None:
      self.browser.quit()

  def Login(self, account, password):
    self.browser.visit("https://arlo.netgear.com/#/login")
    self.browser.fill('userId', account)
    self.browser.fill('password', password)

    button = self.browser.find_by_id('loginButton')
    if button.is_empty():
      self.Debug("Cannot find loginButton.")
      return False

    button.click()

    self.WaitForPageUpdate()
    # Wait for page to load. This can take some time.
    if self.browser.is_element_not_present_by_text('Library', wait_time = cWaitingTimeForPageUpdate):
      return False
    else:
      return True

  def DownloadTodaysVideo(self):
    print "Logging in.."
    if not self.OpenYesterdayPage():
      self.Debug("Err> Cannot open library tab")
      return False

    print "Downloading Video.."
    self.HideRuleNotification()
    self.IterateToDownloadAll()
    self.WaitForDownloading()

  def WaitForPageUpdate(self):
    self.Debug("Wait %d seconds.." % cWaitingTimeForPageUpdate)
    time.sleep(cWaitingTimeForPageUpdate)    

  def HideRuleNotification(self):
    self.browser.find_by_id('day_ok').click()

  def IterateToDownloadAll(self):
    self.SetSelectVideoMode()

    previews = self.browser.find_by_css('.vlist-preview')
    
    # Go over for each video.
    # I didn't try to download all at once, because I couldn't
    # avoid the problem that Browser asking for a permission
    # to download multiple files at once.
    # So, download videos one by one
    previousButton = None
    for button in previews:
      if previousButton is not None:
        # Unselect last one.
        previousButton.click()

      # Select new one
      button.click()
      previousButton = button

      self.PushDownload()

  def OpenYesterdayPage(self):    
    #https://arlo.netgear.com/#/calendar/201512/all/all/20151226/day
    yesterday = self.GetYesterday()
    url = "https://arlo.netgear.com/#/calendar/%d%d/all/all/%d%d%d/day" % (
      yesterday.year, yesterday.month, yesterday.year, yesterday.month, yesterday.day)
    self.Debug("Visiting: %s" % url)
    self.browser.visit(url)
    self.WaitForPageUpdate()
    
    return not self.browser.find_by_id('day_ToggleSelectMode').is_empty()

  def SetSelectVideoMode(self):
    self.browser.find_by_id('day_ToggleSelectMode').click()

  def GetYesterday(self):
    return datetime.datetime.now() - datetime.timedelta(hours=24)

  def PushDownload(self):
    # TODO: Can we change the download folder?
    self.browser.find_by_id('footer_download').click()
    pass

  def WaitForDownloading(self):
    # TODO: How can I know when all the downloading would be completed?
    time.sleep(cWaitingTimeForDownloadingToComplete)

  def Debug(self, message):
    if self.verbose:
      print message

def MoveFilesToUploadFolder(downloadPath, uploadPath):
  # TODO: Go over all MP4 files. Get the timestamp from file name,
  # convert it to human readable format. Move it to target folder.

  print "Accessing '%s' folder.." % downloadPath

  expandedDownloadPath = os.path.expanduser(downloadPath)
  expandedUploadPath = os.path.expanduser(uploadPath)

  for root, dirs, filenames in os.walk(expandedDownloadPath):
    filenames.sort()
    for filename in filenames:
      if IsArloVideo(filename):
        src = "%s/%s" % (expandedDownloadPath, filename)
        dst = "%s/%s" % (expandedUploadPath, filename)
        os.rename(src, dst)
def IsArloVideo(filename):
  # This is not perfect solution.
  if not filename.endswith(".mp4"):
    return False

  filenameOnly = filename[:-4]
  if len(filenameOnly) != 13: # 13 Digit Epoch
    return False

  # Number only.
  if "%d" % int(filenameOnly) != filenameOnly:
    return False
  return True

if __name__ == "__main__":
  import sys, os
  if main():
    sys.exit(os.EX_OK)
  else:
    sys.exit(os.EX_SOFTWARE)
else:
  print "This file must be the main entry point."