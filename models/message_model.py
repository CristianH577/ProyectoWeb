from libs.database import Database

class MessageClass:
    model = {}
    columns = ['id_msg','allowed','id_user','email','subject','content','answer']
    table = "messages"
    answer = {
        "bool": True,
        "class": 'MessageClass',
        "function": '',
        "detail": '',
        "value": ''
    }

    def __init__(self):
        # print('MessageClass')
        self.answer['function'] = '__init__'
        for i in self.columns:
            self.model[i] = ''

    # ------ DB modify ------ #
    def Add(self):
        # print('Add')
        db = Database()
        if db.answer['bool']:
            self.answer['function'] = 'Add'

            fields = ['allowed','id_user','email','subject','content','answer']

            values = []
            for f in fields:
                values.append(self.model[f])

            add = db.ADD(self.table, fields, values)
            if add['bool']:
                self.answer['value'] = add['value']
            else:
                self.answer = add
        else:
            self.answer = db.answer

        return self.answer

    def Update(self):
        # print('Update')
        db = Database()
        if db.answer['bool']:
            self.answer['function'] = 'Update'

            if self.model['answer'] == '':
                fields = ['allowed']
            else:
                fields = ['allowed','answer']

            id = self.model['id_msg']
            if len(id) > 1:
                where = "id_msg IN " + str(tuple(id))
            else:
                where = "id_msg=" + str(id[0])

            values = []
            for f in fields:
                values.append(self.model[f])

            update = db.UPDATE(self.table, fields, where, values)
            if update['bool']:
                self.answer['value'] = update['value']
            else:
                self.answer = update
        else:
            self.answer = db.answer

        return self.answer

    def Delete(self):
        # print('Delete')
        db = Database()
        if db.answer['bool']:
            self.answer['function'] = 'Delete'

            id = self.model['id_msg']
            if len(id) > 1:
                where = "id_msg IN " + str(tuple(id))
            else:
                where = "id_msg=" + str(id[0])

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

    # ------ SET/GET ------ #
    def set(self, param, value):
        if param in self.model:
            self.model[param] = value

    def get(self, param):
        if param in self.model:
            return self.model[param]

        return False