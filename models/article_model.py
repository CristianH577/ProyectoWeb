from libs.database import Database

class ArticleClass:
    model = {}
    columns = ['id_art','id_item','id_user','price','amount','info','detail', 'date_register']
    table = "articles"
    answer = {
        "bool": True,
        "class": 'ArticleClass',
        "function": '',
        "detail": '',
        "value": ''
    }

    def __init__(self):
        # print('ArticleClass')
        self.answer['function'] = '__init__'
        for i in self.columns:
            self.model[i] = ''

    # ------ DB modify ------ #
    def Add(self):
        # print('Add')
        db = Database()
        if db.answer['bool']:
            self.answer['function'] = 'Add'

            fields = ('id_item','id_user','price','amount','info','detail')

            values = []
            for f in fields:
                values.append(self.model[f])
            values = tuple(values)

            add = db.ADD(self.table, fields, values)
            if add['bool']:
                self.answer['value'] = add['value']
            else:
                self.answer = add
        else:
            self.answer = db.answer

        return self.answer
    
    def Delete(self):
        # print('Delete')
        db = Database()
        if db.answer['bool']:
            self.answer['function'] = 'Delete'

            id = self.model['id_art']
            if len(id) > 1:
                where = "id_art IN " + str(tuple(id))
            else:
                where = "id_art=" + str(id[0])

            delete = db.DELETE(self.table, where)
            if delete['bool']:
                self.answer['value'] = delete['value']
            else:
                self.answer = delete
        else:
            self.answer = db.answer

        return self.answer

    # ------ DB get data ------ #
    def GetData(self, select, where):
        # print('GetData')
        db = Database()
        if db.answer['bool']:
            self.answer['function'] = 'GetData'
            select = db.SELECT(self.table, select, where)
            if select['bool']:
                self.answer['value'] = select['value']
            else:
                self.answer = select
        else:
            self.answer = db.answer

        return self.answer
    
    def Count(self, count, where):
        # print('Count')
        db = Database()
        if db.answer['bool']:
            self.answer['function'] = 'Count'
            select = db.COUNT(self.table, count, where)
            if select['bool']:
                self.answer['value'] = select['value']
            else:
                self.answer = select
        else:
            self.answer = db.answer

        return self.answer
    
    # ------ SET/GET ------ #
    def set(self, param, value):
        if param in self.model:
            self.model[param] = value

    def get(self, param):
        if param in self.model:
            return self.model[param]
        
        return False