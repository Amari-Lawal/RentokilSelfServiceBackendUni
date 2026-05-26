from SQLDB.crud import CRUD


class CreateTables:
    def __init__(self) -> None:
        self.usersfields = ("email", "password")

    def create(self, crud: CRUD):
        crud.create_table(
            "userid",
            self.usersfields,
            ("varchar(255) NOT NULL", "varchar(255) NOT NULL"),
            "users",
        )
