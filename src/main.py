import os
import json
from dotenv import load_dotenv
from github import Github


def create_issues(source_directory, target_repository):
    # iterate over JSON requirements in source directory
    for filename in os.listdir(source_directory):
        # compose file path of JSON requirement
        f = os.path.join(source_directory, filename)
        print(type(f))
        # check if it is a file
        if os.path.isfile(f):
            create_issue(target_repository, f)


def create_issue(target_repository, json_path):
    # Open JSON file
    f = open(json_path)

    # Generate dictionary from JSON
    requirement = json.load(f)

    # Create new issue based on JSON requirement
    target_repository.create_issue(
        title=requirement['title'],
        body=requirement['body'],
        labels=requirement['labels'],
        assignees=requirement['assignees'],
        milestone=target_repository.get_milestone(requirement['milestone'])
    )

    # Close JSON file
    f.close()


def close_issues(target_repository):
    open_issues = target_repository.get_issues(state='open')
    for issue in open_issues:
        issue.edit(state='closed')


if __name__ == '__main__':
    # Load environment variables
    load_dotenv()

    # Create GitHub instance based on personal access token
    g = Github(os.environ.get("PERSONAL_ACCESS_TOKEN"))

    # Get GitHub repository based on target repository name
    repo = g.get_user().get_repo(os.environ.get("TARGET_REPOSITORY_NAME"))

    # Create issue for each JSON requirement
    create_issues(os.environ.get("SOURCE_DIRECTORY"), repo)
