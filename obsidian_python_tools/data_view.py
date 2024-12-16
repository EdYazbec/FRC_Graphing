import yaml


class DataView:
    def __init__(self, data: dict):
        '''An object containing obsidian DataView data.

        Parameters
        ----------
        data : dict
            a dict of data for the data view
        '''
        self.data = data

    @classmethod
    def from_text(cls, text: str) -> 'DataView':
        '''Creates a DataView object from a block of text.
        The data view content should be at the beginning of text, bounded by "---"

        For example:

        ---
        name : John Doe
        Age : 18
        ---
        # More text below


        Parameters
        ----------
        text : str
            A block of text as described above

        Returns
        -------
        DataView
            The extracted DataView object.
        '''
        data = {}
        for line in text.splitlines():
            key, val = line.split(':', maxsplit=1)
            key = key.strip()
            val = val.strip()
            if val.isdigit():
                data[key] = int(val)
            elif val.replace('.', '', 1).isdigit():
                data[key] = float(val)
            elif val.lower() in ['true', 'false']:
                data[key] = val.lower() == 'true'
            else:
                data[key] = val

        return cls(data)

    def to_yaml(self) -> str:
        '''Creates a str of the DataView object. 
        The str is how the data would be written in a .md file.

        This may be redundant and removed in favor of __str__

        Returns
        -------
        str
            The data view content as would be written in a .md file.
        '''
        return yaml.dump(self.data)

    def __str__(self) -> str:
        '''Creates a str of the DataView object. 
        The str is how the data would be written in a .md file.

        Returns
        -------
        str
            The data view content as would be written in a .md file.
        '''
        text  = '---\n'
        text += self.to_yaml()
        text += '---'

        return text
        
