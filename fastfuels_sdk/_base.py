import json


class FastFuelsResource:
    """
    Base class for all FastFuels resources. It provides methods for
    serializing and deserializing instances to and from JSON and dictionaries.
    """

    def to_json(self) -> str:
        """
        Serialize the instance into a JSON string.

        Returns
        -------
        str
            The instance serialized into a JSON string.
        """
        return json.dumps(self.__dict__, default=str)

    def to_dict(self) -> dict:
        """
        Return the instance as a dictionary.

        Returns
        -------
        dict
            The instance as a dictionary.
        """
        return self.__dict__

    @classmethod
    def from_json(cls, json_str: str):
        """
        Create an instance of the class from a JSON string.

        Parameters
        ----------
        json_str : str
            The JSON string representing an instance of the class.

        Returns
        -------
        FastFuelsResource
            The instance created from the JSON string.
        """
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create an instance of the class from a dictionary.

        Parameters
        ----------
        data : dict
            The dictionary representing an instance of the class.

        Returns
        -------
        FastFuelsResource
            The instance created from the dictionary.
        """
        return cls(**data)
