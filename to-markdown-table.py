import json
import pytz
from datetime import datetime

zone='US/Central'
tz = pytz.timezone(zone)

interesting=set([
	# https://www.chiefdelphi.com/t/reefscape-matches-to-watch-out-for-at-houston/499561/6
	'2025arc_qm116',
	'2025cur_qm1',
	'2025cur_qm23',
	'2025cur_qm50',
	'2025cur_qm65',
	'2025cur_qm84',
	'2025cur_qm99',
	'2025cur_qm103',
	'2025cur_qm106',
	'2025cur_qm121',
	'2025cur_qm123',
	'2025hop_qm73',
	'2025hop_qm99',
	'2025mil_qm38',
	'2025mil_qm102',
	'2025new_qm42',
	'2025new_qm75',
	'2025new_qm86',
	'2025new_qm115',
	'2025cur_qm23',
	'2025cur_qm40',
	'2025cur_qm65',
	'2025cur_qm78',
	'2025cur_qm85',
	'2025cur_qm99',
	'2025cur_qm110',
	'2025cur_qm121',
	'2025dal_qm1',
	'2025mil_qm112',
	'2025new_qm13',
	'2025new_qm39',
	'2025new_qm42',
	'2025new_qm46',
	'2025new_qm86',
	'2025new_qm92',
	'2025new_qm101',
	'2025new_qm115',
])

allMatches=[]

highScore=0
highCombinedScore=0

for event in ['2025cur','2025new','2025dal','2025joh','2025arc','2025gal','2025hop','2025mil']:
	info = json.load(open(f'data/{event}.event.json'))
	division = info['short_name']
	stream = info['webcasts'][0]['channel']
	matches = json.load(open(f'data/{event}.matches.json'))
	for match in matches:
		match['stream'] = stream
		match['division'] = division
		match['time'] = match['actual_time'] or match['predicted_time']
		match['red'] = " ".join([s.replace("frc","") for s in match['alliances']['red']['team_keys']])
		match['blue'] = " ".join([s.replace("frc","") for s in match['alliances']['blue']['team_keys']])
		dt=datetime.fromtimestamp(match['time'], tz)
		match['mdTime'] = f'[date={dt.strftime("%Y-%m-%d")} time={dt.strftime("%H:%M")} format="LLLL" timezone="{zone}"]'
		allMatches.append(match)
		maxScore = max(match["alliances"]["red"]["score"], match["alliances"]["blue"]["score"])
		combinedScore = match["alliances"]["red"]["score"] + match["alliances"]["blue"]["score"]
		if (maxScore>highScore):
			highScore=maxScore
		if (combinedScore>highCombinedScore):
			highCombinedScore=combinedScore

allMatches.sort(key=lambda x: x['time'])

print('| Match | Result | Red | Blue |')
print('| --- | --- | --- | --- |')
for match in allMatches:
	if match['actual_time']:
		link = f'[{match["division"]} {match['comp_level']}{match["match_number"]}](https://www.thebluealliance.com/match/{match["key"]})'
		scores = f'{match["alliances"]["red"]["score"]} to {match["alliances"]["blue"]["score"]}'
		maxScore = max(match["alliances"]["red"]["score"], match["alliances"]["blue"]["score"])
		combinedScore = match["alliances"]["red"]["score"] + match["alliances"]["blue"]["score"]
		if (maxScore == highScore):
			scores = f"High Score: {scores}"
			interesting.add(match['key'])
		if (combinedScore == highCombinedScore):
			scores = f"High combined Score: {scores}"
			interesting.add(match['key'])
	else:
		link = f'[{match["division"]}](https://www.twitch.tv/{match["stream"]}) {match['comp_level']}{match["match_number"]}'
		scores = ''

	if match['key'] in interesting:
		print(f'| {link} | {scores or match["mdTime"]} | {match["red"]} | {match["blue"]} |')

