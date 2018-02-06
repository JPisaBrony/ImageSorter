import os
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')

currentFolder = None
currentFile = None

class FolderSelectorScreen(Screen):   
    def folder_selected(self, path):
        if(len(path) == 1):
            f = os.listdir(path[0])[0]
            if(f.lower().endswith(('.png',  '.jpg', '.jpeg'))):
                for x in self.manager.screens:
                    if x.name == 'imagesorter':
                        first = path[0] + "/" + f
                        x.ids.img.source = first
                        break
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

class NewLabel(Popup):
    def accept(self):
        text = self.ids.label.text
        if text != "":
            self.dismiss()

class MainScreenManager(ScreenManager):
    pass

root = Builder.load_string('''
#:import os os
#:import Factory kivy.factory.Factory

<NewLabel@Popup>:
    title: 'Enter new label'
    size_hint: (None, None)
    size: (300, 200)
    title_size: 24
    BoxLayout:
        orientation: "vertical"
        TextInput:
            id: label
            font_size: 24
        Button:
            text: 'Accept'
            font_size: 24
            on_release: root.accept()

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
                height: 60
                size_hint_y: None
                text: 'Cancel'
                font_size: 24
                on_press:
                    app.root.current = 'imagesorter'
                    app.root.transition.direction = 'right'
            Button:
                height: 60
                size_hint_y: None
                id: sel_folder
                text: 'Select Folder'
                font_size: 24
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
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: None
                    width: 200
                    TreeView:
                        id: sortview
                    Button:
                        height: 60
                        size_hint_y: None
                        id: add_label_button
                        text: 'Add Label'
                        font_size: 24
                        on_press: Factory.NewLabel().open()
                    Button:
                        height: 60
                        size_hint_y: None
                        id: yes_button
                        text: 'Yes'
                        font_size: 24
                        on_press: root.folder_selected(folderchooser.selection)
                    Button:
                        height: 60
                        size_hint_y: None
                        id: teach_button
                        text: 'Teach'
                        font_size: 24
                        on_press: root.folder_selected(folderchooser.selection)
''')

class ImageSorter(App):
    def build(self):
        return root

if __name__ == '__main__':
    ImageSorter().run()