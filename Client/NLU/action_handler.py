"""
Action Handler file:
Consists of ActionFactory class implementing factory design pattern containing get instance, create action and handle intent method
Responsible for dynamically creating instances of action classes based on specified intent
"""

import importlib
import os


class ActionFactory:
    _factory = None

    @staticmethod
    def get_instance():
        """
        Implements singleton pattern, method set to static ensuring that only one instance of ActionFactory class is created
        If an instance doesnt exist, it creates one, otherwise returns the existing instance

        Returns
        - singleton instance of ActionFactory
        """

        if ActionFactory._factory is None:
            ActionFactory._factory = ActionFactory()
        return ActionFactory._factory

    def create_action(self, intent):
        """
        Creation of instances of action classes based on intent

        Args:
        - intent (string): specified intent designated to create class from

        Execution:
        - Uses intent parameter to dynamically import and create an instance of the corresponding 'action' class
        - Constructs the module name based on the intent and imports it
        - Retrieves the action class from the module and creates an instance of it
        - If there is an exception (if module doesnt exist), raise a value error with helpful message

        Returns:
        - action_class() (class): Action class derived from specified intent
        """

        try:
            module_name = f"NLU.Actions.{intent}_action"
            action_module = importlib.import_module(module_name)
            action_class = getattr(action_module, f"{intent}_action")
            return action_class()

        except Exception as e:
            raise ValueError(f"Action not implemented!: {intent}")

    def handle_intent(self, intent, entities, labels):
        """
        Calls methods to perform creation of action classes, performing associated functionality

        Args:
        - intent (string): specified intent for action class creation
        - entities (list): list of entity texts
        - labels (list): list of entity labels

        Execution:
        - Passes intent parameter to create_action method to return an instance of the action class corresponding to the intent
        - Passes entities and labels list parameters to perform_action method on the created action instance

        Returns:
        - result of execution (string): text returned from created action's perform_action method
        """

        action = self.create_action(intent)
        return action.perform_action(entities, labels)
