from flask import Flask, render_template,request,redirect,url_for, json
from sentimental_analyser import Sentimental_analyser as senti

from youtube_data import Youtube_data as youtube1
from requests_oauthlib import OAuth1Session
import requests
import pandas
import datetime


# ////////////////////////////////////////////////////////////////////////////
settings_data=pandas.read_csv('csv files/settings.csv')
settings_data=settings_data.to_dict(orient="records")

contact_data=pandas.read_csv('csv files/contact.csv')
contact_data=contact_data.to_dict(orient='records')

login=False

# ////////////////////////////////////////////////////////////////////////////
# w_u_t_r
def password_generator():
    symbols=['.','_|','|_|','|_',']','[]','[','-|','|-|','|-']
    time = datetime.datetime.now().date()




data={
            'negative':[],
            'positive':[],
            'neutral':[]
        }
from selenium import webdriver
CHROME_DERIVER = "/home/harsha/Desktop/oop_test/chromedriver"

# Twitter Data collection
# ////////////////////////////////////////////////////////////////////////////

# Selenium bot
def get_code(url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path=CHROME_DERIVER ,options = options)
    # , options = options
    driver.get(url)
    username = driver.find_element_by_id('username_or_email')
    password = driver.find_element_by_id('password')
    button = driver.find_element_by_id('allow')
    username.send_keys('mudholsrirang')
    password.send_keys('Warking@18')
    button.click()
    code = driver.find_element_by_xpath('//*[@id="oauth_pin"]/p/kbd/code')
    code = code.text

    print(type(code))
    driver.quit()

    return code

def get_id(username):
    consumer_key = 'Yk2qAyzL6VTUbxvqftLCC3Svm'
    consumer_secret = 'LwWZHIQ3Ga2DSaVi7wtrEE5RTPLuEkFRAlJ99I9ARzZj3XOS6q'

    params = {"usernames": username, "user.fields": "created_at,description"}
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

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
    verifier=get_code(url=authorization_url)
    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
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

def get_tweets(username):
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAveTgEAAAAA9kIDvOJkbjm%2BucIdcWwV4GseUS0%3DzYwneiyFdPc4zzf84czY5bCqTxsWkvvvbd8OnK8rnF1gSebJa7'

    def create_url():
        # Replace with user ID below
        user_id = get_id(username)
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
        return json_response

    final=main()
    return final
# ////////////////////////////////////////////////////////////////////////////


# Backend flask


app = Flask(__name__)\

Twitter_data={
            'negative':0,
            'positive':0,
            'neutral':0
        }
Youtube_data={
            'negative':0,
            'positive':0,
            'neutral':0
        }
# ////////////////////////////////////////////////////////////////////////////
# home page
# ////////////////////////////////////////////////////////////////////////////

@app.route("/")
def home():
    global login
    login = False
    return render_template("index.html")

@app.route("/",methods=['POST'])
def home_contact_form():
    text=request.form['text']
    print(text)
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone_no']
    message = request.form['text']
    contact_data=[{'name':username,'email':email,'phone':phone,'message':message}]
    z=pandas.DataFrame(contact_data)
    z.to_csv('csv files/contact.csv',mode='a',index=False,header=False)
    return render_template("index.html")

@app.route("/tryit",methods=['POST'])
def tryit_form():
    text = request.form['text']
    print('yesss')
    print(text)
    if text!="":
        x=senti.single_sentence(data=text)
        if x=='Positive':
            y='success'
        elif x=='Negative':
            y='danger'
        elif x=="Neutral":
            y='info'

        x=[f'\n{text} --{x} ']
        print(x)
    else:
        x=[]
        y=''

    return render_template("index.html",tryit_data=x,y=y)


@app.route("/tryit2",methods=['POST'])
def tryit_form2():
    text = request.form['NLP']
    print('yesss')
    print(text)
    if text!="":
        x=senti.nlp_algo_single(data=text)
        if x=='Positive':
            y='success'
        elif x=='Negative':
            y='danger'
        elif x=="Neutral":
            y='info'

        x=[f'\n{text} --{x} ']
        print(x)
    else:
        x=[]
        y=''

    return render_template("index.html",tryit_data=x,y=y)


# ////////////////////////////////////////////////////////////////////////////

# twitter service
# ////////////////////////////////////////////////////////////////////////////

@app.route('/twitter_form')
def twitter():
    if settings_data[0]['check1']==1:
        return render_template('twitter_form.html',data=Twitter_data)
    else:
        return 'site is currently under maintenance'

