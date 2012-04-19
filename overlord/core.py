"""
Created on Apr 19, 2012

@author: quermit
"""


class StatisticsManager(object):
    
    def __init__(self):
        self.call_stats = []
    
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance
    
    def create_call_stats(self, module, function):
        stats = _CallStatistics(module, function)
        self.call_stats.append(stats)
        return stats


class _CallStatistics(object):
    
    _TIME_CONST = 0.01
    
    def __init__(self, module, function):
        self.module = module
        self.function = function
        self.min_time = None
        self.max_time = None
        self.avg_time = None
        self.calls = 0
        self.errors = 0
    
    def add_success(self, exec_time):
        self.calls += 1
        if self.calls == 1:
            self.min_time, self.max_time, self.avg_time = [exec_time] * 3
            return
        self.min_time = min(self.min_time, exec_time)
        self.max_time = max(self.max_time, exec_time)
        self.avg_time = self._exp_mov_avg(
                self.avg_time, exec_time, self._TIME_CONST)
        print "%s %s %s" % (self.min_time, self.max_time, self.avg_time)
    
    def add_failure(self, exception):
        self.calls += 1
        self.errors += 1
        
    def _exp_mov_avg(self, curr_val, next_val, time_const):
        return (1.0 - time_const) * curr_val + time_const * next_val
