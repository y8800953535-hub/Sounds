from yandex_music import Client


def show_code(code):
    print("Открой ссылку:", code.verification_url)
    print("Код подтверждения:", code.user_code)


client = Client()
token = client.device_auth(on_code=show_code)

print("YM_TOKEN:")
print(token.access_token)
