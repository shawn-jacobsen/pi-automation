
# get correct instructure endpoint for assignmnet submission given the provided canvas api url
def getAssignmentLink(API_link):
  INSTRUCTURE_ENDPOINT = "https://osu.instructure.com/"
  API_link = API_link.split('assignments/')[0] + 'assignments/' + API_link.split('~')[1]
  return API_link.replace("https://canvas.instructure.com/",INSTRUCTURE_ENDPOINT)

# determines the correct assignment type given various assignment data
def getAssignmentType(assignmentName, submission_types):
  if "test" in assignmentName.lower() or "exam" in assignmentName.lower() or "final" in assignmentName.lower():
    return "EXAM"

  if ("quiz" in assignmentName.lower()) and ("external_tool" in submission_types):
    return "Book Quiz"

  if "lab" in assignmentName.lower():
    return "Lab"
  
  if ("quiz" not in assignmentName.lower()) and ("hw" in assignmentName.lower()) and ("external_tool" in submission_types):
    return "Book Homework"
  
  if ("online_upload" in submission_types) and ("hw" in assignmentName.lower()):
    return  "PDF Homework"
  
  if ("submit assignment" in assignmentName.lower()) and ("online_upload" in submission_types):
    return "Essay"
  
  if ("reflection post" in assignmentName.lower()):
    return "Essay"
  
  if ("homework" in assignmentName.lower()):
    return "Book Homework"

  if ("online_quiz" in submission_types) and ("hw" in assignmentName.lower()):
    return "Book Homework"

  if ("reading quiz" in assignmentName.lower()):
    return "Book Quiz"

  return ""