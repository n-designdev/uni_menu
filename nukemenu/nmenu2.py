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
    menuCategorydiff=[];

    def Check_isNode(self,CategoryParent):
        if CategoryParent.nodeName == self.menuItemTag or CategoryParent.nodeName == self.categoryTag:
            categoryName = CategoryParent.getAttributeNode(self.nameAttr)
            if CategoryParent.nodeName == self.categoryTag:
                subcate = CategoryParent.getAttributeNode(self.nameAttr)
                print subcate.nodeValue
                print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                # if len(self.catego_history) != 0:
                    # self.catego_history.append('/')
                self.catego_history.append(str(subcate.nodeValue))
                Child_categoryParentNodes = CategoryParent.childNodes
                for Child_categoryParentNode in Child_categoryParentNodes:
                    self.Check_isNode(Child_categoryParentNode)
            elif CategoryParent.nodeName == self.menuItemTag:
                menuItemName = CategoryParent.getAttributeNode(self.nameAttr);
                menuItemName.replace("/","\/")
                x = self.catego_history
                # x.append('/')
                x.append(menuItemName.nodeValue)
                x = '/'.join(self.catego_history)
                self.menuItemNames.append(x);
                # self.catego_history.pop()
                self.catego_history.pop()

                menuItemCommand = CategoryParent.getAttributeNode(self.commandAttr);
                self.menuItemCommands.append(menuItemCommand.nodeValue);
                menuItemShortcut = CategoryParent.getAttributeNode(self.shortcutAttr);
                self.menuCategorydiff.append(categoryName.nodeValue);
                if menuItemShortcut == None:
                    self.menuItemShortcuts.append('');
                else:
                    self.menuItemShortcuts.append(menuItemShortcut.nodeValue);
                    if str(menuItemShortcut.nodeValue) in self.Shortcutlists:
                        print "################################# WARNIG #####################################"
                        print ("ショートカット:" +str(menuItemShortcut.nodeValue)+" は重複しています。"+str(menuItemName.nodeValue)+' が優先されます。')
                        print "##############################################################################"
                    self.Shortcutlists.append(str(menuItemShortcut.nodeValue))

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

    def GetMenuCategorydiff(self):
        return self.menuCategorydiff;

    # Setter Methods -----------------------------------
    # store data into class members
    def SetDataFromXML(self, xmlPath):
        self.menuCategoryNames=[];
        self.menuItemNames=[];
        self.menuItemCommands=[];
        self.menuItemShortcuts=[];
        self.Shortcutlists=[];
        self.menuCategorydiff=[];
        self.catego_history=[];

        dom = parse(xmlPath);#パース処理
        root = dom.documentElement;#xmlのdocmentelement
        menuElem = root.getElementsByTagName(self.menuTag)[0];#rootからmenutag→今回はmenu
        menuName = menuElem.getAttributeNode(self.nameAttr);#menuからnameAttr→今回はmenu
        self.menuName = menuName.nodeValue;#menunameのnodevalue
        menuChildNodes = menuElem.childNodes;
        for menuChild in menuChildNodes:
            self.Check_isNode(menuChild)
            try:
                self.catego_history.pop()
            except:
                pass

        dom.unlink()

def setupMenu(pos='ND',menu=None):
    menuHnd = MenuSetupHandler();
    menuHnd.SetDataFromXML(r"C:\Users\k_ueda\Desktop\nukemenu\nmenu2.xml");
    menuLabel = menuHnd.GetMenuName();#self.menuname
    menuCategoryNames = menuHnd.GetMenuCategorydiff();
    menuItemNames = menuHnd.GetMenuItemNames();
    menuItemCommands = menuHnd.GetMenuItemCommands();
    menuItemShortcuts = menuHnd.GetMenuItemShortcuts();

    categIndex=0;

    if menu is None:
        menu = nuke.menu('Nuke')
    m = menu.addMenu(pos) #NDタブの作成
    toolbar = nuke.menu('Nodes')

    for categoryName, menuItemName, menuItemCmd, menuItemShortcut in zip(menuCategoryNames, menuItemNames, menuItemCommands,menuItemShortcuts):
            print menuItemName
            if str(menuItemShortcut)=='':
                m.addCommand(str(menuItemName), str(menuItemCmd));
            else:
                m.addCommand(str(menuItemName), str(menuItemCmd), str(menuItemShortcut));
    categIndex=categIndex+1;

if __name__ == "__main__":
    setupMenu()