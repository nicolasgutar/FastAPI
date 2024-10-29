#Script para cargar csv a SQL desde python

connection = psycopg2.connect(host = 'localhost',
                              database = 'northwind_olap',
                              user='user',
                              password = 'password',
                              port=5432)

cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS CropData")



