#!/usr/bin/env python3

from main import reddit, authenticate

import pandas as pd
import praw.models as models


def main():
    authenticate()
    me = reddit.user.me()
    new_saved = me.saved(limit=50)
    new_saved = list(new_saved)[::-1]
    saved_posts = pd.read_csv("saved_posts.csv")
    saved_comments = pd.read_csv("saved_comments.csv")

    for submission in new_saved:
        if isinstance(submission, models.Submission):
            if submission.id in saved_posts.id:
                continue
            else:
                row = {
                    'id': submission.id,
                    'subreddit': submission.subreddit.display_name,
                    'title': submission.title,
                    'permalink': submission.permalink,
                    'score': submission.score,
                    'url': submission.url
                }
                saved_posts.loc[-1] = row
                saved_posts.index = saved_posts.index + 1
                saved_posts.sort_index(inplace=True)
        elif isinstance(submission, models.Comment):
            if submission.id in saved_comments.id:
                continue
            else:
                row = {
                    'id': submission.id,
                    'subreddit': submission.subreddit.display_name,
                    'body': submission.body,
                    'permalink': submission.permalink,
                    'score': submission.score,
                    'parent_permalink': submission.submission.permalink
                }
                saved_comments.loc[-1] = row
                saved_comments.index = saved_comments.index + 1
                saved_comments.sort_index(inplace=True)

    return saved_posts, saved_comments


if __name__ == '__main__':
    updated_posts, updated_comments = main()
    updated_posts.to_csv("saved_posts.csv")
    updated_posts.to_excel("saved_posts.xls")
    updated_comments.to_csv("saved_comments.csv")
    updated_comments.to_csv("saved_comments.csv")
