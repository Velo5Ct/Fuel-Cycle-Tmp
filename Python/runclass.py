#!/usr/bin/env python
# File Name: runclass.py
#
# Date Created: Nov 18,2013
#
# Last Modified: Mon Nov 18 11:34:14 2013
#
# Author: code
#
# Description:	
#
##################################################################

"""
def runModel(runNumber, energy_costs, models=[]):
	for m in models:
		#A little syntactic help. Also exposes
		#data from each model globally for the other models
		for p in m.params + m.derived_params:
			globals()[p] = m.data[p]
		for p in m.stochastic_params:
			globals()[p] = m.data[p][runNumber]

		e = energy_costs.get(m.__name__,[])
		e.append(m.run())
		energy_costs[m.__name__] = e
"""
