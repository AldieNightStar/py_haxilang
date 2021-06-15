import pyparser as pp
import haxi_parsers	as hp

def parse(src):
	for (t, cnt) in pp.parse(src, *hp.CORE_PARSER_SET):
		if type(t) in [hp.NextLine, pp.UnknownToken]:
			continue
		yield t, cnt