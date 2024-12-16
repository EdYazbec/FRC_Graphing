import os

import obsidian_python_tools.obsidian_python_tools as opt


def load_notes_from_directory(dir: str) -> list[opt.Note]:
    # List the contents of the directory
    files = os.listdir(dir)

    # Iterate through the directory contents, creating notes
    notes = [opt.Note.from_md(os.path.join(dir, file)) for file in files]

    return notes


def main():
    team_notes = load_notes_from_directory('Fim Graph 2025/Teams/')
    event_notes = load_notes_from_directory('Fim Graph 2025/Events/')
    
    for n, note in enumerate(event_notes):
        print(n)
        print(note)
        print()


if __name__ == '__main__':
    main()
