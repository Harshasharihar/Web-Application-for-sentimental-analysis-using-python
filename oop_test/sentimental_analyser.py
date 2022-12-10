import requests
import pickle



class Sentimental_analyser():
    def __init__(self):
        self.loaded_vectorizer = pickle.load(open("vectorizer.sav", 'rb'))
        self.loaded_model = pickle.load(open("sentimental.sav", 'rb'))






    def sentiment_of_list(data):
        url = 'https://api.monkeylearn.com/v3/classifiers/cl_pi3C7JiL/classify/'
        api_key = '88a20b724080776b540ae80fc5a5ff6a7e9fadef'
        def analyseResp(d):
            dict1 = d[0]

            for k, v in dict1.items():
                if k == 'classifications':
                    new_d = v[0]
                    for k1, v1 in new_d.items():
                        if k1 == 'tag_name':
                            actual_response = v1
                            return actual_response

        senti_data={
            'negative':[],
            'positive':[],
            'neutral':[]
        }
        for lst in data:
            header = {"Authorization": f"Token {api_key}"}
            data = {'data': [lst]}
            response = requests.post(url, headers=header, json=data)
            d = response.json()
            sentiment = analyseResp(d)
            if sentiment.lower() == 'negative':
                senti_data['negative'].append(lst)
            elif sentiment.lower()=='positive':
                senti_data['positive'].append(lst)
            elif sentiment.lower()=='neutral':
                senti_data['neutral'].append(lst)

        return senti_data

    def single_sentence(data):
        url = 'https://api.monkeylearn.com/v3/classifiers/cl_pi3C7JiL/classify/'
        api_key = '88a20b724080776b540ae80fc5a5ff6a7e9fadef'
        def analyseResp(d):
            dict1 = d[0]

            for k, v in dict1.items():
                if k == 'classifications':
                    new_d = v[0]
                    for k1, v1 in new_d.items():
                        if k1 == 'tag_name':
                            actual_response = v1
                            return actual_response

        header = {"Authorization": f"Token {api_key}"}
        data = {'data': [data]}
        response = requests.post(url, headers=header, json=data)
        d = response.json()
        sentiment = analyseResp(d)
        return sentiment


    def nlp_algo_list(data):


        loaded_vectorizer = pickle.load(open("vectorizer.sav", 'rb'))

        senti_data={
            'negative':[],
            'positive':[],
            'neutral':[]
        }
        loaded_model = pickle.load(open("sentimental.sav", 'rb'))
        for n in data:
            df = [n]
            X_train = loaded_vectorizer.transform(df)
            result = loaded_model.predict(X_train)
            if result[0] == 1:
                result="positive"

            else:
                result = "negative"

            if result.lower() == 'negative':
                senti_data['negative'].append(n)
            elif result.lower() == 'positive':
                senti_data['positive'].append(n)
            elif result.lower() == 'neutral':
                senti_data['neutral'].append(n)

        return senti_data

    def nlp_algo_single(data):
        loaded_vectorizer = pickle.load(open("vectorizer.sav", 'rb'))
        loaded_model = pickle.load(open("sentimental.sav", 'rb'))
        df = [data]
        X_train = loaded_vectorizer.transform(df)
        result = loaded_model.predict(X_train)
        if result[0] == 1:
            result = "Positive"

        else:
            result = "Negative"

        return result







