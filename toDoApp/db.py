from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

def create_tables(Base):
  """
  This is to initialize the database tables.
  it is supposed to be called from outside and create the
  tables of metadata extracted from the Base object passed
  as parameter.
  """
  base.metadata.create_all(engine)

def add_user(User):
  pass

def remove_user(user_id):
  pass

def add_task(Task):
  pass

def remove_task(task_id):
  pass

def find_user(user_id):
  pass

def edit_task(task_id):
  pass

def edit_user(user_id):
  pass


