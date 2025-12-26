def transpose_park(doc):
    return {
        "id": doc.get("_id"),
        "parkId": doc.get("parkId"),
        "parkCode": doc.get("parkCode"),
        "name": doc.get("parkName"),
        "fullName": doc.get("fullName"),
        "url": doc.get("url"),
        "description": doc.get("description"),
        "designation": doc.get("designation"),
        "latitude": doc.get("latitude"),
        "longitude": doc.get("longitude"),
        "states": doc.get("states"),
        "directionURL": doc.get("directionURL"),
        "directionInfo": doc.get("directionInfo"),
        "weatherInfo": doc.get("weatherInfo"),
        "country": doc.get("country"),
        "lastUpdatedDate": doc.get("lastUpdatedDate")
    }

def transpose_activities(doc):
    park_id = doc.get("_id")
    activities = doc.get("activities", [])
    return [(park_id, a["id"], a["activity"])
            for a in activities]

def transpose_contacts(doc):
    park_id = doc.get("_id")
    contacts = doc.get("contactDetails", [])
    return [(park_id, c["contactId"], c["contact"], c["contactTypeId"], c["contactType"])
            for c in contacts]

def insert_into_park(cursor, park):
    sql = """INSERT INTO park 
             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,current_timestamp,NULL,current_timestamp)"""

    values = [
            park["id"], park["parkId"], park["parkCode"], park["name"],
            park["fullName"], park["url"], park["description"],
            park["designation"], park["latitude"], park["longitude"],
            park["states"], park["directionURL"], park["directionInfo"],
            park["weatherInfo"], park["country"], park["lastUpdatedDate"]
        ]

    cursor.execute(sql, values)

def insert_into_activities(cursor, activity_rows):
    sql = """INSERT INTO park_activity (_id, activity_Id, activity, load_dtm)
             VALUES (%s, %s, %s, current_timestamp)"""
    cursor.executemany(sql, activity_rows)

def insert_into_contacts(cursor, contact_rows):
    sql = """INSERT INTO park_contact (_id, contact_Id, contact_medium, contact_Type_Id, contact_Type, load_dtm)
             VALUES (%s, %s, %s, %s, %s, current_timestamp)"""
    cursor.executemany(sql, contact_rows)

def update_parks(cursor, park):
    park_sql = """update park 
                  set park_id=%s, park_code=%s, park_name=%s, full_name=%s, url=%s, description=%s, designation=%s, latitude=%s, 
                      longitude=%s, states=%s, direction_url=%s, direction_info=%s, weather_info=%s, country=%s, last_updated_date=%s,
                      load_dt = current_timestamp 
                  where _id=%s and end_date is null"""
    values = [
            park["parkId"], park["parkCode"], park["name"], park["fullName"],
            park["url"], park["description"], park["designation"], park["latitude"],
            park["longitude"], park["states"], park["directionURL"], park["directionInfo"],
            park["weatherInfo"], park["country"], park["lastUpdatedDate"],park["id"]
        ]
    cursor.execute(park_sql, values)

    print(park_sql, values)

def update_activities(cursor, activity_rows, park_id):
    activity_sql = "delete from park_activity where _id=%s"
    cursor.execute(activity_sql, (park_id,))
    sql = """INSERT INTO park_activity (_id, activity_Id, activity, load_dtm)
             VALUES (%s, %s, %s, current_timestamp)"""
    cursor.executemany(sql, activity_rows)

def update_contacts(cursor, contact_rows, park_id):
    contact_sql = "delete from park_contact where _id=%s"
    cursor.execute(contact_sql, (park_id,))
    sql = """INSERT INTO park_contact (_id, contact_Id, contact_medium, contact_Type_Id, contact_Type, load_dtm)
             VALUES (%s, %s, %s, %s, %s, current_timestamp)"""
    cursor.executemany(sql, contact_rows)

def db_insert(cursor, doc):
    park = transpose_park(doc)
    insert_into_park(cursor, park)
    activities = transpose_activities(doc)
    contacts = transpose_contacts(doc)
    if activities:
        insert_into_activities(cursor, activities)
    if contacts:
        insert_into_contacts(cursor, contacts)

def db_delete(cursor, doc_id):
    park_sql = "update park set end_date = current_timestamp, load_dt=current_timestamp, last_Updated_Date=current_timestamp where _id=%s"
    activity_sql = "delete from park_activity where _id=%s"
    contact_sql = "delete from park_contact where _id=%s"
    cursor.execute(park_sql, (doc_id,))
    cursor.execute(activity_sql, (doc_id,))
    cursor.execute(contact_sql, (doc_id,))

def db_update(cursor, doc):
    doc_id = doc["_id"]
    park = transpose_park(doc)
    activities = transpose_activities(doc)
    contacts = transpose_contacts(doc)
    update_parks(cursor, park)
    update_activities(cursor, activities, doc_id)
    update_contacts(cursor, contacts, doc_id)
