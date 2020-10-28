import json
from flask_restplus import fields, marshal
from flask_restplus.mask import Mask

class Girl:
	serializer = {
		"name": fields.String,
		"age grade": fields.Integer(attribute="age_grade"),
		"boo": fields.String,
		"boo's age": fields.Integer(attribute="boo.age")
	}
	def __init__(self, name, age, boo=None):
		self.name = name
		self.age_grade = age
		self.boo = boo

	def __str__(self):
		return self.name

class Boy:
	mask = Mask("name", skip=True)
	serializer = {
		"name": fields.String, 
		"age": fields.Integer,
		"car": fields.String,
		"babe": fields.List(fields.Nested(Girl.serializer, mask=mask))
	}
	def __init__(self, name, age, car, babe):
		self.name = name
		self.age = age
		self.car = car
		self.babe = babe
	def __repr__(self):
		return self.name

sandy = Girl("Sandra", 20, "Harvard")
jenny = Girl("Jenny", 21, "Stanford")

bill = Boy("Bill", 25, "Benz", [jenny, sandy])
sandy.boo = bill
s = json.dumps(marshal(sandy, sandy.serializer))
print(s)
