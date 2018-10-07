import os
import sys
import json

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'libs'))

import requests
from bs4 import BeautifulSoup

def issues_manager(event, context):
    if 'PERSONAL_ACCESS_TOKEN' not in os.environ or os.environ['PERSONAL_ACCESS_TOKEN'] is None:
        # ERROR handling
        print("Please configure PERSONAL_ACCESS_TOKEN.")
        return
    elif 'TARGET_URL' not in os.environ or os.environ['TARGET_URL'] is None:
        # ERROR handling
        print("Please configure TARGET_URL.")
        return
    elif 'STATUS_LIST' not in os.environ or os.environ['STATUS_LIST'] is None:
        # ERROR handling
        print("Please configure STATUS_LIST.")
        return
    
    status_list = os.environ['STATUS_LIST']

    headers = {
       "Private-Token": os.environ['PERSONAL_ACCESS_TOKEN'],
       'Content-Type': 'application/json'
    }

    page = 1
    prev_num = 0


    # Loop with state 'opened' and 'closed'
    status_list_array = status_list.split(",")
    for status in status_list_array:
        #　Check if the previous loop and current loop IDs are same or not for getting all issues.
        prev_curr_diff = True
        while prev_curr_diff:
            query = {
                "scope": "all",
                "state": status,
                "milestone_title": os.environ['MILE_STONE'] ,
                "page": page
            }

            if 'MILE_STONE' not in os.environ or os.environ['MILE_STONE'] is None or os.environ['MILE_STONE'] == "null":
                query.pop("milestone_title")

            response = requests.get(os.environ['TARGET_URL'], headers=headers, params=query)

            soup = BeautifulSoup(response.text, "html.parser")

            issue_num_list = soup.find_all("span", attrs={"class": "issuable-reference"})
            issue_title_list = soup.find_all("span", attrs={"class": "issue-title-text"})

            # Confirm ID for loop
            if issue_num_list[0].text.replace("\n", "\t") == prev_num:
                prev_curr_diff = False
                prev_num = 0
                page = 1
                break
            else:
                prev_num = issue_num_list[0].text.replace("\n", "\t")
                page += 1

            index = 0

            for issue_num in issue_num_list:
                issue_title = issue_title_list[index]
                # issue_status = issue_status_list[index]
                print(issue_num.text.replace("\n", "\t") + 
                    status + "\t" +
                    # issue_status.text.replace("·\n", "").replace("\n", "\t") + 
                    issue_title.text.replace("\n", "\t") )
                index += 1


