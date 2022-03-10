import functools
import inspect
from flask import Flask, request, render_template

from pprint import pformat


class Weblit(object):
	def __init__(self, name):
		self.name = name or __name__
		self.app = Flask(self.name)

		@self.app.route("/")
		def hello_world():
		    return "<p>{}</p>".format(self.name)

	def Form(self, func):


		def view_wrapper(*args, **kwargs):
			return render_template('form.html', fname=func.__name__, sig=inspect.signature(func), helpers=TemplateHelpers)

		def form_wrapper(*args, **kwargs):
			return render_template('form_output.html', fname=func.__name__, sig=inspect.signature(func), helpers=TemplateHelpers, output=func(**request.form))

		self.app.add_url_rule("/{}".format(func.__name__), view_func=view_wrapper)
		self.app.add_url_rule("/{}".format(func.__name__), methods=["POST"], view_func=form_wrapper)
		return func

	def run(self):
		self.app.run()





class TemplateHelpers(object):
	def type(annot):
		if annot is float:
			return "number"
		else:
			return "text"