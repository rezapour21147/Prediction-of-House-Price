import scrapy
import json


class DistrictSpider(scrapy.Spider):
    name = 'district'
    start_urls = ['https://api.divar.ir/v8/web-search/tehran/buy-apartment']

    def parse(self, response):
        data = json.loads(response.body)
        districts = data.get('input_suggestion').get('json_schema').get('properties').get('districts').get('properties').get('vacancies').get('items').get('enum')
        with open('district.json' , 'w') as json_file:
            json.dump(districts , json_file)