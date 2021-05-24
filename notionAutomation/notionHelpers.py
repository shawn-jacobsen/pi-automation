import requests

# add row data  to Notion DB given Notion row object
def addAssignmentToNotionDB(row, class_info, assignment, isCompleteByCarmen, assignment_due_local, hasDueDate):


  row.Class = class_info["notion_name"]
  row.assignment = assignment["name"]
  row.progress = "Complete" if isCompleteByCarmen else "Incomplete"
  row.due_date = assignment_due_local if hasDueDate else ""
  row.type = getAssignmentType(assignment["name"], assignment["submission_types"])
  row.submission = getAssignmentLink(assignment["html_url"])
  row.canvasId = str(assignment['id'])
  db_id
  category
  class_
  assignment
  progress
  due_date
  type_
  submission
  quick_notes
  canvas_id
  do_today


# builds JSON object to be passed as request body when posting new assignment
# db_id        :  string
# category     :  string
# class        :  string
# assignment   :  string
# progress     :  string
# due_date     :  string, ISO_8601 => "YYYY-MM-DDTHH:MM:SS-04:00" (**04:00 for EST**)
# type_        :  string
# submission   :  string
# quick_notes  :  string
# canvas_id    :  string
# do_today     :  boolean
def buildAssignmentRowJSON(db_id, category, class_, assignment, progress, due_date, type_, submission, quick_notes, canvas_id, do_today):
  return {
	"parent": { "database_id": db_id },
	"properties": {
    "Category":{
      "select": {
        "name": category
      }
    },
    "Class":{
      "select": {
        "name": class_
      }
    },
		"Assignment": {
			"title": [
				{
					"text": {
						"content": assignment
					}
				}
			]
		},
    "Progress":{
      "select": {
        "name": progress
      }
    },
    "Due Date":{
      "date": {
        "start": due_date
      }
    },
    "Type":{
      "select": {
        "name": type_
      }
    },
    "Submission":{
      "url": submission
    },
    "Quick Notes":{
			"rich_text": [
				{
					"text": {
						"content": quick_notes
					}
				}
			]
    },
    "canvasId":{
			"rich_text": [
				{
					"text": {
						"content": canvas_id
					}
				}
			]
    },
    "Do Today":{
      "checkbox": do_today
    },
	}
}
