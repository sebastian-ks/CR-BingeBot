
class Methods():
    def getSeries(url):
        if url == "" or url is None:
            return url
        else:
            print()
            st = url.split("https://www.crunchyroll.com/",1)[1]
            st = st.split("/episode")[0]
            if "de/" in st:
                st = st.split("/")[1]
            return st

    def getEpisode(url):
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
