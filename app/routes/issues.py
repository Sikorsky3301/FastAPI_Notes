from fastapi import APIRouter ,  HTTPException , status
from app.schemas import IssueCreate , IssueUpdate , IssueOutput , IssuesStatus 
from app.storage import load_data , save_data
import uuid

router = APIRouter(prefix="/api/v1/issues" , tags = ["issues"])

@router.get("/", response_model=list[IssueOutput])
def get_issues():
    issues = load_data()
    return issues

@router.post("/", response_model=IssueOutput , status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate):
    issues = load_data()
    new_issue = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority.value,
        "status": IssuesStatus.open.value
    }
    issues.append(new_issue)
    save_data(issues)
    return new_issue

@router.get("/{issue_id}", response_model=IssueOutput)
def get_issue(issue_id: str):
    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Issue not found")


@router.put("/{issue_id}", response_model=IssueOutput)
def update_issue(issue_id: str , payload: IssueUpdate):
    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            if payload.title is not None:
                issue["title"] = payload.title
            if payload.description is not None:
                issue["description"] = payload.description
            if payload.priority is not None:
                issue["priority"] = payload.priority.value
            if payload.status is not None:
                issue["status"] = payload.status.value
            save_data(issues)
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Issue not found")


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: str):
    issues = load_data()
    for index , issue in enumerate(issues):
        if issue["id"] == issue_id:
            issues.pop(index)
            save_data(issues)
            return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Issue not found")