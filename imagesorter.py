import os
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.treeview import TreeViewLabel
from kivy.clock import Clock

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')

currentFile = None
currentPath = None

# create sorted folder
sortedFolderName = "sorted"
if not os.path.exists(sortedFolderName):
    os.makedirs(sortedFolderName)

class FolderSelectorScreen(Screen):   
    def folder_selected(self, path):
        if(len(path) == 1):
            f = os.listdir(path[0])
            if len(f) > 0:
                f = f[0]
                if(f.lower().endswith(('.png',  '.jpg', '.jpeg'))):
                    for x in self.manager.screens:
                        if x.name == 'imagesorter':
                            first = path[0] + "/" + f
                            x.ids.img.source = first
                            break
                    global currentFile
                    global currentPath
                    currentPath = path[0]
                    currentFile = f
                    self.manager.current = 'imagesorter'
                    self.manager.transition.direction = 'right'
            else:
                print "no image files"
        else:
            print "no path selected"

class ImageSorterScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(ImageSorterScreen, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.populate_treeview)
    
    def populate_treeview(self, dt):
        for folder in os.listdir(sortedFolderName):
            lab = TreeViewLabel(text=folder)
            self.ids.sortview.add_node(lab)
    
    def node_selected(self, args):
        if args[1].is_double_tap and currentFile is not None and currentPath is not None:
            folder = args[0].selected_node.text
            moveTo = sortedFolderName + "/" + folder + "/" + currentFile
            moveFrom = currentPath + "/" + currentFile
            os.rename(moveFrom, moveTo)
            f = os.listdir(currentPath)
            if len(f) > 0:
                first = currentPath + "/" + f[0]
                self.ids.img.source = first
                global currentFile
                currentFile = f[0]
            else:
                global currentFile
                currentFile = None
                self.ids.img.source = ''

class NewLabel(Popup):
    def accept(self):
        text = self.ids.label.text
        if text != "":
            for x in root.screens:
                if x.name == 'imagesorter':
                    lab = TreeViewLabel(text=text)
                    x.ids.sortview.add_node(lab)
                    create = sortedFolderName + "/" + text
                    if not os.path.exists(create):
                        os.makedirs(create)
                    break
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
                        hide_root: True
                        on_touch_down: root.node_selected(args)
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
                    Button:
                        height: 60
                        size_hint_y: None
                        id: teach_button
                        text: 'Teach'
                        font_size: 24
''')

class ImageSorter(App):
    def build(self):
        return root

if __name__ == '__main__':
    ImageSorter().run()