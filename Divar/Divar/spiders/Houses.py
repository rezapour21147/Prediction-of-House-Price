import scrapy
import json



class HousesSpider(scrapy.Spider):
    name = 'Houses'


    def start_requests(self):
        with open('district.json' , 'r') as json_file:
            districts = json.load(json_file)
        for district in districts:
            yield scrapy.Request(
                url=f'https://api.divar.ir/v8/web-search/tehran/buy-apartment?districts={district}' ,
                callback= self.parse
            )


    def parse(self, response):
        data = json.loads(response.body)
        houses = data.get('web_widgets').get('post_list')
        for house in houses:
            token = house.get('data').get('token')
            yield scrapy.Request(
                url= f'https://api.divar.ir/v5/posts/{token}' ,
                callback= self.parse_token
            )

        if data.get('last_post_date') >= 1649955900000000 :
            page = data.get('seo_details').get('next')
            yield scrapy.Request(
                url=f'https://api.divar.ir/v8/web-search/{page}' ,
                callback= self.parse
            )

    def parse_token(self, response):
        token_data = json.loads(response.body)
        house = token_data.get('widgets').get('list_data')
        data = {}
        area = token_data.get('widgets').get('header').get('place')
        data['area'] = area 
        cordinate = token_data.get('widgets').get('location')
        data['latitude'] = cordinate.get('latitude')
        data['longitude'] = cordinate.get('longitude')
        data['price'] = token_data.get('data').get('webengage').get('price')
        for elm in house:
            if elm.get('format') == 'group_info_row':
                for info in elm.get('items'):
                    data[info.get('title')] = info.get('value')
            elif elm.get('format') == 'group_feature_row':
                for feature in elm.get('items'):
                    data[feature.get('title')] = info.get('avalable')
                if elm.get('next_page'):
                    extra_infos = elm.get('next_page').get('widget_list')
                    for extra_info in extra_infos:
                        if extra_info.get('widget_type') == 'UNEXPANDABLE_ROW':
                            data[extra_info.get('data').get('title')] = extra_info.get('data').get('value')
                        elif extra_info.get('widget_type') == 'FEATURE_ROW':
                            data[extra_info.get('data').get('title')] = 'true'
            elif elm.get('format') == 'string':
                data[elm.get('title')] = elm.get('value')
        yield data
