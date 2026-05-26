from SimpleSQLDB.simplecrud import SimpleCRUD


class SimpleCreateTables:
    def __init__(self) -> None:
        self.usersfields = ("email", "password")

    def create(self, simplecrud: SimpleCRUD):
        simplecrud.create_table(
            "userid",
            self.usersfields,
            ("varchar(255) NOT NULL", "varchar(255) NOT NULL"),
            "users",
        )
