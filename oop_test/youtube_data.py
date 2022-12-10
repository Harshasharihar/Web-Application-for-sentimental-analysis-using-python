import requests

class Youtube_data():
    def __init__(self,video_link):
        self.id=video_link.split('=')
        self.id=self.id[1]
        self.API_KEY="AIzaSyD4QhG0HkPsilhSzPBuUVrvuvsRgb0oClk"
        self.parameters={
            "part":"snippet",
            "videoId":self.id,
            "key":self.API_KEY
        }
        self.special_char="@#$%^*><1234567890"
        self.comments_list=[]

    def get_comments(self):
        response = requests.get(url="https://www.googleapis.com/youtube/v3/commentThreads", params=self.parameters)
        print(response)
        number_of_commments = response.json()["items"]
        i = 0
        for items in range(len(number_of_commments)):

            comments = response.json()["items"][i]["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            i += 1
            for letter in self.special_char:
                comments = comments.replace(letter, "")
            self.comments_list.append(comments)
        return self.comments_list