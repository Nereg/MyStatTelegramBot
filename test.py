import API
token = API.getKey('SamsungS8Oleg','Kisi_lb7W')
print(token)
homeworks = API.GetHomeworks(token)
print(homeworks)