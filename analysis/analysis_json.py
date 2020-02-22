# author:       Rebecca Ramnauth
# last update:  07 January 2020

from datetime import datetime
import json

def reaction_rate(items, sender):
	other_last_sent = 0
	reaction_sum = 0
	for item in items:
		print (item.get('sender_name'))
		if item.get('sender_name') != sender:
			other_last_sent = item.get('timestamp_ms')
		else:
			reaction_sum += other_last_sent - item.get('timestamp_ms')
			#print(item.get('sender_name'), "time to react: ", react_time, " to message ", item.get('content'))
	return reaction_sum/len(items)

def get_typing_speed(items):
	speed_sum = 0
	timestamp_prev = items[0].get('timestamp_ms')
	for item in items:
		time_difference = timestamp_prev - item.get('timestamp_ms')
		timestamp_prev = item.get('timestamp_ms')
		average_time = float(time_difference)/len(item.get('content'))
		speed_sum += average_time
	return speed_sum/len(items)

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
		#print(difference, content, sender)
		
	#print("typing speed: ", get_typing_speed(messages))
	print(reaction_rate(messages, 'Bfl Participant'))
	#print("reaction rate: ", get_reaction_rate(messages, 'Bfl Participant'))

if __name__== "__main__":
	main()
	#print(datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'))