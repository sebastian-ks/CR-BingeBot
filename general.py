import sys
import os

class Methods():

    activeWindow = "main"
    skipTimer = True
    stne = False

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

    def print_series(entry):
        series = Methods.getSeries(entry)
        if len(series) > 27:
            splitted = series.split(" ")
            firstline = ""
            secondline = ""
            for i in range(len(splitted)-1):
                firstline = firstline + splitted[i]+" "
            return firstline+"<br>"+splitted[-1]
        else:
            return series

    def print_season(entry):
        ep = entry.split("#")[2]
        sep = ep.split(",")
        if "Season" in ep or "Staffel" in ep:
            seaString = "<b>"+sep[0] + "</b>"+ "    "+sep[1]
        else:
            seaString = "<b>"+ep+"</b>"
        return seaString

    def print_episodeTitle(entry):
        title = Methods.getTitle(entry)
        if len(title) > 52:
            fit = title[0:48]
            title = fit + "...\""
        return title


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

    def manageMugs():
        mugDir = "assets\\mugs"
        if not os.path.exists(mugDir):
            os.mkdir(mugDir)
        else:
            file = open("progress.txt", "r")
            episodes = file.readlines()
            if episodes:
                newestSeries = Methods.getSeries(episodes[-1])
                topMug = Methods.getMugCode(episodes[-1])
                for mug in os.listdir(mugDir):
                    if mug != topMug:
                        if Methods.getSeries_from_mug_code(mug) == newestSeries:
                            os.remove(mugDir+"\\"+mug)


    def getMugCode(entry):
        epID = Methods.getEpisode(entry)
        series = Methods.getSeries(entry)
        season = Methods.season(epID)
        episode = Methods.episodeCode(epID)
        if "?" in series:
            series = series.replace("?","_;")
        code = series+"#"+season+episode+".jpg"
        return code

    def getSeries_from_mug_code(code):
        return code.split("#")[0]

    def getHotkey():
        file = open("settings","r")
        hotkeySettings = file.readlines()[0]
        return hotkeySettings.split(":")[1]

    def setHotkey(hk):
        file = open("settings","r+")
        lines = file.readlines()
        lines[0] = "HK:"+hk+"\n"
        file.close()
        os.remove("settings")
        open("settings", "a+").writelines(lines)

    def setTimerSettings(bool):
        file = open("settings","r+")
        lines = file.readlines()
        lines[2] = "SkipTimer:"+str(bool)+"\n"
        file.close()
        os.remove("settings")
        open("settings", "a+" ).writelines(lines)

    def setStneSettings(bool):
        file = open("settings","r")
        lines = file.readlines()
        lines[1] = "Shortcut:"+str(bool)+"\n"
        file.close()
        os.remove("settings")
        open("settings", "a+" ).writelines(lines)

    def getSettings():
        file = open("settings","r" )
        lines = file.readlines()
        file.close()
        if lines[1].split(":")[1] == "True\n":
            Methods.stne = True
        else:
            Methods.stne = False

        if lines[2].split(":")[1] == "True\n":
            Methods.skipTimer = True
        else:
            Methods.skipTimer = False
