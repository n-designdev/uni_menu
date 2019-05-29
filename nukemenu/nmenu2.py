# -*- coding: utf-8 -*-

import sys
import os

env_key = 'ND_TOOL_PATH_PYTHON'
ND_TOOL_PATH = os.environ.get(env_key,'Y:/tool/ND_Tools/python')
for path in ND_TOOL_PATH.split(';'):
    path = path.replace('\\','/')
    sys.path.append(path)

import nuke

from xml.dom.minidom import parse

class MenuSetupHandler:
    # constant variables
    menuTag = "menu";
    nameAttr = "name";
    menuItemTag = "menuItem";
    commandAttr = "command";
    shortcutAttr = "shortcut";
    categoryTag = "category";

    # data
    menuName="";
    menuCategoryNames=[];
    menuItemNames=[];
    menuItemCommands=[];
    menuItemShortcuts=[];

    # Getter Methods -----------------------------------
    def GetMenuName(self):
        return self.menuName;

    def GetMenuItemNames(self):
        return self.menuItemNames;

    def GetMenuItemCommands(self):
        return self.menuItemCommands;

    def GetMenuItemShortcuts(self):
        return self.menuItemShortcuts;

    def GetMenuCategoryNames(self):
        return self.menuCategoryNames;
    
    # Setter Methods -----------------------------------
    # store data into class members
    def SetDataFromXML(self, xmlPath):
        self.menuCategoryNames=[];
        self.menuItemNames=[];
        self.menuItemCommands=[];
        self.menuItemShortcuts=[];
        self.Shortcutlists=[]

        dom = parse(xmlPath);#パース処理
        root = dom.documentElement;#xmlのdocmentelement
        menuElem = root.getElementsByTagName(self.menuTag)[0];#rootからmenutag→今回はmenu
        menuName = menuElem.getAttributeNode(self.nameAttr);#menuからnameAttr→今回はmenu
        self.menuName = menuName.nodeValue;#menunameのnodevalue
        menuChildNodes = menuElem.childNodes;
        for menuChild in menuChildNodes:
            if menuChild.nodeName == self.categoryTag:
                categoryName = menuChild.getAttributeNode(self.nameAttr);
                self.menuCategoryNames.append(categoryName.nodeValue);
                self.menuItemNames.append([]);
                self.menuItemCommands.append([]);
                self.menuItemShortcuts.append([]);

                categoryChildNodes = menuChild.childNodes;
                for categoryChild in categoryChildNodes:
                    if categoryChild.nodeName == self.menuItemTag:
                        menuItemName = categoryChild.getAttributeNode(self.nameAttr);
                        self.menuItemNames[-1].append(menuItemName.nodeValue);
                        menuItemCommand = categoryChild.getAttributeNode(self.commandAttr);
                        self.menuItemCommands[-1].append(menuItemCommand.nodeValue);
                        menuItemShortcut = categoryChild.getAttributeNode(self.shortcutAttr);
                        if menuItemShortcut == None:
                            self.menuItemShortcuts[-1].append(0);
                        else:
                            self.menuItemShortcuts[-1].append(menuItemShortcut.nodeValue);
                            if str(menuItemShortcut.nodeValue) in self.Shortcutlists:
                                print "################################# WARNIG #####################################"
                                print ("ショートカット:" +str(menuItemShortcut.nodeValue)+" は重複しています。"+str(menuItemName.nodeValue)+' が優先されます。')
                                print "##############################################################################"
                                print " "
                            self.Shortcutlists.append(str(menuItemShortcut.nodeValue))


        dom.unlink()
        self

def setupMenu(pos='ND',menu=None):
    menuHnd = MenuSetupHandler();
    menuHnd.SetDataFromXML(r"C:\Users\k_ueda\Desktop\nmenu2.xml");
    menuLabel = menuHnd.GetMenuName();#self.menuname
    menuCategoryNames = menuHnd.GetMenuCategoryNames();
    menuItemNames = menuHnd.GetMenuItemNames();
    menuItemCommands = menuHnd.GetMenuItemCommands();
    menuItemShortcuts = menuHnd.GetMenuItemShortcuts();

    categIndex=0;

    if menu is None:
    	menu = nuke.menu('Nuke')
    m = menu.addMenu(pos) #NDタブの作成
    toolbar = nuke.menu('Nodes')

    for categoryName in menuCategoryNames:
        for menuItemName, menuItemCmd, menuItemShortcut in zip(menuItemNames[categIndex], menuItemCommands[categIndex],menuItemShortcuts[categIndex]):
            if str(categoryName) =='alone':
                if menuItemShortcut==0:
                    m.addCommand(str(menuItemName), str(menuItemCmd));
                else:
                    m.addCommand(str(menuItemName), str(menuItemCmd), str(menuItemShortcut));
            elif str(categoryName) == 'Nodes':
                if menuItemShortcut==0:
                    toolbar.addCommand(str(menuItemName), str(menuItemCmd));
                else:
                    toolbar.addCommand(str(menuItemName), str(menuItemCmd), str(menuItemShortcut));
            else:
                if menuItemShortcut==0:
                    m.addCommand(str(categoryName)+'/'+str(menuItemName), str(menuItemCmd));
                else:
                    m.addCommand(str(categoryName)+'/'+str(menuItemName), str(menuItemCmd), str(menuItemShortcut));
        categIndex=categIndex+1;

if __name__ == "__main__":
    print ''
    setupMenu()