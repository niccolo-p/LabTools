#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lab_tool.py
#  
#  Copyright 2018 Luca Arnaboldi
#  
#  
#  

import numpy
import uncertainties as unc
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.odr import odrpack
from scipy.stats import chi2 as chi2pack

## Compatibilità uncertanties

"""
Crea array di ufloat a partire dati dati e le incertezze
"""

def unarray( data, u_data ):
    if len( data ) != len( u_data ):
        raise DataError( "Lunghezza degli array differente!" )
    
    temp = numpy.array( [unc.ufloat(0.,0.)]*len(data) )

    for i in range(0, len(data)):
        numpy.put(temp, i, unc.ufloat(data[i], u_data[i]))

    return temp
    

"""
Crea due numpy.array a partire da array di ufloat
"""

def unpack_unarray( u_array ):
	
	data = numpy.zeros( len(u_array) )
	u_data = numpy.zeros( len(u_array) )
	
	for i in range(0, len(u_array) ):
		data[i] = u_array[i].n
		u_data[i] = u_array[i].s
		
	return data, u_data
	
"""
Funzione anaolga a curve_fit che funziona però con unarrays sia in input che in output.
Il paraetro sigma non c'è più perchè sostituito con uy.
A diffrenze dell'originale absolute_signa è di default True.
"""

def ucurve_fit( model, X, Y, p0 = None, absolute_sigma = True, check_finite = True, bounds = (-numpy.inf, +numpy.inf), method = None, jac = None):
	
	x, ux = unpack_unarray(X)
	y, uy = unpack_unarray(Y)
	
	p, cov = curve_fit( model, x, y, sigma = uy,  p0 = p0, absolute_sigma = absolute_sigma, check_finite = check_finite, bounds = bounds, method = method, jac = jac)
	
	return unc.correlated_values( p, cov )
	

	

## ODR

"""
Esegue un fit utilizzando ODR. La funzione che passa come parametro deve essere formattata
con lo stile di ODR; si può fare per esempio così:
def ODRmodel( param, x ):
	return model( x, *param )
	
Ritorna l'unarray dei parametri e il chi quadro
"""

def ODRfit ( model, X, Y, p0, verbose = False):
	
	if type(p0) != 'numpy.ndarray':
		try:
			p0, up0 = unpack_unarray( p0 )
		except TypeError:
			pass
	
	x, ux = unpack_unarray(X)
	y, uy = unpack_unarray(Y)
	
	modello = odrpack.Model( model )
	data = odrpack.RealData( x, y, sx = ux, sy = uy )
	engine = odrpack.ODR( data, modello, beta0 = p0 )
	output = engine.run()
	
	P = unc.correlated_values( output.beta, output.cov_beta )
	
	if verbose:
		output.pprint()
	
	return P, output.sum_square
	
## Statistica

"""
Calcola il valore e l'incertezza come radice della varianza del valore medio
 a partire dal campione di uno stesso dato
"""
def stat_value( data_set ):
	return unc.ufloat( numpy.mean( data_set ), numpy.std( data_set ) / numpy.sqrt( len( data_set ) - 1 ) )
	

"""
Calcola il valore e l'incertezza come distribuzione uniforme  nella semidispersione
"""
def semi_value ( data_set ):
	return unc.ufloat( numpy.mean( data_set ), ( max( data_set ) - min( data_set ) ) / ( 2 * numpy.sqrt( 12 ) ) )




"""
Calcola il chi quadro quando gli errori sulle x sono trascurabili
"""

def chi2LS(f, P, X, Y):
	
	if type(P) != 'numpy.ndarray':
		param, uparam  = unpack_unarray(P) 
	else:
		param = P
	
	x, ux = unpack_unarray(X)
	y, uy = unpack_unarray(Y)
	
	return sum( ( ( y - f( x, *param ) ) / uy )**2 )
	
"""
Fit minimi quadrati reiterato per tentare di tenere in considerazione gli errori sulle X.
Necessita della funzione derivata del modello.
"""

