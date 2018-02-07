# ImageSorter

ImageSorter is an image sorter that uses machine learning to sort your images automagically.

### Basic usage of the tool

Select a folder with image files in it by clicking the folder selector and selecting a folder. The first image will then be loaded from that folder in the main view.

Create a new label which creates a new folder in the folder created by image sorter called sorted.

Double click on the label to put the displayed image into the folder. Image sorter will automatically load the next image to be sorted.

Repeat until 20 images have been put into at least two folders. This is the manual part of the training but will soon be automated.

### Install guide
```
sudo pacman -S python2-kivy
```
or with pip
```
sudo pip2 install -r requirements.txt
```
