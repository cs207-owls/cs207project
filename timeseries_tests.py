import unittest
import types
import numpy as np
from timeseries import *

class MyTest(unittest.TestCase):
    
    def test_init(self):
        # Check that length of time and value sequences are equal
        times = list(range(10))
        values = np.random.rand(len(times)-1)
        with self.assertRaises(AssertionError):
            ts = TimeSeries(times, values)
            
    def test_len(self):
        times = list(range(10))
        values = np.random.rand(len(times))
        ts = TimeSeries(times, values)
        self.assertEqual(len(ts), len(times))
            
    def test_getitem(self):
        times = list(range(10))
        values = np.random.rand(len(times))
        ts = TimeSeries(times, values)
        index = 4
        right_time = times[index]
        right_value = values[index]
        self.assertEqual(ts[right_time], right_value)
        
    def test_setitem(self):
        times = list(range(10))
        values = np.random.rand(len(times))
        ts = TimeSeries(times, values)
        index = 4
        right_time = times[index]
        right_value = values[index]
        self.assertEqual(ts[right_time], right_value)
        new_value = 10
        ts[right_time] = new_value
        self.assertEqual(ts[right_time], new_value)
    
    def test_contains(self):
        times = list(range(10))
        values = np.random.rand(len(times))
        ts = TimeSeries(times, values)
        valid_time = times[1]
        invalid_time = -3
        self.assertTrue(valid_time in ts)
        self.assertFalse(invalid_time in ts)
        
    def test_eq(self):
        times = list(range(10))
        values = np.random.rand(len(times))
        ts1 = TimeSeries(times, values)
        ts2 = TimeSeries(times, values)
        self.assertEqual(ts1, ts2)
            
    def test_interpolate(self):
        a = TimeSeries([0,5,10], [1,2,3])
        b = TimeSeries([2.5,7.5], [100, -100])
        # Simple cases
        self.assertEqual(a.interpolate([1]), TimeSeries([1],[1.2]))
        self.assertEqual(a.interpolate(b.times), TimeSeries([2.5,7.5], [1.5, 2.5]))
        # Boundary conditions
        self.assertEqual(a.interpolate([-100,100]), TimeSeries([-100,100],[1,3]))
    
    def test_lazy(self):
        times = list(range(10))
        values = np.random.rand(len(times))
        ts = TimeSeries(times, values)
        self.assertEqual(ts, ts.lazy.eval())
                         
    def test_itertimes(self):
        times = list(range(10))
        values = np.random.rand(len(times))
        ts = TimeSeries(times, values)
        self.assertListEqual(list(ts.itertimes()), times)
        self.assertIsInstance(ts.itertimes(), types.GeneratorType)
        
    def test_itervalues(self):
        times = list(range(10))
        values = list(np.random.rand(len(times)))
        ts = TimeSeries(times, values)
        self.assertListEqual(list(ts.itervalues()), values)
        self.assertIsInstance(ts.itervalues(), types.GeneratorType)
        
    def test_iteritems(self):
        times = list(range(10))
        values = np.random.rand(len(times))
        ts = TimeSeries(times, values)
        self.assertListEqual(list(ts.iteritems()), list(zip(times,values)))
        self.assertIsInstance(ts.iteritems(), types.GeneratorType)
    
    def test_mean(self):
        times = list(range(10))
        values = np.random.rand(len(times))
        ts = TimeSeries(times, values)
        self.assertEqual(ts.mean(), np.mean(values))
        
    def test_median(self):
        times = list(range(10))
        values = np.random.rand(len(times))
        ts = TimeSeries(times, values)
        self.assertEqual(ts.median(), np.median(values))

if __name__ == '__main__':
    unittest.main()