def MLS( model, d_model, X, Y, convergence_condition = 1e-7, max_iterations = 20, p0 = None, absolute_sigma = True, verbose = False):
	
	if type(p0) != 'numpy.ndarray':
		try:
			p0, up0 = unpack_unarray( p0 )
		except TypeError:
			pass
	
	x, ux = unpack_unarray(X)
	y, uy = unpack_unarray(Y)
	
	
	# Primo step curve fit
	par, cov = curve_fit( model, x, y, sigma = uy, p0 = p0, absolute_sigma = absolute_sigma )
	
	# Procedimento iterato
	while --max_iterations:
		dif_y = numpy.sqrt( uy**2 + (d_model(x, *par) * ux)**2 )
		
		npar, ncov = curve_fit( model, x, y, sigma = dif_y, p0 = par, absolute_sigma = absolute_sigma)
		
		if verbose:
			print(npar)
			print(ncov)
		
		perror = numpy.abs(npar - par) / npar
		cerror = numpy.abs(ncov - cov) / ncov
		
		if (perror < convergence_condition).all() and (cerror < convergence_condition).all():
			
			if verbose:
				print("MLS Convergence")
				
			break

		par = npar
		cov = ncov
		
	return unc.correlated_values( npar, ncov )
        
     
"""
Calcola il chi quadro quando si usa minimi quadrati iterato
"""

def chi2MLS( f, df, P, X, Y ):
	
	if type(P) != 'numpy.ndarray':
		param, uparam  = unpack_unarray(P) 
	else:
		param = P
	
	x, ux = unpack_unarray(X)
	y, uy = unpack_unarray(Y)
	
	dif_y = numpy.sqrt( uy**2 + ( ux * df(x, *param) )**2 )
	
	return sum( ( ( y - f( x, *param ) ) / dif_y )**2 )
		
		
"""
Calcola il p-value noti chi2 e chi2 aspettato.
"""

def pvalue( chi2value, data = None, param = None, chi2exp = None ):
	
	if chi2exp == None:
		try:
			chi2exp = len(data) - len(param)
		except TypeError:
			raise ParametresError( 'Not enought argument given to pvalue()' )
	
	if chi2value >= chi2exp:

		return chi2pack.sf( chi2value, chi2exp )
		
	else:
		return chi2pack.cdf( chi2value, chi2exp )
		
		

## Grafici

"""
Grafico e grafico dei residui
	-f formattata come vuole curve_fit
	-P sono i parametri indifferetemente come float o ufloat
	-X, Y sono uarray
"""

def plotter( f, P, X, Y, xlabel = "", ylabel = "", title = "", rxlabel = "", rylabel = "", rtitle = ""):
	
	if type(P) != 'numpy.ndarray':
		param, uparam  = unpack_unarray(P) 
	else:
		param = P
	
	x, ux = unpack_unarray(X)
	y, uy = unpack_unarray(Y)
	
	
	grid = numpy.linspace( min(x) - 0.20 * ( max(x)-min(x) ), max(x) + 0.20 * ( max(x)-min(x) ) )
	f_grid = f( grid, *param )
	
	# Calcola residui
	res = y - f( x, *param ) 
	
	# Grafico curva 
	plt.grid()
	plt.xlim( min(x - ux) - 0.05 * ( max(x + ux)-min(x - ux) ), max(x + ux) + 0.05 * ( max(x + ux)-min(x - ux) ) )
	plt.plot( grid, f_grid, 'black' )
	plt.errorbar( x, y, xerr = ux, yerr = uy, marker = 'o', color = 'blue', markersize=4., linestyle = '' )
	plt.xlabel( xlabel )
	plt.ylabel( ylabel )
	plt.title( title )
	plt.show()
	
	#Grafico residui
	plt.grid()
	plt.xlim( min(x - ux) - 0.05 * ( max(x + ux)-min(x - ux) ), max(x + ux) + 0.05 * ( max(x + ux)-min(x - ux) ) )
	plt.plot( grid, grid * 0., 'black' )
	plt.errorbar( x, res, xerr = 0., yerr = uy, marker = 'o', color = 'blue', markersize=4., linestyle = '' )
	plt.xlabel( rxlabel )
	plt.ylabel( rylabel )
	plt.title( rtitle )
	plt.show()
	
