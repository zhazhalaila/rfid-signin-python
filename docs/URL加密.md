自定义一个环境变量来充当Key
```python
secret = os.environ.get('secret') or 'my_spider_key'
```

加密
```python
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()
```

构造URL请求，会在请求中加入Key
```python
payload = {'rfid_id': enc, 'secret': secret}
test = requests.get('http://127.0.0.1:5000/signin', params=payload)
```
解密
```python
def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)
```
提取有关卡号信息
```python
fake_id = request.args.get('rfid_id')
secret = request.args.get('secret')
rfid_id = decode(secret, fake_id)[2:-1]
```

参考链接：

[Simple way to encode a string according to a password?
](https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password)

[vigenère cipher](https://www.youtube.com/watch?v=SkJcmCaHqS0)
