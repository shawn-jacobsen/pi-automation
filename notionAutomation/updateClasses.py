import requests
import pprint
import json
from termcolor import colored
from datetime import *
from pathlib import Path

from updateClassesHelpers import *

CARMEN_USER_ID = '85970000000559345'
ACCESS_TOKEN_CARMEN = '8597~GRZXEV3PCyWaB3wKt0jg4VagALMaou6dH4OTdNj8Dt7ZwRZWEdsXmdQ5kibiFgTP'
NOTION_TOKEN_V2 = 'f094e1add62286410015e39598e998de317fa5fc36538874548034d560cfe596acb01f6c0e12813ec59afbb9ddb11694034668acf23ce3568d1c2c45148975d8e23a76e0abcab7a64321f38a0155'

# load json class data
OSU_CLASSES_DATA_PATH = (Path(__file__).parent / '../osuClasses.json').resolve()
with open(OSU_CLASSES_DATA_PATH) as f:
  data = json.load(f)

# endpoint to access all active class information
CLASS_INFO_URL = f"https://canvas.instructure.com/api/v1/courses?enrollment_state=active&per_page=100&access_token={ACCESS_TOKEN_CARMEN}"

# endpoint to access assignment information
# replace <class_id> with access token for use
CLASS_COURSES_URL = f"https://canvas.instructure.com/api/v1/courses/<class_id>/assignments?per_page=100&include=submission&access_token={ACCESS_TOKEN_CARMEN}"

# notion assignment database url
ASSIGNMENT_DATABASE = 'https://www.notion.so/shawnpersonal/37adf54ce56947f7bce06da37a451b5d?v=1bdae244cd674966b2dbc9bafd16a5cb'

# setup Notion session
notion_client = getNotionClient(NOTION_TOKEN_V2)

# assignment collection view
assignment_cv = notion_client.get_collection_view(ASSIGNMENT_DATABASE)

# get assignments
for class_info in data['class_Data'][0]['classes']:
  # print json data available for each class_info
  print(colored(f"CLASS:{class_info['name']}",'magenta'))
  print(colored(f"ID:   {class_info['id']}",'magenta'))
  print('--------------')

  assignment_endpt = CLASS_COURSES_URL.replace('<class_id>', class_info['id']).replace('<token>', ACCESS_TOKEN_CARMEN)
  response = requests.get(assignment_endpt)
  if response:
    assignments_info = response.json()

    for assignment in assignments_info:

      isCompleteByCarmen = (str(assignment["submission"]["user_id"]) == CARMEN_USER_ID) and (assignment["submission"]["submitted_at"] is not None)
      isGraded =  assignment["points_possible"] > 0

      # check if in Notion already
      found_assignments = assignment_cv.collection.get_rows(search=str(assignment['id']))
      isInNotionDB = False
      for row in found_assignments:
        isInNotionDB = True
        break

      # check due date
      hasDueDate = assignment['due_at'] is not None;
      assignment_due_utc = None
      assignment_due_local = None
      isFuture = None

      # get time in local time
      if (hasDueDate):
        assignment_due_str = assignment['due_at'].replace('Z','')
        assignment_due_utc = datetime.strptime(assignment_due_str, '%Y-%m-%dT%H:%M:%S')
        assignment_due_local = assignment_due_utc.replace(tzinfo=timezone.utc).astimezone(tz=None)

        # check if future assignment
        isFuture = assignment_due_utc > datetime.now();

      # valid to be added to Notion DB
      if (not isCompleteByCarmen) and (not hasDueDate or isFuture) and (not isInNotionDB) and isGraded:

        # print attributes
        print(colored(f"{assignment['name']}",attrs=['bold']))
        print(f"    id:     {assignment['id']}")
        print(f"    done:   {isCompleteByCarmen}")
        print(f"    Due at: {assignment_due_local if assignment_due_local is not None else 'Undated'}")
        print()
        
        try:
          row = assignment_cv.collection.add_row()
          addRowToNotionDB(row, class_info, assignment, isCompleteByCarmen, assignment_due_local, hasDueDate)
        except:
          print(colored(f"ERROR: cannot add to Notion DB", "red"))


  # err getting response data
  else:
    print('An error has occurred.')