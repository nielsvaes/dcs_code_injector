## 1.4.8
* Bug fix for Ctrl -X

## 1.4.7
* Added keyboard shortcut Ctrl -X to delete the current line
* Added keyboard shortcut Ctrl -D to duplicate the current line

## 1.4.6
* Added checkbox in the View menu to turn off the log view in case you're using an external log viewer

## 1.4.5
* Copying of hook file is now an option in the settings that defaults to False

## 1.4.4
* Various bug fixes 
* Hook file will be automatically copied every time the application starts
* Stability improvements when executing code in the game. Whenever DCS needs to run code, there's a chance it will pause for a fraction of a second. Ideally the server runs in a separate thread, but I don't have the energy to research how to make a compiled C++ DLL right now to do that. Have to look into the Olympus guys' code maybe. Anyway, never eat yellow snow. 

## 1.4.3
* Keeping indentation when pressing enter.
* Backspace will remove any leading 4 x space to jump back an indentation level

## 1.4.2
* Added ability to pick font for log view
* Added ability to pick font for code view
* Added ability to change between Material Neon and Fusion Dark themes
* Settings typo fix

## 1.4.1
* Fixed a bug where the code wasn't reliably sent to DCS. You need to do Tools > Copy Hook File to make sure it works. 

## 1.4.0
* Added code completion
* Added code editor quality of life updates

## 1.3.0
* Flipped the connection: DCS is now the server and the Code Injector is the client. This help gain back just about all lost frames from the hook code. 
* Added a version dialog

## 1.2.7
* Added pygtail to requirements

## 1.2.6
* Removed leftover import

## 1.2.5
* Bugfix for not showing entire error messages
* Fix for Lua hook sometimes not working

## 1.2.4
* Added optional error sound when there are mission scripting errors
* Check to see if port for server is available on startup

## 1.2.3
* Added line numbers to the code views
* Refactoring of classes and modules

## 1.2.1
* Added versioner that makes a back up of the settings file on startup. Back ups are saved in a .local_history folder next to the settings file

## 1.2.0
* Updated settings file, old settings should be converted to new settings on first startup. Your old settings are saved in an `__OLD` file in your Documents/dcs_code_injector folder.
* Added support for picking log highlighting colors
* Log and code views can now be updated independently
* Window transform and scale is saved after shutdown
* Added ability to write the hook file from the tool instead of people having to manually copy it over

## 1.1.1
* Bugfix when creating new code tab

## 1.1.0
* Added Ctrl-F to search the log

## 1.0.4
* Version bump to test build and deploy pipeline

## 1.0.3
* Updated CCMOOSE keywords


## 1.0.2
* First initial test release for the public
