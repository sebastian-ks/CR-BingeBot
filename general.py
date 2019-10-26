import sys
import os

class Methods():
    def restart():
        python = sys.executable
        os.execl(python,python, * sys.argv)

    def season(ep):
        if "Season" not in ep and "Staffel" not in ep:
            return "0"
        else:
            season = ep.split(",")[0]
            season = season.split(" ")[1]
            return season

    def episode(ep):
        if "Season" in ep or "Staffel" in ep:
            return ep.split(", ")[1]
        else:
            return ep

    def episodeCode(ep):
        if "Season" in ep or "Staffel" in ep:
            crunch = ep.split(", ")[1]
        else:
            crunch = ep
        dis = crunch.split(" ")
        return dis[0]+dis[1]

    def print_season(entry):
        ep = entry.split("#")[2]
        sep = ep.split(",")
        if "Season" in ep or "Staffel" in ep:
            seaString = "<b>"+sep[0] + "</b>"+ "    "+sep[1]
        else:
            seaString = "<b>"+ep+"</b>"
        return seaString

    def getSeries_from_url(url):
        if url == "" or url is None:
            return url
        else:
            st = url.split("https://www.crunchyroll.com/",1)[1]
            st = st.split("/episode")[0]
            if "de/" in st:
                st = st.split("/")[1]
            return st

    def url(entry):
        return entry.split("#")[0]

    def getSeries(entry):
        return entry.split("#")[1]

    def getEpisode(entry):
        return entry.split("#")[2]

    def getTitle(entry):
        return entry.split("#")[3]


    def getEpisode_from_url(url):
        if url == "" or url is None:
            return url
        else:
            st = ""
            try:
                area = url.split("episode-",1)[1][:4]
            except IndexError as ie:
                print("url:" + url)
            for i in range(len(area)):
                try:
                    st += str(int(area[i]))
                except ValueError as f:
                    pass
            return st

    def getEpisodeID(url):
        first = 0
        if url == "" or url is None:
            return url
        else:
            st = url[-7:]
            for letter in st:
                try:
                    first = int(letter)
                    first = st.index(letter)
                    break
                except:
                    pass
            newst = st[first:]
            return int(newst)

    def getMugCode(entry):
        epID = Methods.getEpisode(entry)
        series = Methods.getSeries(entry)
        season = Methods.season(epID)
        episode = Methods.episodeCode(epID)
        code = series+season+episode+".jpg"
        return code
