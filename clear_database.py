from database.db import session, Machine

session.query(Machine).delete()

session.commit()

print("All machine data deleted successfully")