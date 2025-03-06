import requests

res = requests.get(
    url="https://www.gutenberg.org/files/132/132-h/132-h.htm",
    timeout=(10,5)
    )
print(f"Status_code: {res.status_code}")
text = res.text
print(f"{text}")