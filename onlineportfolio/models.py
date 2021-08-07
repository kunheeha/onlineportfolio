from onlineportfolio import db, login_manager
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(user_id):
    return Person.query.get(int(user_id))


class Person(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cv_file = db.Column(db.String(20), nullable=True)
    personal_statement = db.Column(db.String(500), nullable=False)

    def __repr__(self, *args):
        return f"'{self.name}', '{self.email}'"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(12), unique=True, nullable=False)
    profile_photo = db.Column(db.String(20), nullable=True)
    cv_file = db.Column(db.String(20), nullable=True)
    personal_statement = db.Column(db.Text(), nullable=False)

class Skill(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    skill_name = db.Column(db.String(30), nullable=False)
    proficiency_level = db.Column(db.Integer(), nullable=False)

class PSkill(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class WebProjectSkills(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    web_project_id = db.Column(db.Integer(), db.ForeignKey('web_project.id', ondelete='CASCADE'))
    p_skill_id = db.Column(db.Integer(), db.ForeignKey('p_skill.id', ondelete='CASCADE'))

class SoftwareProjectSkills(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    software_project_id = db.Column(db.Integer(), db.ForeignKey('software_project.id', ondelete='CASCADE'))
    p_skill_id = db.Column(db.Integer(), db.ForeignKey('p_skill.id', ondelete='CASCADE'))

class SoftwareProject(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    source_code = db.Column(db.String(50), nullable=False)
    windows_file = db.Column(db.String(20), nullable=True)
    macos_file = db.Column(db.String(20), nullable=True)
    linux_file = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text(), nullable=False)
    installation_guide = db.Column(db.String(20), nullable=True)
    user_guide = db.Column(db.String(20), nullable=True)
    upcoming_functionality = db.Column(db.Text(), nullable=True)
    images = db.Column(db.String(50), nullable=False)
    skills = db.relationship('PSkill', secondary='software_project_skills')

class WebProject(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    source_code = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    user_guide = db.Column(db.String(20), nullable=True)
    upcoming_functionality = db.Column(db.Text(), nullable=True)
    images = db.Column(db.String(50), nullable=False)
    skills = db.relationship('PSkill', secondary='web_project_skills')
