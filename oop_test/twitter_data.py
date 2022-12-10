from requests_oauthlib import OAuth1Session
import scraper
import requests
import json
from selenium import webdriver

class Twitter_data():
    def __init__(self,username):
        self.consumer_key = 'Yk2qAyzL6VTUbxvqftLCC3Svm'
        self.consumer_secret = 'LwWZHIQ3Ga2DSaVi7wtrEE5RTPLuEkFRAlJ99I9ARzZj3XOS6q'
        self.username=username






    def get_id(self):
        params = {"usernames": self.username, "user.fields": "created_at,description"}
        # Get request token
        request_token_url = "https://api.twitter.com/oauth/request_token"
        oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret)

        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print(
                "There may have been an issue with the consumer_key or consumer_secret you entered."
            )

        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")

        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print(authorization_url)
        verifier=scraper.Scraper(url=authorization_url).get_code()
        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=int(verifier),
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

        # Make the request
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

        response = oauth.get(
            "https://api.twitter.com/2/users/by", params=params
        )

        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )



        json_response = response.json()
        return json_response['data'][0]['id']


    def get_tweets(self):
        bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAveTgEAAAAA9kIDvOJkbjm%2BucIdcWwV4GseUS0%3DzYwneiyFdPc4zzf84czY5bCqTxsWkvvvbd8OnK8rnF1gSebJa7'

        def create_url():
            # Replace with user ID below
            user_id = self.get_id()
            return "https://api.twitter.com/2/users/{}/mentions".format(user_id)

        def get_params():
            # Tweet fields are adjustable.
            # Options include:
            # attachments, author_id, context_annotations,
            # conversation_id, created_at, entities, geo, id,
            # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
            # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
            # source, text, and withheld
            return {"tweet.fields": "created_at"}

        def bearer_oauth(r):
            """
            Method required by bearer token authentication.
            """

            r.headers["Authorization"] = f"Bearer {bearer_token}"
            r.headers["User-Agent"] = "v2UserMentionsPython"
            return r

        def connect_to_endpoint(url, params):
            response = requests.request("GET", url, auth=bearer_oauth, params=params)
            print(response.status_code)
            if response.status_code != 200:
                raise Exception(
                    "Request returned an error: {} {}".format(
                        response.status_code, response.text
                    )
                )
            return response.json()

        def main():
            url = create_url()
            params = get_params()
            json_response = connect_to_endpoint(url, params)
            return json.dumps(json_response, indent=4, sort_keys=True)

        final=main()
        return final
