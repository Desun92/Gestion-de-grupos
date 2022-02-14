# -*- coding: utf-8 -*-

from attr import field
from odoo.exceptions import ValidationError
from datetime import date
from enum import unique
from odoo import models, fields, api

CATEGORIAS= [
    ('0','Guitarras eléctricas'),
    ('1','Guitarras acústicas'),
    ('2','Percusión'),
    ('3','Bajos'),
    ('4','Micros'),
    ('5','Sistemas PA'),
    ('6','Monitores'),
    ('7','Iluminación'),
    ('8','Mesas de mezcla')
]

CIUDADES = [
    ('0','Madrid'),
    ('1','Barcelona'),
    ('2','Valencia'),
    ('3','Sevilla'),
    ('4','Córdoba'),
    ('5','Toledo'),
    ('6','Salamanca'),
    ('7','Zaragoza'),
    ('8','Bilbao'),
    ('9','Granada'),
    ('10','Murcia'),
    ('11','San Sebastián'),
    ('12','Burgos'),
    ('13','Ávila'),
    ('14','Valladolid'),
    ('15','Alicante'),
    ('16','Las Palmas de Gran Canaría'),
    ('17','Cáceres'),
    ('18','Cádiz'),
    ('19','Santiago de Compostela'),
    ('20','Cuenca'),
    ('21','Segovia'),
    ('22','Tarragona'),
    ('23','Málaga'),
    ('24','Palma'),
    ('25','Lérida'),
    ('26','La Coruña'),
    ('27','Cartagena'),
    ('28','Gijón'),
    ('29','Ourense'),
    ('30','Almería'),
    ('31','Albacete'),
    ('32','Teruel'),
    ('33','Huelva'),
    ('34','Ceuta'),
    ('35','Lugo'),
    ('36','Badajoz'),
    ('37','Vitoria-Gasteiz'),
    ('38','San Cristóbal de La Laguna'),
    ('39','Alcalá de Henares'),
    ('40','Vigo'),
    ('41','Girona'),
    ('42','Santa Cruz de Tenerife'),
    ('43','Logroño'),
    ('44','León'),
    ('45','Ciudad Real'),
    ('46','Santander'),
    ('47','Pamplona'),
    ('48','Pontevedra'),
    ('49','Huesca'),
    ('50','Jaén') 
]

class Grupo(models.Model):
    _name = 'gestion_de_grupos.grupo'
    _description = 'Bandas de musica'

    name = fields.Char(string="Nombre del grupo",required=True,unique=True)
    descripcion = fields.Text(string="Datos de interés")
    email = fields.Char(string="Email de contacto")
    sitioWeb = fields.Char(string="Sitio web")
    foto = fields.Binary(string="Foto del grupo")
    estilo = fields.Char(string="Estilo musical")
    rider = fields.Many2one('gestion_de_grupos.rider',string="Rider")
    representante = fields.Many2one('gestion_de_grupos.representante',string="Representante del grupo")
    conciertos = fields.Many2many('gestion_de_grupos.concierto',string="Lista de conciertos programados")
    musicos = fields.Many2many('gestion_de_grupos.musico',string="Lista de músicos del grupo")

class Rider(models.Model):
    _name='gestion_de_grupos.rider'
    _description='Riders técnicos'

    name = fields.Char(string="Nombre/ID del rider",required=True,unique=True)
    foto = fields.Binary(string="Foto del rider")
    anotaciones = fields.Html(string="Anotaciones sobre el rider (Canales a usar en la mesa, micros, disposición sobre el escenario...)")
    grupo = fields.Many2one('gestion_de_grupos.grupo',string="Grupo al que pertenece el rider",required=True)
    instrumentos = fields.One2many('gestion_de_grupos.instrumento','rider',string="Lista de equipos/instrumentos")

class Instrumento(models.Model):
    _name='gestion_de_grupos.instrumento'
    _description='Equipos/Instrumentos'

    name = fields.Char(string="Número de serie del equipo/instrumento (código de identificación)",required=True,unique=True)
    modelo = fields.Char(string="Nombre y modelo del equipo/instrumento",required=True)
    foto = fields.Binary(string="Foto del equipo/instrumento (opcional)")
    rider = fields.Many2one('gestion_de_grupos.rider',string="Rider del grupo al que pertenece",required=True)
    categoria = fields.Selection(CATEGORIAS,select=True,string="Categoría")

class Concierto(models.Model):
    _name = 'gestion_de_grupos.concierto'
    _description = 'Conciertos'

    name = fields.Char(string="Nombre del concierto (ID para registro)",required=True,unique=True)
    fecha = fields.Date(string="Fecha",required=True)
    precio = fields.Float(string="Precio sin IVA",digits=(4,2),required=True)
    iva = fields.Boolean(string="Aplicar IVA del 10%")
    precioConIva = fields.Float(string="Precio con IVA",digits=(4,2),readonly=True,compute="_precio_iva")
    grupos = fields.Many2many('gestion_de_grupos.grupo',string="Lista de grupos")
    recinto = fields.Many2one('gestion_de_grupos.recinto',string="Recinto/festival asignado",required=True)

    @api.constrains('fecha')
    def _check_date(self):
        for record in self:
            if  (date.today().year - record.fecha.year>0):
                raise ValidationError("El concierto debe realizarse en una fecha futura")
            elif (date.today().year - record.fecha.year==0 and date.today().month - record.fecha.month>0):
                raise ValidationError("El concierto debe realizarse en una fecha futura")
            elif (date.today().year - record.fecha.year==0 and date.today().month - record.fecha.month==0 and date.today().day - record.fecha.day>0):
                raise ValidationError("El concierto debe realizarse en una fecha futura")
    
    @api.depends('precio','iva')
    def _precio_iva(self):
        for record in self:
            if (self.iva):
                record.precioConIva = record.precio + (record.precio*0.10)
            else:
                record.precioConIva = 0.00

class Recinto(models.Model):
    _name = 'gestion_de_grupos.recinto'
    _description = 'Recintos'

    name = fields.Char(string="Nombre del recinto o festival",required=True,unique=True)
    ciudad = fields.Selection(CIUDADES,select=True,string="Ciudad")
    direccion = fields.Char(string="Dirección")
    contacto = fields.Char(string="Mail de contacto")
    capacidad = fields.Integer(string="Capacidad del recinto")
    concierto = fields.One2many('gestion_de_grupos.concierto','recinto',string="Lista de conciertos realizados en el recinto/festival")

class Representante(models.Model):
    _name = 'gestion_de_grupos.representante'
    _inherit = 'personas.persona'
    _description = 'Representantes musicales(managers)'

    grupo = fields.One2many('gestion_de_grupos.grupo','representante',string="Lista de grupos representados",required=True)

class Musico(models.Model):
    _name = 'gestion_de_grupos.musico'
    _inherit = 'personas.persona'
    _description = 'Músicos'

    grupo = fields.Many2many('gestion_de_grupos.grupo',string="Grupos a los que pertenece el músico")