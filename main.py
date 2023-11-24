import sys
from time import sleep
from pyautogui import click, hotkey, alert, confirm, write, press
import json

groups_file = sys.argv[1]
json_file = sys.argv[2]

date = "231110"

def fetch_groups(filename):
	with open(filename) as f:
		return ' '.join([ line.strip() for line in f.readlines() ]).strip().split(' ')
#
all_groups = fetch_groups(groups_file)
group_ids = all_groups

def fetch_db(filename)->dict:
	try:
		with open(filename, "r") as f:
			return json.loads(f.read())
	except FileNotFoundError:
		return { group:dict() for group in all_groups }
#
records = fetch_db(json_file)

print(group_ids)
link = "www.facebook.com/groups/"
#
def onShift(key):
	hotkey("shift",key)
def write_url(url):
	url = url.replace('/',':')
	for char in url:
		onShift(char) if char.isdecimal() or char=='.' else write(char)
def post_group(group_id):
	write_url(link+group_id)
	press("enter")
	sleep(7)
	press('p')
	sleep(3) # wait the post form to load
	hotkey("ctrl", 'v')
	sleep(0.5) # wait to lower the "post" button
	#press("tab", presses=8) not good
	click(x=850,y=950)
	#sleep(3) # interval between groups
	status = confirm(
		text="Post status",
		buttons=["Published", "Pending"]
	)
	records[group_id][date] = status
	press("f6")
def execute(groups):
	copy="Wait"
	while copy=="Wait":
		copy = confirm(
		text="Please copy the post to your clipboard and click Done.",
		buttons=["Done", "Wait"]
	)
	# db stuff
	
	# end
	copy = confirm(
		text="Click OK then select Chrome and the operation will start in 5 seconds.",
		buttons=["OK", "Cancel"]
	)
	if copy=="Cancel": return -1
	print("Starting...\nPlease keep Chrome the selected window.")
	sleep(5)
	hotkey('ctrl', 't')
	####
	for group in groups:
		post_group(group)
		#sleep(groups_interval)
	with open(json_file, "w") as f:
		f.write(json.dumps(records, indent=4))
execute(group_ids)
