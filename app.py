# This is a sample Python script.
import requests
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_best_post():
    # Use a breakpoint in the code line below to debug your script.
    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth('YOUR CLIENT ID', 'YOUR SECRET API ID')

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': 'YOUR USERNAME',
            'password': 'YOUR PASSWORD '}

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'MyBot/0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    json = requests.get('https://oauth.reddit.com/api/v1/me',
                        headers=headers).json()  # Press Ctrl+F8 to toggle the breakpoint.
    res2 = requests.get("https://oauth.reddit.com/r/python/best",
                        headers=headers)
    for post in res2.json()['data']['children']:
        print('this is the title : ' + str(post['data']['title']) + ' . ==> and this is the score : ' + str(
            post['data']['score']))
    # print(res2.json())
    print('finish')
    return res2


def best_5(res2):
    df = pd.DataFrame()  # initialize dataframe

    # loop through each post retrieved from GET request
    for post in res2.json()['data']['children']:
        # append relevant data to dataframe
        df = df.append({
            'title': post['data']['title'],
            'score': float(post['data']['score'])
        }, ignore_index=True)
    df = df.sort_values(by=['score'], ascending=False)
    print('we are here ==============================')
    print(df.head(5))
    return df.head(5)


@app.route('/reddit')
def hello_world():
    res = get_best_post()
    df = best_5(res)
    return df.to_json(orient='records')[1:-1].replace('},{', '} {')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
