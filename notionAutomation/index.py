from pathlib import Path
ENV_PATH = Path('../') / '.ENV'
from dotenv import load_dotenv
load_dotenv(dotenv_path=ENV_PATH)
import os

from notionAutomation.updateClasses import (
  updateNotionClasses
)

from notionAutomation.updateSleep import (
  updateNotionSleepHours
)

# get env variables

CARMEN_USER_ID = os.getenv('CARMEN_USER_ID')
CARMEN_SECRET =  os.getenv('CARMEN_SECRET')

NOTION_DOODLEBOT_SECRET =  os.getenv('NOTION_DOODLEBOT_SECRET')
NOTION_HABITS_DB_ID = os.getenv('NOTION_HABITS_DB_ID')
NOTION_ASSIGNMENT_DB_ID =  os.getenv('NOTION_ASSIGNMENT_DB_ID')

# update class assignments
def updateClasses():
  rval = True
  try:
    updateNotionClasses(NOTION_ASSIGNMENT_DB_ID, CARMEN_USER_ID, CARMEN_SECRET, NOTION_DOODLEBOT_SECRET)
  except Exception as err:
    print(err)
    rval = False
  return rval

# update hours slept
def updateSleepHours(sleep_hrs):
  print(NOTION_TOKEN_V2)
  rval = True
  try:
    updateNotionSleepHours(HABIT_TRACKER_URL, NOTION_TOKEN_V2, sleep_hrs)
  except Exception as err:
    print(err)
    rval = False
  return rval