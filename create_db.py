from db_init import db, create_app, models
db.create_all(app=create_app())
