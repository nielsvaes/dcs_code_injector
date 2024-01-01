![PyPI - Version](https://img.shields.io/pypi/v/dcs-code-injector)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/nielsvaes/dcs_code_injector/release.yml)
![Discord](https://img.shields.io/discord/1037079186524876820)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F1F4PYTO7)

# Supported by JetBrains' Open Source Development Project
<img src="https://github.com/nielsvaes/dcs_code_injector/assets/7821618/af6bdb1f-3dd4-4e27-be43-c03742874f68" alt="JetBrains" width="200"/>



# 📲 DCS Code Injector

_Don't worry, I'll change the name to something cool later_ 🌴🥥

Questions or concerns? Find me under the name `coconutcockpit` on my Discord server here: ![Discord](https://img.shields.io/discord/1037079186524876820)

Here's a video of an older version in action: https://youtu.be/m2tGLFgLp8Y

![01](https://github.com/nielsvaes/dcs_code_injector/assets/7821618/e2bfb31a-87c7-4258-9cf8-89e78bb8c65f)

## 🙋‍What is it?
It's a small program that you can run alongside DCS to influence a mission while it's running. I use it a lot to quickly try out scripting ideas without having to reload the mission all the time. It's a REPL (Read-Eval-Print-Loop) that I kind of based on Autodesk Maya's script editor.

Some things other people have been using it for: 
 - Something happened in a mission that didn't fire a trigger. Instead of calling it quits we got to activate the event that was supposed to happen
 - Adding extra functionality to paid campaigns, such as a splash damage script.
 - Spawning new enemies in a mission without having to set up a bunch of radio commands
 - ... 



## 💾 How to download
You can grab a .zip file that contains an executable that should run on any Windows machine from the releases page here: https://github.com/nielsvaes/dcs_code_injector/releases

If you have Python installed on your computer, you can also find it on `PyPi` and `pip` install (and upgrade) it with the following command:

`pip install --upgrade dcs-code-injector`

It also makes an entry point to the application, so type `dcs-code-injector` to run it.

⚠️ False antivirus positives! 
All code is written in Python. To make it easier for people who don't have Python installed, I use a package called [Nuitka](https://github.com/Nuitka/Nuitka) to make it an executable that runs on Windows. A side effect of this is that sometimes it triggers antivirus software because they think it's a trojan. It is not. All the code for the program is available here on the github page. If you're running into troubles, it's easier to just use Python to run the program instead of the executable. Feel free to reach out to me if you need help getting it up and running with just Python.

## 🥇First time use
When you open the application for the first time, you need to tell it where your `dcs.log` file is saved. Browse to the file (it's in your `Saved Games` folder) and save the settings. You will then be presented with the main window and the log panel. The log gets updated automatically while DCS is running, so it's easy to see if you're getting any errors or warnings when running code. 

## 🪝 Add the hook
A Lua hook needs to be loaded in order to tell DCS to connect to the application. The easiest way to do this is to go to `Tools > Copy hook file`. ⚠️ You need to have set the path to your `dcs.log` file for this to work, since it uses that log's location to figure out where the hook should go

![image](https://github.com/nielsvaes/dcs_code_injector/assets/7821618/d7f3b81f-180e-4c54-ab22-2b649ea4d75f)

> In case this doesn't work (but it really should!) you can copy the file over manually:
Find a file called `dcs-code-injector-hook.lua` in the Github repository or in the downloaded .zip archive. You need to copy this file into the `Scripts/Hooks` folder inside your `Saved Games/DCS.openbeta` or `Saved Games/DCS` folder. Remember where you put the `SRS` hook file? This one goes right next alongside it :)

## ✒️ Edit MissionScripting.lua
In the `Scripts` folder if your DCS install directory, there's a file called `MissionScripting.lua`. Comment out the lines that start with `_G` to make sure the hook can load everything it needs to: 


`MissionScripting.lua:`
```Lua
local function sanitizeModule(name)
	_G[name] = nil
	package.loaded[name] = nil
end

do
	sanitizeModule('os')
	sanitizeModule('io')
	sanitizeModule('lfs')
	--_G['require'] = nil
	--_G['loadlib'] = nil
	--_G['package'] = nil
end
```

## ❓How to use
Press `Ctrl-N` to make a new tab. This will add a new `UNNAMED` tab. `UNNAMED` tabs are not saved on shutdown, so it's best to rename the tab if you want to keep the code around for later use. Double-click on the tab name to rename it. Anything you write in a tab is saved automatically.

Select a block of code and press `Ctrl-Enter` or `Ctrl-Return` to execute it. The code block will appear in the log panel and will be run inside the mission. Any errors in the code will show up as red in the log.
If nothing is selected, all the code in the currrent active code tab will be executed

You can save code you run often to `Favorite` buttons. I use this to reload MOOSE for example, when I've made changes to it. To save a button, select the lines of code you want to save and drag them to the blank strip beneath the code panel and above the connection icon. Pick a name and click save. To delete a `Favorite` button, right click on it and click `Delete`.

Press `Ctrl-F` to open a search box in the Log view. The `Cc` toggles between case sensitive and insensitive search.

Use `Shift + Numpad+` and `Shift + Numpad-` to increase and decrease the log font size. 

Use `Ctrl + Numpad+` and `Ctrl + Numpad-` to increase and decrease the code font size. 

## 🎨 Log highlighting colors
I've added some "default" highlighting colors for the log. These are the colors that I'm using, but they might not be to everyone's liking. You can add new highlighting rules in the settings, they can be individual words or phrases or regular expressions. Select a rule and press the `delete` key to delete it. 

![image](https://github.com/nielsvaes/dcs_code_injector/assets/7821618/53866ae7-7fdb-4fc1-bf4e-eea50a7ea6b7)

You need to restart the application for the new rules to be applied. If you want to get the defaults back, just delete all the rules and restart. 


## 🎨 Code completion

The Code Injector supports some basic code completion for lightweight Lua, MOOSE and Mist
![code_completion](https://github.com/nielsvaes/dcs_code_injector/assets/7821618/e2b399d4-86f7-40cb-8d55-b4f0164a25e1)

You can update code completion for MOOSE and Mist from the settings
![image](https://github.com/nielsvaes/dcs_code_injector/assets/7821618/e4aaf417-0abc-49a2-9d52-06ff835f8a3f)

- Lua keywords are completed
- Variable names in the document are completed
- Function definitions in the document are completed
- It's a "dumb" completion model, it doesn't understand context, meaning:
```Lua
my_group = GROUP:FindByName("goose_and_maverick") -- <=== GROUP:FindByName... will be auto completed
my_group:GetVec3() -- <== "my_group" will be autocompleted, but "GetVec3()" will not be, since it doesn't know that "my_group" is a MOOSE GROUP
```


## 🗺️Future plans
#### REPL
- Better code highlighting

#### Other parts
The REPL is actually just a small part of larger project I had in mind. Future plans include:

- Battlefield Commander Mode: This will show a map with all the units in the mission that you can manipulate in real time. In a limited testing mode I've used this to turn on SAM sites, spawn enemy fighters and things like that. I haven't really used LotATC, but I think it offers similar functionality.
- Integration with Standalone Servers
- Plugins
- and more!

## 🤙Contributing
I am not a hardcore coder or programmer, so if you are and want to lend a helping hand, GREAT! Fork the project and create a PR with your changes.
Other ways you can contribute is by reporting issues or posting feature requests on the [Issues](https://github.com/nielsvaes/dcs_code_injector/issues) page of the GitHub repository. I started this project just to make my own life easier, but I would to hear what you might want to use it for!


## 📖License
Licensed under GNU GENERAL PUBLIC LICENSE v3

