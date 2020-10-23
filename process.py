""" Module containing a class to process rainfall data."""
import pandas as pd 
import numpy as np 
from urllib import urlopen 

class Reader:
    """Class to process rainfall data."""

    def __init__(self, filename):

        self.data = pd.read_csv(filename)
        
        """Read in the rainfall data from a named .csv file using pandas

        The data is stored in a class variable reader.data

        Parameters
        ----------

        filename: str
            The file to be read

        >>> Reader('rainfall.csv').data.loc[0].stationReference
        'E12560'
        """

    def station_total_rainfall(self, station_ref):

        data1 = self.data[~self.data['value'].isin(['0.0|0.2'])]
        subset = data1[data1['stationReference'] == station_ref]
        subset_float = subset['value'].astype(float)
        total_rainfall = subset_float.sum()
        
        """Return the total rainfall at station reference station_ref.

        Parameters
        ----------

        station_ref: str
            Station Reference

        Returns
        -------

        float
            Total rainfall

        >>> round(Reader('rainfall.csv').station_total_rainfall('E24767'), 1)
        2.6
        """

        return total_rainfall

    def station_rainfall(self, station_ref):
        
        data1 = self.data[~self.data['value'].isin(['0.0|0.2'])]
        subset1 = data1[data1['stationReference'] == station_ref]
        a = np.array(subset1.value).tolist()
        b = np.array(subset1.dateTime).tolist()
        subset2 = pd.Series(a, index = b)

        """Return the rainfall at station reference station_ref
        as a pandas Series, indexed by the dateTime series.

        Parameters
        ----------

        station_ref: str
            Station Reference

        Returns
        -------

        pandas.Series
            Station rainfall values (indexed by date & time)

        >>> series = Reader('rainfall.csv').station_rainfall('E24767')
        >>> float(series.loc['2020-10-12T02:00:00Z'])
        0.2
        """

        return subset2

    def station_url(self, station_ref):
        
        data1 = self.data[~self.data['value'].isin(['0.0|0.2'])]
        subset1 = data1[data1['stationReference'] == station_ref]     
        station_url = subset1.station.iloc[0]

        """Return the API URL for station reference station_ref

        Parameters
        ----------

        station_ref: str
            Station Reference

        Returns
        -------

        str
            REST API URL
        

        >>> Reader('rainfall.csv').station_url('261923TP')
        'http://environment.data.gov.uk/flood-monitoring/id/stations/261923TP'
        """ 

        return station_url

    def station_location(self, station_ref):
        
        data1 = self.data[~self.data['value'].isin(['0.0|0.2'])]
        subset1 = data1[data1['stationReference'] == station_ref]     
        station_url = subset1.station.iloc[0]
        data2 = pd.read_json(urlopen(station_url).read(),orient = 'recodes' )
        data2_sub = data2['items']

        """Returns API reported easting and northing for station
        reference station_ref

        Parameters
        ----------

        station_ref: str
            Station Reference

        Returns
        -------

        tuple
            easting, northing pair

        >>> Reader('rainfall.csv').station_location('E24767')
        (623550, 274550)
        """

        return (data2_sub.easting,data2_sub.northing)

