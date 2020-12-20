- Download datasets from IMDB, they can be found here: https://datasets.imdbws.com/ 
	- These are required:
		- title.basics
		- title.episode
		- title.ratings
	- Unzip the `.gz` files and name the `.tsv` files appropriately if they are not
- Run the script to have it ask you what to search for: `python3 imdb.py`  OR run it with your search query as a parameter:
	- `python3 imdb.py "friends 1994"`
	- `python3 imdb.py tt8111088`

For TV Shows a `.csv` will be created listing the episode number, rating and amount of votes.

For Movies, no `.csv` will be written. It will just write the rating in the prompt.

Use pip to install the natsort package: `pip3 install natsort`

![Screenshot](https://lambdan.se/img/2020-12-20_14-16-24.340.png)
![Screenshot](https://lambdan.se/img/2020-12-20_14-16-24.232.png)
![Screenshot](https://lambdan.se/img/2020-12-20_14-16-24.270.png)
![Screenshot](https://lambdan.se/img/2020-12-20_14-21-31.159.png)