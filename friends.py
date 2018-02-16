# This module gets information about Twitter friends of specified user
import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

def get_friends_list(acct):
    """
    (str) -> list
    Return list of acct friends got from Twitter API
    """
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    friends = list()
    cursor = -1
    # friends info is got from Twitter in chunks of 200 friends by one request
    # keep sending requests until all friends info is got or request limit is
    # reached
    while cursor:
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '200',
                             'cursor': str(cursor)})
        print('Retrieving:', url)
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()
        js = json.loads(data)
        friends.extend(js['users'])
        cursor = js['next_cursor']
        headers = dict(connection.getheaders())
        print('Remaining', headers['x-rate-limit-remaining'], 'request')

    return friends


def get_info_from_json(friends, fr_number, out_type='file'):
    """
    (list, int, str) -> None
    Writes to file or in the console(depending on the out_type parameter)
    information about first fr_number friends from friends list
    """
    if out_type not in {'file', 'console'}:
        out_type = 'file'
    info = ''
    for i in range(fr_number):
        friend = friends[i]
        info += (f"Name: {friend['name']}\n" +
                 f"Nickname: {friend['screen_name']}\n" +
                 f"Location: {friend['location']}\n" +
                 f"Description: {friend['description']}\n" +
                 f"URL: {friend['url']}\n" +
                 f"Followers number: {friend['followers_count']}\n" +
                 f"Friends number: {friend['friends_count']}\n" +
                 f"Account creation date: {friend['created_at']}\n" +
                 f"Verified: {friend['verified']}\n" +
                 f"Language: {friend['lang']}\n" +
                 f"Status: {friend['status']['text'].strip()}\n" +
                 '=' * 79 + '\n')
    if out_type == 'file':
        with open('friends.txt', 'w', encoding='utf-8') as writefile:
            writefile.write(info)
    elif out_type == 'console':
        print(info)


if __name__ == '__main__':
    acct_name = input('Account name: ')
    friends = get_friends_list(acct_name)
    print(f'{len(friends)} friends were found')
    while True:
        try:
            fr_number = int(input(
                'How many should be displayed?\nFriends number: '))
            output_type = input('Output type(file\console):')
            get_info_from_json(friends, min(fr_number, len(friends)))
            break
        except ValueError as err_msg:
            print(err_msg)
            continue

