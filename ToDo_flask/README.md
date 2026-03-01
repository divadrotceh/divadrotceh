This is a To Do Application built usign Flask
The Database management is implemented using sqlite3

It has two different tables separated in two ".db" files (This is only for better management during development)

Main Features:
- Create a User Account (account stored locally with sqlite3)
- Create tasks only with an account registered
- Edit only the owned tasks per user
- Show all the tasks owned by the registered user
- Token Authentication implemented in the Session
- Session Management
- Cookies Management
- Add Jinga2 for HTML Templates

Basic HTML with Jinga2 made by me, all desgin style made by IA.

- Detailed db management /db/db_controller-
  For learning purposes al the database management is implemented using SQL querys,
  Create tables, conditional selection of data, edit data, insert new values.
  All these have its own data validation to avoid SQL injections.
  Data is stored in memory. and there is no relational data (to implement after).

- Authentication /auth.py-
  Is made by sessions management. Once login, creates a session with JWT token included.
  This is validated every request, for future implementations, add time ended sessions.
  It checks username already in use and uses hashed passwords with SHA1.

- Main menu /views.py-
  It only has features for:
  - Task creation
  - Task data updates manually (there is no frontend for this, it should be by curl)
  - Tasks are made only by the name. The app automatically adds creation's date, unique id (UUID4)
    and is completed flag.
  - There are superuser API endpoint but only possible usage via curl.
  - Usage of bluepring to easy scalability.
