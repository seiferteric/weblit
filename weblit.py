import functools
import inspect
from enum import Enum
from flask import Flask, request, render_template
import typing as t
from pprint import pformat


class Weblit(object):
	def __init__(self, name):
		self.name = name or __name__
		self.app = Flask(self.name)
		self.forms = []

		@self.app.route("/")
		def index():
		    return render_template('index.html', app=self)

	def Form(self, _func=None, *, in_format={}, out_format={}):
		# in_format = options.pop("in_format", None)
		# out_format = options.pop("out_format", None)
		def decorator_form(func):
			print("NOW HERE A ", func)
			@functools.wraps(func)
			def decorator_args():
				print("NOW HERE B")
				self.forms.append(func.__name__)
				def view_wrapper():
					print("NOW HERE C")
					return render_template('form.html', fname=func.__name__, sig=inspect.signature(func), helpers=TemplateHelpers, param_format=in_format)

				def form_wrapper():
					print("NOW HERE D", request.form)

					return render_template('form.html', fname=func.__name__, sig=inspect.signature(func), helpers=TemplateHelpers, param_format=in_format, result=func(**request.form))

				self.app.add_url_rule("/{}".format(func.__name__), view_func=view_wrapper)
				self.app.add_url_rule("/{}".format(func.__name__), methods=["POST"], view_func=form_wrapper)

			print(decorator_args)
			return decorator_args()
		

		if _func is None:
			print("HERE A ", self)
			return decorator_form
		else:
			print("HERE B ", self, _func)
			return decorator_form(_func)


            

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
			return "select"
		else:
			return "text"
	def default(param):
		if param.default is inspect._empty:
			return ''
		else:
			return param.default
	
