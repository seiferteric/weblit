import functools
import inspect
from enum import Enum
from flask import Flask, request, render_template
import typing as t

class Weblit(object):
	def __init__(self, name):
		self.name = name or __name__
		self.app = Flask(self.name)
		self.forms = []

		@self.app.route("/")
		def index():
		    return render_template('index.html', app=self)

	def Form(self, _func=None, *, in_format={}, out_format={}):
		def decorator_form(func):
			@functools.wraps(func)
			def decorator_args():
				self.forms.append(func.__name__)
				def view_wrapper():
					return render_template('form.html', fname=func.__name__, sig=inspect.signature(func), helpers=TemplateHelpers, param_format=in_format)

				def form_wrapper():
					return render_template('form.html', fname=func.__name__, sig=inspect.signature(func), helpers=TemplateHelpers, param_format=in_format, result=func(**request.form))

				self.app.add_url_rule("/{}".format(func.__name__), view_func=view_wrapper)
				self.app.add_url_rule("/{}".format(func.__name__), methods=["POST"], view_func=form_wrapper)

			return decorator_args()
		
		if _func is None:
			return decorator_form
		else:
			return decorator_form(_func)

	def run(self):
		self.app.run()


class Select(object):
	multi: False
	def __init__(self, multi=False):
		self.multi = multi

class TemplateHelpers(object):
	def type(param, param_format=None):
		if param_format.get(param.name, None) is not None:
			return param_format.get(param.name)
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
	
