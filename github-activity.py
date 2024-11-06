import argparse
import sys
import urllib.request
import json
from github_api_response import parse_event_list

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Get Github User Activity")
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)
    parser.add_argument("username", help="Github Username")
    args = parser.parse_args()

    url = f"https://api.github.com/users/{args.username}/events"

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        resp = response.read()
    events_data = json.loads(resp.decode('utf-8'))
    all_event_summary = parse_event_list(events_data)
    for month, event_list in all_event_summary.items():
        print(month)
        for event in event_list:
            print("-", event)
        print()