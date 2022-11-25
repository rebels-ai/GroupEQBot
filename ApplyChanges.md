
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
- [x] Assets (completly empty)
- [x] Configurations (completly empty)
- [x] Drivers (root is not finished - fulfill & apply changes to per each submodule)
- [x] Interfaces (root is empty - fulfill & apply changes to per each submodule)
- [x] Storage (apply changes)
- [x] utilities (completly empty)


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
- [x] Drivers
- [x] Interfaces
- [x] Storage
- [x] utilities