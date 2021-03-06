from .. import db


class ValidatedAudio(db.Model):
    __tablename__ = 'validated_audio'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    file_name = db.Column(
        db.String(500)
    )
    created_at = db.Column(
        db.DateTime
    )
    created_by = db.Column(
        db.String(100)
    )
    validator_skill_level = db.Column(
        db.Integer
    )
    expected_language_code = db.Column(
        db.String(100)
    )
    validation_value = db.Column(
        db.String(100)
    )
    video_id = db.Column(
        db.String(100)
    )
    video_title = db.Column(
        db.String(500)
    )

    def _asdict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<ValidatedAudio {}>'.format(self.file_name)
