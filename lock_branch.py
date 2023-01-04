from argparse import ArgumentParser
import os
import json

import requests


if __name__ == '__main__':

    # parse cli
    parser = ArgumentParser(description='lock / unlock main branch')
    parser.add_argument('--lock', action='store_true')
    args = parser.parse_args()

    # get git token
    git_token = os.environ['GIT_TOKEN']

    # get url
    url = 'https://api.github.com/repos/lakes-legendaries/dyno-nb-ci/branches/main/protection'

    # get request headers
    headers={
        'Accept': 'application/vnd.github+json',
        'Authorization': f"token {os.environ['GIT_TOKEN']}",
        'X-GitHub-Api-Version': '2022-11-28',
    }

    # get current protection rules
    rules = {
        key: (
            value['enabled']
            if 'enabled' in value
            else {
                k: v
                for k, v in value.items()
                if k != 'url'
            }
        )
        for key, value in requests.get(url, headers=headers).json().items()
        if key != 'url'
    }

    # modify rules, set required if not provided
    rules['lock_branch'] = args.lock
    rules.setdefault('required_pull_request_reviews', None)
    rules.setdefault('required_status_checks', None)
    rules.setdefault('restrictions', None)

    # update rules
    print(rules)
    print(requests.put(url, headers=headers, data=json.dumps(rules)).json())
