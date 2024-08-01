import os
import requests

GITHUB_TOKEN = os.getenv('TOKEN_GITHUB')
ORG_NAME = os.getenv('ORG_NAME')

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_repos(org_name):
    url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return [repo['name'] for repo in response.json()]

def get_dependabot_alerts(org_name, repo_name):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/dependabot/alerts'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    repos = get_repos(ORG_NAME)
    for repo in repos:
        print(f'Fetching Dependabot alerts for {repo}...')
        alerts = get_dependabot_alerts(ORG_NAME, repo)
        if alerts:
            print(f'{repo} has {len(alerts)} alerts:')
            for alert in alerts:
                print(f"- {alert['dependency']['package']['name']}: {alert['security_advisory']['summary']}")
        else:
            print(f'{repo} has no alerts.')

if __name__ == '__main__':
    main()
