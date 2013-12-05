#!/usr/bin/env python
# File Name: test.py
#
# Date Created: Nov 12,2013
#
# Last Modified: Mon Dec  2 12:29:27 2013
#
# Author: code
#
# Description:	
#
##################################################################


import math, random
import cgi, cgitb, os
import numpy, collections
import json

cgitb.enable()


form = cgi.FieldStorage()

Distributions = {  'gauss':  random.gauss ,
		   'uniform': random.uniform,
		   'log': random.lognormvariate,
		}



stochastic_params= {"LWR": ["ir", "cc1", "com1", "c1","c2","c3","c4","c5","cwl",
		   		 "cfpcond", "tcons", "tecons"],
		    "FR": ["cs", "com2", "cc2", "fr1" ,"ff1","rb"   ],
		    "MOX" : ["cb1"]
	}


params = {"LWR": ["cr", "cf1", "eff1",
	  	"lwrinv" , "fff", "fswu", "fcon","xf" , "xw", "bu1" ],
	   "FR": ["cf2","eff2", "fdrvpu",  "frdrvpu", "freppu", "frtruinv", "frcr", "bu2" ],
	  "MOX": ["fmoxpu","bu3"]
	  }



derived_params = {  "LWR": ["xp", "xf", "xw", "swu","mat_flow", "energy_gen", "fpusf", "f239sf"],
		    "FR" : ["frenr", "frcreff"],
		    "MOX": ["f239mox"]
		}

#====Parameter Defaults====
#LEU  Fuel
FreshLEUTable = (  (0.0325, 0.037 , 0.044),
		   (0,0,0),
		   (0.9675,0.963,0.956)
		)

SpentLEUTable = (
		   (0.00884, 0.0076, 0.0076),
		   (0.00391, 0.00481, 0.00594),
		   (0.94372, 0.9325, 0.91983),
		   (0.00012,0.00021, 0.00033 ),
		   (0.0054,0.00572,0.00607),
		   (0.00221,0.00262,0.00291),
		   (0.00132,0.00160,0.00182),
		  (0.00045,0.00068,0.00085),
		   (0.00003,0.00005, 0.00006),
		   (0.966, 0.95579, 0.9455)
		)


#FR
FRTable = ( (0,    0.25, 0.5,   0.75,   0.999),
            (0.986,0.56, 0.333, 0.212,  0.139),
	    (0    ,0.28, 0.56,  0.82,   0.999)
	  )
		
	
#LWR-MOX
FreshMoxTable = { 0 : ( (0.00213,0.00212, 0.00209),
			  (0,0,0),
			  (0.94632,0.93871,0.92667),
			  (0.0007,0.0008,0.00096),
			  (0.03019,0.03465,0.04172),
			  (0.01215,0.01394,0.01679),
			  (0.0055,0.00631,0.0076),
			  (0.00054,0.00062,0.00074),
			  (1.00001,1.000,1.0)     

			),
		 1 : ( (None, 0.0021, 0.00207),
		 	 (None, 0, 0),
			(None, 0.93053,0.91631),
			(None, 0.00129, 0.00156),
			(None, 0.03678, 0.04457),
			(None, 0.01659, 0.0201),
			(None, 0.00768, 0.00931),
			(None, 0.00428, 0.00519),
			(None, 0.00075, 0.00091),
			(None, 1.0, 1.00002)
		),

		2: ( (None, None, None),
			(None, None, None),
			(None, None, None),
			(None, None, None),
			(None, None, None),
			(None, None, None),
			(None, None, None),
			(None, None, None),
			(None, None, None),
			(None, None, None)
		
			)
	}



