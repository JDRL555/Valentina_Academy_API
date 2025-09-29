from mongoengine import connect

def connectToMongo(db: str, host: str, port: int):
  connect(db=db, host=host, port=port)