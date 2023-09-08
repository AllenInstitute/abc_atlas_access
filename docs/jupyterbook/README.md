# JupyterBook Guide

## Anatomy of Jupyter Book 
- A configuration file (_config.yml) : Contains all of the configuration for the book
- A table of contents file (_toc.yml)
- The book’s content

## Notes For Modifying Existing Files (Files listed in _toc.yml)
- If .ipynb: Make sure to **execute** all the cells before saving the file
- If .md: N/A

## Notes For Adding New Files (Files not listed in _toc.yml)
- Add files to _toc.yml (Files are added as names with no extensions and relative to the book’s root folder.)
- If .ipynb: Make sure to **execute** all the cells before saving the file
- If .md: N/A

## Building The Book's HTML 
- This allows you to build the book locally. The command below will generate a fully-functioning HTML site using a static site generator.\
Run the following command: ```jupyter-book build PATH_TO_BOOK_ROOT_FOLDER/```
- **IMP**: If you have made many edits, it is recommended to first remove the _build directory then build.\
Run the following command: ```jupyter-book clean -a PATH_TO_BOOK_ROOT_FOLDER/```

## Publishing The Book
- **push** changes to **main** branch 
- **Note**: Do **not** push the _build directory 
- **Note**: A GitHub Action is already created to automatically build the book and update the website when a **push** event happens on **main**. Nothing else needs to be done. 

## Useful Resources
- JupyterBook Documentation: https://jupyterbook.org/en/stable/intro.html
- How to structure and organize content: https://jupyterbook.org/en/stable/basics/organize.html
- Command-line interface reference: https://jupyterbook.org/en/stable/reference/cli.html