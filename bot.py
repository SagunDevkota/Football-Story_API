import requests
import bs4
from flask import Flask
import json
import re

app = Flask(__name__)
all_matches = dict()
@app.route("/all_matches_name")
def all_matches_name():
    try: 
        res = requests.get("https://totalsportek.pro/")

        soup = bs4.BeautifulSoup(res.text,'lxml').find_all('div',attrs={"class":"div-main-box"})

        all_match_link = []
        all_match_name = []
        for league in soup:
            links = league.find_all("a")
            for link in links:
                temp = link.find_all("span",attrs={"class":"mt-2"})
                all_match_name.append((f'{temp[0].contents[0]} vs {temp[1].contents[0]}').replace(" "," "))
                all_match_link.append(link['href'])
                all_matches = dict(zip(all_match_name,all_match_link))
        return json.dumps(all_matches, indent = 4)
    except:
        return {}
@app.route("/selected_match/<user_match_name>")
def selected_match(user_match_name):
    all_matches = json.loads(all_matches_name())
    users_match = requests.get(all_matches[user_match_name])
    all_contents = bs4.BeautifulSoup(users_match.text,'lxml').find_all("tr",attrs={"class":"rounded-pill"})
    all_individual_match_link = {}
    valid_links = ["http://soccermotor.com","http://dailysportsexpress.blogspot.com","http://mazystreams.xyz/","https://mazystreams.xyz/","http://allsportsmedia.live"]
    i=0
    for content in all_contents:
        for links in valid_links:
            if(links in content.find_all("input")[0]['value']):
                all_individual_match_link[i] = content.find_all("input")[0]['value']
                i=i+1
    #print(all_individual_match_link)
    return all_individual_match_link
    #return {"0":"http://soccermotor.com/watford-vs-liverpool-highlights-16-october-2021/"}
@app.route("/soccermotor/<path:link>")
def link_soccermotor(link):
    res = requests.get(link)
    pattern = ".m3u8"
    match = re.compile(r'\b' + r'\S*' + re.escape(pattern) +'\S*')
    soup = bs4.BeautifulSoup(res.text,'lxml')
    if(len(match.findall(str(soup))) == 0):
        soup = soup.find_all('iframe',attrs={"src":re.compile(r"\b"+"://mazystreams.xyz/*")})
        link = soup[0]["src"]
        res = requests.get(link)
        soup = bs4.BeautifulSoup(res.text,'lxml')

    m3u8_link = match.findall(str(soup))[0][:-2]
    return m3u8_link    #return 'https://hg-n2.dotice.me/plyvivo/30noxuxapiy03uhilu3e/chunklist.m3u8'
if __name__ == '__main__':
   app.run(host="0.0.0.0")