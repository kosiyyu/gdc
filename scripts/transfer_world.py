import httpx

def transfer_world():
  address = ";)))"
  headers = {'Content-type': 'application/json'}
  body = {
    "user_id": "12345678" # dummy user_id
  }

  response = httpx.post(url=address, headers=headers, json=body)
  status_code = response.status_code

  if(status_code != 200):
    exit(1)

  presign_url: str = response.json()["body"]
  # print(presign_url)

  with open("world.tar.gz", "rb") as file:
    response = httpx.put(presign_url, data=file)
    # print(response)

def main():
  pass
