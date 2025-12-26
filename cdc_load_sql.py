import json
import psycopg2 as pg
import configparser
from utils import jsonParse as jp

def cdc_db_insert(message):
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    db_host = config.get('Postgre', 'db_host')
    db_name = config.get('Postgre', 'db_name')
    db_user = config.get('Postgre', 'db_user')
    db_port = config.get('Postgre', 'db_port')
    db_password = config.get('Postgre', 'db_password')

    try:
        json_str=json.loads(message)
        connection = pg.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        cursor = connection.cursor()

        if json_str["event"]=="insert":
            doc=json_str["document"]
            #print("Inserting into database: ", doc)
            jp.db_insert(cursor, doc)

        elif json_str["event"]=="update":
            doc=json_str["document"]
            #print("Updating in database: ", doc)
            jp.db_update(cursor, doc)

        elif json_str["event"]=="delete":
            doc_id=json_str["documentKey"]
            #print("deleting from database: ", doc_id["_id"])
            jp.db_delete(cursor, doc_id["_id"])

        connection.commit()

    except Exception as e:
        print(f"Error connecting or loading data: {e}")



"""
str={"event": "insert", "document": {"_id": "6923ae31cdaac97078b0cb32", "parkId": "77E0D7F0-1942-494A-ACE2-9004D2BDC59E", "parkCode": "abli", "parkname": "Abraham Lincoln Birthplace", "fullName": "Abraham Lincoln Birthplace National Historical Park", "url": "https://www.nps.gov/abli/index.htm", "description": "For over a century people from around the world have come to rural Central Kentucky to honor the humble beginnings of our 16th president, Abraham Lincoln. His early life on Kentucky"s frontier shaped his character and prepared him to lead the nation through Civil War. Visit our country"s first memorial to Lincoln, built with donations from young and old, and the site of his childhood home.", "designation": "National Historical Park", "latitude": "37.5858662", "longitude": "-85.67330523", "states": "KY", "directionURL": "http://www.nps.gov/abli/planyourvisit/directions.htm", "directionInfo": "The Birthplace Unit of the park is located approximately 2 miles south of the town of Hodgenville on U.S. Highway 31E South. The Boyhood Home Unit at Knob Creek is located approximately 10 miles northeast of the Birthplace Unit of the park.", "weatherInfo": "There are four distinct seasons in Central Kentucky. However, temperature and weather conditions can vary widely within those seasons. Spring and Fall are generally pleasant with frequent rain showers. Summer is usually hot and humid. Winter is moderately cold with mixed precipitation.", "country": "USA", "lastUpdatedDate": "2025-12-25T22:17:53.110Z", "activities": [{"id": "0B685688-3405-4E2A-ABBA-E3069492EC50", "activity": "Wildlife Watching"}, {"id": "0C0D142F-06B5-4BE1-8B44-491B90F93DEB", "activity": "Park Film"}, {"id": "13A57703-BB1A-41A2-94B8-53B692EB7238", "activity": "Astronomy"}, {"id": "1DFACD97-1B9C-4F5A-80F2-05593604799E", "activity": "Food"}, {"id": "24380E3F-AD9D-4E38-BF13-C8EEB21893E7", "activity": "Shopping"}, {"id": "42FD78B9-2B90-4AA9-BC43-F10E9FEA8B5A", "activity": "Hands-On"}, {"id": "B33DC9B6-0B7D-4322-BAD7-A13A34C584A3", "activity": "Guided Tours"}, {"id": "C8F98B28-3C10-41AE-AA99-092B3B398C43", "activity": "Museum Exhibits"}, {"id": "DF4A35E0-7983-4A3E-BC47-F37B872B0F25", "activity": "Junior Ranger Program"}], "contactDetails": [{"contactId": "1", "contact": "+12703583127", "contactTypeId": "2", "contactType": "Voice"}, {"contactId": "2", "contact": "+12703583874", "contactTypeId": "3", "contactType": "Fax"}, {"contactId": "3", "contact": "ABLI_Administration@nps.gov", "contactTypeId": "1", "contactType": "Email"}]}}
cdc_db_insert(str)

str={"event": "update", "document": {"_id": "6923ae31cdaac97078b0cb58", "parkId": "3262234F-A56A-447D-AE6C-F5C734ABD3A4", "parkCode": "biho", "parkname": "Big Holes", "fullName": "Big Hole National Battlefield", "url": "https://www.nps.gov/biho/index.htm", "description": "On August 9, 1877, gun shots shattered a chilly dawn on a sleeping camp of Nez Perce. By the time the smoke cleared on August 10, almost 90 Nez Perce were dead along with 31 soldiers and volunteers. Big Hole National Battlefield was created to honor all who were there.", "designation": "National Battlefield", "latitude": "45.64647324", "longitude": "-113.6458443", "states": "MT", "directionURL": "https://www.nps.gov/biho/planyourvisit/directions.htm", "directionInfo": "Big Hole National Battlefield is located on Highway 43 ten miles west of the town of Wisdom in southwestern Montana. Bear Paw Battlefield is located on Route 240 sixteen miles south of the town of Chinook in north-central Montana.", "weatherInfo": "This climatic region is typified by large seasonal temperature differences, with warm to hot (and often humid) summers and cold (sometimes severely cold) winters. Wisdom has a humid continental climate.", "country": "USA", "lastUpdatedDate": "2025-11-27T23:56:33.486Z", "activities": [{"id": "01D717BC-18BB-4FE4-95BA-6B13AD702038", "activity": "Snowshoeing"}, {"id": "09DF0950-D319-4557-A57E-04CD2F63FF42", "activity": "Arts and Culture"}, {"id": "0B685688-3405-4E2A-ABBA-E3069492EC50", "activity": "Wildlife Watching"}, {"id": "0C0D142F-06B5-4BE1-8B44-491B90F93DEB", "activity": "Park Film"}, {"id": "1DFACD97-1B9C-4F5A-80F2-05593604799E", "activity": "Food"}, {"id": "24380E3F-AD9D-4E38-BF13-C8EEB21893E7", "activity": "Shopping"}, {"id": "AE42B46C-E4B7-4889-A122-08FE180371AE", "activity": "Fishing"}, {"id": "B33DC9B6-0B7D-4322-BAD7-A13A34C584A3", "activity": "Guided Tours"}, {"id": "BFF8C027-7C8F-480B-A5F8-CD8CE490BFBA", "activity": "Hiking"}, {"id": "C8F98B28-3C10-41AE-AA99-092B3B398C43", "activity": "Museum Exhibits"}, {"id": "DF4A35E0-7983-4A3E-BC47-F37B872B0F25", "activity": "Junior Ranger Program"}, {"id": "F9B1D433-6B86-4804-AED7-B50A519A3B7C", "activity": "Skiing"}], "contactDetails": [{"contactId": "89", "contact": "+14066893155", "contactTypeId": "2", "contactType": "Voice"}, {"contactId": "90", "contact": "biho_visitor_information@nps.gov", "contactTypeId": "1", "contactType": "Email"}]}, "updateDescription": {"updatedFields": {"parkname": "Big Holes"}, "removedFields": [], "truncatedArrays": []}}
cdc_db_insert(str)

str={"event": "delete", "documentKey": {"_id": "6923ae31cdaac97078b0cb58"}}
cdc_db_insert(str)
"""