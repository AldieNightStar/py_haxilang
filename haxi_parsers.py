from typing import NoReturn
import pyparser as pp
from pyparser.util import UntilTag

class Separator:
	value=""
	def __repr__(self) -> str:
		return f"Sep({self.value})"
class Variable:
	value=""
	def __repr__(self) -> str:
		return f"Var({self.value})"
class Bracket:
	opening=False
	value=""
	def __repr__(self) -> str:
		return f"Bracket({self.value})"
class FuncCall:
	name=""
	args=[]
	def __repr__(self) -> str:
		return f"FuncCall({self.name} : {self.args})"
class String:
	value=""
	quote=""
	def __repr__(self) -> str:
		return f"Str{self.quote}({self.value})"
class Comment:
	value=""
	def __repr__(self) -> str:
		return f"Comment({self.value})"
class NextLine:
	pass
class CodeBlock:
	lines=[]
	def __repr__(self) -> str:
		return f"Code(Lines: {len(self.lines)})"

def indexOf(t, s):
	try:
		return t.index(s)
	except ValueError:
		return -1

def parser_variable(txt: str):
	if not txt[0:1].isalpha():
		return None, 0
	arr = []
	for c in txt:
		if c.isalpha() or c.isnumeric() or c == '_':
			arr.append(c)
		else:
			break
	if len(arr) < 1:
		return None, 0
	v = Variable()
	v.value = "".join(arr)
	return v, len(arr)

def parser_number(txt: str):
	arr = []
	for c in txt:
		if c.isnumeric():
			arr.append(c)
		else:
			break
	if len(arr) < 1:
		return None, 0
	return int("".join(arr)), len(arr)

def parser_separator(txt: str):
	c = txt[0:1]
	if c in " ,\n\t":
		s = Separator()
		s.value = c
		return s, 1
	return None, 0

def parser_bracket(txt: str):
	c = txt[0:1]
	if c in "{[<(":
		b = Bracket()
		b.opening = True
		b.value = c
		return b, 1
	elif c in "}]>)":
		b = Bracket()
		b.opening = False
		b.value = c
		return b, 1
	return None, 0

def parser_code(txt: str):
	if txt[0:1] != "{":
		return None, 0
	arr = []
	proc = 1
	for (t, cnt) in pp.parse(txt[1:], *[*CORE_PARSER_SET, parser_bracket]):
		proc += cnt
		if type(t) == Bracket:
			if not t.opening and t.value == "}":
				break
		elif type(t) in [FuncCall]:
			arr.append(t)
	cb = CodeBlock()
	cb.lines = arr
	return cb, proc

def parser_args(txt):
	args = []
	preArgs = []
	proc = 0
	for (t, cnt) in pp.parse(txt, *ARGS_PARSER_SET):
		proc += cnt
		if type(t) == Separator:
			if len(preArgs) > 0:
				args.append(preArgs[-1])
				preArgs.clear()
		elif type(t) in [int, Variable, CodeBlock, Comment, FuncCall]:
			preArgs.append(t)
		elif type(t) == pp.StringToken:
			s = String()
			s.value = t.value
			s.quote = t.quotes
			preArgs.append(s)
		elif type(t) == Bracket:
			if not t.opening:
				break
	if len(preArgs) > 0:
		args.append(preArgs[-1])
	return args, proc

def parser_func_call(txt):
	# Parse [ sym
	if txt[0:1] != "[":
		return None, 0
	# Parse [NAME (space)
	cnt = 1
	arr = []
	for c in txt[1:]:
		cnt += 1
		if c in " \t\n":
			break
		arr.append(c)
	cmdName = "".join(arr)
	# Parse args
	args, i = parser_args(txt[cnt:])
	if i < 1:
		f = FuncCall()
		f.name = cmdName
		f.args = []
		return f, cnt + i
	f = FuncCall()
	f.name = cmdName
	f.args = args
	return f, cnt + i

def parser_comment(txt: str):
	if txt[0:1] != "#":
		return None, 0
	arr = []
	for c in txt[1:]:
		if c in "#\n":
			break
		arr.append(c)
	if len(arr) < 1:
		return None, 0
	c = Comment()
	c.value = "".join(arr)
	return c, len(arr) + 2

def parser_nextline(txt: str):
	if txt[0:1] == "\n":
		return NextLine(), 1
	return None, 0








CORE_PARSER_SET = [parser_nextline, parser_comment, parser_func_call]
ARGS_PARSER_SET = [parser_func_call, parser_comment, parser_variable, parser_number, pp.parser_string, parser_separator, parser_code, parser_bracket]