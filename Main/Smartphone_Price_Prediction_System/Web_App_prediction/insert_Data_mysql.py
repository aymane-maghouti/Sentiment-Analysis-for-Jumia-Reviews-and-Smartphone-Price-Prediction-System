import mysql.connector


def insert_Data(data):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="aymane2002",
        database="smartphone_db"
    )

    cursor = conn.cursor()

    try:
        insertion_query = "insert into smartphone (brand,screen_size,ram,rom,sim_type,battery,price) values (%s, %s, %s,%s, %s, %s,%s)"


        cursor.execute(insertion_query, data)

        conn.commit()

        print("Data inserted successfully!")

    except mysql.connector.Error as err:
        print("Error inserting data:", err)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


