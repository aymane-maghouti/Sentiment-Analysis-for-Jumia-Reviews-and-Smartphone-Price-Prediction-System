import mysql.connector
import pandas as pd
import pickle


def contineus_learning():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="aymane2002",
        database="smartphone_db"
    )


    def fetch_data():
        cursor = conn.cursor()

        try:
            select_query = "SELECT * FROM smartphone"

            cursor.execute(select_query)

            rows = cursor.fetchall()

            # Obtenez les noms de colonnes à partir de la description du curseur
            columns = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(rows, columns=columns)

            return df

        except mysql.connector.Error as err:
            print("Erreur lors de la récupération des données:", err)

        finally:
            cursor.close()
            conn.close()

    dataframe = fetch_data()


    def map_brand_to_numeric(brand):
        brand_mapping = {
            'Maxfone': 1,
            'Infinix': 2,
            'Freeyond': 3,
            'XIAOMI': 4,
            'Tecno': 5,
            'Oppo': 6,
            'Nokia': 7,
            'Samsung': 8,
            'Huawei': 9,
            'Vivo': 10,
            'Realme': 11,
            'Sowhat': 12,
            'Apple': 13,
            'Gionee': 14
        }

        # Use the get method to handle cases where the brand is not in the mapping
        return brand_mapping.get(brand, 0)


    dataframe['brand'] = dataframe['brand'].apply(map_brand_to_numeric)


    def map_sim_type_to_numeric(sim_type):
        sim_type_mapping = {
            'Dual': 1,
            'Single': 2,
        }

        return sim_type_mapping.get(sim_type, 0)


    dataframe['sim_type'] = dataframe['sim_type'].apply(map_sim_type_to_numeric)


    with open('models/xgb_model.pkl', 'rb') as file:
        model = pickle.load(file)

    X = dataframe[["brand",  "screen_size",  "ram",  "rom",  "sim_type",  "battery"]]
    y = dataframe["price"]

    model.fit(X,y)

    with open('models/xgb_model.pkl', 'wb') as file:
        pickle.dump(model, file)



    print(dataframe)

