class Table:

    def __init__(self):
        self._row_ids = []
        self._column_ids = []
        self._data = {}
        self._undo_stack = []
        self._redo_stack = []
    
    def add_row(self, row_id):
        '''
        Adds a new row to the table. 
        '''

        if row_id in self._row_ids:
            raise KeyError("Row already exists.")
        
        self._row_ids.append(row_id)
        row_index = len(self._row_ids) - 1

        self._data[row_id] = {}
        for col_id in self._column_ids:
            self._data[row_id][col_id] = None
        
        # create history entry
        payload = {}
        payload['row_id'] = row_id
        payload['row_index'] = row_index

        entry = {}
        entry['action_type'] = 'add_row'
        entry['payload'] = payload

        self._undo_stack.append(entry)
        self._redo_stack.clear()


    def remove_row(self, row_id):
        '''
        Removes a row from the table.
        '''

        if not row_id in self._row_ids:
            raise KeyError("Row does not exist.")
        
        row_index = self._row_ids.index(row_id)
        self._row_ids.pop(row_index)

        row_data = self._data[row_id]
        del self._data[row_id]

        # create history entry
        payload = {}
        payload['row_id'] = row_id
        payload['row_index'] = row_index
        payload['row_data'] = row_data

        entry = {}
        entry['action_type'] = "remove_row"
        entry['payload'] = payload

        self._undo_stack.append(entry)
        self._redo_stack.clear()


    def add_column(self, col_id):
        '''
        Adds a new col to the table. 
        '''

        if col_id in self._column_ids:
            raise KeyError("Column already exists.")
        
        self._column_ids.append(col_id)
        col_index = len(self._column_ids) - 1

        for row_id in self._row_ids:
            self._data[row_id][col_id] = None
        
        # create history entry
        payload = {}
        payload['col_id'] = col_id
        payload['col_index'] = col_index

        entry = {}
        entry['action_type'] = 'add_column'
        entry['payload'] = payload

        self._undo_stack.append(entry)
        self._redo_stack.clear()

    def remove_column(self, col_id):
        '''
        Removes a column from the table.
        '''

        if not col_id in self._column_ids:
            raise KeyError("Column does not exist.")
        
        col_index = self._column_ids.index(col_id)
        self._column_ids.pop(col_index)

        col_data = {}
        for row_id in self._row_ids:
            col_data[row_id] = self._data[row_id][col_id]
            del self._data[row_id][col_id]

        # create history entry
        payload = {}
        payload['col_id'] = col_id
        payload['col_index'] = col_index
        payload['col_data'] = col_data

        entry = {}
        entry['action_type'] = "remove_column"
        entry['payload'] = payload

        self._undo_stack.append(entry)
        self._redo_stack.clear()

    def set_cell(self, row_id, col_id, new_value):
        '''
        Sets the new value in cell at (row_id, col_id). 
        '''

        # Validate row id and cell id
        if not row_id in self._row_ids or not col_id in self._column_ids:
            raise KeyError("Cell does not exist.")
        
        old_value = self._data[row_id][col_id]
        if old_value == new_value:
            return

        self._data[row_id][col_id] = new_value

        # create history entry
        payload = {}
        payload['row_id'] = row_id
        payload['col_id'] = col_id
        payload['old_value'] = old_value
        payload['new_value'] = new_value

        entry = {}
        entry['action_type'] = 'set_cell'
        entry['payload'] = payload

        self._undo_stack.append(entry)
        self._redo_stack.clear()


    def undo(self):
        '''
        Undo the most recent history entry.
        '''
        if not self._undo_stack:
            return

        last_entry = self._undo_stack.pop()

        action_type = last_entry['action_type']

        if action_type == 'set_cell':
            row_id = last_entry['payload']['row_id']
            col_id = last_entry['payload']['col_id']
            old_value = last_entry['payload']['old_value']

            self._data[row_id][col_id] = old_value
        
        elif action_type == 'add_row':
            row_id = last_entry['payload']['row_id']
            row_index = last_entry['payload']['row_index']
            
            self._row_ids.pop(row_index)
            del self._data[row_id]

        elif action_type == 'remove_row':
            row_id = last_entry['payload']['row_id']
            row_index = last_entry['payload']['row_index']
            row_data = last_entry['payload']['row_data']

            self._row_ids.insert(row_index, row_id)
            self._data[row_id] = row_data

        elif action_type == 'add_column':
            col_id = last_entry['payload']['col_id']
            col_index = last_entry['payload']['col_index']
            
            self._column_ids.pop(col_index)
            for row_id in self._row_ids:
                del self._data[row_id][col_id]

        elif action_type == 'remove_column':
            col_id = last_entry['payload']['col_id']
            col_index = last_entry['payload']['col_index']
            col_data = last_entry['payload']['col_data']

            self._column_ids.insert(col_index, col_id)
            for row_id in self._row_ids:
                self._data[row_id][col_id] = col_data[row_id]

        self._redo_stack.append(last_entry)

    def redo(self):
        '''
        Redo the most recent history entry.
        '''
        if not self._redo_stack:
            return

        last_entry = self._redo_stack.pop()

        action_type = last_entry['action_type']

        if action_type == 'set_cell':
            row_id = last_entry['payload']['row_id']
            col_id = last_entry['payload']['col_id']
            new_value = last_entry['payload']['new_value']

            self._data[row_id][col_id] = new_value
        
        elif action_type == 'add_row':
            row_id = last_entry['payload']['row_id']
            row_index = last_entry['payload']['row_index']

            self._row_ids.insert(row_index, row_id)
            self._data[row_id] = {}
            for col_id in self._column_ids:
                self._data[row_id][col_id] = None
            
        elif action_type == "remove_row":
            row_id = last_entry['payload']['row_id']
            row_index = last_entry['payload']['row_index']
            
            self._row_ids.pop(row_index)
            del self._data[row_id]
        
        elif action_type == "add_column":
            col_id = last_entry['payload']['col_id']
            col_index = last_entry['payload']['col_index']

            self._column_ids.insert(col_index, col_id)
            for row_id in self._row_ids:
                self._data[row_id][col_id] = None
        
        elif action_type == "remove_column":
            col_id = last_entry['payload']['col_id']
            col_index = last_entry['payload']['col_index']
            
            self._column_ids.pop(col_index)
            for row_id in self._row_ids:
                del self._data[row_id][col_id] 

        self._undo_stack.append(last_entry)