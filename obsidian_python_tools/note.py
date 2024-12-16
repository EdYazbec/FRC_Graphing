import os

from .content import Content


class Note:
    def __init__(self, name: str, content: Content) -> None:
        '''A object representing a single obsidian .md note / file.

        Parameters
        ----------
        name : str
            The File name of the note.
        content : Content
            The content of the note
        '''
        self.name = name
        self._file_name = self.name + '.md'
        self.content = content

    @classmethod
    def from_md(cls, md_file_path: str) -> 'Note':
        '''Creates a Note object from a .md file path.

        Parameters
        ----------
        md_file_path : str
            The path of the .md file.

        Returns
        -------
        Note
            The Note object representing the file.
        '''
        # grab the name from the file path
        name = os.path.basename(md_file_path)

        # parse the file for content
        content = Content.from_md(md_file_path)

        # return the note object
        return cls(name, content)

    def __str__(self) -> str:
        '''Creates a str of the Note object. 
        The str is how the Note would be written in a .md file.

        Returns
        -------
        str
            The Note as would be written in a .md file.
        '''
        text = (self.name + '\n')
        text += str(self.content)
        
        return text

