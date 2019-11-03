
#  LabTools - measure.py
#  Copyright 2019 Luca Arnaboldi

from .utils import de2unc

from operator import attrgetter
import yaml

class Instrument():
    
    def __init__(self, config):
        with open(config) as conf:
            self.measure_types = yaml.full_load(conf)
        
        # Sort all the measure types by ascending order of scale
        for measure_type, scale in self.measure_types.items():
            scale.sort(key = lambda scale: scale['full-scale'])
            
    def measure(self, measure_type, value, fond = None):
        """
        Take a value measured with this instrument and it returns an uncertainty
        item. The error is calculated with the specification for this instrument
        given in the configuration.
        If fond is None the best full-scale one is choosed.
        """
        value = float(value)
        for item in self.measure_types[measure_type]:
            if (fond is None and value < item['full-scale']) or (fond is not None and float(fond) == float(item['full-scale'])):
                return de2unc(
                    value,
                    item['resolution'] * item['digit_error'],
                    item['percentage_error'],
                )
        # Right full-scale not found        
        raise ValueError('Unable to compute this measure: {0}, {1}, {2}'.format(
            measure_type,
            value,
            fond
        ))
