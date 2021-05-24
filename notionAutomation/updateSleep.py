import requests
import pprint
import json
from termcolor import colored
from datetime import *
from pathlib import Path
from datetime import date

from notionAutomation.notionHelpers import (
  addRowToNotionDB,
  getNotionClient
)

def updateNotionSleepHours(HABIT_TRACKER_URL, NOTION_TOKEN_V2, sleep_hrs):
  # setup Notion session
  notion_client = getNotionClient(NOTION_TOKEN_V2)
  print(notion_client)

  # assignment collection view
  assignment_cv = notion_client.get_collection_view(HABIT_TRACKER_URL)

  today = date.today()

  # check if in Notion already
  found_assignments = assignment_cv.collection.get_rows(search="test")
  isInNotionDB = False
  for row in found_assignments:
    isInNotionDB = True
    break
  print(today)
  print(isInNotionDB)

  # row = assignment_cv.collection.add_row()
  # addRowToNotionDB(row, class_info, assignment, isCompleteByCarmen, assignment_due_local, hasDueDate)
    
  #try:

  #except Exception as e:
  #  print(colored(f"ERROR: cannot add to Notion DB", "red"))
  #  print(str(e))
