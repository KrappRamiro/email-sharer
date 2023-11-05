https://fastapi.tiangolo.com/tutorial/sql-databases/

SQLAlchemy uses the term "model" to refer to the classes and instances that interact with the database.
But Pydantic also uses the term "model" to refer to something different, the data validation, conversion, and documentation classes and instances.

To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file models.py with the SQLAlchemy models, and the file schemas.py with the Pydantic models.

These Pydantic models define more or less a "schema" (a valid data shape).

So this will help us avoiding confusion while using both.
