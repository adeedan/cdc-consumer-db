import psycopg2 as pg
import configparser
from utils import jsonParse as jp

def cdc_db_insert(json_str):
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    db_host = config.get('Postgre', 'db_host')
    db_name = config.get('Postgre', 'db_name')
    db_user = config.get('Postgre', 'db_user')
    db_port = config.get('Postgre', 'db_port')
    db_password = config.get('Postgre', 'db_password')

    try:
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

json_string={"event": "delete", "documentKey": {"_id": "6923ae31cdaac97078b0cb58"}}
cdc_db_insert(json_string)

"""
str={"event": "insert", "document": {"_id": "6923ae31cdaac97078b0cb58", "parkId": "E84B1E08-CCE8-4FFF-8DB6-B92F40953226", "parkCode": "hello adridh", "parkname": "Arlington House, The Robert E. Lee Memorial", "fullName": "Arlington House, The Robert E. Lee Memorial", "url": "https://www.nps.gov/arho/index.htm", "description": "Arlington House is the nation\u2019s memorial to Robert E. Lee. It honors him for specific reasons, including his role in promoting peace and reunion after the Civil War. In a larger sense it exists as a place of study and contemplation of the meaning of some of the most difficult aspects of American history: military service; sacrifice; citizenship; duty; loyalty; slavery and freedom.", "designation": "", "latitude": 38.8822021484, "longitude": -77.0734786987, "states": "VA", "directionURL": "https://www.nps.gov/arho/planyourvisit/directions.htm", "directionInfo": "Public Transportation: The Memorial is accessible by the Blue Line of the Metro subway system. The Arlington Cemetery subway station is near the Visitor Center for the cemetery. Car: Arlington House is located inside Arlington National Cemetery. If you plan to come in a vehicle, the nearest parking is in the Arlington National Cemetery parking garage. From the entrance and Welcome Center at Arlington National Cemetery, one can walk up the hill to Arlington House (approximately 15 minutes-steep)", "weatherInfo": "Summers at Arlington House are generally hot and humid, with daytime highs frequently above 90 degrees Fahrenheit and scattered afternoon thunderstorms. Please carry water while participating in physical activity and be prepared to take shelter from lightning. Winters at Arlington are generally cold, with nighttime lows frequently near freezing and occasional snowfall. Please be alert for snowplows and icy spots on roadways. Weather during spring and fall is generally moderate, but can change quickly.", "country": "USA", "lastUpdatedDate": "2025-11-27T23:56:33.486000", "activities": [{"id": "B33DC9B6-0B7D-4322-BAD7-A13A34C584A3", "activity": "Guided Tours"}, {"id": "C8F98B28-3C10-41AE-AA99-092B3B398C43", "activity": "Museum Exhibits"}], "contactDetails": [{"contactId": "62", "contact": "+17032351530", "contactTypeId": "2", "contactType": "Voice"}, {"contactId": "63", "contact": "gwmp_superintendent@nps.gov", "contactTypeId": "1", "contactType": "Email"}], "createdAt": "2025-12-20T19:20:50.102000", "updatedAt": "2025-12-20T19:20:50.102000", "__v": 0}}
cdc_db_insert(str)

str={"event": "update", "document": {"_id": "6923ae31cdaac97078b0cb58", "parkId": "3262234F-A56A-447D-AE6C-F5C734ABD3A4", "parkCode": "biho", "parkname": "Big Holes", "fullName": "Big Hole National Battlefield", "url": "https://www.nps.gov/biho/index.htm", "description": "On August 9, 1877, gun shots shattered a chilly dawn on a sleeping camp of Nez Perce. By the time the smoke cleared on August 10, almost 90 Nez Perce were dead along with 31 soldiers and volunteers. Big Hole National Battlefield was created to honor all who were there.", "designation": "National Battlefield", "latitude": "45.64647324", "longitude": "-113.6458443", "states": "MT", "directionURL": "https://www.nps.gov/biho/planyourvisit/directions.htm", "directionInfo": "Big Hole National Battlefield is located on Highway 43 ten miles west of the town of Wisdom in southwestern Montana. Bear Paw Battlefield is located on Route 240 sixteen miles south of the town of Chinook in north-central Montana.", "weatherInfo": "This climatic region is typified by large seasonal temperature differences, with warm to hot (and often humid) summers and cold (sometimes severely cold) winters. Wisdom has a humid continental climate.", "country": "USA", "lastUpdatedDate": "2025-11-27T23:56:33.486Z", "activities": [{"id": "01D717BC-18BB-4FE4-95BA-6B13AD702038", "activity": "Snowshoeing"}, {"id": "09DF0950-D319-4557-A57E-04CD2F63FF42", "activity": "Arts and Culture"}, {"id": "0B685688-3405-4E2A-ABBA-E3069492EC50", "activity": "Wildlife Watching"}, {"id": "0C0D142F-06B5-4BE1-8B44-491B90F93DEB", "activity": "Park Film"}, {"id": "1DFACD97-1B9C-4F5A-80F2-05593604799E", "activity": "Food"}, {"id": "24380E3F-AD9D-4E38-BF13-C8EEB21893E7", "activity": "Shopping"}, {"id": "AE42B46C-E4B7-4889-A122-08FE180371AE", "activity": "Fishing"}, {"id": "B33DC9B6-0B7D-4322-BAD7-A13A34C584A3", "activity": "Guided Tours"}, {"id": "BFF8C027-7C8F-480B-A5F8-CD8CE490BFBA", "activity": "Hiking"}, {"id": "C8F98B28-3C10-41AE-AA99-092B3B398C43", "activity": "Museum Exhibits"}, {"id": "DF4A35E0-7983-4A3E-BC47-F37B872B0F25", "activity": "Junior Ranger Program"}, {"id": "F9B1D433-6B86-4804-AED7-B50A519A3B7C", "activity": "Skiing"}], "contactDetails": [{"contactId": "89", "contact": "+14066893155", "contactTypeId": "2", "contactType": "Voice"}, {"contactId": "90", "contact": "biho_visitor_information@nps.gov", "contactTypeId": "1", "contactType": "Email"}]}, "updateDescription": {"updatedFields": {"parkname": "Big Holes"}, "removedFields": [], "truncatedArrays": []}}
cdc_db_insert(str)

str={"event": "delete", "documentKey": {"_id": "6923ae31cdaac97078b0cb58"}}
cdc_db_insert(str)
"""