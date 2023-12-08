"""
Date + time action file:
Consists of datetime_query_action class containing get data, parse data, substitute data, get location and perform action methods
Responsible for getting data related to world time queries, use additional methods for validation, forming sentences, substituting into sentence templates

To Note:
Very basic level implementation to facilitate further varied demonstration of subsequent modules
"""


import datetime
import requests

class datetime_query_action:
    def __init__ (self):
        """
        To Do:
        Initialize World Time API key with {} used to format entity labels

        Pseudocode:
        - self.url = "loremipsumdolor"

        """
        # self.url =
        pass


    def get_data(self, labels):
        """
        Uses API url to request for world time information and form a sentence based on given information

        Args:
        - labels (list): entities labels (locations) passed to give context to user queries

        Execution:
        - Use system datetime to form simple response with current hour and minute

        Returns:
        - response (string): sentence formed with weather information

        To note:
        - Method to be changed to use data returned from world time api returning json data
        """

        now = datetime.datetime.now()
        response = 'Time is {} {}'.format(now.hour, now.minute)
        return response

    def parse_data(self, json_data):
        """
        Note: separate method to be used to parse json data returned from get_data method

        Args:
        - json_data (json): weather data

        Pseudocode:
        - hour = json_data['hour']
        - min = json_data['minutes']

        Returns:
        - dictionary (dict): parsed time information
        """

        pass

    def substitute_data(self, dict1, location):
        """
        Note: separate method to be used to substitute parsed json data from parse_data method to form sentences at random (varying responses)

        Args:
        - dict1 (dict): contains parsed json data in dictionary form
        - location (string): contains location associated with time query

        Pseudocode:
        - sentence = "The current time in {location} is {hour}:{min}"
        - sentence = "Current time is {hour}:{min} in {location}"
        - sentence.randint if (0-1): return sentence

        Returns:
        - sentence (string): formed time sentence
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

        To Note:
        - Pseudocode to be implemented to change from exclusively getting raw system data to use additional methods facilitating world time API responses
        """

        response = self.get_data(labels)

        return response
