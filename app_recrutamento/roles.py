from rolepermissions.roles import AbstractUserRole

class Candidato(AbstractUserRole):
    name = 'candidato'
    available_permissions = {'inicial':False}

class Empresa(AbstractUserRole):
    name = 'empresa'
    available_permissions = {'criar_vagas':True}

