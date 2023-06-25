from fastapi import FastAPI, Query, Response, status
from crawler.crawler import GetJobs
from config.config import LOCATIONS, JOB_CATEGORIES
from typing import List

app = FastAPI(title='Jobinja Crawler',
              version="0.1.0",
              contact={'Email': 'night.error.go@gmail.com'},
              )


@app.get('/')
def get_jobs(*,
             keywords: List[str] = Query(None, title="Keywords to filter jobs.",
                                         example=["پایتون", "بک اند"]),
             categories: List[str] = Query(None, title="Categories to filter jobs.",
                                           example=["وب،‌ برنامه‌نویسی و نرم‌افزار", "دیجیتال مارکتینگ"]),
             locations: List[str] = Query(None, title="Locations to filter jobs.",
                                          example=["تهران", "البرز"]),
             page: int = Query(1, title="Number of pages to be crawled(each page 20 jobs.)"),
             response: Response
             ):
    # Check if locations are valid
    if locations:
        # Validate each location against the predefined list of valid locations
        if [location for location in locations if location not in LOCATIONS]:
            # Return an error response if any location is not valid
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'error': 'Not valid locations',
                    'detail': 'Check if your given locations are valid. \
They must be available on https://jobinja.ir'}

    # Check if categories are valid
    if categories:
        # Split the string values on ', ' to create a list of categories
        categories = categories[0].split(', ')
        # Validate each category against the predefined list of valid categories
        if [category for category in categories if category not in JOB_CATEGORIES]:
            # Return an error response if any category is not valid
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'error': 'Not valid categories',
                    'detail': 'Check if your given categories are valid. \
They must be available on https://jobinja.ir'}

    print(f'Keywords: {keywords}\nLocations: {locations}\nCategories: {categories}\nPage: {page}')

    # crawl
    crawler = GetJobs(keywords=keywords,
                      locations=locations,
                      categories=categories,
                      page=page)
    try:  # Handle exceptions while crawling
        crawler.start()
    except Exception as error:
        return {'error': 'Something went wrong while crawling.',
                'detail': error}

    # result
    response.status_code = status.HTTP_200_OK
    return {'message': 'Crawling finished successfully.',
            'jobs': crawler.get_jobs_detail()}
