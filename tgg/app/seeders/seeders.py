import os
from sqlalchemy.orm import Session

from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder
from app.models.V1.users import User


def seed_data(db: Session)->bool:
    
    user = db.query(User).filter(User.username=="admin").first()
    if not user:
        # load entities
        entities = load_entities_from_json(os.path.join("app", "seeders", "data_seeders.json"))
        # Initializing Seeder
        seeder = Seeder(db)
        # Seeding
        seeder.seed(entities)
        # Committing
        db.commit()
        return True
    return False