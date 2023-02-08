import requests


response = requests.post('http://127.0.0.1:5000/users', json={'username':'user2', 'email':'user2@net.com', 'password':'1234'})

#response = requests.get('http://127.0.0.1:5000/users/1')

#response = requests.post('http://127.0.0.1:5000/ads', json={'header':'second_ad', 'description':'cgjdhgfkjkgjk', 'user_id':'1'})

#response = requests.get('http://127.0.0.1:5000/ads/2')

#response = requests.delete('http://127.0.0.1:5000/ads/2')

#response = requests.get('http://127.0.0.1:5000/ads/2')

#response = requests.get('http://127.0.0.1:5000/ads/1')




print(response.status_code)
print(response.json())