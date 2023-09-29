import json as js
from datetime import datetime
from  more_itertools import flatten
import csv
from geopy.distance import geodesic as gd


dict_streets_bus = {}
def bus_station ():
    name_streets = []
    with open ("bus_stops.csv", 'r', encoding='windows 1251') as f:
        fields = ['ID','Name','Longitude_WGS84','Latitude_WGS84','AdmArea','District',
                'RouteNumbers','StationName','Direction','Pavilion','OperatingOrgName','EntryState','global_id',
                'PlaceDescription','Works','geodata_center','geoarea']

        reader = csv.DictReader(f,fields,delimiter=';')
        for name in reader:
            name_streets.append(name['PlaceDescription'].split(', ')[0])

    for name in name_streets:
        if len(name) > 0:
            if  name in dict_streets_bus:
                dict_streets_bus[name] += 1
            else:
                dict_streets_bus[name] = 1
    max_streets = max(dict_streets_bus.keys(), key = dict_streets_bus.get)
    return f"На улице {max_streets} больше всего автобусных остановок" 

def metro_repair():

    repair_station = {}
   
    with open ("metro_works.json", 'r', encoding="windows-1251") as f:
        file = js.load(f)
    
        for line in file:
            if len(line['RepairOfEscalators'])> 0:
                repair_station[line["Name"]] = line
                repair_station[line['Name']]['repair_date'] = []
                for num in repair_station[line['Name']]['RepairOfEscalators']:
                    date_num = ''
                    date_num = num['RepairOfEscalators'].split('-')
                    repair_station[line['Name']]['repair_date'].append(date_num)
                    

    today = datetime.now()
    repair_escalators = []           
    for k,v in repair_station.items():
        for date in flatten(v['repair_date']):
            date = date.replace('.', '/')
            date = date[:-4]+date[-2:]
            date = datetime.strptime(date,"%d/%m/%y")
            delta = date - today
            if delta.days > 0:
                repair_escalators.append(k)
    return repair_escalators

def bus_and_metro ():
    geo_bus = {}
    geo_metro = {}
    with open ("bus_stops.csv", 'r', encoding='windows 1251') as f:
        fields = ['ID','Name','Longitude_WGS84','Latitude_WGS84','AdmArea','District',
                'RouteNumbers','StationName','Direction','Pavilion','OperatingOrgName','EntryState','global_id',
                'PlaceDescription','Works','geodata_center','geoarea']

        reader = csv.DictReader(f,fields,delimiter=';')
        for line in list(reader)[2:]:
            geo_bus[line['Name']] = line['Longitude_WGS84'], line['Latitude_WGS84']
            
    with open ("metro_works.json", 'r', encoding="windows-1251") as f:
        file = js.load(f)
        for line in file:
            name = line['NameOfStation']
            geo_metro[name] = line['Longitude_WGS84'], line['Latitude_WGS84']
            
    metro_with_bus = {}
    for station,coordinats in geo_metro.items():
        item_bus = []
        for name_bus, bus_coord in geo_bus.items():
            if gd(coordinats,bus_coord).km <0.5:
                item_bus.append(name_bus)
        metro_with_bus[station] = len(item_bus)
    max_count = max(metro_with_bus, key = metro_with_bus.get)
    return f"больше всего остановок у станции метро {max_count}"
     



if __name__ == "__main__":
    print(bus_station())                
    for name in metro_repair():
        print(f"эсколаторы на ремонте в {name}")
    print(bus_and_metro())



