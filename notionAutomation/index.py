from updateClasses import (
  updateClasses
)

from secrets import (
  ASSIGNMENT_DATABASE_URL,
  CARMEN_USER_ID,
  ACCESS_TOKEN_CARMEN,
  NOTION_TOKEN_V2
)

# update class assignments
updateClasses(ASSIGNMENT_DATABASE_URL, CARMEN_USER_ID, ACCESS_TOKEN_CARMEN, NOTION_TOKEN_V2)