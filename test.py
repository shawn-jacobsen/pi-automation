from dotenv import load_dotenv
load_dotenv()
import os

from notionAutomation.index import (
  updateClasses,
  updateSleepHours
)

# updateClasses()
updateSleepHours(5)