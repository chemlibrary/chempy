import inspect

def get_default_args(func):
	signature = inspect.signature(func)
	return {
		k: v.default
		for k, v in signature.parameters.items()
		if v.default is not inspect.Parameter.empty
	}

def list_default_values(function):
	default_values = {}
	sig = inspect.signature(function)
	for param in sig.parmeters.value():
		if param.default is not param.empty:
			default_values[{param.name}] = {param.defualt}
	return default_values
