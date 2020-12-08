# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 17:15:05 2020

@author: Adrián Segura
"""

import pymongo
import json
from json2xml import json2xml
from pprint import pprint
import lxml.etree as ET

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


def Consulta_1 ():
    result = psiquiatras.aggregate([
        {
            '$lookup': {
                'from': 'paciente', 
                'localField': '_id', 
                'foreignField': 'psiquiatra asignado', 
                'as': 'pacientes actuales'
            }  
        },
        {
            '$lookup': {
                'from': 'paciente', 
                'localField': '_id', 
                'foreignField': 'patologias previas.psiquiatra asignado', 
                'as': 'pacientes antiguos'
            }  
        }
    ])
    return result

def Consulta_2 ():
    result = pacientes.aggregate([
        {
            '$lookup': {
                'from': 'formulario consulta', 
                'localField': 'formularios consultas.formulario', 
                'foreignField': '_id', 
                'as': 'formularios actuales'
            }
        },
        {
            '$lookup': {
                'from': 'formulario consulta', 
                'localField': 'patologias previas.formularios consultas.formulario', 
                'foreignField': '_id', 
                'as': 'formularios previos'
            }
        }
    ])
    return result

def Consulta_3():
    result = familiares.aggregate([
        {
            '$lookup': {
                'from': 'paciente', 
                'localField': 'paciente asociado', 
                'foreignField': '_id', 
                'as': 'paciente asociado'
            }
        },
        {
            '$lookup': {
                'from': 'mensaje', 
                'localField': 'mensajes recibidos.mensaje', 
                'foreignField': '_id', 
                'as': 'mensajes recibidos'
            }
        },
        {
            '$lookup': {
                'from': 'psiquiatra', 
                'localField': 'mensajes recibidos.emisor', 
                'foreignField': '_id', 
                'as': 'emisores'
            }
        }
    ])
    return result

def GuardaArchivo(cadena, nombre_archivo):
    f = open(nombre_archivo, "w", encoding="utf-8")
    f.write(cadena)
    f.close()

def AplicaXSLT(res_consulta_xml, archivo_xsl):
    xslt = ET.parse(archivo_xsl)
    transform = ET.XSLT(xslt)
    newdom = transform(res_consulta_xml)
    return newdom
    
def GeneraVista(num_consulta, guardar_json, guardar_xml):
    if(num_consulta == 1):
        res_consulta_json = Consulta_1()
    elif(num_consulta == 2):
        res_consulta_json = Consulta_2()
    elif(num_consulta == 3):
        res_consulta_json = Consulta_3()
    else:
        return "consulta no implementada"

    json_docs = []
    for doc in res_consulta_json:
        json_docs.append(doc)
    
    if(guardar_json):
        with open('Consultas json/resultado_consulta_' + str(num_consulta) + '.json', 'w', encoding="utf-8") as file:
            str(json_docs).encode('utf-8')
            json.dump(json_docs, file, indent=4, ensure_ascii=False)
    
    res_consulta_xml_string = json2xml.Json2xml(json_docs, attr_type=False).to_xml()
    
    if(guardar_xml):
        GuardaArchivo(res_consulta_xml_string[0:-1], "Consultas xml/resultado_consulta_" + str(num_consulta) + ".xml")
    
    res_consulta_xml = ET.XML(res_consulta_xml_string)
    
    html = AplicaXSLT(res_consulta_xml, "Consultas xsl/vista_" + str(num_consulta) + ".xsl")
    GuardaArchivo(str(html), "Vistas html/vista_" + str(num_consulta) + ".html")
   
GeneraVista(1, True, True)
GeneraVista(2, True, True)
GeneraVista(3, True, True)