# Other parameter defaults (mu,std)
paramDefaults= { "ir" :  (0.1,0.17),          #discount rate
		 "cc1":  (1800., 256),        #lwr overnight cost
		 "com1": (78,7.8),            #lwr o&m cost
		 "c1": (100.,17),             #uranium cost
		 "c2": (11.5,1.7),	      #UF6 conversion cost	
		 "c3": (115., 5.1),	      #enrichment cost
		 "c4": (220.,9.2),            #LEU fabrication cost
		 "c5": (0,0),                 #Spent fuel interim dry storage cost
		 "cwl": (1.,0),               #Spent LEU direct disposal cost
		 "cfpcond": (5400.,1502),     #fission product conditioning cost
		 "rb": (211.,35),             #HLW disposal cost
		 "tcons": (7.,0.7),           #construction duration
		 "tecons": (30.,3),           #economic lifetime
		 "cr": (1000.,),              #reference reactor capacity
		 "cf1": (0.9,),               #lwr capacity factor
		 "cf2": (0.9,),               #fr capacity factor
		"eff1": (0.32,),              #lwr thermal efficiency
		"lwrinv": (78.,),             #lwr inventory
		"fff": (0.01,),		      #loss during fresh LEU fab.
		"fswu": (0.005,),	      #loss during enrichment	
		"fcon": (0.005,),	      #loss during U308-UF6 conversion	
		"xf": (0.00711,),             #feed enrichment %w/f of U235 in feed
		"xw": (0.003,),               #w/f of U235 in tails
		"bu1": (43,),                 #lwr burnup
		"bu2": (100,),                #fr burnup
		"bu3": (43,),                 #lwr-mox burnup
		"frcr": (0.75,),              #fr conversion ratio
		"cs": (502.,63),              #spent leu reprocessing cost
		"cc2": (2000.,410.),          #fr overnight  cost      
		"com2": (70.,7.),	      #fr o&m cost
		"fr1": (2700.,552.),          #fr fuel reproc. cost
		"ff1": (1800.,80.),           #fr fuel fabrication cost
		"frtruinv": (7.5,),           #fr TRU inventory
		"freppu": (0.005,),           #loss of TRU during LEU reproc.
		"fdrvpu": (0.005,),           #loss of TRU in fr drive fuel fabrication
		"frdrvpu": (0.005,),          #loss of TRU in fr drive fuel reproc.
		"eff2": (0.38,),              #thermal efficiency of fr
		"cb1": (1600.,751),           #mox fuel fabrication cost
		"fmoxpu": (0.005,),           #loss of pu during mox fuel fab.
		"nrealize": (1,)	      #no. of times to run models
	  }


#Misc
YR = 365.25
YHR = YR * 24
THOU = 1000
MILL = 1000000




def getFormElement(element ):
	d=form.getfirst(element)
	if type(d) == type('abc'):
		 return d.strip().lower()
	return d


def getP(param):
	p = getFormElement(param)
	if p is None:
		return float(paramDefaults[param][0])
	else:
		return float(p)
	

def getSP(param, n):
	mu = getFormElement(param)
	if mu is None:
		mu = float(paramDefaults[param][0])
	else:
		mu = float(mu)



	dist = getFormElement(param + 'dist')

	if dist == "none" or dist is None:
		return (mu,) * n
	
	#Else Get num realizations
	std = getFormElement(param + 'std')
	
	if std is None:
		std = paramDefaults[param][1]
	else:
		std = float(std)


	dFunc = Distributions[dist]
	dVec  =  []
		
	for i in xrange(n):
		try:
			dVec.append(dFunc(mu,std))
		except OverflowError,e:
			dVec.append(float('inf'))

	return tuple(dVec)
		
			



def initLWRParams(nruns, data={}):
	#Get Parameters
	for p in stochastic_params['LWR']:
		data[p]=getSP(p, nruns)

	for p in params['LWR']:
		data[p] = getP(p)



	fuelIndDict = lambda:{33:0, 43:1,53:2}.get(data['bu1'],0)

	data['fuelInd'] = fuelInd= fuelIndDict()

	FreshLEU = tuple(x[fuelInd] for x in FreshLEUTable)
	SpentLEU = tuple(x[fuelInd] for x in SpentLEUTable)


	

	data['xp'] = xp = FreshLEU[0]
	data['fpusf'] = sum(SpentLEU[3:9]) 
	data['f239sf'] = SpentLEU[4]
	




	xw = data['xw']
	xf = data['xf']

	log = math.log
	data['swu'] = (2*xp-1) * log(xp/(1-xp)) - (2*xw-1) * log(xw/(1-xw)) - (xp-xw)/(xf-xw) \
		* ((2*xf-1) * log(xf/(1-xf))- (2*xw-1) * log(xw/(1-xw)))


	cr = data['cr']
	cf1 = data['cf1']
	bu1 = data['bu1']
	eff1 = data['eff1']
	data['mat_flow'] = cr / eff1 * YR * cf1/bu1
	data['energy_gen'] = cr * THOU * YHR * cf1




	return data



