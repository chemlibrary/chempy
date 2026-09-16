# This file is part of ChemPy.
# Copyright (C) 2026 Chem
#
# ChemPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ChemPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ChemPy. If not, see <http://www.gnu.org/licenses/>.

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
