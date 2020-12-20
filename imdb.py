import os, sys
from operator import itemgetter
from natsort import natsorted
from datetime import datetime

# Get these from https://datasets.imdbws.com/ 
# TODO maybe automatically download them?
title_basics_file = "./title_basics.tsv"
ratings_file = "./ratings.tsv"
episodes_file = "./title_episode.tsv"

if not os.path.isfile(title_basics_file):
	print(title_basics_file, "not found")
	sys.exit(1)
if not os.path.isfile(ratings_file):
	print(ratings_file, "not found")
	sys.exit(1)
if not os.path.isfile(episodes_file):
	print(episodes_file, "not found")
	sys.exit(1)


def find_rating(titleID):
	with open(ratings_file, encoding="utf8") as f:
		lines = f.readlines()
	for l in lines:
		if titleID.lower() in l.lower():
			rating = l.split("\t")[1].rstrip()
			votes = l.split("\t")[2].rstrip()
			return {"rating": rating, "votes": votes}
	return False

def find_episodes(parentID):
	with open(episodes_file, encoding="utf8") as f:
		lines = f.readlines()
	episodes = []
	for l in lines:
		if parentID == l.split("\t")[1]: # 1 is parent ID
			episodes.append({ "id": l.split("\t")[0].rstrip(), "season": l.split("\t")[2].rstrip(), "episode": l.split("\t")[3].rstrip() }) # 0 is episode ID, 2 is season, 3 is episode number
	
	# sort https://stackoverflow.com/a/16082979
	s = natsorted(episodes, key=itemgetter('season', 'episode'))
	return s

def sxxeyy(s, e):
	return "S" +  str(s.zfill(2)) + "E" + str(e.zfill(2))

def write_csv(filename, episode, rating, votes):
	if not os.path.isfile(filename):
		csvf = open(filename,"w")
		csvf.write("Episode,Rating,Votes\n")
		csvf.close()

	with open(filename, "a") as csvf:
		csvf.write(episode + "," + str(rating) + "," + str(votes) + "\n")

def search_fuzzy(line, query):
	for word in query.split():
		if word.lower() not in line.lower():
			return False
	return True



if len(sys.argv) > 1:
	search_show = sys.argv[1].rstrip()
else:
	search_show = input("Enter name of movie/tv show: ").rstrip()
#print("Searching: ", search_show)

with open(title_basics_file, encoding="utf8") as f:
	lines = f.readlines()

matches = []

for l in lines:
	if search_fuzzy(l, search_show):
		titleID = l.split("\t")[0].rstrip()
		kind = l.split("\t")[1].rstrip()
		name = l.split("\t")[2].rstrip()
		year = l.split("\t")[5].rstrip()
		if year == "\\N":
			continue # no year means its in development or not released etc
		if kind == "tvSeries" or kind == "movie":
			matches.append({"id": titleID, "kind": kind, "name": name, "year": year})
			#print("Found match:", name, year, kind)
		#if titleID == search_show or name == search_show: # instant match?
		#	print("Perfect match")
		#	matches = [{"id": titleID, "kind": kind, "name": name, "year": year}]
		#	break
	if len(matches) > 50:
		print("More than 50 matches... try to be more specific")
		sys.exit(1)


if len(matches) == 1:
	picked = matches[0]
elif len(matches) > 0:
	#print("*********")
	i = 0
	for match in matches:
		print(i, "-", match["name"], "(" + str(match["year"]) + ")","[" + str(match["kind"]) + "]", "[" + str(match["id"]) + "]")
		i += 1

	pick = int(input("Pick a number: "))
	if pick >= 0 and pick <= i:
		picked = matches[pick]
else:
	print("Didnt find any matches")
	sys.exit(1)

#print("*********")
print()
print(picked["name"], "(" + str(picked["year"]) + ")")
print("https://www.imdb.com/title/" + picked["id"] + "/")
print()

csv_filename = picked["name"] + "-" + str(datetime.today().strftime('%Y%m%d-%H%M%S')) + ".csv"

if picked["kind"]  == "movie":
	rating_data = find_rating(picked["id"])
	if rating_data:
		print("Rating:", rating_data["rating"], "(" + str(rating_data["votes"]) + " votes)")
	else:
		print("No rating found")
elif picked["kind"] == "tvSeries":
	episodes = find_episodes(picked["id"])
	for ep in episodes:
		rating_data = find_rating(ep["id"])

		if rating_data:
			print(sxxeyy(ep["season"], ep["episode"]), rating_data["rating"], "(" + str(rating_data["votes"]) + " votes)")
			write_csv(csv_filename, sxxeyy(ep["season"], ep["episode"]), rating_data["rating"], rating_data["votes"])


print()