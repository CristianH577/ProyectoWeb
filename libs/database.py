import mysql.connector

class Database:
    answer = {
        "bool": True,
        "type": 'error',
        "class": 'Database',
        "function": '',
        "detail": '',
        "value": ''
    }

    def __init__(self):
        # print('Database')
        self.answer['function'] = '__init__'
        try:
            connect = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                db="proyectoweb_bd"
            )

            if connect.is_connected():
                self.connect = connect
            else:
                self.answer['bool'] = False
                self.answer['detail'] = 'no connected'

        except Exception as e:
            self.answer['bool'] = False
            self.answer['detail'] = 'cant get connected'
            self.answer['value'] = str(e)

    def ADD(self, table, fields, values):
        # print('ADD')
        self.answer['function'] = 'ADD'
        
        cols = "(" + ", ".join(fields) + ")"

        val = "("
        for i in range(len(fields)):
            val = val + "%s, "
        val = val.rstrip(", ")
        val = val + ")"

        query = "INSERT INTO " + table + cols + " VALUES " + val
        
        values = tuple(values)
    
        connect = self.connect
        if connect:
            try:
                cursor = connect.cursor()
                cursor.execute(query, values)
                result = cursor.rowcount
                connect.commit()

                self.answer['value'] = result

            except Exception as e:
                self.answer['bool'] = False
                self.answer['detail'] = 'cant execute'
                self.answer['value'] = str(e)
                
            connect.close()

        return self.answer

    def UPDATE(self, table, fields, where, values):
        # print('UPDATE')
        self.answer['function'] = 'UPDATE'

        set = ""
        for f in fields:
            set = set + str(f) + "=%s, "
        set = set.rstrip(', ')

        query = "UPDATE " + table + " SET " + set + " WHERE " + where
        
        values = tuple(values)
        
        connect = self.connect
        if connect:
            try:
                cursor = connect.cursor()
                cursor.execute(query, values)
                result = cursor.rowcount
                connect.commit()

                self.answer['value'] = result

            except Exception as e:
                self.answer['bool'] = False
                self.answer['detail'] = 'cant execute'
                self.answer['value'] = str(e)

            connect.close()
        return self.answer

    def DELETE(self, table, where):
        # print('DELETE')
        self.answer['function'] = 'DELETE'
        
        query = "DELETE FROM " + table + " WHERE " + where
    
        connect = self.connect
        if connect:
            try:
                cursor = connect.cursor()
                cursor.execute(query)
                result = cursor.rowcount
                connect.commit()

                self.answer['value'] = result
            except Exception as e:
                self.answer['bool'] = False
                self.answer['detail'] = 'cant execute'
                self.answer['value'] = str(e)
                
            connect.close()

        return self.answer

    def SELECT(self, table, select, where):
        # print('SELECT')
        self.answer['function'] = 'SELECT'

        query = "SELECT " + select + " FROM " + table

        if where:
            query = query + " WHERE " + where

        connect = self.connect
        if connect:
            try:
                cursor = connect.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                
                self.answer['value'] = result
            except Exception as e:
                self.answer['bool'] = False
                self.answer['detail'] = 'cant execute'
                self.answer['value'] = str(e)

            connect.close() 
        return self.answer
    
    def COUNT(self, table, count, where):
        # print('COUNT')
        self.answer['function'] = 'COUNT'

        query = "SELECT COUNT(" + count + ") FROM " + table

        if where:
            query = query + " WHERE " + where

        connect = self.connect
        if connect:
            try:
                cursor = connect.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                
                self.answer['value'] = result[0]
            except Exception as e:
                self.answer['bool'] = False
                self.answer['detail'] = 'cant execute'
                self.answer['value'] = str(e)
                
            connect.close()

        return self.answer