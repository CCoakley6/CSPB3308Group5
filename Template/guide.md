How to set up PostgreSQL and pgAdmin (Windows)

https://www.postgresql.org/download/

Note: When you install this, please uncheck the pgAdmin. If you install it at the same, when you open it, it will load forever.

https://www.pgadmin.org/download/pgadmin-4-windows/

Note: download the version: 4 v 7.3


Please install the following packages to access your database.

`pip install psycopg2`

`pip install python-dotenv`

Please create a file called `.env` and copy and paste the following code

```
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'demo'  # Open your pgAdmin and create a database name and replace it
DB_USER = 'postgres'
DB_PASSWORD = 'admin123' # replace this with your own created password
```
