import time, requests, pandas
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from sty import fg, bg, rs


BASE_URL = "https://www.imdb.com/title/tvShowImdbId/episodes/?season="

def mainMethod():
	for id in TV_SHOW_LIST:
		fullData = scrap(id)
		transposedFullData = transposeData(fullData)
		table = PrettyTable(transposedFullData[0], title=fullData[0]["title"])
		table.add_rows(transposedFullData[1:])
		print(table)
		print()

def getSoupData(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
	r = requests.get(url, headers=headers)
	return BeautifulSoup(r.content, "html.parser")

def scrap(tvShowImdbId):
	soup = getSoupData(BASE_URL.replace("tvShowImdbId", tvShowImdbId) + "1")
	# print(soup.prettify())
	title = soup.find("title").text.split(" - ")[0]
	print("Title - " + title)
	seasons = soup.find_all("a", {"data-testid":"tab-season-entry"})
	fullData = []
	i = 0
	while i < len(seasons):
		i += 1
		if i != 1:
			soup = getSoupData(BASE_URL.replace("tvShowImdbId", tvShowImdbId) + str(i))
		episodeNumberList = [t.text for t in soup.find_all("div", {"class":"ipc-title__text"})]
		episodeDescriptionList = [t.text for t in soup.find_all("div", {"class":"ipc-html-content-inner-div"})]
		episodeRatingList = [t.text for t in soup.find_all("span", {"class":"ipc-rating-star--rating"})]
		episodeVoteCountList = [t.text[2:-1] for t in soup.find_all("span", {"class":"ipc-rating-star--voteCount"})]
		if any(not lst for lst in [episodeNumberList, episodeDescriptionList, episodeRatingList, episodeVoteCountList]):
			break
		season = {
			"title": title,
			"episodeNumberList": episodeNumberList,
			# "episodeDescriptionList": episodeDescriptionList,
			"episodeRatingList": episodeRatingList,
			"episodeVoteCountList": episodeVoteCountList,
			"length": len(episodeNumberList)
		}
		fullData += [season]
		print("Season - " + f"S{i:02}")
	# print(fullData)
	return fullData

def transposeData(fullData):
	lengthOfColumn = max([i["length"] for i in fullData])
	transposedData = [[""] + [f"S{(i + 1):02}" for i in range(len(fullData))]]
	for i in range(lengthOfColumn):
		episodeRow = [f"E{(i + 1):02}"]
		for j in range(len(fullData)):
			if i >= fullData[j]["length"] or i >= len(fullData[j]["episodeRatingList"]):
				episodeRow += [""]
			else:
				episodeRow += [getColoredRating(fullData[j]["episodeRatingList"][i])]
		transposedData += [episodeRow]
	return transposedData

def getColoredRating(rating):
	if float(rating) >= 9.5:
		return getStyColoredText(rating, "#084430", "#FFFFFF")
	elif float(rating) >= 9:
		return getStyColoredText(rating, "#065C40", "#FFFFFF")
	elif float(rating) >= 8:
		return getStyColoredText(rating, "#0c9d6a", "#000000")
	elif float(rating) >= 7:
		return getStyColoredText(rating, "#a2cc2e", "#000000")
	elif float(rating) >= 6:
		return getStyColoredText(rating, "#c1cc24", "#FFFFFF")
	elif float(rating) >= 5:
		return getStyColoredText(rating, "#cc9724", "#FFFFFF")
	elif float(rating) >= 4:
		return getStyColoredText(rating, "#ca2b2b", "#FFFFFF")
	return getStyColoredText(rating, "#662e7a", "#000000")

def getStyColoredText(text, bgHex="#000000", fgHex="#FFFFFF"):
	r_bg, g_bg, b_bg = hex_to_rgb(bgHex)
	r_fg, g_fg, b_fg = hex_to_rgb(fgHex)
	return f"{fg(r_fg, g_fg, b_fg)}{bg(r_bg, g_bg, b_bg)} {text} {rs.fg}{rs.bg}"

def hex_to_rgb(hex_color):
	hex_color = hex_color.lstrip("#")
	if len(hex_color) != 6:
		raise ValueError("Hex color must be in the format RRGGBB")
	return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# TV_SHOW_LIST = ["tt0944947", "tt2560140", "tt0412142"]
TV_SHOW_LIST = ["tt7587890"]
# TV_SHOW_LIST = ["tt7366338"]

if __name__ == '__main__':
	print("START!!!")
	mainMethod()
	print("END!!!")