@app.route('/twitter_form', methods=['POST'])
def my_form():
    global data

    text = request.form['text']
    twitter_data2=get_tweets(username=text)
    print(twitter_data2)
    new_data=[n['text'] for n in twitter_data2['data']]
    data_id=[n['id'] for n in twitter_data2['data']]
    result=senti.sentiment_of_list(data=new_data)
    data = {
        'negative': result['negative'],
        'positive': result['positive'],
        'neutral': result['neutral']
    }
    print(result)
    Twitter_data = {
        'negative': len(result['negative']),
        'positive':len(result['positive']),
        'neutral': len(result['neutral'])
    }
    # Display_list = json.dumps([Twitter_data['negative'], Twitter_data['negative'], Twitter_data['negative']])
    z=[10.0, 18.0, 3.0]

    return render_template('twitter_form.html', data=Twitter_data,data2=json.dumps(z,default='default'))

# ////////////////////////////////////////////////////////////////////////////
# youtube service
# ///////////////////////////////////////////////////////////////////////////

@app.route('/youtube_form')
def youtube():
    if settings_data[0]['check2']==1:
        return render_template('youtube_form.html',data=Youtube_data)
    else:
        return 'site is currently under maintenance'


@app.route('/youtube_form',methods=['POST'])
def youtube_form_2():
    global data

    text=request.form['text']
    print(text)
    youtube_data=youtube1(video_link=text).get_comments()
    print(youtube_data)
    result2 = senti.sentiment_of_list(data=youtube_data)
    data={
        'negative': result2['negative'],
        'positive':result2['positive'],
        'neutral': result2['neutral']
    }
    Youtube_data = {
        'negative': len(result2['negative']),
        'positive':len(result2['positive']),
        'neutral': len(result2['neutral'])
    }


    return render_template('youtube_form.html', data=Youtube_data)

# ////////////////////////////////////////////////////////////////////////////
# Results
# ////////////////////////////////////////////////////////////////////////////

@app.route('/results')
def results(result_type):
    if result_type==1:
        x='Positive'
    elif result_type==2:
        x='Negative'
    elif result_type==3:
        x="Neutral"
    return render_template('results.html',show_type=x)


@app.route('/results_positive')
def positive():
    x = 'Positive'
    y='success'
    z = data['positive']
    return render_template('results.html',show_type=x,y=y,data=z)


@app.route('/results_negative')
def negative():
    x = 'Negative'
    y = 'danger'
    z = data['negative']
    return render_template('results.html', show_type=x,y=y,data=z)


@app.route('/results_neutral')
def neutral():
    x = "Neutral"
    y = 'info'
    print(data)

    z= data['neutral']


    return render_template('results.html', show_type=x,y=y,data=z)

# ////////////////////////////////////////////////////////////////////////////
# Backend website
# ////////////////////////////////////////////////////////////////////////////

@app.route('/backend')
def backend():
    global login
    if login==True:
        login=False

        return render_template('new.html',check1=settings_data[0]['check1'],check2=settings_data[0]['check2'],data=contact_data)
    else:
        return redirect(url_for('back_end_login'))


@app.route('/backend' ,methods=['GET','POST'])
def backend_control():
    contact_data = pandas.read_csv('csv files/contact.csv')
    contact_data = contact_data.to_dict(orient='records')
    global settings_data
    check=request.form.get('check1')
    check2 = request.form.get('check2')
    check3 = request.form.getlist('check3')

    print(f"{check2}----yessss")
    print(f"{check3}----yessss")

    if check=='1':
        x=1
    else:
        x=0

    if check2=='1':
        y=1
    else:
        y=0

    if check3=='1':
        z=1
    else:
        z=0

    settings_data=[{'check1': x, 'check2': y, 'check3': z}]
    set = pandas.DataFrame(settings_data)
    set.to_csv("csv files/settings.csv",mode="w",index=False)


    return render_template('new.html',check1=x,check2=y,check3=z,data=contact_data)



@app.route('/backendcontrol')
def back_end_login():
    global login
    login = False
    return render_template('login.html',check=0)



@app.route('/backendcontrol',methods=['POST'])
def backend_form():
    global login
    text = request.form['text']
    password=request.form['password']
    print(type(text),type(password))
    if text=="srirang" and password=="Warking@18":
        login=True


        return redirect(url_for('backend'))
    else:
        return render_template('login.html' ,check=1)

# ////////////////////////////////////////////////////////////////////////////




if __name__ == '__main__':
    app.run(debug=True)
