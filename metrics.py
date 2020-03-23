import time
from datetime import datetime, timedelta

import gitlab
import requests

from config import Config


class Metrics:
    # def __init__(self):
    #     self.gl = gitlab.Gitlab(Config.git_url, private_token=Config.git_token, api_version='4',
    #                             session=requests.Session())
    #     self.projects = self.gl.projects.list(as_list=False)
    #     self.inactive_projects = self.get_inactive_projects()
    #     self.open_issues = self.get_issues()
    #     self.groups = self.gl.groups.list(as_list=False)
    #     self.users = self.gl.users.list(as_list=False)
    #     self.inactive_users = None
    #     self.total_branches = self.get_branches()
    #     self.commits_last_day = self.get_commits_last_day()
    #     self.commits_last_week = self.get_commits_last_week()

    def __init__(self):
        self.gl = gitlab.Gitlab(Config.git_url, private_token=Config.git_token, api_version='4',
                                session=requests.Session())
        self.projects = self.gl.projects.list(as_list=False)
        self.users = self.gl.users.list(as_list=False)

    def total_projects(self):
        return self.projects.total

    def total_groups(self):
        return self.groups.total

    def total_users(self):
        return self.users.total

    def get_inactive_projects(self):
        now = datetime.utcnow()
        since = now - timedelta(days=Config.inactive_project_days_since_last_commit)
        since = since.replace(microsecond=0).isoformat()
        since = str(since) + "Z"

        i = 0
        for project in self.projects:
            try:
                if not len(project.commits.list(since=since)):
                    i += 1
            except Exception as error:
                print("The project '" + project.name + "' could not be accessed. Project ID: " +
                      str(project.id) + ". Skipped...")
                print(error)

        return i

    def get_branches(self):
        sum_branches = 0
        i = 0
        print("Counting branches...")

        for project in self.projects:
            try:
                sum_branches += len(project.branches.list())
                i += 1
                if i % 200 == 0:
                    print(f"Still counting branches...{i}")
            except:
                print("The project '" + project.name + "' could not be accessed. Project ID: " +
                      str(project.id) + ". Skipped...")

        return sum_branches

    def get_issues(self):
        page = 1
        sum = 0
        while open_issues := self.gl.issues.list(state='opened', scope="all", per_page=100, page=page):
            sum += len(open_issues)
            page += 1

        return sum

    def get_commits_last_day(self):
        now = datetime.utcnow()
        since = now - timedelta(hours=6)
        since = since.replace(microsecond=0).isoformat()
        since = str(since) + "Z"

        i = 0
        nr_projects = 0
        for project in self.projects:
            nr_projects += 1
            try:
                commits = len(project.commits.list(since=since))
                i += commits
            except:
                print("The project '" + project.name + "' could not be accessed. Project ID: " +
                      str(project.id) + ". Skipped...")
        return i

    def get_commits_last_week(self):
        now = datetime.utcnow()
        since = now - timedelta(days=7)
        since = since.replace(microsecond=0).isoformat()
        since = str(since) + "Z"

        i = 0
        for project in self.projects:
            try:
                commits = len(project.commits.list(since=since))
                i += commits
            except Exception as error:
                print("The project '" + project.name + "' could not be accessed. Project ID: " +
                      str(project.id) + ". Skipped...")
                print(error)

        return i

    def get_inactive_users(self):
        active_users = self.gl.user_activities.list(all=True, as_list=False)
        self.inactive_users = self.users.total - len(active_users)

    # def to_prometheus(self):
    #     now = datetime.now()
    #     return f"""
    #         branches  {self.total_branches} {now}
    #         projects {self.total_projects()} {now}
    #         git_users {self.total_users()} {now}
    #         git_groups {self.total_groups()} {now}
    #         issues {self.open_issues} {now}
    #         commits_last_day {self.commits_last_day} {now}
    #         commits_last_week {self.commits_last_week} {now}
    #         inactive_projects {self.inactive_projects} {now}
    #         inactive_users {self.inactive_users} {now}
    #     """

    @staticmethod
    def log_format(name, value, timestamp):
        return f"gitlabstats_{name} {value} {timestamp}\n"

    def to_prometheus(self):
        now = time.time() * 1000
        return f"{self.log_format('projects', self.total_projects(), now)}" \
               f"{self.log_format('total_users', self.total_users(), now)}"
