import os
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')

currentFolder = None
currentFile = None

class FolderSelectorScreen(Screen):   
    def folder_selected(self, path):
        if(len(path) == 1):
            f = os.listdir(path[0])[0]
            if(f.lower().endswith(('.png',  '.jpg', '.jpeg'))):
                #first = path[0] + "/" + f
                #self.ids.img.source = first
                for x in self.manager.screens:
                    if x.name == 'imagesorter':
                        first = path[0] + "/" + f
                        x.ids.img.source = first
                currentFolder = path[0]
                currentFile = f
                self.manager.current = 'imagesorter'
                self.manager.transition.direction = 'right'
            else:
                print "no image files"
        else:
            print "no path selected"

class ImageSorterScreen(Screen):
    def folder_selected(self, path):
        if(currentFolder != None and currentFile != None):
            print "yay"
        else:
            print "no path selected"

class MainScreenManager(ScreenManager):
    pass

root = Builder.load_string('''
#:import os os

MainScreenManager:
    ImageSorterScreen
    FolderSelectorScreen

<FolderSelectorScreen>:
    name: 'folderselector'
    BoxLayout:
        orientation: 'vertical'
        FileChooserListView:
            id: folderchooser
            path: os.getcwd()
            dirselect: True
            mutliselect: False
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            Button:
                height: 100
                size_hint_y: None
                text: 'Cancel'
                font_size: 50
                on_press:
                    app.root.current = 'imagesorter'
                    app.root.transition.direction = 'right'
            Button:
                height: 100
                size_hint_y: None
                id: sel_folder
                text: 'Select Folder'
                font_size: 50
                on_press: root.folder_selected(folderchooser.selection)

<ImageSorterScreen>:
    name: 'imagesorter'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 30
            Button:
                size: (100, 30)
                size_hint: (None, None)
                text: 'Folder Selector'
                on_release:
                    app.root.current = 'folderselector'
                    app.root.transition.direction = 'left'
                font_size: 10
        BoxLayout:
            orientation: 'horizontal'
            BoxLayout:
                Image:
                    id: img
                    width: 700
                    size_hint_x: None
                BoxLayout:
                    orientation: 'vertical'
                    FileChooserListView:
                        id: folderchooser
                        path: os.getcwd()
                        dirselect: True
                        mutliselect: False
                    Button:
                        height: 100
                        size_hint_y: None
                        id: sel_folder
                        text: 'Select Folder'
                        font_size: 50
                        on_press: root.folder_selected(folderchooser.selection)
''')

class ImageSorter(App):
    def build(self):
        return root

if __name__ == '__main__':
    ImageSorter().run()