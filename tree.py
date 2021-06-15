from typing import List

import haxi as h
import haxi_parsers as hp
import time

class Import:
	name=""
	alias=None
	def __repr__(self) -> str:
		return f"import({self.name}, {self.alias})"

class Func:
	name=""
	args=[]
	lines=[]
	def __repr__(self) -> str:
		return f"Func({self.name}, {self.args}, Lines: {len(self.lines)})"

class FuncCall:
	name=""
	args=[]
	def __repr__(self) -> str:
		return f"Call({self.name} : {self.args})"

class Eval:
	value=""
	def __repr__(self) -> str:
		return f"Eval({self.value})"

def get_import(t):
	if type(t) != hp.FuncCall:
		return None
	t: hp.FuncCall = t
	if t.name != "use":
		return None
	if len(t.args) < 1:
		raise ValueError("Use at least one module.")
	i = Import()
	if len(t.args) == 1:
		if type(t.args[0]) != hp.Variable:
			raise ValueError("Incorect module name. Use variable like syntax")
		i.name = t.args[0].value
		return [i]
	elif len(t.args) == 2:
		if type(t.args[0]) != hp.Variable or type(t.args[1]) != hp.Variable:
			raise ValueError("Incorect module/alias name. Use variable like syntax")
		i.name = t.args[0].value
		i.alias = t.args[1].value
		return [i]
	else:
		raise ValueError("Too much args for import")

def get_func_call(t):
	if type(t) != hp.FuncCall:
		return None
	t : hp.FuncCall = t
	f = FuncCall()
	f.name = t.name
	args = t.args
	f.args = []
	funcs = []
	for arg in args:
		if type(arg) == hp.CodeBlock:
			c : hp.CodeBlock = arg
			fc = Func()
			fc.name = "___f" + str(time.time_ns())
			fc.args = []
			fc.lines = []
			for line in c.lines:
				codes = of_codes(line, *CORE_GETS)
				if codes != None:
					fc.lines.extend(codes)
			funcs.append(fc)
			f2 = FuncCall()
			f2.name = fc.name
			f2.args = []
			f.args.append(f2)
		fc = get_func_create(arg)
		if fc != None and len(fc) > 0 and type(fc[0]) == Func:
			funcs.append(fc[0])
			v = hp.Variable()
			v.value = fc[0].name
			f.args.append(v)
		else:
			f.args.append(arg)
	return [*funcs, f]

	

def get_func_create(t):
	if type(t) != hp.FuncCall:
		return None
	t: hp.FuncCall = t
	if t.name != "def":
		return None
	if len(t.args) < 2:
		raise ValueError("Function creation takes arguments: NAME, [ARGS], CODE")
	if type(t.args[-1]) != hp.CodeBlock:
		raise ValueError("Last argument of the function creation should be CODEBLOCK")
	f = Func()
	f.name = t.args[0].value
	f.args = [a.value for a in t.args[1:-1]]
	f.lines = []
	for line in t.args[-1].lines:
		codes = of_codes(line, *CORE_GETS)
		if codes != None:
			f.lines.extend(codes)
	return [f]

def get_eval(t):
	if (type(t)) != hp.FuncCall:
		pass
	t: hp.FuncCall = t
	if t.name != "eval":
		return None
	if len(t.args) != 1 and type(t.args[0] == hp.String):
		raise ValueError("Eval function should have 1 STRING arg")
	e = Eval()
	e.value = t.args[0].value
	return [e]
	

def of_codes(token, *arr: List):
	for f in arr:
		c = f(token)
		if c != None and len(c) > 0:
			return c
	return None

def convert(src) -> str:
	for (t, cnt) in h.parse(src):
		codes = of_codes(t, *CORE_GETS)
		if codes != None:
			for c in codes:
				yield c
	

CORE_GETS = [get_import, get_func_create, get_eval, get_func_call]

#with open('test.hax', 'r') as f:
#	for code in convert(f.read()):
#		print(code)