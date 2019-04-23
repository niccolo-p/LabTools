#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lab_tool.py
#  Copyright 2018 Luca Arnaboldi
#  Strumenti Python per Laboratorio 2. È una avrsione aggiornata di lab_tool.py
#  secondo le esigenze di Lab2.

import numpy
import from scipy.optimize import curve_fit
import matplotlib.pyplot as plot

"""
Calcola la matrice di covarianza normalizzata data la matrice di covarianza
"""
def normCov(cov):
    normcov = numpy.zeros_like(cov)
    n = a.shape[0]
    for i in range(0, n):
        for j in range(0, n):
            normcov = cov[i][j] / numpy.sqrt(cov[i][i] * cov[j][j])
    return normcov

### FIT MINIMI QUADRATI
"""
Calcola il chi quadro quando nel caso LS. Restituisce anche il numero di
gradi di libertà.
"""
def chi2LS(f, x, y, param, ux, uy,):
	return sum(((y - f(x, *param)) / uy)**2), len(x) - len(param)

### FIT ITERATO
"""
Fit minimi quadrati reiterato per tentare di tenere in considerazione gli
errori sulle X. Necessita della funzione derivata del modello.
verbose = True fa stampare anche tutti gli step intermedi
"""
def MLS(model, d_model, x, y, ux, uy, convergence_condition = 1e-7, max_iterations = 20, p0 = None, absolute_sigma = False, verbose = False):
    
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
        
    return par, cov
    
"""
Calcola il chi quadro quando si usa minimi quadrati iterato. Restituisce
anche il numero di gradi di libertà.
"""
def chi2MLS( f, df, param, x, y, ux, uy ):
    dif_y = numpy.sqrt( uy**2 + ( ux * df(x, *param) )**2 ) # errore
    return sum( ( ( y - f( x, *param ) ) / dif_y )**2 )
        
### GRAFICI
def plotter( f, param, x, y, ux, uy, xlabel = "", ylabel = "", title = "", rxlabel = "", rylabel = "", rtitle = "",xlogscale = False, ylogscale = False, figfile = None):
    
    fig, (main, res) = plt.subplots(2, sharex=True)
	
	if xlogscale:
        d_interval = (numpy.log10(max(x)) - numpy.log10(min(x))) * 0.001
        grid = numpy.logspace(numpy.log10(min(x)) - d_interval, numpy.log10(max(x)) + d_interval, 1000)
    else:
        d_interval = (max(x) - min(x)) * 0.01
        grid = numpy.linspace(min(x) - d_interval, max(x) + d_interval)
    f_grid = f(grid, *param)
	
	# Calcola residui
	residui = y - f(x, *param)
	
	# Grafico curva 
	main.grid()
    main.minorticks_on()
	main.plot( grid, f_grid, 'black' )
	main.errorbar( x, y, xerr = ux, yerr = uy, marker = 'o', color = 'blue', markersize=4., linestyle = '' )
	main.xlabel(xlabel)
	main.ylabel(ylabel)
	main.title(title)
	plt.show()
	
	#Grafico residui
	res.grid()
	res.plot( grid, grid * 0., 'black' )
	res.errorbar( x, residui, xerr = 0., yerr = uy, marker = 'o', color = 'blue', markersize=4., linestyle = '' )
	res.xlabel( rxlabel )
	res.ylabel( rylabel )
	res.title( rtitle )
	plt.show()
