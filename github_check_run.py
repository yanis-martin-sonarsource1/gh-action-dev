import time
import requests

GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "your-repo-owner"
REPO_NAME = "your-repo-name"
ACCESS_TOKEN = "your-access-token"

def get_open_pull_requests():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/pulls?state=open"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_pull_request_head_sha(pull_request_number):
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pull_request_number}"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["head"]["sha"]

def create_check_run(pull_request_number):
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/check-runs"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": "Example Check Run",
        "head_sha": get_pull_request_head_sha(pull_request_number),
        "status": "in_progress",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    check_run_id = response.json()["id"]
    return check_run_id

def update_check_run(check_run_id):
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/check-runs/{check_run_id}"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "status": "completed",
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "conclusion": "success"
    }
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()

def main():
    pull_requests = get_open_pull_requests()
    for pr in pull_requests:
        pr_number = pr["number"]
        check_run_id = create_check_run(pr_number)
        time.sleep(30)
        update_check_run(check_run_id)

if __name__ == "__main__":
    main()