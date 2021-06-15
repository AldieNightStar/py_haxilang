# HaxiLang

## Code samples
* Import other code
```
[use console]
[use math m] # import 'math' with alias
```
* Function creation
```
[def funcName arg1 arg2 {
	[do operation1] # etc
}]
```
* Function call
```
[funcName 1 2]
```

* Function pass as argument
	* Function created BEFORE function call, so this impl can be used even for python, where function need to create BEFORE call
```
[send "Hi Jack" [def onResponse resp {
	[print resp]
}]]
```

# Current work
* Currently we read only `test.hax`
* No constructions like `[if ...]` but we can use `[eval "if a == b"]` to create such a functionality

# API 
```py
import haxi as h

for codeToken in h.parse(src):
	print(codeToken)
```