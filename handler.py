import os
import sys
import json

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'libs'))

import requests
from bs4 import BeautifulSoup

def issues_manager(event, context):
    if 'PERSONAL_ACCESS_TOKEN' in os.environ['PERSONAL_ACCESS_TOKEN'] or os.environ['PERSONAL_ACCESS_TOKEN'] is None:
        # ERROR handling
        print("Please configure PERSONAL_ACCESS_TOKEN.")
        return
    elif 'TARGET_URL' in os.environ['TARGET_URL'] or os.environ['TARGET_URL'] is None:
        # ERROR handling
        print("Please configure TARGET_URL.")
        return
    elif 'TARGET_URL' in os.environ['MILE_STONE'] or os.environ['MILE_STONE'] is None:
        # ERROR handling
        print("Please configure MILE_STONE.")
        return

    headers = {
       "Private-Token": os.environ['PERSONAL_ACCESS_TOKEN'],
       'Content-Type': 'application/json'
    }

    page = 1
    prev_num = 0

    #　前回ループと今回ループの最初のIDが同じかどうかの確認
    prev_curr_diff = True

    while prev_curr_diff:
        query = {
            "scope": "all",
            "state": "all",
            "milestone_title": os.environ['MILE_STONE'],
            "page": page
        }

        response = requests.get(os.environ['TARGET_URL'], headers=headers, params=query)
        soup = BeautifulSoup(response.text, "html.parser")
        issue_num_list = soup.find_all("span", attrs={"class": "issuable-reference"})
        issue_status_list = soup.find_all("span", attrs={"class": "issuable-status"})
        issue_title_list = soup.find_all("span", attrs={"class": "issue-title-text"})

        # IDの確認
        if issue_num_list[0].text.replace("\n", "\t") == prev_num:
            break
        else:
            prev_num = issue_num_list[0].text.replace("\n", "\t")
            page += 1

        index = 0

        print(issue_status_list)

        for issue_num in issue_num_list:
            issue_title = issue_title_list[index]
            # issue_status = issue_status_list[index]
            print(issue_num.text.replace("\n", "\t") + 
                # issue_status.text.replace("·\n", "").replace("\n", "\t") + 
                issue_title.text.replace("\n", "\t") )
            index += 1


