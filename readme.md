# ChemLib by Chem
## Description
ChemLib is a python framework for developers that is human readable and intuitive. It simplifies and accelerates development by providing highly functional, standardized building blocks so that you can focus on what makes your project unique. The classes and methods all follow a standardized convention, allowing you to spend less time reading documentation.
## Styling and Conventions
- Single quotes ('') are used first, and double quotes ("") are used inside of single quotes. The reason for this is many languages use single quotes for character literals, and double quotes for string literals. This makes escaping easier when creating strings that will be interpreted by other languages.
### Source Comments:
```
#   -> functional code that has been temporarily disabled.
##  -> code comments that should be included in production.
### -> psuedocode, notes, todo items, etc.; should be removed before production.
```
### Import String Delimiters:
```
|:|
```

### Commits:
Commits will list the changes made and to what file/object they are made if the commit is a finished product. For in-progress changes, the commit will be the date and commit number for that date in the format {YYYMMDD###}.

## Future Features:
 - files.py:
    - method for locking file, then reading it, then writing changes to the file, before unlocking it
    - CONSIDER CHANGING "FILE_READ", "FILE_WRITE", ETC., TO "READ_FILE", "WRITE_FILE", ETC.


 - module for tracking files in multiple repos (ex lumberjack still lives in local repo but also changes get pushed to public repo)
