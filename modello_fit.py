#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fit.py
#  
#  Copyright 2018 Luca Arnaboldi
#  
"""
Questo file costituisce un modello funzionante per i fit. 
Non dovrebbe essere necessario modificare nulla fuori da dove indicato.
Gli errori sono assunti statistici.
"""

from lab_tool import *
import uncertainties as unc

##########- INIZIO PARTE MODIFICABILE -##########

# Modello
def model( x, a, b ):
	return a * x + b
	
# Derivata modello (solo per MLS)
def d_model( x, a, b):
	return a
	
# Dati del fit
x = numpy.array( [ 1.3, 2.4, 2.8, 4.9] )
ux = numpy.array( [0.5, 0.2, 0.3, 0.2] )
y = numpy.array( [4.6, 10.3, 15.0, 24.1] )
uy = numpy.array( [0.8, 0.3, 0.7, 1.5] )


###########- FINE PARTE MODIFICABILE -###########

X = unarray( x, ux )
Y = unarray( y, uy )

## Curve_fit 

P_ct = ucurve_fit(model, X, Y)

print( "Parametri curve_fit:", P_ct )
print( "Chi quadro:", chi2LS(model, P_ct, X, Y) )
print( "p-value: ", pvalue( chi2LS(model, P_ct, X, Y), X, P_ct ) )

## Curve_fit reiterato

P_ci = MLS( model, d_model, X, Y, p0 = P_ct)

print( "Parametri curve_fit iterato:", P_ci )
print( "Chi quadro:", chi2MLS(model, d_model, P_ci, X, Y) )
print( "p-value: ", pvalue( chi2MLS(model, d_model, P_ci, X, Y), X, P_ci ) )

## ODR

def ODRmodel( param, x ):
	return model( x, *param )
	
P_odr, chi2 = ODRfit( ODRmodel, X, Y, p0 = P_ci )
	
print( "Parametri ODR:", P_odr )
print( "Chi quadro:", chi2 )
print( "p-value: ", pvalue( chi2, X, P_odr ) )

plotter(model, P_odr, X, Y)
	
	
	
	
	