def initFRParams(nruns, data):

	#Get Parameters
	for p in stochastic_params['FR']:
		data[p]=getSP(p, nruns)

	for p in params['FR']:
		data[p] = getP(p)


	frfuelInd = lambda:{0:0, 0.25:1, 0.5:2 , 0.75:3 , 0.99:4}.get(data['frcr'])
	frvect = tuple(x[frfuelInd()] for x in FRTable )

	data['frenr'] = frenr = frvect[1]		#FR TRU Enrichment
	data['frcreff'] = frcreff = frvect[2]         #Effective conversion ratio for Mass calculations


	return data



def initMOXParams(nruns, data):
	#Get Parameters
	for p in stochastic_params['MOX']:
		data[p]=getSP(p, nruns)

	for p in params['MOX']:
		data[p] = getP(p)
	

	fuelInd = data['fuelInd']
	moxFuelInd = lambda:{33:0, 43:1,53:2}.get(data['bu3'],0)
	freshMoxTable = FreshMoxTable[fuelInd]
	freshMox = tuple( x[moxFuelInd()] for x in freshMoxTable)   
	data['f239mox'] = freshMox[4]


	#error checking

	return data



def LWR():


	capital_cost = cc1* cr * THOU
	om_cost = com1 * MILL

	dandd_cost = cr * ( 173 + 0.024*(cr/eff1-1200))/cr * ir/((1+ir)**tecons-1) * MILL 


	#Discount factors
	df1 = (((1 + ir)**tcons - 1)/(ir * tcons)) * ( ir/(1-(1+ir)**(-tecons)))
	df2 = cwl/THOU
	df3 = 1/(1-fff)
	df4 = swu
	
	df5 = (xp - xw)/ (xf - xw)/(1 - fswu)
	df6 = 1/(1 -fcon)
	df7 = lwrinv  * cr * (ir/(1-(1 + ir)**(-tecons)))
	

	#The Model
	res = capital_cost * df1 + om_cost
	

	res +=	(mat_flow * c5)
	res +=	(energy_gen * df2)

	intres = ( (mat_flow * c4)              #fuel fabrication
		+ (mat_flow * df3 * swu * c3)   #enrichment
		+ (mat_flow * df3 *df5 * c2)    #conversion
		+ (mat_flow * df3 * df5 * df6 * c1)
		)


	res += ((intres * df7)/ mat_flow)
	res += intres  + dandd_cost

	res = res/energy_gen

	return (res * THOU )


def FR():


	df1 = (cs + bu1 * cfpcond/THOU + rb)
	df2 = fpusf * (1 - freppu) * 1.1
	df3 = (1-fdrvpu) / (cf2 * YR/eff2 * (frenr/bu2-(frenr/bu2-(1-frcreff)/THOU)* (1-frdrvpu)*(1-fdrvpu)))

	df4 = frtruinv * (ff1/frenr + c2 * (1/frenr-1))* (ir/(1-(1+ir)**(-tecons)))
	df5 = cf2 * THOU * YHR
	df6 = frtruinv / (1-fdrvpu)* (ir/(1-(1+ir)**(-tecons)))

	df7 = cf2 * YR/eff2 * (frcreff/THOU+((1-frenr)/bu2-frcreff/THOU)*(frdrvpu + (1-frdrvpu)*fdrvpu))

	df8 = ((((1+ir)**tcons-1)/(ir*tcons))*(ir/(1-(1+ir)**(-tecons))))*cc2*THOU
		
	df9 = (197 + 0.024 * (cr/eff2-1200))*eff1/eff2/cr*ir/((1+ir)**tecons-1)* MILL
		
	df0 = com2 * MILL/cr
	df11 = cf2 * YR/eff2/bu2

	df12 = (fr1 + bu2 *cfpcond/THOU + rb)
	df13 = -cwl/THOU




	reproc = mat_flow * df2
	frpow = reproc * df3
	first_core = frpow * df4


	resfr = mat_flow * df1
	resfr += (frpow * df7 * c2)
	resfr += (frpow * df8)
	resfr += (frpow * df9)
	resfr += (frpow * df0)
	
	resfr += (frpow * df11 * df12)
	resfr += (frpow * df11  * ff1)

	leu_dispos = df13 * energy_gen 

	resfr +=  leu_dispos




	int1 = frpow/reproc * ((mat_flow *df1) + leu_dispos)

	resfr += (int1 * df6 + frpow * df4)
	resfr = resfr/ (frpow * df5)

	return resfr * THOU


