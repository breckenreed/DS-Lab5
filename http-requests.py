import requests


for i in range(10):
    post_req = requests.post('http://localhost:8000/', json={"Message": f"THIS_IS_A_MESSAGE_NUMERO_{str(i)}"})
    print(post_req.text)

get_req = requests.get('http://localhost:8000/')
print(get_req.text)
