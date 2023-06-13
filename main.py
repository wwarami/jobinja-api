from crawler.get_cookie import get_cookie, save_cookies
from crawler.crawler import GetJobs
import argparse
from crawler.validators import email_validator


def cookies(email, password):
    # check if provided email and password is validated.
    if not email_validator(email) or password is None:
        raise ValueError('To get cookies you should provide\
 "email" and "password" for your jobinja account.\n\
Your info will only be used to login and get cookies.(read the source code.)\n\
Use "-e" for email and "-p" for password.')

    # get the cookies and store it.
    response = get_cookie(email, password)
    save_cookies(cookies=response)


def get_jobs():
    crawler = GetJobs(page=10)
    crawler.start()
    links = crawler.links
    print(len(links))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Jobinja Crawler')
    parser.add_argument('--cookies', action='store_true')
    parser.add_argument('--get-jobs', action='store_true')
    parser.add_argument('-e', '--email', type=str)
    parser.add_argument('-p', '--password', type=str)
    args = parser.parse_args()

    if args.cookies:
        cookies(email=args.email, password=args.password)
    elif args.get_jobs:
        get_jobs()
    else:
        raise NotImplementedError()
