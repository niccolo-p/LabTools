
#  lab_tool.py
#  Copyright 2019 Luca Arnaboldi
#  Strumenti Python per Laboratorio 2. È una versione aggiornata di lab_tool.py
#  secondo le esigenze di Lab2.

import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as plot

"""
Calcola la matrice di covarianza normalizzata data la matrice di covarianza
"""
def normCov(cov):
    normcov = numpy.zeros_like(cov)
    n = cov.shape[0]
    for i in range(0, n):
        for j in range(0, n):
            normcov[i][j] = cov[i][j] / numpy.sqrt(cov[i][i] * cov[j][j])
    return normcov

### FIT MINIMI QUADRATI
"""
Calcola il chi quadro quando nel caso LS. Restituisce anche il numero di
gradi di libertà.
"""
def chi2LS(f, x, y, param, uy):
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
    return sum( ( ( y - f( x, *param ) ) / dif_y )**2 ), len(x) - len(param)
        
### GRAFICI
def plotter( f, param, x, y, uy, ux = None, df = None, xlabel = "", normres = True, fontsize = 12, ylabel = "", title = None, rylabel = None, xlogscale = False, ylogscale = False, figfile = None):
    
    fig = plot.figure()
    fig.set_size_inches(10., 7.5)
    main = plot.subplot2grid((12,9), (0,0), colspan = 9, rowspan = 6, fig = fig)
    res = plot.subplot2grid((12,9), (6,0), colspan = 9, rowspan = 3, fig = fig)
    
    fig.subplots_adjust(hspace=0) # Non lascia spazio tra i grafici
    
    ## Calcola residui
    #Propago errori su y da x
    if ux is not None:
        if df is None:
            raise ParametresError('Errors on x were given but no derivative of f')
        else:
            errore = numpy.sqrt( uy**2 + (df(x, *param) * ux)**2 )
    else:
        errore = uy
    residui = y - f(x, *param)
    if normres:
        residui = residui / errore
        
    if ux is None: #Evita casini futuri se ux è None
        ux = numpy.array([0.] * len(x))
    
    
    ## Setto i limiti sulle x
    if xlogscale:
        d_interval = (numpy.log10(max(x)) - numpy.log10(min(x))) * 0.01
        main.set_xlim(numpy.power(10., numpy.log10(min(x)) - d_interval), numpy.power(10., numpy.log10(max(x)) + d_interval))
        res.set_xlim(numpy.power(10., numpy.log10(min(x)) - d_interval), numpy.power(10., numpy.log10(max(x)) + d_interval))
    else:
        d_interval = (max(x) - min(x)) * 0.01
        main.set_xlim(min(x) - max(ux) - d_interval, max(x) + max(ux) + d_interval)
        res.set_xlim(min(x) - max(ux) - d_interval, max(x) + max(ux) + d_interval)
    
    
    ##Crea la grid appropriata e setta i limiti
    if xlogscale:
        d_interval = (numpy.log10(max(x)) - numpy.log10(min(x))) * 0.01
        grid = numpy.logspace(numpy.log10(min(x)) - d_interval, numpy.log10(max(x)) + d_interval, 1000)
    else:
        d_interval = (max(x) - min(x)) * 0.01
        grid = numpy.linspace(min(x) - max(ux) - d_interval, max(x) + max(ux) + d_interval)
    f_grid = f(grid, *param)
    
    
    # Grafico curva 
    main.grid()
    main.minorticks_on()
    main.plot(grid, f_grid, 'green')
    main.errorbar( x, y, xerr = ux, yerr = uy, marker = 'o', color = 'blue', markersize = 4., linestyle = '' )
    
    if xlogscale:
        main.set_xscale('log')
        
    if ylogscale:
        main.set_yscale('log')
    main.set_xticklabels([]) #Leva i numeri sotto il primo grafico

    main.set_ylabel(ylabel)
    if title is not None:
        main.set_suptitle(title)
    
    ## Grafico residui
    res.grid()
    res.plot(grid, grid * 0., 'green')
    
    if normres:
        res.plot(x, residui, marker = 'o', color = 'blue', markersize = 4., linestyle = '')
    else:
        res.errorbar(x, residui, xerr = 0., yerr = uy, marker = '.', color = 'blue', markersize = 4., linestyle = '')
    
    if xlogscale:
        res.set_xscale('log')
        
    res.set_xlabel(xlabel)
    
    if rylabel is None:
        if normres:
            res.set_ylabel('Res. Norm')
    else:
        res.set_ylabel(rylabel)
        
    ## Salva immagine
    if figfile is not None:
        fig.savefig(figfile, format = 'pdf', bbox_inches = 'tight')
