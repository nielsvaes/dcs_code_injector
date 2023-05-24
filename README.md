# 📲 DCS Code Injector

_Don't worry, I'll change the name to something cool later_ 🌴🥥

Questions or concerns? Find me under the name `coconutcockpit` on my Discord server: https://discord.gg/jQbWJSK2cw

## 🙋‍What is it?
It's a small program that you can run alongside DCS to influence a mission while it's running. I use it a lot quickly trying out scripting ideas without having to reload the mission all the time. It's a REPL (Read-Eval-Print-Loop) that I kind of based on Autodesk Maya's script editor.

Right now it's only designed to run in an active mission, but this might change in the future. 

## 💾 How to download
You can grab a .zip file that contains an executable that should run on any Windows machine from the releases page here: https://github.com/nielsvaes/dcs_code_injector/releases

If you have Python installed on your computer, you can also find it on `PyPi` and `pip` install it with the following command:

`pip install dcs-code-injector`

It also makes an entry point to the application, so type `dcs-code-injector` to run it.


## 🪝 Add the hook
Find a file called `dcs-code-injector-hook.lua` in the Github repository or in the downloaded .zip archive. You need to copy this file into the `Scripts/Hooks` folder inside your `Saved Games/DCS.openbeta` or `Saved Games/DCS` folder. Remember where you put the `SRS` hook file? This one goes right next alongside it :)


## 🥇First time use
When you open the application for the first time, you need to tell it where your `dcs.log` file is saved. Browse to the file (it's in your `Saved Games` folder and then just close the `Settings` dialog to save the path. You will then be presented with the main window and the log panel. The log gets updated automatically while DCS is running, so it's easy to see if you're getting any errors or warnings when running code. 

## ❓How to use
Press `Ctrl-N` to make a new tab. This will add a new `UNNAMED`. `UNNAMED` tabs are not saved by on shutdown, so it's best to rename the tab if you want to keep the code around for later use. Double-click on the tab name to rename it. Anything you write in a tab is saved automatically.

Select a block of code and press `Ctrl-Enter` or `Ctrl-Return` to execute it. The code block will appear in the log panel and will be run inside the mission. Any errors in the code will show up as red in the log.

You can save code you run often to `Favorite` buttons. I use this to reload MOOSE for example, when I've made changes to it. To save a button, select the code block and drag it to the blank strip beneath the code panel and above the connection icon. Pick a name and click save. To delete a  `Favorite` button, right click on it and click `Delete`.

## 🗺️Future plans
#### REPL
- Better code highlighting
- Code completion
- Just a better all-round coding feel

#### Other parts
The REPL is actually just a small part of larger project I had in mind. Future plans include:

- Battlefield Commander Mode: This will show a map with all the units in the mission that you can manipulate in real time. In a limited testing mode I've used this to turn on SAM sites, spawn enemy fighters and things like that. I haven't really used LotATC, but I think it offers similar functionality.
- Integration with Standalone Servers
- Plugins
- and more!

## 🤙Contributing
I am not a hardcore code or programmer, so if you are and want to lend a helping hand, GREAT! Fork the project and create a PR with your changes.


## 📖License
Licensed under GNU GENERAL PUBLIC LICENSE v3

