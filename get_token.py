
from yandex_music import Client


def show_code(code):
    print("\n=== Авторизация Яндекс Музыки ===")
    print("Открой ссылку:", code.verification_url)
    print("Код подтверждения:", code.user_code)
    print("\nВойди в свой аккаунт и подтверди доступ.")


def main():
    client = Client()

    token = client.device_auth(on_code=show_code)

    print("\nАвторизация успешно завершена.")
    print("Твой токен получен.")
    print("Добавь его в Render → Environment → YM_TOKEN.")
    print("\nНЕ отправляй токен другим людям и не публикуй его.")


if __name__ == "__main__":
    main()
