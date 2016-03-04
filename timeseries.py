import reprlib
import numpy as np
from lazy import *

class TimeSeries():
    
    '''
    Class object for storing and manipulating time series data.
    
    Parameters:
    -----------
        - times: a list of time indexes
        - values: an list of corresponding values 
        
    Properties:
    -----------
        - times: returns a sequence of the times
        - values: returns a sequence of the values
        - items: returns a sequence of time, value tuples
        - lazy: returns a LazyOperation instance which stores and identity function and the TimeSeries object
        
    Methods:
    --------
        - interpolate: returns a new TimeSeries object with values that are generated 
          from the values within the current time series object
        - mean: returns the mean value of the items within TimeSeries object
        - media: returns the median value of the items within TimeSeries object
        - itertimes: iterates over the times within the TimeSeries object
        - itervalues: itereates over the values within the TimeSeries object
        - iteritems: iterates over the time, value pairs within the TimeSeries object

    '''
    
    def __init__(self, times=[], values=None):
        
        if values==None:
            values = np.zeros(len(times))
            
        assert len(times) == len(values), "Sequence of times does not match sequences of values."
        
        self._times = np.array(times)
        self._values = np.array(values)
        
    def __len__(self):
        """
        Returns the length of time series object
        """
        return len(self._times)
    
    def __getitem__(self, time):
        """
        Returns the corresponding value for a given time within the time series
        """       
        index = np.where(self._times==time)[0]
        
        if len(index) == 0:
            raise ValueError('Time ({}) not in TimeSeries'.format(time))
        
        return self._values[index[0]]
    
    def __setitem__(self, time, value):
        """
        Sets the value of a given time if the time is present with in the time series
        """
        index = np.where(self._times==time)[0]
        
        if len(index) == 0:
            raise ValueError('Time ({}) not in TimeSeries'.format(time))
        
        self._values[index] = value
        
        
    def __str__(self):
        """
        Returns a printable representation of the timeseries object

        If the length of the timeseries is greater than five we abreviate the values in between 
        the first and last values. 
        """
        name = type(self).__name__
        
        if len(self) <= 5:
            all_samples = [(t, v) for t, v in zip(self._times,self._values)]
            return "{} {} ({} Samples)".format(name, all_samples, len(self))
        else:
            first_sample = (self._times[0],self._values[0])
            last_sample = (self._times[-1], self._values[-1])
            return "{} [{}...{}] ({} Samples)".format(name, first_sample, last_sample, len(self))
        
    def __repr__(self):
        """
        Returns a representation of the timeseries object
        
        If the length of the timeseries is greater than five we abreviate the values in between 
        the first and last values. 
        """
        name = type(self).__name__
        
        if len(self) <= 5:
            all_samples = [(t, v) for t, v in zip(self._times,self._values)]
            return "{}({})".format(name, all_samples, len(self))
        else:
            first_sample = (self._times[0],self._values[0])
            last_sample = (self._times[-1], self._values[-1])
            return "{}({}...{})".format(name, first_sample, last_sample, len(self))
        
    def __contains__(self, time):
        return (time in self._times)
    
    def __iter__(self):
        for value in self._values:
            yield value
            
    def __eq__(self, ts):
        return self.items == ts.items
            
    @property
    def times(self):
        """
        Returns a sequence of the times within time series object
        """
        return self._times
    
    @property
    def values(self): 
        """
        Returns a sequence of the values within time series object
        """
        return self._values
    
    @property
    def items(self):
        """
        Returns a sequence of time, value tuples within time series object
        """
        return [(t,v) for t,v in zip(self._times,self._values)]
    
    @property 
    def lazy(self):
        """
        Return a new LazyOperation instance using an identity function and 
        self as the only argument. This wraps up the TimeSeries instance 
        and a function which does nothing and saves them both for later.
        """ 
        def func(self):
            return self
        
        return LazyOperation(func, self)
    
    def interpolate(self, times):
        """
        Takes a sequence of times and returns a new time series object with 
        values that are generated from the values within the current time series object
        """
        values = []
        
        for time in times:
            
            right_index = np.searchsorted(self._times, time, side='right')
            
            if right_index == len(self):
                values.append(self._values[-1])
                continue
            
            if right_index == 0:
                values.append(self._values[0])
                continue
                    
            left_index = right_index - 1

            time_delta = float(self._times[right_index] - self._times[left_index])            
            val_delta = float(self._values[right_index] - self._values[left_index])
            
            slope = time_delta / val_delta
            step = (time - self._times[left_index]) / slope
            
            values.append(self._values[left_index]+step)
            
        return TimeSeries(times, values)
    
    def mean(self):
        return np.mean(self._values)
    
    def median(self):
        return np.median(self._values)
    
    def itertimes(self):
        for time in self.times:
            yield time
            
    def itervalues(self):
        for value in self.values:
            yield value
            
    def iteritems(self):
        for item in self.items:
            yield item