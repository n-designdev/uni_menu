# -*- coding: utf-8 -*-

import sys
import os

env_key = 'ND_TOOL_PATH_PYTHON'
ND_TOOL_PATH = os.environ.get(env_key,'Y:/tool/ND_Tools/python')
for path in ND_TOOL_PATH.split(';'):
    path = path.replace('\\','/')
    sys.path.append(path)

from xml.dom.minidom import parse
import xml.dom.minidom
import subprocess

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
                self.catego_history.append(str(subcate.nodeValue))
                Child_categoryParentNodes = CategoryParent.childNodes
                for Child_categoryParentNode in Child_categoryParentNodes:
                    self.Check_isNode(Child_categoryParentNode)
            elif CategoryParent.nodeName == self.menuItemTag:
                menuItemName = CategoryParent.getAttributeNode(self.nameAttr);
                x = self.catego_history
                try:
                    print (x[0])
                except:
                    pass
                print (x)
                print (menuItemName.nodeValue)
                x.append(menuItemName.nodeValue)
                x = '/'.join(self.catego_history)
                self.menuItemNames.append(x);
                self.catego_history.pop()

                menuItemCommand = CategoryParent.getAttributeNode(self.commandAttr);
                print (menuItemCommand)
                print (menuItemCommand.nodeValue)
                self.menuItemCommands.append(menuItemCommand.nodeValue);
                menuItemShortcut = CategoryParent.getAttributeNode(self.shortcutAttr);
                self.menuCategorydiff.append(categoryName.nodeValue);

                if menuItemShortcut == None:
                    self.menuItemShortcuts.append('');
                else:
                    self.menuItemShortcuts.append(menuItemShortcut.nodeValue);
                    # if str(menuItemShortcut.nodeValue) in self.Shortcutlists:
                    #     print "################################# WARNIG #####################################"
                    #     print ("ショートカット:" +str(menuItemShortcut.nodeValue)+" は重複しています。"+str(menuItemName.nodeValue)+' が優先されます。')
                    #     print "##############################################################################"
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
    menuHnd.SetDataFromXML(r"C:\Users\k_ueda\Desktop\hudimenu\nmenu2.xml");
    menuLabel = menuHnd.GetMenuName();#self.menuname
    menuCategoryNames = menuHnd.GetMenuCategorydiff();
    menuItemNames = menuHnd.GetMenuItemNames();
    menuItemCommands = menuHnd.GetMenuItemCommands();
    menuItemShortcuts = menuHnd.GetMenuItemShortcuts();

    categIndex=0;
    count = 0;
    dom=xml.dom.minidom.Document()

    root_HoudiniWindow = dom.createElement('mainMenu')
    dom.appendChild(root_HoudiniWindow)

    node_his = []
    cate_dict = {}

    menu = dom.createElement('menu')
    root_HoudiniWindow.appendChild(menu)
    sub1 = dom.createElement('subMenu')
    menu.appendChild(sub1)

    ndmenu = dom.createElement('label')
    ndmenu.appendChild(dom.createTextNode('ND_menu'))

    for categoryName, menuItemName, menuItemCmd, menuItemShortcut in zip(menuCategoryNames, menuItemNames, menuItemCommands,menuItemShortcuts):

        for i in menuItemName.split('/'):
            print (len(menuItemName.split('/')))
            print (i)
            print (menuItemName+ ' ' + menuItemCmd + ' ' + menuItemShortcut)
            # dom.createElement
            print (count)
            print (node_his)

            if count+1 == len(menuItemName.split('/')):
                if count == 0:
                    scriptItem = dom.createElement('subMenu')

                    titleItem = dom.createElement('scriptItem')
                    # scriptItem.appendChild(titleItem)
                    label = dom.createElement('label')
                    label.appendChild(dom.createTextNode(str(i)))
                    titleItem.appendChild(label)
                    sub1.appendChild(titleItem)
                    scriptCode = dom.createElement('scriptCode')
                    scriptCode.appendChild(dom.createCDATASection(str(menuItemCmd)))

                    titleItem.appendChild(scriptCode)

                    count = 0
                    del node_his[:]
                else:
                    titleItem = dom.createElement('scriptItem')
                    node_his[count-1].appendChild(titleItem)

                    label = dom.createElement('label')
                    label.appendChild(dom.createTextNode(str(i)))
                    titleItem.appendChild(label)

                    scriptCode = dom.createElement('scriptCode')
                    scriptCode.appendChild(dom.createCDATASection(str(menuItemCmd)))

                    titleItem.appendChild(scriptCode)




                    count = 0
                    del node_his[:]
            else:
                if count == 0:
                    if str(i) in cate_dict:

                        if count + 2 == len(menuItemName.split('/')):
                            node_his.append(cate_dict[str(i)])

                        else:
                            subMenu = dom.createElement('subMenu')
                            cate_dict[str(i)].appendChild(subMenu)
                            node_his.append(subMenu)

                    else:

                        scriptItem = dom.createElement('subMenu')

                        sub1.appendChild(scriptItem)

                        label = dom.createElement('label')
                        label.appendChild(dom.createTextNode(str(i)))

                        scriptItem.appendChild(label)

                        scriptCode = dom.createElement('scriptCode')
                        scriptCode.appendChild(dom.createCDATASection(str(menuItemCmd)))

                        scriptItem.appendChild(scriptCode)

                        if count + 2 == len(menuItemName.split('/')):
                            node_his.append(scriptItem)
                            cate_dict[str(i)] = scriptItem

                        else:
                            subMenu = dom.createElement('subMenu')
                            scriptItem.appendChild(subMenu)
                            node_his.append(subMenu)
                            cate_dict[str(i)] = subMenu

                else:
                    if str(i) in cate_dict:
                        node_his[count-1].parentNode.removeChild(node_his[count-1])

                        if count + 2 == len(menuItemName.split('/')):
                            node_his.append(cate_dict[str(i)])
                        else:
                            subMenu = dom.createElement('subMenu')
                            cate_dict[str(i)].appendChild(subMenu)
                            node_his.append(subMenu)

                    else:
                        label = dom.createElement('label')
                        label.appendChild(dom.createTextNode(str(i)))
                        node_his[count-1].appendChild(label)

                        if count + 2 == len(menuItemName.split('/')):
                            node_his.append(node_his[-1])
                            cate_dict[str(i)] = node_his[-1]
                        else:
                            subMenu = dom.createElement('subMenu')
                            node_his[count-1].appendChild(subMenu)
                            node_his.append(subMenu)
                            cate_dict[str(i)] = subMenu


                count = count + 1
    sub1.appendChild(ndmenu)


    categIndex=categIndex+1;
    print (dom.toprettyxml())
    print (cate_dict)

    path = 'E:/temp/hou_menu'
    if not os.path.isdir(path):
        os.makedirs(path)
    file = open(path+'/MainMenuCommon.xml','w')
    file.write(dom.toprettyxml())
    file.close()

if __name__ == "__main__":
    setupMenu()