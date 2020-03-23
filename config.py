import os


class Config:
    git_token = os.getenv('GIT_PRIVATE_TOKEN')
    git_url = os.getenv('GIT_URL', "https://git.equinor.com")
    update_freq = int(os.getenv('GRAFANA_FREQ', "3600"))
    inactive_project_days_since_last_commit = 90
    flask_debug = bool(os.getenv("FLASK_DEBUG", 0))
