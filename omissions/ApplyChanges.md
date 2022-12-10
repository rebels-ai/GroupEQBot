
# Documentation
Apply general structure for the documentation:

    - problem statement (what the module (folder) stands for)

    - structure of folders with mindful description

    - technical description (if module is required to be described from technical point of view)

Example:
1. `Assets`

# Problem Statement
Stands for persisting validation questions, which are further configured in `configurations.(sample.yaml | configuration.yaml)` file.
There are no any constraints in namings as well as structuring. 

# Structure
```bash
- audio - folder, which stands for stroing audio questions
    ...

- text - folder, which stands for stroing text questions
    ...
```

# ACTION: documentation
- [] Assets (completly empty)
- [] Configurations (completly empty)
- [] Drivers (root is not finished - fulfill & apply changes to per each submodule)
- [] Interfaces (root is empty - fulfill & apply changes to per each submodule)
- [] Storage (apply changes)
- [] utilities (completly empty)


# Docstrings
Apply general action per each class:
```
class XYZ:
    """ Interface to ...

        Usage:
            XYZ().foo()
    """
    
    def foo(self):
        """ I'm here for the sake of example. """
        ...
```

# ACTION: docstrings
- [] Drivers
- [] Interfaces
- [] Storage
- [] utilities