def MOX():



	df1 = -cwl/THOU
	df2 = f239sf * (1-freppu) * (1-fmoxpu)/f239mox
	df3 = cs + bu1 * cfpcond / THOU + rb
	df4 = lwrinv * (ir/(1-(1+ir)**(-tecons)))
	df5 = 1 - f239mox
	df6 = bu3 * eff1 * THOU * 24
	df7 = cwl/THOU
	df8 = 1/(cf1 * THOU *YHR)
	df9 =  (( ( (1+ir)**tcons-1)/(ir*tcons))* (ir/(1-(1+ir)**(-tecons))))*cc1 * THOU
	df10 = com1 * MILL/cr
	df11 = (173 + 0.024 *(cr/eff1 -1200))/cr * ir/((1+ir)**tecons-1)* MILL 

	leudisp = energy_gen *  df1
	reprocmx = mat_flow * df2
	leureproc = mat_flow * df3
	
	ufconv = reprocmx * df5 * c2
	intstor = reprocmx * c5

	resmox = leudisp + leureproc + ufconv

	firstcore= resmox +  (reprocmx * cb1)
	

	mxpow = reprocmx * df6 * df8
	resmox = firstcore * df4/ reprocmx * mxpow

	resmox += ( reprocmx * df6 * df7 )
	resmox += intstor + firstcore  + (mxpow * df9 )

	
	
	resmox += (mxpow * df10)
	resmox += (mxpow * df11)

	return (resmox / (reprocmx * df6) * THOU)



def runModel(data, runNo, energy_costs, models=[LWR] ):

	graph={}

	for m in models:
		name = m.__name__
		#A little syntactic help. Also makes 
		#values from one model globally available to the others
		for p in params[name] + derived_params[name]:
			globals()[p] = data[p]
		for p in stochastic_params[name]:
			globals()[p] = data[p][runNo]
	

		dt=energy_costs.get(name,[]) 
		dt.append(round(m(),2))
		energy_costs[name] = dt
	


def main():

	nRealize = int(getP('nrealize'))
	
	modelType=getFormElement('modelType')

	print "Content-Type:application/json"
	#print "Content-Type:text/html"
	print
	

	data = initLWRParams(nRealize)
	data = initFRParams(nRealize,data)
	data = initMOXParams(nRealize,data)

	


	energy_costs={}
	graph={}

	#run model
	for i in xrange(nRealize):
		runModel(data,i ,energy_costs, models=[LWR,FR,MOX])
		#runModel(data,i ,energy_costs, models=[LWR,FR])

	if modelType == 's':
		#Sort data into bins for display
		for m in energy_costs.keys():

			c = collections.Counter(energy_costs[m])
			vals = c.keys()
			freqs = c.values()

			hist = numpy.histogram(vals, bins=50, weights=freqs)
			y = hist[0].tolist() 
			x = hist[1].tolist()
			x = [round(n,2) for n in x] 
			

			graph["%sy" % m] = y
			graph["%sx" % m] = x


		graph['modelType'] = modelType
		graph['nrealizations'] = "{:,}".format(nRealize)
		print json.dumps(graph)

	else:
		energy_costs['modelType'] = modelType
		print json.dumps(energy_costs)





main()
	





