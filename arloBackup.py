# ArloBackup Script
# Author: Jake Jung
import argparse
import os
import time

cVersion = "0.1a"

def main():
  ShowApplicationTitle()
  inputs = ProcessCommandLineInputs()

  print "Accessing Arlo webpage.."
  DownloadAllTodaysVideo(inputs.account, inputs.password, inputs.verbose)
  print "Processing Video.."
  MoveFilesToUploadFolder(inputs.download_path, inputs.upload_path)
  print "Done"
  pass

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
    return
  downloader.DownloadTodaysVideo()

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

    return self.browser.is_text_present('Library')

  def DownloadTodaysVideo(self):
    print "Logging in.."
    if not self.OpenLibraryTab():
      self.Debug("Err> Cannot open library tab")
      return False

    print "Downloading Video.."
    self.HideRuleNotification()
    self.IterateToDownloadAll()
    self.WaitForDownloading()

  def OpenLibraryTab(self):
    self.browser.find_by_id('footer_library').click()
    return not self.browser.find_by_id('day_ToggleSelectMode').is_empty()

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

  def SetSelectVideoMode(self):
    # TODO: Select YESTERDAY.
    self.browser.find_by_id('day_ToggleSelectMode').click()

  def PushDownload(self):
    # TODO: Can we change the download folder?
    self.browser.find_by_id('footer_download').click()
    pass

  def WaitForDownloading(self):
    # TODO: How can I know when all the downloading would be completed?
    # Wait for one second for now.
    time.sleep(1)

  def Debug(message):
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
      if filename.endswith(".mp4"):
        # os.rename(dirs)
        src = "%s/%s" % (expandedDownloadPath, filename)
        dst = "%s/%s" % (expandedUploadPath, filename)
        os.rename(src, dst)

if __name__ == "__main__":
  main()
else:
  print "This file must be the main entry point."