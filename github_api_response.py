from datetime import datetime

def event_group(event):
    event_type = event['type']
    repo = event['repo']['name']
    return {"type": event_type,
            "repo": repo}

def group_summary(event_group):
    event_type = event_group["event"]["type"]
    repo = event_group["event"]["repo"]
    rep_count = event_group["rep_count"]
    if event_type=="CommitCommentEvent":
        return f"{rep_count} commit comment(s) created in {repo}"
    elif event_type=="CreateEvent":
        return f"{rep_count} Git branch/tag created in {repo}"
    elif event_type=="DeleteEvent":
        return f"{rep_count} Git branch/tag deleted in {repo}"
    elif event_type=="ForkEvent":
        return f"Forked repo {repo}"
    elif event_type=="GollumEvent":
        return f"Created/updated wiki page in {repo}"
    elif event_type=="IssueCommentEvent":
        return f"{rep_count} Issue Comment on {repo}"
    elif event_type=="IssuesEvent":
        return f"Opened {rep_count} new issue on {repo}"
    elif event_type=="MemberEvent":
        return f"{rep_count} Member event on {repo}"
    elif event_type=="PublicEvent":
        return f"Made {repo} public"
    elif event_type=="PullRequestEvent":
        return f"Pulled from {repo}"
    elif event_type=="PullRequestReviewEvent":
        return f"Reviewed {rep_count} Pull Request on {repo}"
    elif event_type=="PullRequestReviewCommentEvent":
        return f"{rep_count} comment on Pull Request Review"
    elif event_type=="PullRequestReviewThreadEvent":
        return f"{rep_count} comment thread on Pull Request Review"
    elif event_type=="PushEvent":
        return f"Pushed {rep_count} commits to {repo}"
    elif event_type=="ReleaseEvent":
        return f"ReleaseEvent {repo}"
    elif event_type=="SponsorshipEvent":
        return f"SponsorshipEvent {repo}"
    elif event_type=="WatchEvent":
        return f"Started watching {repo}"

def parse_event_list(events_data):
    events_data = sorted(events_data, key=lambda x: x['created_at'], reverse=True)
    events_by_month = {}
    for event in events_data:
        month = datetime.fromisoformat(event['created_at']).strftime("%B%Y")
        if month not in events_by_month:
            events_by_month[month] = []
        events_by_month[month].append(event_group(event))
    
    summary_by_month = {}
    for month, event_list in events_by_month.items():
        curr_month_summary = []
        prev_event, rep_count = None, 0
        for idx, event in enumerate(event_list):
            curr_event = event ######
            if curr_event==prev_event or prev_event==None:
                rep_count += 1
            else:
                curr_month_summary.append(group_summary({"event": prev_event,
                                                         "rep_count": rep_count}))
                rep_count = 1
            prev_event = curr_event
            if idx==len(event_list)-1:
                curr_month_summary.append(group_summary({"event": curr_event,
                                                         "rep_count": rep_count}))
                summary_by_month[month] = curr_month_summary
                
    return summary_by_month
