# guidb
The aim of this project is to create a visual way of sorting organizing various files.
While this can be done with any set of files, the main goal will be to focused on media (images, videos).

In order to do this, a local SQLite3 database will be used to store all relevant information and TKinter will be used to provide a GUI.

# TODO
* GUI
  * Offer a method of adding columns/attributes
  * Provide a way of previewing files.  Include a way of generating these previews without relying on external libs?
    * Images: Contact sheet
    * Videos: One image preview or gif of 10 frames

* DB
  * Provide a way to automatically update entries if a file is moved or renamed (hashing?)
  * When using a custom constructor for columns/types need to make sure to do a type check to make sure input is correct
  * Function to check for typeof() when either passing in initial columnTypeList or when adding a new column