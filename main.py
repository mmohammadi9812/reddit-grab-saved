#!/usr/bin/env python3
# Copyright (c) 2020 Mohammad Mohammadi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# Used this link for authentication:
# https://medium.com/@nickpgott/how-to-login-to-a-reddit-account-with-praw-when-2fa-is-enabled-4db9e82448a5

from dotenv import load_dotenv as load
import praw

import os
import random
import webbrowser
import socket
import pandas as pd

load()

client_id      = os.getenv("CLIENT_ID")
client_secret  = os.getenv("CLIENT_SECRET")
user_agent     = os.getenv("USER_AGENT")
username       = os.getenv("REDDIT_USER_NAME")
password       = os.getenv("REDDIT_PASWORD")

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password,
                     redirect_uri="http://localhost:8080")


def receive_connection():
    """
    Wait for and then return a connected socket..
    Opens a TCP connection on port 8080, and waits for a single client.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """
    Send message to client and close the connection.
    """
    client.send('HTTP/1.1 200 OK\r\n\r\n{}'.format(message).encode('utf-8'))
    client.close()


def authenticate():
    """
    Authenticate application for user access
    """
    state = str(random.randint(0, 65000))
    scopes = ['identity', 'history', 'read', 'edit']
    url = reddit.auth.url(scopes, state, 'permanent')
    webbrowser.open(url)

    client = receive_connection()
    data = client.recv(1024).decode('utf-8')

    param_tokens = data.split(' ', 2)[1].split('?', 1)[1].split('&')
    params = {key: value for (key, value) in [token.split('=')
                                              for token in param_tokens]}

    if state != params['state']:
        send_message(client, f'State mismatch. Expected: {state} Received: {params["state"]}')
        return 1
    elif 'error' in params:
        send_message(client, params['error'])
        return 1

    refresh_token = reddit.auth.authorize(params["code"])
    send_message(client, f"Refresh token: {refresh_token}")

    print(refresh_token)
    return 0


def main():
    authenticate()
    savedsubs = reddit.user.me().saved(limit=None)
    posts, comments = [], []
    for s in savedsubs:
        if isinstance(s, praw.models.Submission):
            posts.append(
                {
                    'id': s.id,
                    'subreddit': s.subreddit.display_name,
                    'title': s.title,
                    'permalink': s.permalink,
                    'score': s.score,
                    'url': s.url
                }
            )
        elif isinstance(s, praw.models.Comment):
            comments.append(
                {
                    'id': s.id,
                    'subreddit': s.subreddit.display_name,
                    'body': s.body,
                    'permalink': s.permalink,
                    'score': s.score,
                    'parent_permalink': s.submission.permalink
                }
            )
    postsdf = pd.DataFrame(posts)
    commentsdf = pd.DataFrame(comments)
    return postsdf, commentsdf


if __name__ == '__main__':
    postsdf, commentsdf = main()

    subgroup = postsdf.groupby('subreddit')
    subreddits = [subgroup.get_group(x) for x in subgroup.groups]
    subreddits = sorted(subreddits, key=len, reverse=True)

    os.makedirs("posts", exist_ok=True)

    for subreddit in subreddits:
        name = subreddit.subreddit.unique()[0]
        subreddit.to_csv(f"posts/{name}.csv")
        subreddit.to_excel(f"posts/{name}.xls")
    postsdf.to_csv('saved_posts.csv')
    postsdf.to_excel('saved_posts.xls')

    commentsdf.to_csv('saved_comments.csv')
    commentsdf.to_excel('saved_comments.xls')
