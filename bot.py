import requests
import bs4
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
                home = ""
                away = ""
                for chars in temp[0].contents[0].upper():
                    if(ord(chars)>=65 and ord(chars)<=90):
                        home+=chars
                for chars in temp[1].contents[0].upper():
                    if(ord(chars)>=65 and ord(chars)<=90):
                        away+=chars
                all_match_name.append((f'/{home}vs{away}').replace(" ",""))
                all_match_link.append(link['href'])


        all_matches = dict(zip(all_match_name,all_match_link))


        return all_matches
    except:
        return None

def selected_match(all_matches,user_match_name):
    try:
        all_links = 0
        users_match = requests.get(all_matches[user_match_name])

        all_contents = bs4.BeautifulSoup(users_match.text,'lxml').find_all("tr",attrs={"class":"rounded-pill"})
        all_individual_match_link = []
        for content in all_contents:
            all_links = all_links+1
            all_individual_match_link.append(content.find_all("input")[0]['value'])
            if(all_links>=15):
                break
        return all_individual_match_link
    except:
        return None