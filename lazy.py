
class LazyOperation:
    
    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
        
    def eval(self):
        """
        Recursively evaluate LazyOperation object
        """
        arg_list = list(self.__args)
        for i, arg in enumerate(self.__args):
            if isinstance(arg, LazyOperation): 
                arg_list[i] = arg.eval()
        
        self.__args = tuple(arg_list)
                
        for key in self.__kwargs:
            if isinstance(self.__kwarg[key], LazyOperation):
                self.__kwarg[key] = self.__kwarg[key].eval()
                
        return self.__func(*self.__args, **self.__kwargs)