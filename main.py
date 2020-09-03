import requests, pandas
from bs4 import BeautifulSoup

def scrap(w):
    c = w.content
    soup = BeautifulSoup(c, "html.parser")
    #print(soup.prettify())
    tit = soup.find("title").text
    det = soup.find_all("td", {"class":"titleColumn"})
    rat = soup.find_all("td", {"class":"ratingColumn imdbRating"})
    #print(tit)
    #print(len(det))
    #print(len(rat))
    
    l = []
    for i in range(len(det)):
        d = {}
        a = det[i].text.strip()
        x = a[:a.index(".")]
        y = a[a.index(".") + 1:-6].strip()
        z = a[-5:-1]
        r = rat[i].text.strip()
        #print(x, y, z, r)
        d["Rank"] = x
        d["Title"] = y
        d["Year"] = z
        d["Rating"] = r
        l.append(d)

    df = pandas.DataFrame(l)
    print(df)
    fn = tit + ".csv"
    df.to_csv(fn)
    print("\n" + fn + " Exported\n")
    print("-" * 60 + "\n")


r = requests.get("https://www.imdb.com/chart/top/")
scrap(r)

r = requests.get("https://www.imdb.com/chart/toptv/")
scrap(r)