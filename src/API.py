import requests
import json
import sys


#validate parsed JSON data from MyStat
def validate (data):
        try: # Yeah I can`t do it without catching some error (P.S. somehow doesn`t working for GET with auth)
            error = data[0]['message']
            raise Exception('Error from MyStat ! ' + error)
        except KeyError:
            return data
        except IndexError: # if data is [] (empty JSON)
            return data

def GetWithHeader (token,url,data=''):
    response = requests.get(url, data = data, headers={"authorization":"Bearer "+token})
    response = json.loads(response.text)
    return validate(response)

def PostWithHeader (token,url,data):
    response = requests.post(url, data = data, headers={"authorization":"Bearer "+token})
    response = json.loads(response.text)
    return validate(response)

#make response validate for any errors and return parsed JSON 
def Post (data,url,headers={}):
    response = requests.post(url, data = data,headers=headers)
    response = json.loads(response.text)
    return validate(response)

def Get (data,url):
    response = requests.get(url, data = data)
    response = json.loads(response.text)
    return validate(response)

def getKey (password,username):
    url = 'https://msapi.itstep.org/api/v2/auth/login'
    myobj = {'application_key': '6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6',
             'id_city':31 , # my dear city KHERSON
             'username':username,
             'password':password
            }
    result = Post(myobj,url)
    return [result['access_token'],result['refresh_token']]

def getRefreshTime(password,username):
    url = 'https://msapi.itstep.org/api/v2/auth/login'
    myobj = {'application_key': '6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6',
             'id_city':31 ,
             'username':username,
             'password':password
            }
    result = Post(myobj,url)
    access_refresh_time = result['expires_in_access']
    refresh_token_time = result['expires_in_refresh']
    return [access_refresh_time,refresh_token_time] #just UNIX timestamps 

def GetUserData(token):
    url = 'https://msapi.itstep.org/api/v2/settings/user-info'
    return GetWithHeader(token,url)

def GetStreamLeaderboard(token):
    url ="https://msapi.itstep.org/api/v2/dashboard/progress/leader-stream"
    return GetWithHeader(token,url)

def GetClassLeaderboard(token):
    url ="https://msapi.itstep.org/api/v2/dashboard/progress/leader-group"
    return GetWithHeader(token,url)

# first value : number of crystals
#second value : number of coins
#third value : sum of it (it's points)
def GetPoints(token):
        points = GetUserData(token)
        points = points['gaming_points']
        data = [points[0]['points'] , points[1]['points'] , points[0]['points'] + points[1]['points']]
        return data

def GetHomeworks(token):
        # Note L outputs only all done and overdue hometasks. Why ? Because I have only this types of homeworks on my accaunt (not 0!)
        url = 'https://msapi.itstep.org/api/v2/count/homework'
        get = GetWithHeader(token,url)
        print(get)
        all = get[5]['counter']
        done = get[0]['counter']
        overdue = get[2]['counter']
        current = get[1]['counter'] # I took position from old code so it may be wrong
        review = get[3]['counter']
        data = [all,done,overdue,current,review]
        return data

def GetFutureExsams(token):
        url = 'https://msapi.itstep.org/api/v2/dashboard/info/future-exams'
        get = GetWithHeader(token,url)
        return get

def RefreshToken(refresh_token):
    data = json.dumps({"refresh_token":refresh_token})
    url = "https://msapi.itstep.org/api/v2/auth/refresh"
    result = Post(data,url,{'content-type': 'application/json'})
    return [result['access_token'],result['refresh_token']]

    