from abc import abstractmethod

from ..radiosonde import  Radiosonde
from ..radiosonde import  RadiosondeList

class BaseSondeLoader:
    """Base loader interface for radiosonde to define common loading
    interface

    To use: 
    >>> loader = SondeLoader(filepath=path)
    >>> loader.list_vars()
    ['U','UDir', 'z', 'p' ..]
    >>> loader.available()
    TODO: Some  representation of radiosonde here. 
    >>> loader.load(start='2018-09-13 11:00:00', '2018-09-13 20:00:00')
    TODO: Some  representation of radiosonde here. 
    """

    def __init__(self, filepath):
        """Init. 

        Args:
           filepath  (str) : filepath  or directory path (for list of files)
        """
        self.filepath = filepath

    @abstractmethod
    def list_vars(self):
        """Return a list of available parameters in the given source

        TODO: There should be a check to ensure uniformity of all files. 

        Returns: 
            list[str] : variables names
        """
        assert self._is_var_uniform(), "varaibles needs to be uniform"

    def _is_var_uniform(self):
        """Check if variables names across files are the same. 

        TODO

        Note: 
            To implement, make sure clear criteria is sticked to.
        """

        return True

    def _is_criteria_valid(self):
        """Check if the criteria passed to available and load are valid

        TODO

        """

        return True


    @abstractmethod
    def available(self,  criteria : dict):
        """Peek first understand available radiosondes based on certain criteria. 

        Args:
            criteria (dict) : dictionary for criteria when testing radiosonde
            data

        Notes: 
            criteria is arbitrary based on the available vars and data format
            (for recursing into all files). Specific implementation is
            required. 
        """
        pass

    @abstractmethod
    def load_one(self, launchtime):
        """Abstract interface for radiosonde loader

        Args:
           start, end (str) : iso_format timestring used for bounding sounde
               launchtimes

        Returns: 
            Radiosonde : The composite type of radiosonde collections. 
        """
        pass

    def load_many(self, launchtime_list, verbose=True):

        sondeList =  RadiosondeList()
        for time  in launchtime_list:
            sondeList.add(self.load_one(time))
            print(f"Sonde at {time} downloaded succesfully")
        return sondeList
