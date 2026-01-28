from app import create_app, db
from app.models.role import Role

app = create_app()
app.app_context().push()

if not Role.query.first():
    db.session.add(Role(id=1, name="Usuario"))
    db.session.add(Role(id=2, name="Administrador"))
    db.session.commit()
    print("Roles creados")
else:
    print("Roles ya existen")