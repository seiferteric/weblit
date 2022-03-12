import functools
import inspect
from enum import Enum
from flask import Flask, request, render_template

from pprint import pformat


class Weblit(object):
	def __init__(self, name):
		self.name = name or __name__
		self.app = Flask(self.name)
		self.forms = []

		@self.app.route("/")
		def index():
		    return render_template('index.html', app=self)

	def Form(self, in_format = {}, out_format={}):

		def decorator_form(func):
			self.forms.append(func.__name__)
			def view_wrapper(*args, **kwargs):
				return render_template('form.html', fname=func.__name__, sig=inspect.signature(func), helpers=TemplateHelpers, param_format=in_format)

			def form_wrapper(*args, **kwargs):
				return render_template('form.html', fname=func.__name__, sig=inspect.signature(func), helpers=TemplateHelpers, result=func(**request.form))

			self.app.add_url_rule("/{}".format(func.__name__), view_func=view_wrapper)
			self.app.add_url_rule("/{}".format(func.__name__), methods=["POST"], view_func=form_wrapper)
			return func
		return decorator_form


            

	def run(self):
		self.app.run()


class Select(object):
	multi: False
	def __init__(self, multi=False):
		self.multi = multi


class TemplateHelpers(object):
	def type(param):
		if param.annotation is float:
			return "number"
		if issubclass(param.annotation, Enum):
			return "radio"
		else:
			return "text"
	def default(param):
		if param.default is inspect._empty:
			return ''
		else:
			return param.default
	
