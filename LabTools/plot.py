
#  LabTools - plot.py
#  Copyright 2019 Luca Arnaboldi

from .utils import unpack_unarray
from tikzplotlib import save as save_tikz
import matplotlib.pyplot as plot
import numpy
from uncertainties import unumpy

from functools import wraps

##  Costant
DEFAULT_PLOT_DIMENSION = [10., 7.5]
DEFAULT_ERRORBAR_STYLE = {
    'linestyle' : '',
    'c' : 'k',
    'capsize' : 0,
    'elinewidth' : 0.7,
}
DEFAULT_PLOT_STYLE = {
    'c' : 'b',
    'lw' : .3,
}
DEFAULT_NORM_RES_STYLE = {
    'marker' : '.',
    'color' : 'blue',
    'markersize' : 2.,
    'linestyle' : '',
}

def rcConfig(
    usetex = True,
    latex_adds = True,
    fontsize = 12,
    ):
    """
    This defines the rcConfig for my plots.
    Thanks to: Niccolò Porciani
    """
    # Set the usage of LaTeX in labels and titles. It needs a LaTeX compiler
    # installed on the PC.
    plot.rcParams['text.usetex'] = usetex
    # LaTeX things needed:
    #   - siunitx
    #   - amsmath
    if latex_adds:
        plot.rcParams['text.latex.preamble'] = [
            r'''
            \usepackage{amsmath}
            \usepackage{siunitx}
            '''
        ]
    plot.rcParams['font.family'] = 'serif'
    plot.rcParams['font.serif'] = 'Computer Modern'
    plot.rcParams['font.size'] = fontsize
    

def residual_plot(
    f,
    param,
    X,
    Y,
    use_ux = True,
    df = None,
    xlabel = "",
    normres = True,
    fontsize = 12,
    ylabel = "",
    title = None,
    rylabel = None,
    xlogscale = False,
    ylogscale = False,
    figfile = None
    ):
    """
    It takes X and Y as unumpy.uarray and makes a plot with the residual graph.
    """
        
    # Load Configuration
    rcConfig(fontsize = fontsize)
    
    # Redefine f  and df for curvefit
    @wraps(f) # need for pass the number of parametres. Without curve_fit fails
    def uf(x, *pars):
        # if you give to nominal_values a standard  numpy.array it returns it
        return unumpy.nominal_values(f(x, *pars))
    # df is analogous
    if df is not None:
        @wraps(df) 
        def udf(x, *pars):
            return unumpy.nominal_values(df(x, *pars))
    
    x, ux = unpack_unarray(X)
    y, uy = unpack_unarray(Y)
    
    fig = plot.figure()
    fig.set_size_inches(*DEFAULT_PLOT_DIMENSION)
    main = plot.subplot2grid((12,9), (0,0), colspan = 9, rowspan = 6, fig = fig)
    res = plot.subplot2grid((12,9), (6,0), colspan = 9, rowspan = 3, fig = fig)
    
    fig.subplots_adjust(hspace=0) # Non lascia spazio tra i grafici
    
    ## Calcola residui
    #Propago errori su y da x
    if use_ux:
        if df is None:
            raise ParametresError('Errors on x were given but no derivative of f')
        else:
            errore = numpy.sqrt( uy**2 + (df(x, *param) * ux)**2 )
    else:
        errore = uy
    residui = y - uf(x, *param)
    if normres:
        residui = residui / errore
    
    
    ## Setto i limiti sulle x
    if xlogscale:
        d_interval = (numpy.log10(max(x)) - numpy.log10(min(x))) * 0.01
        main.set_xlim(
            numpy.power(10., numpy.log10(min(x)) - d_interval),
            numpy.power(10., numpy.log10(max(x)) + d_interval)
        )
        res.set_xlim(
            numpy.power(10., numpy.log10(min(x)) - d_interval),
            numpy.power(10., numpy.log10(max(x)) + d_interval)
        )
    else:
        d_interval = (max(x) - min(x)) * 0.01
        main.set_xlim(
            min(x) - max(ux) - d_interval,
            max(x) + max(ux) + d_interval
        )
        res.set_xlim(
            min(x) - max(ux) - d_interval,
            max(x) + max(ux) + d_interval
        )
    
    
    ##Crea la grid appropriata e setta i limiti
    if xlogscale:
        d_interval = (numpy.log10(max(x)) - numpy.log10(min(x))) * 0.01
        grid = numpy.logspace(
            numpy.log10(min(x)) - d_interval,
            numpy.log10(max(x)) + d_interval,
            1000
        )
    else:
        d_interval = (max(x) - min(x)) * 0.01
        grid = numpy.linspace(
            min(x) - max(ux) - d_interval,
            max(x) + max(ux) + d_interval
        )
    f_grid = uf(grid, *param)
    
    
    # Grafico curva 
    #main.grid()
    main.minorticks_on()
    main.plot(grid, f_grid, **DEFAULT_PLOT_STYLE)
    main.errorbar( x, y, xerr = ux, yerr = uy, **DEFAULT_ERRORBAR_STYLE)
    
    if xlogscale:
        main.set_xscale('log')
        
    if ylogscale:
        main.set_yscale('log')
    main.set_xticklabels([]) #Leva i numeri sotto il primo grafico

    main.set_ylabel(ylabel)
    if title is not None:
        main.set_title(title)
    
    ## Grafico residui
    #res.grid()
    res.minorticks_on()
    res.plot(grid, grid * 0., **DEFAULT_PLOT_STYLE)
    
    if normres:
        res.plot(x, residui, **DEFAULT_NORM_RES_STYLE)
    else:
        res.errorbar(x, residui, xerr = 0., yerr = uy, **DEFAULT_ERRORBAR_STYLE)
    
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
        if figfile.endswith('tex'):
            raise NotImplementedError('tikzplotlib does not suppurt subplots.')
            save_tikz(
                figure = fig,
                figurewidth = '\\linewidth',
                filepath = figfile,
                textsize = fontsize,
            )
        else:
            fig.savefig(figfile, format = 'pdf', bbox_inches = 'tight')
