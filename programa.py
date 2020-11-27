# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 17:15:05 2020

@author: Adrián Segura
"""

import pymongo
import json
from pprint import pprint

myclient = pymongo.MongoClient("mongodb+srv://adriansegura:adrianseguraortiz1999@psicotreatbd.e4kvw.mongodb.net/PsycoTreat?retryWrites=true&w=majority")
mydb = myclient["PsycoTreat"]
psiquiatras = mydb["psiquiatra"]
administrativos = mydb["administrativo"]
pacientes = mydb["paciente"]
familiares = mydb["familiar autorizado"]
formularios = mydb["formulario consulta"]
mensajes = mydb["mensaje"]

def MuestraPsiquiatras ():
    for psiquiatra in psiquiatras.find():
        pprint(psiquiatra)
        
def MuestraAdministrativos ():
    for administrativo in administrativos.find():
        pprint(administrativo)
        
def MuestraPacientes ():
    for paciente in pacientes.find():
        pprint(paciente)

def MuestraFamiliares ():
    for familiar in familiares.find():
        pprint(familiar)
        
def MuestraFormularios ():
    for formulario in formularios.find():
        pprint(formulario)

def MuestraMensajes ():
    for mensaje in mensajes.find():
        pprint(mensaje)

print("Psiquiatras:")
print()
MuestraPsiquiatras()
print()
print("Administrativos:")
print()
MuestraAdministrativos()
print()
print("Pacientes")
print()
MuestraPacientes()
print()
print("Familiares autorizados:")
print()
MuestraFamiliares()
print()
print("Formularios consultas:")
print()
MuestraFormularios()
print()
print("Mensajes:")
print()
MuestraMensajes()