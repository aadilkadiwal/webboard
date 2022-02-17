# Django Web Board

This project is a discussion board (a forum). The whole idea is to maintain several boards, which will behave like categories. Inside a specific board, a user can start a new discussion by creating a new topic. In this topic, other users can engage in the discussion posting replies.

## Running the Project on Local Machine
--- 
Open Command Prompt and set a path where the project is cloned or downloaded.

For Example, My Project is located on the desktop.

```
    C:\Users\Shaan\Desktop\webboard
```

### PostgreSQL Database
---
Setup database based on your OS. Please also install Postgis plugin for postgresql and postgresql-contrib package for pgcrypto. You can then create a DB as follows

Enter into postgres(superuser) user's shell

```
    sudo -u postgres -i
```

Copy paste below commands till EOF and press enter:

```
    export DB_NAME=webboard
    export DB_OWNER=$DB_NAME
    export DB_PASSWORD=devpassword
    psql <<EOF
    CREATE USER $DB_OWNER WITH PASSWORD '$DB_PASSWORD';
    ALTER ROLE $DB_OWNER SET client_encoding TO 'utf8';
    ALTER ROLE $DB_OWNER SET default_transaction_isolation TO 'read committed';
    ALTER ROLE $DB_OWNER SET timezone TO 'UTC';
    CREATE DATABASE  $DB_NAME WITH ENCODING='UTF8' OWNER='$DB_OWNER';
    EOF
```

### On Local Machine
---
Make sure that in your system **python** is installed and the python --version should be **3.6** or **above**.

With the help of pip, a tool to manage and install python packages, to install **virtualenv**.

```
    C:\Users\Shaan\Desktop\webboard>pip install virtualenv
```

After installing **virtualenv** let's create it.

```
    C:\Users\Shaan\Desktop\webboard>virtualenv venv
```

Now your webboard directory looks like:

* webboard
  * src
  * venv
  * requirements.txt

Virtual Environement is created, to **activate** it.

```
    C:\Users\Shaan\Desktop\webboard>source venv/bin/activate
```
Your Command Prompt looks like:

```
    (venv) C:\Users\Shaan\Desktop\webboard>
```

For installing all dependencies.

```
    (venv) C:\Users\Shaan\Desktop\webboard>pip install -r requirements.txt
```

After installing all libraries. Now it's time to run a project.Before that you have to go in src folder.

```
    (venv) C:\Users\Shaan\Desktop\webboard>cd src
```

Before running your project your Command Prompt should look like:

```
    (venv) C:\Users\Shaan\Desktop\webboard\src>
```

Run migrations:

```
    (venv) C:\Users\Shaan\Desktop\webboard\src>python manage.py migrate
```

Finally, run the development server:

```
    (venv) C:\Users\Shaan\Desktop\webboard\src>python manage.py runserver
```

The **Project** will be available at:**http://127.0.0.1:8000**