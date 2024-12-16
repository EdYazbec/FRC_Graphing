from typing import Union
import re

from .data_view import DataView


class Content:
    def __init__(self, data: list[Union[str, DataView]]) -> None:
        '''An object containing text and / or a Data view

        Parameters
        ----------
        data : list[Union[str, DataView]]
            A list of strings and / or a DataView object.
        '''
        self.data = data

    @classmethod
    def from_md(cls, md_file_path: str) -> 'Content':
        '''Creates a Content object from a .md file path.

        Parameters
        ----------
        md_file_path : str
            The path of the .md file.

        Returns
        -------
        Content
            A Content object.
        '''
        data = []

        # define a pattern to extract the dataview
        yaml_pattern = r'^---\n(.*?)\n---\n(.*?)$'

        # open the file
        with open(md_file_path, 'r') as file:
            # Read the entire file content
            file_content = file.read()
        
            # attempt to find the data view content
            match = re.search(yaml_pattern, file_content, re.DOTALL)

            # if found
            if match:
                # create a data view and add it to the list of data
                data_view = DataView.from_text(match.group(1))
                data.append(data_view)

                # update the file content to be the remaining content
                file_content = match.group(2)

                #TODO: implement file links
                data.append(file_content)

        return cls(data)

    def __str__(self) -> str:
        '''Creates a str of the Content object. 
        The str is how the content would be written in a .md file.

        Returns
        -------
        str
            The content as would be written in a .md file.
        '''
        text = ''
        for data in self.data:
            text += str(data)
            text += '\n'
        
        return text
