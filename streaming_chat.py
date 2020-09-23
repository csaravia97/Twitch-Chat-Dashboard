import sys
import socket
import constants
import logging
import re
import yaml
from time import time
from datetime import datetime
from collections import defaultdict, Counter
from os import listdir


# Pull from constants file so certain information isn't public
server = constants.server
port = constants.port
token = constants.token
nickname = constants.nickname

def stream_twitch_chat(channel, file):
    # instantiate a socket and connect it Twitch
    sock = socket.socket()
    sock.connect((server, port))

    # send auth token, username, and desired channel to connect to over socket
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN #{channel}\n".encode('utf-8'))

    # logger to write messages to file
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler(file, encoding='utf-8')])


    # continuously write messages to file
    while True:
        resp = sock.recv(2048).decode('utf-8')

        # send response to verify that we're still using this connection
        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif len(resp) > 0:
            logging.info(resp)

    sock.close()

# extract important parts of each message
def extract_message_data(msg):
    message_parts = msg.split('—')
    time_part = message_parts[0].strip()
    chat_part = message_parts[1].strip()

    time_logged = datetime.strptime(time_part, '%Y-%m-%d_%H:%M:%S')
    username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)',chat_part).groups()
    d = {
        'time': time_logged,
        'channel': channel,
        'username': username,
        'message': message
    }
    return d

# For each message in chat log, get message data
def extract_chat_data(file):
    chat_data = []

    with open(file, 'r', encoding='utf-8') as chat_logs:
        messages = chat_logs.read().split('\n\n\n')
        
        for message in messages:
            try:
                msg_data = extract_message_data(message)
                chat_data.append(msg_data)
            except:
                pass

    return chat_data


def combine_chat_logs(logs):
    combined_logs = []
    for chat_log in logs:
        chat_data = extract_chat_data(chat_log)
        combined_logs += chat_data
    return combined_logs


# Check if the word is in the given emote set
def check_membership(word, emote_set):
    for key in emote_set:
        if word in emote_set[key]:
            return 1
    return 0 


# Count the number of emotes, given chat data
def emote_count(chat_data, emotes):
    emote_freq = defaultdict(int)
    for message in chat_data:
        message_data = message['message'].split(' ')
        channel = message['channel']
        for word in message_data:
            is_emote = check_membership(word, emotes[channel]) or check_membership(word, emotes['global'])
            if is_emote:
                emote_freq[word] += 1
    else:
        return emote_freq

def emote_count_message(channel, message , emotes):
    emote_freq = defaultdict(int)
    message_data = message.split(' ')
    for word in message_data:
        is_emote = check_membership(word, emotes[channel]) or check_membership(word, emotes['global'])
        if is_emote:
            emote_freq[word] += 1
    return Counter(emote_freq)

# if __name__ == "__main__":
#     chat_logs = listdir('./Chat Logs/')
#     chat_logs = ['./Chat Logs/' + file for file in chat_logs]
#     chat_data = combine_chat_logs(chat_logs)  
#     with open("emotes.yaml", 'r') as stream:
#         emotes = yaml.safe_load(stream)
#     start = time()
#     xd = emote_count(chat_data, emotes)
#     print(time() - start)
# stream_twitch_chat(sys.argv[1], sys.argv[2])