from malaffinity.exceptions import *
from malaffinity import MALAffinity
from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
from string import Template
from datetime import date
import datetime
import time

class Friend(object):
	def __init__(self, name, affinity, shared):
		self.name = name
		self.affinity = affinity
		self.shared = shared

# prompts the user for their username
while True:
	try:
		username = input("What is your username?\n")
		test_open = urlopen("https://myanimelist.net/profile/" + username)
		break
	except URLError:
		print("\nUsername incorrect, try again\n")

urls = []
offset = 0

try:
	while True:
		# makes the url where their friends will appear
		url = "https://myanimelist.net/profile/" + username + "/friends?offset=" + str(offset)
		#Need to go to the next pages if they exist, because this only shows first 100
		test_open = urlopen(url)
		urls.append(url)
		offset += 100
except URLError:
	print(str(offset) + " is the offset")


friends = []

for url in urls:
	# query the website and return the html
	html = urlopen(url)

	# parse the html
	# soup will contain the html of the page
	soup = BeautifulSoup(html, 'html.parser')

	# finds all the things in the strong tag
	# which happen to be the friend names
	friends.extend(soup.find_all('strong'))

# number of friends
print(str(len(friends)) + " friends")

#list to hold the friend objects
friend_list = []

ma = MALAffinity(username)
for friend in friends:
	friend_name = friend.string
	# because the API will only let you calculate affinity every 2 seconds.
	time.sleep(2)
	shared = 0
	try:
		affinity, shared = ma.calculate_affinity(friend_name)
	except NoAffinityError:
		affinity = 0
	except InvalidUsernameError:
		affinity, shared = 0, 0
	f = Friend(friend_name, affinity, shared)
	friend_list.append(f)
	print(f.name)
	
#sort based on affinity	
friend_list.sort(key=lambda x: x.affinity, reverse=True)

filename = username + ".txt"

#gets the date
current_time = datetime.datetime.now().strftime("%m-%d-%y %H:%M")

separator = "\n--------------------------------------------------------------------------------------------------\n"

file = open(filename, "a+")

file.write(username + "\n")
file.write(current_time + "\n")
file.write(separator)

for i in range(len(friend_list)):
	friend = friend_list[i]
	s = ' ' * 10
	#string = Template('$num $name' + s + '$affinity%' + s + '$shared').substitute(num=i, name=friend.name, affinity=friend.affinity, shared=friend.shared)
	string = '{:<4}{:<30}{:<30}{:>10}'.format(i+1, friend.name, friend.affinity, friend.shared)
	file.write(string)
	file.write(separator)
# write and close the file
file.write("\n")
file.close()