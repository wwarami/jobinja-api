from src.get_cookie import get_cookie, save_cookies


def main():
    email = 'night.error.go@gmail.com'
    password = 'errorNight1234'
    save_cookies(cookies=get_cookie(email, password))


if __name__ == '__main__':
    main()
