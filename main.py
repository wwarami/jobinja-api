import json
from crawler.get_cookie import get_cookie, save_cookies
from crawler.crawler import GetJobs, GetJobDetail
import argparse
from crawler.validators import email_validator


def cookies(email, password):
    # check if provided email and password is validated.
    if email is None or not email_validator(email) or password is None:
        raise ValueError('To get cookies you should provide\
 "email" and "password" for your jobinja account.\n\
Your info will only be used to login and get cookies.(read the source code.)\n\
Use "-e" for email and "-p" for password.')

    # get the cookies and store it.
    response = get_cookie(email, password)
    save_cookies(cookies=response)


def get_jobs(config, detail=True):
    # read the config file and handle exceptions
    try:
        with open(config, 'r') as file:
            filters = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"{config} does not exists!\
\nYou should provide this file to filter results based on it.\nRead crawler's documentation for more detail.")
    except json.JSONDecodeError:
        raise Exception("Something is wrong with your config file.\nRead crawler's documentation for more detail.")

    # create an instance of jobs crawler using provided filter
    try:
        jobs_crawler = GetJobs(page=filters['page'],
                               keywords=filters['keywords'],
                               categories=filters['categories'],
                               locations=filters['locations'])
    except KeyError:
        # handle config files problems
        raise KeyError("Something is wrong with your config file.\nRead crawler's documentation for more detail.")

    jobs_crawler.start()  # crawl
    links = jobs_crawler.links
    print(f'{len(links)} jobs were crawled...')

    # get each jobs detail
    if detail:
        print("Crawling job details...")
        result = jobs_crawler.get_jobs_detail()
        print(f'\nCrawling result: {result}')
    else:
        print(f'Links: {links}')


def get_job_detail(url):
    if url is None:
        raise ValueError('You should provide a url to crawl.')
    crawler = GetJobDetail()
    response = crawler.start(url)
    print(f"Result: {response}")


if __name__ == '__main__':
    print("THIS IS ONLY FOR TESTING...")

    parser = argparse.ArgumentParser(prog='Jobinja Crawler')

    parser.add_argument('--cookies',
                        action='store_true',
                        help="Add this if you want get cookies(you should provide email\
'address' and 'password' too.).")
    parser.add_argument('-e', '--email',
                        type=str,
                        help="Email to your jobinja.com account(add when you get cookies).")
    parser.add_argument('-p', '--password',
                        type=str,
                        help="Password to your jobinja.com account(add when you get cookies).")

    parser.add_argument('--jobs',
                        action='store_true',
                        help="Add to crawl many jobs. You should first configure a config.json \
file for filters(or you will get all available jobs on jobinja.ir....).")
    parser.add_argument('--config',
                        type=str,
                        help='Path to your config.json file.')
    parser.add_argument('--detail',
                        action='store_true',
                        help="If you are crawling many jobs, add this to get each job's detail.")

    parser.add_argument('--jobdetail',
                        action='store_true',
                        help='Use to crawl a single job(provide url by --url).')
    parser.add_argument('--url',
                        type=str,
                        help="Url for job...")

    args = parser.parse_args()

    if args.cookies:
        cookies(email=args.email, password=args.password)
    elif args.jobs:
        get_jobs(config=args.config, detail=args.detail)
    elif args.jobdetail:
        get_job_detail(args.url)
    else:
        print("Please provide a command.\nRun 'python main.py -h' for help.")
