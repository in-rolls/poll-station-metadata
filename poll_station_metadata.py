import requests
from requests.adapters import HTTPAdapter
from scrapy import Selector
import csv
import os
import json
import re

#--------------------define variables-------------------
OUTPUT_FILE = 'poll_station_metadata.csv'
START_STATE = 'Karnataka'
START_DISTRICT = 'CHIKKABALLAPUR '
START_AC = 'Chintamani'
START_PS = '163 - Kanampalli'
#-------------------------------------------------------

#--------------------define global functions------------

# -----------------------------------------------------------------------------------------------------------------------
class PSMScraper:
    def __init__(self,
                 base_url='http://psleci.nic.in/Default.aspx'
                 ):
        # define session object
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(max_retries=4))

        # set proxy
        # self.session.proxies.update({'http': 'http://127.0.0.1:40328'})

        # define urls
        self.base_url = base_url

    def GetStateList(self):
        # set url
        url = self.base_url

        # get request
        ret = self.session.get(url)

        if ret.status_code == 200:
            # get form data
            self.form_data = {
                '__VIEWSTATE': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0],
                '__VIEWSTATEGENERATOR': Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0],
                '__EVENTVALIDATION': Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0]
            }
            # print(self.form_data)

            # get state list
            options = Selector(text=ret.text).xpath('//select[@id="ddlState"]/option').extract()

            state_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                state = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                state_list.append(state)

            print(state_list)
            return state_list
        else:
            print('fail to get state list')

    def GetDistrictList(self, state):
        params = {
            '__LASTFOCUS': '',
            '__EVENTTARGET': 'ddlState',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.form_data['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.form_data['__VIEWSTATEGENERATOR'],
            '__EVENTVALIDATION': self.form_data['__EVENTVALIDATION'],
            'ddlState': state['value'],
            'ddlDistrict': '-1',
            'ddlAC': '-1',
            'ddlPS': 'ALL',
            'GoogleMapForASPNet1$hidEventName': '',
            'GoogleMapForASPNet1$hidEventValue': ''
        }
        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get form data
            self.form_data['DISTRICT__VIEWSTATE'] = Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0]
            self.form_data['DISTRICT__VIEWSTATEGENERATOR'] = Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            self.form_data['DISTRICT__EVENTVALIDATION'] = Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[ 0]
            # print(self.form_data)

            # get district list
            options = Selector(text=ret.text).xpath('//select[@id="ddlDistrict"]/option').extract()

            district_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                district = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                district_list.append(district)

            print(district_list)
            return district_list
        else:
            print('fail to get district list')

    def GetACList(self, state, district):
        params = {
            '__LASTFOCUS': '',
            '__EVENTTARGET': 'ddlDistrict',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.form_data['DISTRICT__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.form_data['DISTRICT__VIEWSTATEGENERATOR'],
            '__EVENTVALIDATION': self.form_data['DISTRICT__EVENTVALIDATION'],
            'ddlState': state['value'],
            'ddlDistrict': district['value'],
            'ddlAC': '--Select--',
            'ddlPS': '--ALL--',
            'GoogleMapForASPNet1$hidEventName': '',
            'GoogleMapForASPNet1$hidEventValue': ''
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get form data
            self.form_data['AC__VIEWSTATE'] = Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0]
            self.form_data['AC__VIEWSTATEGENERATOR'] = Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            self.form_data['AC__EVENTVALIDATION'] = Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0]
            # print(self.form_data)

            # get ac list
            options = Selector(text=ret.text).xpath('//select[@id="ddlAC"]/option').extract()

            ac_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                ac = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                ac_list.append(ac)

            print(ac_list)
            return ac_list
        else:
            print('fail to get ac list')

    def GetPSList(self, state, district, ac):
        params = {
            '__LASTFOCUS': '',
            '__EVENTTARGET': 'ddlDistrict',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.form_data['AC__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.form_data['AC__VIEWSTATEGENERATOR'],
            '__EVENTVALIDATION': self.form_data['AC__EVENTVALIDATION'],
            'ddlState': state['value'],
            'ddlDistrict': district['value'],
            'ddlAC': ac['value'],
            'ddlPS': '--ALL--',
            'GoogleMapForASPNet1$hidEventName': '',
            'GoogleMapForASPNet1$hidEventValue': ''
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            # get form data
            self.form_data['PS__VIEWSTATE'] = Selector(text=ret.text).xpath('//input[@id="__VIEWSTATE"]/@value').extract()[0]
            self.form_data['PS__VIEWSTATEGENERATOR'] = Selector(text=ret.text).xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract()[0]
            self.form_data['PS__EVENTVALIDATION'] = Selector(text=ret.text).xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0]
            # print(self.form_data)

            # get ps list
            options = Selector(text=ret.text).xpath('//select[@id="ddlPS"]/option').extract()

            ps_list = []
            for idx in range(1, len(options)):
                option = options[idx]
                ps = {
                    'value': Selector(text=option).xpath('//@value').extract()[0],
                    'name': Selector(text=option).xpath('//text()').extract()[0]
                }
                ps_list.append(ps)

            print(ps_list)
            return ps_list
        else:
            print('fail to get ps list')

    def GetLocation(self, state, district, ac, ps):
        params = {
            '__LASTFOCUS': '',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': self.form_data['PS__VIEWSTATE'],
            '__VIEWSTATEGENERATOR': self.form_data['PS__VIEWSTATEGENERATOR'],
            '__EVENTVALIDATION': self.form_data['PS__EVENTVALIDATION'],
            'ddlState': state['value'],
            'ddlDistrict': district['value'],
            'ddlAC': ac['value'],
            'ddlPS': ps['value'],
            'GoogleMapForASPNet1$hidEventName': '',
            'GoogleMapForASPNet1$hidEventValue': ''
        }

        # set url
        url = self.base_url

        # get request
        ret = self.session.post(url, data=params)

        if ret.status_code == 200:
            ret_data = {}

            scripts = Selector(text=ret.text).xpath('//script').extract()
            for script in scripts:
                if 'var latitude = ' in script:
                    ret_data['latitude'] = str(script).split('var latitude = \'')[1].split('\'')[0]
                if 'var longitude = ' in script:
                    ret_data['longitude'] = str(script).split('var longitude = \'')[1].split('\'')[0]

            print(ret_data)
            return ret_data
        else:
            print('failed to get location')

    def GetPSInfo(self, state, district, ac, ps):
        params = {
            'S': state['value'],
            'A': ac['value'],
            'P': ps['value']
        }

        # set url
        url = 'http://psleci.nic.in/pslinfoc.aspx'

        # get request
        ret = self.session.get(url, params=params)

        if ret.status_code == 200:
            psinfo = {}
            # from the first html table
            psinfo['blo'] = Selector(text=ret.text).xpath('//span[@id="BLO"]/text()').extract()[0]
            psinfo['ero'] = Selector(text=ret.text).xpath('//span[@id="ERO"]/text()').extract()[0]
            psinfo['deo'] = Selector(text=ret.text).xpath('//span[@id="DEO"]/text()').extract()[0]
            psinfo['ceo'] = Selector(text=ret.text).xpath('//span[@id="CEO"]/text()').extract()[0]
            psinfo['eroll'] = Selector(text=ret.text).xpath('//a[@id="linkERollpdf"]/@href').extract()[0]
            psinfo['supplementary'] = ''
            if len(Selector(text=ret.text).xpath('//a[@id="linkSuppdf"]/@href').extract()) > 0:
                psinfo['supplementary'] = Selector(text=ret.text).xpath('//a[@id="linkSuppdf"]/@href').extract()

            # from the second html table
            psinfo['Building Quality'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="BuildingQuality"]/text()').extract()) > 0:
                psinfo['Building Quality'] = Selector(text=ret.text).xpath('//span[@id="BuildingQuality"]/text()').extract()[0]

            psinfo['PS with less than 20 sqmts'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwithlessthan20sqmts"]/text()').extract()) > 0:
                psinfo['PS with less than 20 sqmts'] = Selector(text=ret.text).xpath('//span[@id="PSwithlessthan20sqmts"]/text()').extract()[0]

            psinfo['PS buildings is dilapidated or dangerous'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSbuildingsdilapidatedordangerous"]/text()').extract()) > 0:
                psinfo['PS buildings is dilapidated or dangerous'] = Selector(text=ret.text).xpath('//span[@id="PSbuildingsdilapidatedordangerous"]/text()').extract()[0]

            psinfo['PS is in Govt building/Premises'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSnotinGovtbuildingPremises"]/text()').extract()) > 0:
                psinfo['PS is in Govt building/Premises'] = Selector(text=ret.text).xpath('//span[@id="PSnotinGovtbuildingPremises"]/text()').extract()[0]

            psinfo['PS located in an institution/religious place'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSlocatedinanreligiousplace"]/text()').extract()) > 0:
                psinfo['PS located in an institution/religious place'] = Selector(text=ret.text).xpath('//span[@id="PSlocatedinanreligiousplace"]/text()').extract()[0]

            psinfo['PS in School/College building'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSinSchoolCollegebuilding"]/text()').extract()) > 0:
                psinfo['PS in School/College building'] = Selector(text=ret.text).xpath('//span[@id="PSinSchoolCollegebuilding"]/text()').extract()[0]

            psinfo['PS in ground floor'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSnotingroundfloor"]/text()').extract()) > 0:
                psinfo['PS in ground floor'] = Selector(text=ret.text).xpath('//span[@id="PSnotingroundfloor"]/text()').extract()[0]

            psinfo['PS having Separate door for Entry and Exit'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSnothavingSeparatedoorforEntryandExit"]/text()').extract()) > 0:
                psinfo['PS having Separate door for Entry and Exit'] = Selector(text=ret.text).xpath('//span[@id="PSnothavingSeparatedoorforEntryandExit"]/text()').extract()[0]

            psinfo['political party office situated within 200 meters of PS premises'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="politicalpartyofficesituatedwithin200m"]/text()').extract()) > 0:
                psinfo['political party office situated within 200 meters of PS premises'] = Selector(text=ret.text).xpath('//span[@id="politicalpartyofficesituatedwithin200m"]/text()').extract()[0]

            psinfo['PS is having drinking water facilities in the premises'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwithoutdrinkingwaterfacilities"]/text()').extract()) > 0:
                psinfo['PS is having drinking water facilities in the premises'] = Selector(text=ret.text).xpath('//span[@id="PSwithoutdrinkingwaterfacilities"]/text()').extract()[0]

            psinfo['PS buildings having Electricity Supply'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="psbuildingswithoutElectricitySupply"]/text()').extract()) > 0:
                psinfo['PS buildings having Electricity Supply'] = Selector(text=ret.text).xpath('//span[@id="psbuildingswithoutElectricitySupply"]/text()').extract()[0]

            psinfo['PS buildings with Proper lighting, Fixtures etc.'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="buildingswithoutProperlighting"]/text()').extract()) > 0:
                psinfo['PS buildings with Proper lighting, Fixtures etc.'] = Selector(text=ret.text).xpath('//span[@id="buildingswithoutProperlighting"]/text()').extract()[0]

            psinfo['PS buildings with Toilet(Male/Female)'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="buildingswithoutToilet"]/text()').extract()) > 0:
                psinfo['PS buildings with Toilet(Male/Female)'] = Selector(text=ret.text).xpath('//span[@id="buildingswithoutToilet"]/text()').extract()[0]

            psinfo['PS with ramps For Disable'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwithoutramps"]/text()').extract()) > 0:
                psinfo['PS with ramps For Disable'] = Selector(text=ret.text).xpath('//span[@id="PSwithoutramps"]/text()').extract()[0]

            psinfo['PS buildings with Adequate Furniture'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="buildingswithoutAdequateFurniture"]/text()').extract()) > 0:
                psinfo['PS buildings with Adequate Furniture'] = Selector(text=ret.text).xpath('//span[@id="buildingswithoutAdequateFurniture"]/text()').extract()[0]

            psinfo['PS with shade/shelter for protection from sun/rain etc.'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwithoutshadeshelterforprotection"]/text()').extract()) > 0:
                psinfo['PS with shade/shelter for protection from sun/rain etc.'] = Selector(text=ret.text).xpath('//span[@id="PSwithoutshadeshelterforprotection"]/text()').extract()[0]

            psinfo['PS with Proper road connectivity'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwithoutProperroadconnectivity"]/text()').extract()) > 0:
                psinfo['PS with Proper road connectivity'] = Selector(text=ret.text).xpath('//span[@id="PSwithoutProperroadconnectivity"]/text()').extract()[0]

            psinfo['PS where voters have to cross river/valley/ravine or natural obstacle to reach PS'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwherevotershavetocrossriver"]/text()').extract()) > 0:
                psinfo['PS where voters have to cross river/valley/ravine or natural obstacle to reach PS'] = Selector(text=ret.text).xpath('//span[@id="PSwherevotershavetocrossriver"]/text()').extract()[0]

            psinfo['Building Quality'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="BuildingQuality"]/text()').extract()) > 0:
                psinfo['Building Quality'] = \
                Selector(text=ret.text).xpath('//span[@id="BuildingQuality"]/text()').extract()[0]

            psinfo['PS with Landline Telephone/Fax Connection'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwithoutLandlineTelephoneFaxConnection"]/text()').extract()) > 0:
                psinfo['PS with Landline Telephone/Fax Connection'] = Selector(text=ret.text).xpath('//span[@id="PSwithoutLandlineTelephoneFaxConnection"]/text()').extract()[0]

            psinfo['PS with Mobile connectivity'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwithoutMobileconnectivity"]/text()').extract()) > 0:
                psinfo['PS with Mobile connectivity'] = Selector(text=ret.text).xpath('//span[@id="PSwithoutMobileconnectivity"]/text()').extract()[0]

            psinfo['PS with Internet facility'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwithoutInternetfacility"]/text()').extract()) > 0:
                psinfo['PS with Internet facility'] = Selector(text=ret.text).xpath('//span[@id="PSwithoutInternetfacility"]/text()').extract()[0]

            psinfo['PS with Proper signage of Building name and address'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwithoutPropersignageofBuildingname"]/text()').extract()) > 0:
                psinfo['PS with Proper signage of Building name and address'] = Selector(text=ret.text).xpath('//span[@id="PSwithoutPropersignageofBuildingname"]/text()').extract()[0]

            psinfo['PS with in LWE/insurgency affected area'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSwithinLWEinsurgency"]/text()').extract()) > 0:
                psinfo['PS with in LWE/insurgency affected area'] = Selector(text=ret.text).xpath('//span[@id="PSwithinLWEinsurgency"]/text()').extract()[0]

            psinfo['PS With in forest/semi-forest area'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSWithinforestsemiforestarea"]/text()').extract()) > 0:
                psinfo['PS With in forest/semi-forest area'] = Selector(text=ret.text).xpath('//span[@id="PSWithinforestsemiforestarea"]/text()').extract()[0]

            psinfo['PS in vulnerable critical location'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="PSinvulnerablecriticallocation"]/text()').extract()) > 0:
                psinfo['PS in vulnerable critical location'] = Selector(text=ret.text).xpath('//span[@id="PSinvulnerablecriticallocation"]/text()').extract()[0]

            psinfo['sensitive/hyper-sensitive PS'] = ''
            if len(Selector(text=ret.text).xpath('//span[@id="sensitivehypersensitivePS"]/text()').extract()) > 0:
                psinfo['sensitive/hyper-sensitive PS'] = Selector(text=ret.text).xpath('//span[@id="sensitivehypersensitivePS"]/text()').extract()[0]

            return psinfo
        else:
            print('fail to get psinfo')

    def WriteHeader(self):
        # set headers
        header_info = []
        header_info.append('state_or_ut')
        header_info.append('district')
        header_info.append('ac')
        header_info.append('polling_station')
        header_info.append('lat')
        header_info.append('long')
        header_info.append('blo')
        header_info.append('ero')
        header_info.append('deo')
        header_info.append('ceo')
        header_info.append('eroll')
        header_info.append('supplementary')
        header_info.append('Building Quality')
        header_info.append('PS with less than 20 sqmts')
        header_info.append('PS buildings is dilapidated or dangerous')
        header_info.append('PS is in Govt building/Premises')
        header_info.append('PS located in an institution/religious place')
        header_info.append('PS in School/College building')
        header_info.append('PS in ground floor')
        header_info.append('PS having Separate door for Entry and Exit')
        header_info.append('political party office situated within 200 meters of PS premises')
        header_info.append('PS is having drinking water facilities in the premises')
        header_info.append('PS buildings having Electricity Supply')
        header_info.append('PS buildings with Proper lighting, Fixtures etc.')
        header_info.append('PS buildings with Toilet(Male/Female)')
        header_info.append('PS with ramps For Disable')
        header_info.append('PS buildings with Adequate Furniture')
        header_info.append('PS with shade/shelter for protection from sun/rain etc.')
        header_info.append('PS with Proper road connectivity')
        header_info.append('PS where voters have to cross river/valley/ravine or natural obstacle to reach PS')
        header_info.append('PS with Landline Telephone/Fax Connection')
        header_info.append('PS with Mobile connectivity')
        header_info.append('PS with Internet facility')
        header_info.append('PS with Proper signage of Building name and address')
        header_info.append('PS with in LWE/insurgency affected area')
        header_info.append('PS With in forest/semi-forest area')
        header_info.append('PS in vulnerable critical location')
        header_info.append('sensitive/hyper-sensitive PS')

        # write header into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'w'), delimiter=',', lineterminator='\n')
        writer.writerow(header_info)

    def WriteData(self, data):
        # write data into output csv file
        writer = csv.writer(open(OUTPUT_FILE, 'a', encoding='utf-8'), delimiter=',', lineterminator='\n')
        writer.writerow(data)

    def Start(self):
        # write header into output csv file
        if START_STATE == '' and START_DISTRICT == '' and START_AC == '' and START_PS == '': self.WriteHeader()

        # get state list
        print('getting state list ...')
        state_list = self.GetStateList()

        state_flag = False
        if START_STATE == '': state_flag = True

        district_flag = False
        if START_DISTRICT == '': district_flag = True

        ac_flag = False
        if START_AC == '': ac_flag = True

        ps_flag = False
        if START_PS == '': ps_flag = True

        for state in state_list:
            if START_STATE == state['name']: state_flag = True
            if state_flag == False: continue

            # get district list
            print('getting district list for %s ...' % (state['name']))
            district_list = self.GetDistrictList(state)

            for district in district_list:
                if START_DISTRICT == district['name']: district_flag = True
                if district_flag == False: continue

                # get AC list
                print('getting AC list for %s:%s ...' % (state['name'], district['name']))
                ac_list = self.GetACList(state, district)

                for ac in ac_list:
                # for idx in range(5, len(ac_list)):
                #     ac = ac_list[idx]
                    if START_AC == ac['name']: ac_flag = True
                    if ac_flag == False: continue

                    # get polling station list
                    print('getting polling station list for %s:%s:%s ...' % (state['name'], district['name'], ac['name']))
                    ps_list = self.GetPSList(state, district, ac)

                    for ps in ps_list:
                        if START_PS == ps['name']: ps_flag = True
                        if ps_flag == False: continue

                        # get location
                        print('getting location for %s:%s:%s:%s ...' % (state['name'], district['name'], ac['name'], ps['name']))
                        location = self.GetLocation(state, district, ac, ps)

                        # get psinfo
                        print('getting psinfo for %s:%s:%s:%s ...' % (state['name'], district['name'], ac['name'], ps['name']))
                        psinfo = self.GetPSInfo(state, district, ac, ps)

                        # write data into output csv file
                        data = []
                        data.append(state['name'])
                        data.append(district['name'])
                        data.append(ac['name'])
                        data.append(ps['name'])
                        data.append(location['latitude'])
                        data.append(location['longitude'])
                        data.append(psinfo['blo'])
                        data.append(psinfo['ero'])
                        data.append(psinfo['deo'])
                        data.append(psinfo['ceo'])
                        data.append(psinfo['eroll'])
                        data.append(psinfo['supplementary'])
                        data.append(psinfo['Building Quality'])
                        data.append(psinfo['PS with less than 20 sqmts'])
                        data.append(psinfo['PS buildings is dilapidated or dangerous'])
                        data.append(psinfo['PS is in Govt building/Premises'])
                        data.append(psinfo['PS located in an institution/religious place'])
                        data.append(psinfo['PS in School/College building'])
                        data.append(psinfo['PS in ground floor'])
                        data.append(psinfo['PS having Separate door for Entry and Exit'])
                        data.append(psinfo['political party office situated within 200 meters of PS premises'])
                        data.append(psinfo['PS is having drinking water facilities in the premises'])
                        data.append(psinfo['PS buildings having Electricity Supply'])
                        data.append(psinfo['PS buildings with Proper lighting, Fixtures etc.'])
                        data.append(psinfo['PS buildings with Toilet(Male/Female)'])
                        data.append(psinfo['PS with ramps For Disable'])
                        data.append(psinfo['PS buildings with Adequate Furniture'])
                        data.append(psinfo['PS with shade/shelter for protection from sun/rain etc.'])
                        data.append(psinfo['PS with Proper road connectivity'])
                        data.append(psinfo['PS where voters have to cross river/valley/ravine or natural obstacle to reach PS'])
                        data.append(psinfo['PS with Landline Telephone/Fax Connection'])
                        data.append(psinfo['PS with Mobile connectivity'])
                        data.append(psinfo['PS with Internet facility'])
                        data.append(psinfo['PS with Proper signage of Building name and address'])
                        data.append(psinfo['PS with in LWE/insurgency affected area'])
                        data.append(psinfo['PS With in forest/semi-forest area'])
                        data.append(psinfo['PS in vulnerable critical location'])
                        data.append(psinfo['sensitive/hyper-sensitive PS'])
                        self.WriteData(data)

                        # break
            #         break
            #     break
            # break


#------------------------------------------------------- main -------------------------------------------------------

def main():
    # create scraper object
    scraper = PSMScraper()

    # start to scrape
    scraper.Start()

if __name__ == '__main__':
    main()
