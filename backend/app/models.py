from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, login, db
from flask import session, url_for
import json
import base64
import os


users = db.Table('users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id'), primary_key=True)
)


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(UserMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(140))
    gender = db.Column(db.String(32))
    access = db.Column(db.Integer, default=0)
    
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)


    def is_manager_of(self, hospital):
        return self.hospitals.filter(
            users.c.hospital_id == hospital.id).count() > 0

    def promote_to_user(self):
        self.access==0
        db.session.commit()
        return self

    def promote_to_pacient(self):
        self.access==1
        db.session.commit()
        return self

    def promote_to_nurse(self):
        self.access==2
        db.session.commit()
        return self  

    def promote_to_manager(self):
        self.access==3
        db.session.commit()
        return self

    def promote_to_admin(self):
        self.access==4
        db.session.commit()
        return self

    def add_attendance(self): #, hospital, responsible, temperature
        attendance = Attendance(pacient=self) #, hospital=hospital, responsible=responsible, temperature=temperature
        return attendance

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=36000):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    @staticmethod
    def get_by_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_by_userid(userid):
        return User.query.filter_by(userid=userid).first()

    def to_dict(self, include_email=False, include_rg=False):
        data = {
            'id': self.id,
            'userid': self.userid,
            'name': self.name,
            'gender': self.gender,
            'access': self.access,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        if include_rg:
            data['rg'] = self.rg
        return data

    def from_dict(self, data, new_user=False):
        for field in ['userid', 'name', 'gender', 'access']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def __repr__(self):
        return '<User {}>'.format(self.userid)


class Attendance(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pacient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    responsible_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    pacient = db.relationship('User', foreign_keys=[pacient_id], backref='attendances')
    responsible = db.relationship('User', foreign_keys=[responsible_id], backref='responsibles')

    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    #General info
    age = db.Column(db.Integer)
    height= db.Column(db.Integer)
    weight = db.Column(db.Integer)
    temperature = db.Column(db.Numeric)

    #CBC + PCR
    hemacias = db.Column(db.Float(10, 2))
    hematocritos = db.Column(db.Float(10, 2))
    hemoglobinas = db.Column(db.Float(10, 2))
    vcm = db.Column(db.Float(10, 2))
    hcm = db.Column(db.Float(10, 2))
    chcm = db.Column(db.Float(10, 2))
    rdw = db.Column(db.Float(10, 2))
    eritoblastos = db.Column(db.Integer)
    leucocitos = db.Column(db.Integer)
    mielocitos = db.Column(db.Integer)
    metamielocitos = db.Column(db.Integer)
    bastonetes = db.Column(db.Integer)
    segmentados = db.Column(db.Integer)
    neutrofilos_totais = db.Column(db.Integer)
    eosinofilos = db.Column(db.Integer)
    basofilos = db.Column(db.Integer)
    linfocitos = db.Column(db.Integer)
    monocitos = db.Column(db.Integer)
    plasmocitos = db.Column(db.Integer)
    plaquetas = db.Column(db.Float(10, 2))
    vmp = db.Column(db.Float(10, 2))
    pcr = db.Column(db.Float(10, 2))

    #Respiratory Infections
    influenza = db.Column(db.Integer)
    parainfluenza = db.Column(db.Integer)
    h1n1 = db.Column(db.Integer)
    chlamidophila_plenumonae = db.Column(db.Integer)
    rhinovirus_enterovirus = db.Column(db.Integer)
    virus_sincicial = db.Column(db.Integer)
    outros_coranavirus = db.Column(db.Integer)
    outras_infeccoes_respiratorias = db.Column(db.Integer)

    #Model prediction and medical confirmation
    sars_cov_2_labtest_score = db.Column(db.Float(10, 2))
    sars_cov_2_labtest_pred = db.Column(db.Integer)
    sars_cov_2_confirmation = db.Column(db.Integer)
    
    @staticmethod
    def get_by_id(id):
        return Attendance.query.filter_by(id=id).first()

    def to_dict(self):
        data = {
            'id': self.id,
            'userid': self.pacient.userid,
            'name': self.pacient.name,
            'gender': self.pacient.gender,
            'timestamp': self.timestamp,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'temperature': str(self.temperature),
            
            'cbc': {
                'hemacias': str(self.hemacias),
                'hematocritos': str(self.hematocritos),
                'hemoglobinas': str(self.hemoglobinas),
                'vcm': str(self.vcm),
                'hcm': str(self.hcm),
                'chcm': str(self.chcm),
                'rdw': str(self.rdw),
                'eritoblastos': self.eritoblastos,
                'leucocitos': self.leucocitos,
                'mielocitos': self.mielocitos,
                'metamielocitos': self.metamielocitos,
                'bastonetes': self.bastonetes,
                'segmentados': self.segmentados,
                'neutrofilos_totais': self.neutrofilos_totais,
                'eosinofilos': self.eosinofilos,
                'basofilos': self.basofilos,
                'linfocitos': self.linfocitos,
                'monocitos': self.monocitos,
                'plasmocitos': self.plasmocitos,
                'plaquetas': str(self.plaquetas),
                'vmp': str(self.vmp)
            },

            'pcr': str(self.pcr),
            
            'respiratory_infections': {
                'influenza': self.influenza,
                'parainfluenza': self.parainfluenza,
                'h1n1': self.h1n1,
                'chlamidophila_plenumonae': self.chlamidophila_plenumonae,
                'rhinovirus_enterovirus': self.rhinovirus_enterovirus,
                'virus_sincicial': self.virus_sincicial,
                'outros_coranavirus': self.outros_coranavirus,
                'outras_infeccoes_respiratorias': self.outras_infeccoes_respiratorias,
            }
        }
        return data

    def from_dict(self, data):
        remaining_fields = ['age', 'height', 'weight', 'temperature', 'cbc', 'pcr', 'respiratory_infections']
        for field in remaining_fields:
            if field in data:
                if type(data[field]) == 'dict':
                    for field2 in data[field]:
                        setattr(self, field, data[field])
                setattr(self, field, data[field])


    def __repr__(self):
        return '<Attendance {}>'.format(self.id)


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attendances = db.relationship('Attendance', backref='hospital', lazy='dynamic')
    name = db.Column(db.String(50))
    address = db.Column(db.String(140))
    uti_places = db.Column(db.Integer)
    care_places = db.Column(db.Integer)
    available_uti_places = db.Column(db.Integer)
    available_care_places = db.Column(db.Integer)

    users = db.relationship('User', secondary=users, lazy='dynamic',
        backref=db.backref('hospitals', lazy='dynamic'))

    def set_manager(self, user):
        if user.is_manager_of(self):
            return None
        user.hospitals.append(self)
        user.promote_to_manager()
        db.session.commit()
        return None

    def get_managers(self):
        return self.users.all()

    @staticmethod
    def get_by_id(id):
        return Hospital.query.filter_by(id=id).first()

    @staticmethod
    def get_by_name(name):
        return Hospital.query.filter_by(name=name).first()

    def __repr__(self):
        return '<Hospital {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
