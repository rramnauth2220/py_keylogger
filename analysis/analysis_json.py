# author:       Rebecca Ramnauth
# last update:  4 March 2020

from datetime import datetime
import json
import matplotlib.pyplot as plt
import numpy as np

def reaction_rate(items, sender):
    other_last_sent = 0
    reaction_sum = 0
    for item in items[1:]:
        if item.get('sender_name') != sender:
            other_last_sent = item.get('timestamp_ms')
            #print(item.get('sender_name'), other_last_sent)
        else:
            reaction_sum += abs(other_last_sent - item.get('timestamp_ms'))
    #print("reaction sum = ", reaction_sum, "; queries = ", len(items), "rate = ", reaction_sum/len(items))
    return reaction_sum / len(items)

# incorrect measure of typing speed --
    # calculates time distance between current msg and previous msg sent
    # divided by the length of the current msg
    # divided by 1000 to convert milliseconds to seconds
# return typing speed of @sender in characters per second
def get_typing_speed(messages, sender):
    speed_sum = 0
    items = filter_messages_by_sender(messages, sender)
    timestamp_prev = items[0].get('timestamp_ms')
    for item in items:
        time_difference = timestamp_prev - item.get('timestamp_ms')
        timestamp_prev = item.get('timestamp_ms')
        average_time = float(time_difference) / len(item.get('content'))
        speed_sum += average_time
    return speed_sum / len(items) / 1000

def filter_messages_by_sender(items, sender):
    filtered = []
    for item in items:
        if item.get('sender_name') == sender:
            filtered.append(item)
    return filtered

def test_plot():
    fig = plt.figure()  # an empty figure with no axes
    fig.suptitle('No axes on this figure')  # Add a title so we know which it is

    fig, ax_lst = plt.subplots(2, 2)

def main():
    with open('run_1.json', 'r') as f:
        messages_dict = json.load(f)

    messages = messages_dict.get('messages')
    timespent_content = []

    timestamp_prev = messages[0].get('timestamp_ms')
    for message in messages:
        content = message.get('content')
        sender = message.get('sender_name')
        difference = timestamp_prev - message.get('timestamp_ms')
        timestamp_prev = message.get('timestamp_ms')
        timespent_content.append([difference, content, sender])
    # print(difference, content, sender)

    #print("typing speed: ", get_typing_speed(messages, 'Bfl Participant'))
    print(reaction_rate(messages, 'Bfl Human'))
    #test_plot()

# print("reaction rate: ", get_reaction_rate(messages, 'Bfl Participant'))

if __name__ == "__main__":
    main()