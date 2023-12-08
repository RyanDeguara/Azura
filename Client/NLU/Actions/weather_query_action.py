"""
Weather action file:
Consists of weather_query_action class containing get data, parse data, substitute data, get location and perform action methods
Responsible for getting data related to weather queries, use additional methods for validation, forming sentences, substituting into sentence templates

To Note:
Basic level implementation to facilitate further demonstration of subsequent modules
"""

import requests

class weather_query_action:
    def __init__ (self):
        """
        Initialize OpenWeatherMap API key with {} used to format entity labels
        """

        self.url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=18766f93e3f314a2a3cb842880cb279e&units=metric'
        
    
    def get_data(self, labels):
        """
        Uses API url to request for weather information and form a sentence based on given information

        Args:
        - labels (list): entities labels (locations) passed to give context to user queries

        Execution:
        - Loops through labels (locations) list formatting API url request passing label increment to get data corresponding to label
         - Returns json data from request, parse it to grab important weather information
        - Use label, temperature and weather description to form sentence
        - Check if wind levels are high, if so append helpful sentence to end of response

        Returns:
        - response (string): sentence formed with weather information

        To note:
        - Method to be changed to exclusively get data from api returning json data - label formatting, parsing and sentence forming to be done in separate methods
        """

        for label in (labels):
            parse = self.url.format(label)
            res = requests.get(parse)
            data = res.json()
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind = data['wind']['speed']
            description = data['weather'][0]['description']
            temp = data['main']['temp']

        # print('Temperature:',temp,'°C')
        # print('Wind:',wind)
        # print('Pressure: ',pressure)
        # print('Humidity: ',humidity)
        # print('Description:',description)
        # print(data)

        response = f"{labels[0]} will have temperature of {temp} with some {description}"
        if (wind > 5):
            response += " and will be windy"

        return response
    
    def parse_data(self, json_data):
        """
        Note: separate method to be used to parse json data returned from get_data method

        Args:
        - json_data (json): weather data

        Pseudocode:
        - precipitation = json_data['precipitation']
        - if precipitation > 8:
        -    dictionary.append(key='precipitation', value=precipitation)

        Returns:
        - dictionary (dict): parsed weather information
        """

        pass

    def substitute_data(self, dict1, location):
        """
        Note: separate method to be used to substitute parsed json data from parse_data method to form sentences at random (varying responses)

        Args:
        - dict1 (dict): contains parsed json data in dictionary form
        - location (string): contains location associated with weather query

        Pseudocode:
        - sentence = "{location} will be {hot/cold} at a temp of {temperature} this evening"
        - sentence = "Generally {hot/cold} at a temp of {temperature} predicted for {location} tonight"
        - sentence.randint if (0-1): return sentence

        Returns:
        - sentence (string): formed weather sentence
        """

        pass
    
    def get_location(self, labels):
        """
        Note: Gets device location to address queries with no context provided

        Args:
        - labels (list): contains list of labels associated to entities in user query sentence

        Pseudocode:
        - if labels.contains('GPE')
        -   return label
        - else: use system info to get location

        Returns:
        - label (string): device system location or passed location
        """

        pass
    
    def perform_action(self, entities, labels):
        """
        Standardized method across all action classes, to perform associated action methods functionality

        Args:
        - entities (list): contains list of entities associated in sentence
        - labels (list): associated entities labels passed to give context to user queries

        Pseudocode:
        - try:
        -   location = get_location(labels)
        -   json_data = get_data(location)
        -   dict1 = parse_data(json_data)
        -   response = substitute_data(dict1, location)
        - except:
        -   response = "Didn't provide sufficient data"

        Returns:
        - response (string): containing relevant response formed for weather query or validated response
        """

        try:
            response = self.get_data(labels)
        
        except: 
            response = "Did not provide sufficient data"

        return response
