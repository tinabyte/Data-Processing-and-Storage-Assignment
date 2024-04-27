class InMemoryDB:
    def __init__(self):
        self.main_db = {}
        self.transaction_active = False
        self.transaction_db = {}

    def get(self, key):
        if self.transaction_active and key in self.transaction_db:
            return self.transaction_db[key]
        return self.main_db.get(key, None)

    def put(self, key, value):
        if not self.transaction_active:
            raise Exception("Transaction not in progress. Start a transaction before modifying the database.")
        self.transaction_db[key] = value

    def begin_transaction(self):
        if self.transaction_active:
            raise Exception("Another transaction is already in progress.")
        self.transaction_active = True
        self.transaction_db = {}

    def commit(self):
        if not self.transaction_active:
            raise Exception("No transaction is active to commit.")
        self.main_db.update(self.transaction_db)
        self.transaction_active = False
        self.transaction_db = {}

    def rollback(self):
        if not self.transaction_active:
            raise Exception("No transaction is active to rollback.")
        self.transaction_active = False
        self.transaction_db = {}

# Example usage and testing based on the provided cases
if __name__ == "__main__":
    db = InMemoryDB()

    print(db.get("A"))  # Should print: None

    try:
        db.put("A", 5)
    except Exception as e:
        print(e)  # Should print: Transaction not in progress. Start a transaction before modifying the database.

    db.begin_transaction()
    db.put("A", 5)
    print(db.get("A"))  # Should print: None (value not visible until committed)

    db.put("A", 6)
    print(db.get("A"))  # Should print: None (value not visible until committed)

    db.commit()
    print(db.get("A"))  # Should print: 6

    try:
        db.commit()
    except Exception as e:
        print(e)  # Should print: No transaction is active to commit.

    try:
        db.rollback()
    except Exception as e:
        print(e)  # Should print: No transaction is active to rollback.

    print(db.get("B"))  # Should print: None

    db.begin_transaction()
    db.put("B", 10)
    db.rollback()
    print(db.get("B"))  # Should print: None
