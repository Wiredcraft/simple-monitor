import json
import os
import requests
from os import listdir


default_config = {
    "description": "Description",
    "url": "",
    "method": "POST",
    "body": "",  # exists only if method is POST
    "headers": {},
    "timeout": 5,
    "code": 200,
    "text": "",
    "slack_notify": "https://wiredcraft.slack.com/services/hooks/slackbot?token=4qNSl8UdnaipTg2f36ZnoEU1&channel=song_for_testing",
}


def notify(msg, url, description=None):
    '''
    Send message to Notification channel
    '''
    print msg
    if description: 
        msg = "[%s] %s" % (description, msg)
    result = requests.post(url, data=msg.encode("utf-8"))
    if result.status_code != 200:
        print "Notification fail!"


def get_config(config_file):
    '''
    Load web checks from config file
    '''
    try:
        with open(config_file) as c:
            config = json.load(c)
    except Exception as e:
        print "Config can not be parsed correctly: %s" % e
        raise

    return config


def handle_config(config):
    '''
    Set defaults of each web check
    '''
    for attr in ('timeout', 'code', 'slack_notify', 'headers'):
        config.setdefault(attr, default_config[attr])

    return config


def health_check(config):
    '''
    Perform the monitoring check
    '''
    print 'Start check: %s - %s' % (config.get('description'), config.get('url'))
    try:
        if config['method'] == "GET":
            result = requests.get(
                config['url'],
                headers = config['headers'],
                timeout = float(config['timeout']),
            )
        elif config['method'] == "POST":
            result = requests.post(
                config['url'],
                data = json.dumps(config['body']),
                headers = config['headers'],
                timeout = float(config['timeout']),
            )
        elif config['method'] == "PUT":
            result = requests.put(
                config['url'],
                headers = config['headers'],
                timeout = float(config['timeout']),
            )
        elif config['method'] == "DEL":
            result = requests.delete(
                config['url'],
                headers = config['headers'],
                timeout = float(config['timeout']),
            )
        else:
            notify(
                "Service %s method is %s, only POST/GET/DEL/PUT are supported" % (
                    config['url'],
                    config['method']
                ),
                config['slack_notify'],
                config.get('description')
            )
            return

    except requests.exceptions.Timeout:
        notify(u"Service %s timeout" % config['url'], config['slack_notify'], config.get('description'))
        return

    except requests.exceptions.ConnectionError:
        notify(u"Service %s can not be connected" % config['url'], config['slack_notify'], config.get('description'))
        return

    if result.status_code != config['code'] or result.text != config['text']:
        msg = u"Service %s return code is %s, expect: %s,\n" \
        u"return text is %s, expect: %s" % (
            config['url'], result.status_code, config['code'],
            result.text, config['text']
        )
        notify(msg, config['slack_notify'], config.get('description'))
    return


def main():
    for filename in listdir('./checks'):
        _, file_extension = os.path.splitext(filename)
        if file_extension == '.conf':
            read_config = get_config(filename)
            if not read_config:
                raise IOError
            config = handle_config(read_config)
            health_check(config)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print e
        notify('Error while running monitor check. Check logs.', default_config.get('slack_notify'))
