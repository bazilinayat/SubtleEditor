#for some nornal system finctions
import sys
#for the functions of geeting file name and paths and extensions
import os
#All for geeting our gui ready
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *
#for openenig the default ewb browser
import webbrowser
#for timing our appplication for some different stuff
import time

#aditya imported this for speech recognition for our voice stuff
#aditya imports---------------
import speech_recognition as sr
import sys
from subprocess import Popen, PIPE
import pyttsx3
import github3
#aditya imports---------------

#mayuresh import----------------
#import googledriveuploader as gd
#mayuresh import----------------

#MAYURESH


#for knowing how many custom themes are made in one application go
THEME_CUSTOM_COUNT = 0

#for knowing the custom theme selected and to be applied now ,right now
THEME_CUSTOM_SELECT = 0

#for knowing which theme was selected
THEME_SELECT = 0

#themes for the default stuff
themeStyle1="""
QWidget{
background-color:rgba(100,150,200,0.4);
padding:1;
font-family:Helvetica Neue;
color:white;
}
"""

themeStyle2="""
QWidget{
background-color:rgba(255,255,255,0.5);
padding:2;
font-family:Arial;
color:green;
}
"""

themeStyle3="""
QWidget{
background-color:rgba(0,0,0,0.5);
padding:1;
font-family:Caesar;
color:rgb(0,255,0);
}
"""

themeStyle4="""
QWidget{
background-color:rgba(0,0,0,0.5);
padding:1;
font-family:Caesar;
color:rgb(255,255,255);
}
"""

#for the spot light stuff
wordList = ['New(File Menu)',
            'Open(File Menu)',
            'Save(File Menu)',
            'SaveAs(File Menu)',
            'SaveAll(File Menu)',
            'Close(File Menu)',
            'CloseAll(File Menu)',
            'Exit(File Menu)',
            'Undo(Edit Menu)',
            'Redo(Edit Menu)',
            'Cut(Edit Menu)',
            'Copy(Edit Menu)',
            'Paste(Edit Menu)',
            'SelectAll(Edit Menu)',
            'Clear(Edit Menu)',
            'ZoomIn(Edit Menu)',
            'ZoomOut(Edit Menu)',
            'Compile(Execute Menu)',
            'Find(Search Menu)',
            'Find&Replace(Search Menu)',
            'WebSearch(Search Menu)',
            'Upload File(Upload Menu)',
            'Code(Voice Menu)',
            'Operate(Voice Menu)',
            'Select Theme(Theme Menu)',
            'Select Custom(Theme Menu)',
            'Create Custom(Theme Menu)',
            'Help',
            'About']


#MAYURESH

#associative array for addresses
myadd={}

#for a timer for stuff
start = time.time()
PERIOD_OF_TIME = 30

#scintilla for stuff
ARROW_MARKER_NUM = 8

#MAYURESH


#array for identifying the type of file to open from tree
FILEEND = ['.bat','.cmd','.btm',
          '.c','.C','.cc','.cpp','.CPP','.c++','.cp','.cxx','.hpp','.hxx','.Hxx','.HXX',
          '.cs',
          '.java',
          '.js',
          '.html',
          '.css',
          '.xml','.xrb',
          '.m','.p','.mlx',
          '.pl','.PL','.pm',
          '.py',
          '.rb',
          '.txt']


#MAYURESH

#bazil


#a new class for find dialog to find stuff
class Find(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.initFindUI()

    def initFindUI(self):
        try:
        	#window for find dialog
            self.setWindowTitle('Find')
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
            self.setFixedSize(200,60)

            #the text box to enter the pattern to search
            findtext = QLabel('<p align="left";">Find : </p>')
            self.findbox = QLineEdit()

            #the layout for adding the text box
            labtext = QHBoxLayout()
            labtext.addWidget(findtext)
            labtext.addWidget(self.findbox)

            #pos = 0 we can start from the begining of file
            self.pos = 0

            #buttons for finding which call functions
            findb = QPushButton('Find')
            findb.setFixedSize(70, 20)
            findb.clicked.connect(self.next)

            #buttons for canceling so we can exit the dialog
            cancelb = QPushButton('Cancel')
            cancelb.setFixedSize(70, 20)
            cancelb.clicked.connect(self.cancel)

            #layout foe buttons
            buttons = QHBoxLayout()
            buttons.addWidget(findb)
            buttons.addWidget(cancelb)

            #layout for both the above layout so it comes to one above another
            Mainbox = QVBoxLayout()
            Mainbox.addLayout(labtext)
            Mainbox.addLayout(buttons)

            #make a window and add the thrid layout to it and make it the central widget
            window = QWidget()
            window.setLayout(Mainbox)

            self.setCentralWidget(window)

            #calling for selectig the theme
            SELECTHEME(self)

            self.show()
        except Exception as e:
            print('Exception in find class init : ',str(sys.exc_info()))

    def next(self):
        try:
        	#get the current tab index and text
            self.parent.information()
            found = True
            line = 1
            index = 0
            #get the pattern from text box
            pattern = self.findbox.text()

            #found = self.parent.globaltext.findFirst(pattern,regular_expression, is_case_sensitive, match_whole_word_only, use_wrap, search_forward)
            found = self.parent.globaltext.findFirst(pattern,True,False,True,True,True,-1,-1,True,False)

            if found:
            	#if found we track the starting and ending positioon of the pattern
                start = self.parent.globaltext.positionFromLineIndex(line, index)
                print('start ',start)
                end = self.parent.globaltext.positionFromLineIndex(line, index+len(pattern))
                print('end ',end)

                # Attempts to highlight
                self.parent.globaltext.SendScintilla(QsciScintilla.SCI_INDICGETSTYLE, QsciScintilla.INDIC_BOX)
                self.parent.globaltext.SendScintilla(QsciScintilla.SCI_INDICSETFORE, 0x007f00)
                self.parent.globaltext.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, start, end - start)
                self.parent.globaltext.setIndicatorForegroundColor(QColor(159, 144, 0))
                #self.parent.globaltext.setColor(QColor(159, 144, 0))
        except Exception as e:
            print('Exception in find function as:',str(sys.exc_info()))

    def cancel(self):
        self.close()

#class for making a find and replace dialog
class FindReplace(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.initFindReplaceUI()

    def initFindReplaceUI(self):
        try:
        	#window
            self.setWindowTitle('Find And Replace')
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
            self.setFixedSize(500,150)

            #find textbox
            findtext = QLabel('<p align="left";">Find : </p>')
            self.findbox = QLineEdit()

            #layout for find textbox
            labtext = QHBoxLayout()
            labtext.addWidget(findtext)
            labtext.addWidget(self.findbox)

            #replace text box
            replacetext = QLabel('<p align="left";">Replace : </p>')
            self.replacebox = QLineEdit()

            #replace text box layout
            labtext1 = QHBoxLayout()
            labtext1.addWidget(replacetext)
            labtext1.addWidget(self.replacebox)

            #o start from beging of the file
            self.pos = 0

            #the buttons for find replace rplace all and cencel
            findb = QPushButton('Find')
            findb.setFixedSize(70, 20)
            findb.clicked.connect(self.next)

            replaceb = QPushButton('Replace')
            replaceb.setFixedSize(70,20)
            replaceb.clicked.connect(self.replace)

            replaceallb = QPushButton('ReplaceAll')
            replaceallb.setFixedSize(70,20)
            replaceallb.clicked.connect(self.replaceAll)

            cancelb = QPushButton('Cancel')
            cancelb.setFixedSize(70, 20)
            cancelb.clicked.connect(self.cancel)

            #layout for buttons
            buttons = QHBoxLayout()
            buttons.addWidget(findb)
            buttons.addWidget(replaceb)
            buttons.addWidget(replaceallb)
            buttons.addWidget(cancelb)

            #layout for text boxes and buttons together
            Mainbox = QVBoxLayout()
            Mainbox.addLayout(labtext)
            Mainbox.addLayout(labtext1)
            Mainbox.addLayout(buttons)

            #the main widget to add layout and setting it as central widget
            window = QWidget()
            window.setLayout(Mainbox)

            self.setCentralWidget(window)

            #to selecting theme
            SELECTHEME(self)

            self.show()
        except Exception as e:
            print('Exception in find and replace class init : ',str(sys.exc_info()))

    def next(self):
        try:
        	#getting tab index and text
            self.parent.information()
            found = True
            line = 1
            index = 0
            #getting pattern from find text box
            pattern = self.findbox.text()

            #found = self.parent.globaltext.findFirst(pattern,regular_expression, is_case_sensitive, match_whole_word_only, use_wrap, search_forward)
            found = self.parent.globaltext.findFirst(pattern,True,False,True,True,True,-1,-1,True,False)

            if found:
            	# to get the startand end of pattern
                start = self.parent.globaltext.positionFromLineIndex(line, index)
                end = self.parent.globaltext.positionFromLineIndex(line, index+len(pattern))

                # Attempts to highlight
                self.parent.globaltext.SendScintilla(QsciScintilla.SCI_INDICGETSTYLE, QsciScintilla.INDIC_BOX)
                self.parent.globaltext.SendScintilla(QsciScintilla.SCI_INDICSETFORE, 0x007f00)
                self.parent.globaltext.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, start, end - start)
                self.parent.globaltext.setIndicatorForegroundColor(QColor(159, 144, 0))
        except Exception as e:
            print('Exception in find and replace function as:',str(sys.exc_info()))


    def replace(self):
        try:
            # Select the matched text and apply the desired format
            self.parent.globaltext.replaceSelectedText(self.replacebox.text())
        except Exception as e:
            print('Exception in find function as:',str(sys.exc_info()))


    def replaceAll(self):
        try:
        	#getting tab index and text
            self.parent.information()
            line = 0
            index = 0
            found = True
            #getting the epattern to search for
            pattern = self.findbox.text()
            while found :
                cursor = self.parent.globaltext.getCursorPosition()
                #found = self.parent.globaltext.findFirst(pattern,regular_expression, is_case_sensitive, match_whole_word_only, use_wrap, search_forward)
                found = self.parent.globaltext.findFirst(pattern,True,False,True,True,True,-1,-1,True,False)

                if found:
                    start = self.parent.globaltext.positionFromLineIndex(line, index)
                    end = self.parent.globaltext.positionFromLineIndex(line, index+len(pattern))

                    # Attempts to highlight
                    self.parent.globaltext.SendScintilla(QsciScintilla.SCI_INDICGETSTYLE, QsciScintilla.INDIC_BOX)
                    self.parent.globaltext.SendScintilla(QsciScintilla.SCI_INDICSETFORE, 0x007f00)
                    self.parent.globaltext.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, start, end - start)
                    self.parent.globaltext.setIndicatorForegroundColor(QColor(159, 144, 0))
                    #once the pattern foundreplace it to our replacing pattern
                    self.replace()
        except Exception as e:
            print('Exception in find and replace function as:',str(sys.exc_info()))

    def cancel(self):
        self.close()


#bazil

#MAYURESH


#class for themes where we create a dialog and user can select from the default themes
class Themes(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.initThemeUI()

    def initThemeUI(self):
        try:
            self.setWindowTitle('Select Theme')
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
            self.setFixedSize(500,150)

           	#just the buttons for applying themes
            default = QPushButton('Default')
            default.setFixedSize(70, 30)
            default.clicked.connect(self.DefaultTheme)

            theme1 = QPushButton('Theme 1')
            theme1.setFixedSize(70, 30)
            theme1.clicked.connect(self.SelectTheme1)

            theme2 = QPushButton('Theme 2')
            theme2.setFixedSize(70, 30)
            theme2.clicked.connect(self.SelectTheme2)

            theme3 = QPushButton('Theme 3')
            theme3.setFixedSize(70, 30)
            theme3.clicked.connect(self.SelectTheme3)

            theme4 = QPushButton('Theme 4')
            theme4.setFixedSize(70, 30)
            theme4.clicked.connect(self.SelectTheme4)

            #their layout
            vbox = QHBoxLayout()
            vbox.addWidget(default)
            vbox.addWidget(theme1)
            vbox.addWidget(theme2)
            vbox.addWidget(theme3)
            vbox.addWidget(theme4)

            window = QWidget()
            window.setLayout(vbox)

            self.setCentralWidget(window)

            #for selecting theme
            SELECTHEME(self)

            self.show()
        except Exception as e:
            print('Exception e in theme ui: ',str(sys.exc_info()))

    def DefaultTheme(self):
        global THEME_SELECT
        THEME_SELECT = 0
        self.setStyleSheet(None)
        self.parent.setStyleSheet(None)
        f = open("Data\Custom\selected.txt","w+")
        f.write("0")
        f.close()
        self.Write_Theme()

    def SelectTheme1(self):
        global THEME_SELECT
        THEME_SELECT = 1
        self.setStyleSheet(themeStyle1)
        self.parent.setStyleSheet(themeStyle1)
        self.Write_Theme()

    def SelectTheme2(self):
        global THEME_SELECT
        THEME_SELECT = 2
        self.setStyleSheet(themeStyle2)
        self.parent.setStyleSheet(themeStyle2)
        self.Write_Theme()

    def SelectTheme3(self):
        global THEME_SELECT
        THEME_SELECT = 3
        self.setStyleSheet(themeStyle3)
        self.parent.setStyleSheet(themeStyle3)
        self.Write_Theme()

    def SelectTheme4(self):
        global THEME_SELECT
        THEME_SELECT = 4
        self.setStyleSheet(themeStyle4)
        self.parent.setStyleSheet(themeStyle4)
        self.Write_Theme()

    #for writing the selected theme number in a file so we can retrive it and aplly for later
    def Write_Theme(self):
        global THEME_SELECT
        f = open("Data\THEME_SELECT.txt","w+")
        f.write(str(THEME_SELECT))
        f.close()


#class for custom themes to be saved by user
class CustomThemes(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.initCustomThemeUI()

    def initCustomThemeUI(self):
        try:

            self.setWindowTitle('Custom Theme')
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
            self.setFixedSize(300,200)

            #these are the things the user can change
            back = QLabel('Background-Color :')
            color = QLabel('Font-Color :')
            font = QLabel('Font-Family')

            #buttons who call color dialog and text box where we can write font family name
            backColor = QPushButton('Select Background Color')
            backColor.setFixedSize(150,30)
            backColor.clicked.connect(self.chooseBackColor)
            fontColor = QPushButton('Select Font Color')
            fontColor.setFixedSize(150,30)
            fontColor.clicked.connect(self.chooseFontColor)
            self.fontText = QLineEdit()
            self.fontText.setFixedSize(150,20)

            #grid layout for the above six things
            self.grid = QGridLayout()

            self.grid.addWidget(back,0,0)
            self.grid.addWidget(backColor,0,1)
            self.grid.addWidget(color,1,0)
            self.grid.addWidget(fontColor,1,1)
            self.grid.addWidget(font,2,0)
            self.grid.addWidget(self.fontText,2,1)

            #buttons for resetting and seeing and applying the themes
            reset = QPushButton('Reset')
            reset.clicked.connect(self.Reset)
            see = QPushButton('See')
            see.clicked.connect(self.See)
            apply = QPushButton('Apply')
            apply.clicked.connect(self.Apply)

            self.hbox = QHBoxLayout()
            self.hbox.addWidget(reset)
            self.hbox.addWidget(see)
            self.hbox.addWidget(apply)

            self.vbox = QVBoxLayout()

            win1 = QWidget()
            win1.setLayout(self.grid)

            win2 = QWidget()
            win2.setLayout(self.hbox)

            self.vbox.addWidget(win1)
            self.vbox.addWidget(win2)

            win = QWidget()
            win.setLayout(self.vbox)
            self.setCentralWidget(win)

            #selecting theme
            SELECTHEME(self)

            # to get the current style sheet and which theme was selected
            # so if the user dont want the new them he/she can reset the theme to
            # the preious theme which is now current
            self.STYLE = self.styleSheet()
            self.selected = THEME_SELECT
            self.customselected = THEME_CUSTOM_SELECT

            self.show()

        except Exception as e:
            print('in init cutom theme :',str(sys.exc_info()))


#for choosing the color for background
    def chooseBackColor(self):
        print('choosing colors')
        self.back = QColorDialog.getColor()
        self.back = self.back.name()
        print(self.back)

#for choosing the color for font color
    def chooseFontColor(self):
        print('choosing font color')
        self.fontColor = QColorDialog.getColor()
        self.fontColor = self.fontColor.name()
        print(self.fontColor)


#if we dont want the theme now then we can reset the theme to previously applied
    def Reset(self):
        print('reset')
        try:
        	#first we get the current theme selected from files
            global THEME_SELECT
            global THEME_CUSTOM_SELECT
            THEME_SELECT = self.selected
            print(self.selected)
            THEME_CUSTOM_SELECT = self.customselected
            print(self.customselected)
            #we set the theme to the previous style sheet
            self.setStyleSheet(self.STYLE)
            self.parent.setStyleSheet(self.STYLE)
            #we write the selected theme numbers in the files to get again
            f = open("Data\THEME_SELECT.txt","w+")
            f.write(str(THEME_SELECT))
            f.close()
            f = open("Data\Custom\selected.txt","w+")
            f.write(str(THEME_CUSTOM_SELECT))
            f.close()
        except Exception as e:
            print('Exception in reset of cutom themes :',str(sys.exc_info()))


#function for just seeing the new theme we created
    def See(self):
        print('see')
        try:
            self.custom="""
            QWidget{
            background-color:"""+self.back+""";
            padding:1;
            font-family:Arial;
            color:"""+self.fontColor+""";
            }
            """
            self.parent.setStyleSheet(self.custom)
            self.setStyleSheet(self.custom)
        except Exception as e:
            print('Exception in see in thmes for cutom ',str(sys.exc_info()))


#applying the newly created theme to our application
    def Apply(self):
        try:
            print('apply')
            # we get the count of the custom themes created from the files
            global THEME_CUSTOM_COUNT
            f = open("Data\Custom\count.txt","r")
            data = f.read()
            THEME_CUSTOM_COUNT = int(data)
            f.close()
            #since we created a new theme custom theme count is incremented
            THEME_CUSTOM_COUNT = THEME_CUSTOM_COUNT + 1
            #we then make a style sheet with the new parameters
            self.custom="""
            QWidget{
            background-color:"""+self.back+""";
            padding:1;
            font-family:Arial;
            color:"""+self.fontColor+""";
            }
            """
            #we write the incremented custom theme count to selected file since we just selected it
            f = open("Data\Custom\selected.txt","w+")
            f.write(str(THEME_CUSTOM_COUNT))
            f.close()
            # we make a new file with the new stye sheet
            f = open("Data\Custom\THEME_CUSTOM_"+str(THEME_CUSTOM_COUNT)+".txt","w+")
            f.write(self.custom)
            f.close()
            #we write the incremented custom theme count to a file to know how many themes we created till now
            f = open("Data\Custom\count.txt","w+")
            f.write(str(THEME_CUSTOM_COUNT))
            f.close()
            #since we applied a custom theme then we are not using a default theme
            # so default theme selected is set to 0
            f = open("Data\THEME_SELECT.txt","w+")
            f.write("0")
            f.close()
            #finallly apply the new created style sheet to application
            self.parent.setStyleSheet(self.custom)
            self.setStyleSheet(self.custom)

        except Exception as e:
            print("in Apply of custom theme",str(sys.exc_info()))


#for selecting a theme from custom cerated themes
class ThemeCustomSelect(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.initThemeCustomSelectUI()


    def initThemeCustomSelectUI(self):
        try:
        	# we use a combo box(select box) to store all the custom created themes
            layout = QHBoxLayout()
            self.cb = QComboBox()

            # we get the count of custome created themes
            f = open("Data\Custom\count.txt","r")
            data = f.read()
            cnt = int(data)
            f.close()

            # we fill the combo box with all the themes user created
            for i in range(cnt):
                print("Custom Theme ",str(i+1))
                self.cb.addItem("Custom Theme "+str(i+1))


            # adding to the layout the combo box
            layout.addWidget(self.cb)

            #making buttons for seeing , resting if not happy and applying the themes
            reset = QPushButton('Reset')
            reset.clicked.connect(self.Reset)
            see = QPushButton('See')
            see.clicked.connect(self.See)
            apply = QPushButton('Apply')
            apply.clicked.connect(self.Apply)

            self.hbox = QHBoxLayout()
            self.hbox.addWidget(reset)
            self.hbox.addWidget(see)
            self.hbox.addWidget(apply)

            win1 = QWidget()
            win1.setLayout(layout)
            win2 = QWidget()
            win2.setLayout(self.hbox)

            vbox = QVBoxLayout()

            vbox.addWidget(win1)
            vbox.addWidget(win2)

            win = QWidget()
            win.setLayout(vbox)

            self.setCentralWidget(win)

            #selecting theme
            SELECTHEME(self)

            # to get the current style sheet and which theme was selected
            # so if the user dont want the new them he/she can reset the theme to
            # the preious theme which is now current
            self.STYLE = self.styleSheet()
            self.selected = THEME_SELECT
            self.customselected = THEME_CUSTOM_SELECT

            self.show()

        except Exception as e:
            print("init of custom theme sekecting",str(sys.exc_info()))


#if we dont want the theme now then we can reset the theme to previously applied
    def Reset(self):
        print('reset')
        try:
        	#first we get the current theme selected from files
            global THEME_SELECT
            global THEME_CUSTOM_SELECT
            THEME_SELECT = self.selected
            print(self.selected)
            THEME_CUSTOM_SELECT = self.customselected
            print(self.customselected)
            #we set the theme to the previous style sheet
            self.setStyleSheet(self.STYLE)
            self.parent.setStyleSheet(self.STYLE)
            #we write the selected theme numbers in the files to get again
            f = open("Data\THEME_SELECT.txt","w+")
            f.write(str(THEME_SELECT))
            f.close()
            f = open("Data\Custom\selected.txt","w+")
            f.write(str(THEME_CUSTOM_SELECT))
            f.close()
        except Exception as e:
            print('Exception in reset of cutom themes :',str(sys.exc_info()))


#function for just seeing the new theme we created
    def See(self):
        print('see')
        try:
        	# we gwt the index of the data in combo box
            index = self.cb.currentIndex()
            print(index)
            #we increment the index because the combo box indices start from 0
            index= index + 1
            # we get the file accordingly and read the data from it as style sheet
            f = open("Data\Custom\THEME_CUSTOM_"+str(index)+".txt","r")
            self.custom = f.read()
            f.close()
            # apply the data taken from the file to the application
            self.parent.setStyleSheet(self.custom)
            self.setStyleSheet(self.custom)
        except Exception as e:
            print('Exception in see in thmes for cutom ',str(sys.exc_info()))

#applying the newly created theme to our application
    def Apply(self):
        print('apply')
        global THEME_CUSTOM_SELECT
        # we gwt the index of the data in combo box
        index = self.cb.currentIndex()
        print(index)
        #we increment the index because the combo box indices start from 0
        index= index + 1
        # we get the file accordingly and read the data from it as style sheet
        f = open("Data\Custom\THEME_CUSTOM_"+str(index)+".txt","r")
        self.custom = f.read()
        f.close()
        # apply the data taken from the file to the application
        self.parent.setStyleSheet(self.custom)
        self.setStyleSheet(self.custom)
        #since we applied the theme we have to enter the theme number into the file
        THEME_CUSTOM_SELECT = index
        f = open("Data\Custom\selected.txt","w+")
        f.write(str(THEME_CUSTOM_SELECT))
        f.close()
        f = open("Data\THEME_SELECT.txt","w+")
        f.write("0")
        f.close()


#MAYURESH


# aditya's window for uploading file


class UploadWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.initUploadUI()

    def initUploadUI(self):
        self.setObjectName("MainWindow")
        self.resize(565, 268)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 29, 101, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 80, 61, 20))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 180, 75, 23))
        self.pushButton.setObjectName("pushButton")
        #action performed
        self.pushButton.clicked.connect(self.OpenFileToUpload)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 230, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        #action Performed
        self.pushButton_2.clicked.connect(self.UploadToGithub)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(390, 60, 151, 101))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("giitcat.png"))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(160, 30, 181, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 80, 181, 20))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 130, 181, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 180, 181, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 130, 81, 20))
        self.label_4.setObjectName("label_4")
        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        #selecting theme
        SELECTHEME(self)




    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Upload To GitHub"))
        self.label.setText(_translate("MainWindow", "GitHub Username"))
        self.label_2.setText(_translate("MainWindow", "Password"))
        self.pushButton.setText(_translate("MainWindow", "Open File"))
        self.pushButton_2.setText(_translate("MainWindow", "Upload"))
        self.label_4.setText(_translate("MainWindow", "Repository Name:"))
        self.show()


    def showdialog(self,text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle("Subtle Window")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def OpenFileToUpload(self):
        filename = QFileDialog.getOpenFileName(self,"Open Files",".","files (*.txt *.css *.perl *.sh *.bat *.js *.php *.html *.rb *.c *.cpp *.java); All files (*.*)");
        filepath = os.path.basename(filename[0])
        self.lineEdit_4.setText(filepath)

    def UploadToGithub(self):
        Username = self.lineEdit.text()
        Password = self.lineEdit_2.text()
        Repo = self.lineEdit_3.text()
        file_info = self.lineEdit_4.text()
        gh = github3.login(username=Username, password=Password)
        repository = gh.repository(Username,Repo)
        #for file_info in files_to_upload:
        with open(file_info, 'rb') as fd:
            contents = fd.read()
            repository.create_file(
                path=file_info,
                message='Start tracking {!r}'.format(file_info),
                content=contents,
            )
        self.showdialog("File Uploaded.")
        self.close()



#starting page
class Starter(QMainWindow):

    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(465, 331)
        self.setAccessibleDescription("")
        self.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, -200, 841, 731))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("start.png"))
        self.label.setObjectName("label")
        self.setCentralWidget(self.centralwidget)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        time.sleep(3)
        self.close


#aditya's end window for uploading file


#bazil


#main appication of editor interface and functions
class App(QMainWindow):
    def __init__(self):
#defining and initialising the variables for mymain window
        super().__init__()
        self.title="Subtle Editor"
        self.left=50
        self.top=50
        self.width=640
        self.height=400
#to change the color of main window title and borders
        #self.setStyleSheet(appStyle)
        self.theme = 0
        self.initUI()

    def initUI(self):

        #text = QTextEdit()
        #textline = QTextEdit()
#setting stuff for main window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
#creates a menubar on top of main window
        pal = QPalette()
        pal.setColor(QPalette.Highlight,Qt.yellow)
        pal.setColor(QPalette.HighlightedText,Qt.blue)
        mainMenu = self.menuBar()
        self.spotLight = QLineEdit()
        self.spotLight.setPalette(pal)
        self.spotLight.textEdited.connect(self.suggest)
        mainMenu.setCornerWidget (self.spotLight,Qt.TopRightCorner)
#adding different menus in menubar
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        executeMenu = mainMenu.addMenu('Execute')
        searchMenu = mainMenu.addMenu('Search')
        uploadMenu = mainMenu.addMenu('Upload')
        voiceMenu = mainMenu.addMenu('Voice')
        themesMenu = mainMenu.addMenu('Themes')
        helpMenu = mainMenu.addMenu('Help')
        aboutMenu = mainMenu.addMenu('About')

#adding options to file menu sub options
#new option and settings
        subNew = QAction('New',self)
        subNew.setShortcut('Ctrl+N')
        fileMenu.addAction(subNew)
        subNew.triggered.connect(self.newTab)
#open option and settings
        subOpen = QAction('Open',self)
        subOpen.setShortcut('Ctrl+O')
        fileMenu.addAction(subOpen)
        subOpen.triggered.connect(self.openFile)
#separator
        fileMenu.addSeparator()
#save option and settings
        subSave = QAction('Save',self)
        subSave.setShortcut('Ctrl+s')
        fileMenu.addAction(subSave)
        subSave.triggered.connect(self.saveFile)
#save as option and settings
        subSaveAs = QAction('SaveAs',self)
        fileMenu.addAction(subSaveAs)
        subSaveAs.triggered.connect(self.saveAsFile)
#save all option  and settings
        subSaveAll = QAction('SaveAll',self)
        fileMenu.addAction(subSaveAll)
        subSaveAll.triggered.connect(self.saveAllFile)
#separator
        fileMenu.addSeparator()
#close option and settings
        subClose = QAction('Close',self)
        subClose.setShortcut('Ctrl+W')
        fileMenu.addAction(subClose)
        subClose.triggered.connect(self.closeTab)
#close all option and settings
        subCloseAll = QAction('CloseAll',self)
        fileMenu.addAction(subCloseAll)
        subCloseAll.triggered.connect(self.closeAllTabs)
#separator
        fileMenu.addSeparator()
#exit option and setings
        subExit = QAction('Exit',self)
        subExit.setShortcut('Ctrl+Q')
        fileMenu.addAction(subExit)
        subExit.triggered.connect(self.exit)

#adding options to edit menu sub options
#undo option and settings
        subUndo = QAction('Undo',self)
        subUndo.setShortcut('Ctrl+Z')
        editMenu.addAction(subUndo)
        subUndo.triggered.connect(self.opUndo)
#redo option and settings
        subRedo = QAction('Redo',self)
        editMenu.addAction(subRedo)
        subRedo.setShortcut('Ctrl+Shift+Z')
        subRedo.triggered.connect(self.opRedo)
#adding separator
        editMenu.addSeparator()
#copy option and settings
        subCopy = QAction('Copy',self)
        subCopy.setShortcut('Ctrl+C')
        editMenu.addAction(subCopy)
        subCopy.triggered.connect(self.opCopy)
#cut option and settings
        subCut = QAction('Cut',self)
        subCut.setShortcut('Ctrl+X')
        editMenu.addAction(subCut)
        subCut.triggered.connect(self.opCut)
#paste option and settings
        subPaste = QAction('Paste',self)
        subPaste.setShortcut('Ctrl+V')
        editMenu.addAction(subPaste)
        subPaste.triggered.connect(self.opPaste)
#adding separator
        editMenu.addSeparator()
#clear option and settings
        subClear = QAction('Clear',self)
        editMenu.addAction(subClear)
        subClear.triggered.connect(self.opClear)
#select all option and settings
        subSelectAll = QAction('SelectAll',self)
        subSelectAll.setShortcut('Ctrl+A')
        editMenu.addAction(subSelectAll)
        subSelectAll.triggered.connect(self.opSelectAll)
#adding separator
        editMenu.addSeparator()
#zoomin option and settings
        subZoomIn = QAction('ZoomIn',self)
        subZoomIn.setShortcut('Ctrl++')
        editMenu.addAction(subZoomIn)
        subZoomIn.triggered.connect(self.opZoomIn)
#zoom out option and settings
        subZoomOut = QAction('ZoomOut',self)
        subZoomOut.setShortcut('Ctrl+-')
        editMenu.addAction(subZoomOut)
        subZoomOut.triggered.connect(self.opZoomOut)

#adding options to execute menu sub options
#compile option and settings
        subCompile = QAction('Compile',self)
        executeMenu.addAction(subCompile)
        subCompile.triggered.connect(self.openCmd)

#adding options to search menu suboptions
#find option and settings
        subFind = QAction('Find',self)
        subFind.setShortcut('Ctrl+F')
        searchMenu.addAction(subFind)
        subFind.triggered.connect(self.findWord)
#find and replace option and settings
        subFindAndReplace = QAction('Find && Replace',self)
        subFindAndReplace.setShortcut('Ctrl+H')
        searchMenu.addAction(subFindAndReplace)
        subFindAndReplace.triggered.connect(self.findReplaceWord)
#adding separator
        searchMenu.addSeparator()
#web search option and settings
        subWebSearch = QAction('Web Search',self)
        subWebSearch.setShortcut('Ctrl+Shift+W')
        searchMenu.addAction(subWebSearch)
        subWebSearch.triggered.connect(self.webSearch)

# aditya upload file sub menu
        subUploadFile = QAction('Upload File',self)
        uploadMenu.addAction(subUploadFile)
        subUploadFile.triggered.connect(self.uploadFile)
# aditya

#aditya subvoicemenus
        subvoice1 = QAction('Code',self)
        subvoice2 = QAction('Operation',self)
        voiceMenu.addAction(subvoice1)
        voiceMenu.addAction(subvoice2)
        subvoice1.triggered.connect(self.voicecode)
        subvoice2.triggered.connect(self.voiceoperation)
#aditya

#submenus for themes
        subSelect = QAction('Select',self)
        themesMenu.addAction(subSelect)
        subSelect.triggered.connect(self.selectTheme)
#for selecting the themes from custom theme
        subSelectCustom = QAction('Select Custom',self)
        themesMenu.addAction(subSelectCustom)
        subSelectCustom.triggered.connect(self.selectCustomTheme)
#for the user to make their own custom themes
        subCustom = QAction('Create Custom',self)
        themesMenu.addAction(subCustom)
        subCustom.triggered.connect(self.createCustomTheme)

#Aditya help and about Menu

        subhelp = QAction('Help That You Need',self)
        subAbout = QAction('About Us',self)
        helpMenu.addAction(subhelp)
        aboutMenu.addAction(subAbout)
        subhelp.triggered.connect(self.helpmethod)
        subAbout.triggered.connect(self.aboutmethod)

#Aditya
#creating grid layout and seting it up
        self.grid = QGridLayout(self)
        self.grid.setColumnStretch(0,2)
        self.grid.setColumnStretch(1,5)

#creating a tree widget for the file browsing stuff
        try:
#file system model for getting a system view on the left side to browse
            self.model = QFileSystemModel()
#rroot path is nothing so every disk is given
            self.model.setRootPath('')
#to show all the files and not show . and..
            self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
            m_path = "C:"
            self.model.setRootPath(m_path)
#tree view to apply the file system model on
            self.tree = QTreeView()
#setting the model i tree
            self.tree.setModel(self.model)
#hiding the size type and somthing to show only name
            self.tree.hideColumn(1)
            self.tree.hideColumn(2)
            self.tree.hideColumn(3)
            self.tree.resizeColumnToContents(0)
#if the file the double clicked the function to be called is connected
            self.tree.doubleClicked.connect(self.clickedDouble)

            self.tree.setAnimated(False)
            self.tree.setIndentation(20)
            self.tree.setSortingEnabled(True)

        except Exception as e:
            print('Exception near tree : ',str(sys.exc_info()))


#creating tab widgets and settings
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.South)
        self.tabs.setTabShape(QTabWidget.Triangular)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)

#adding a plus'+' button to add new tabs in tab widget
        self.plusButton = QToolButton()
        self.plusButton.setText('+')
        self.font = self.plusButton.font()
        self.font.setBold(True)
        self.plusButton.setFont(self.font)
        self.tabs.setCornerWidget(self.plusButton)
        self.tabs.tabCloseRequested.connect(self.closeTab)

#connecting to the module which will add a new tab
        self.plusButton.clicked.connect(self.newTab)
        try:
            text = QsciScintilla()
            self.preview(text)
            text.textChanged.connect(self.textChange)

            self.tab1 = QWidget()
            self.layout = QGridLayout(self)
            self.layout.addWidget(text)
            self.tab1.setLayout(self.layout)
            self.tabs.addTab(self.tab1,'UnTitled')

#creating text edit fro adding in tabs

#adding stuff to grid layout only 2 as we need only 2 of them
            self.grid.addWidget(self.tree,0,0)
            self.grid.addWidget(self.tabs,0,1)

#creating a widget to set the grid layout on which will
#eventually be set as the central widget in our application window
            self.window = QWidget()
            self.window.setLayout(self.grid)
            #self.window.setStyleSheet(appStyleWidget)

#setting the widget above as central widegt in our application window
            self.setCentralWidget(self.window)

            SELECTHEME(self)

#so our application is shown
            self.destroyed.connect(self.handleExit)
            self.show()
            self.timecheck()
        except Exception as e:
            print('Exception near text : ',str(sys.exc_info()))


#module for adding new tabs with text edits
#by using new option and that corner plus button
    def newTab(self):
        tab = QWidget()
        text = QsciScintilla()
        self.preview(text)
        text.textChanged.connect(self.textChange)
        layout = QGridLayout()
        layout.addWidget(text)
        tab.setLayout(layout)
        self.tabs.addTab(tab,'UnTitled')
        self.timecheck()


#module for opening files
    def openFile(self):
        global myadd
        self.information()
#open file dialog
        try:
#gives me the file name the type of d=file in a tuple
            filename = QFileDialog.getOpenFileName(self,"Open Files",".","Text files (*.txt); All files (*.*)");
#extracting only the file name from the tuple reeturned above

            justfile = os.path.basename(filename[0])
            self.lexer(justfile,self.globaltext)
#opening file
            file = open(filename[0],'r')
            data = file.read()
            self.globaltext.setText(data)
            self.tabs.setTabText(self.globalindex,justfile)
            self.timecheck()
            myadd[justfile] = filename[0]
        except Exception as e:
            print("Exception in open: ",str(sys.exc_info()))
            self.tabs.setTabText(self.globalindex,'UnTitled')


#module for saving file
    def saveFile(self,index = None):
        self.information()
        print('in save file')
        #print(index)
#saving the file normally
        try :
#if we are gtting a index from save all function then we work with
#parameter index or else we work with global index
            if index is None:
                name = self.tabs.tabText(self.globalindex)
            else:
                name = self.tabs.tabText(index)
            #print(name)
#checking if file is not saved hence, is untitled with or without *
            if name == 'UnTitled' or name == 'UnTitled*':
#if not saved calling save as....
                #print('saveas calling')
                self.saveAsFile(index)
            else:
#since file already exists we call save so the file is only written
                #print(''save calling')
                name = name.replace('*','')
                path = myadd[name]
                widget = QWidget()
                lay = QLayoutItem
#according to the index used above we get text document from
#widget for index or global index
                if index is None:
                    self.tabs.setTabText(self.globalindex,name)
                    widget = self.tabs.widget(self.globalindex)
                    grid = widget.layout()
                    lay = grid.itemAtPosition(0,0)
                    text = lay.widget()
                else:
                    self.tabs.setTabText(index,name)
                    widget = self.tabs.widget(index)
                    grid = widget.layout()
                    lay = grid.itemAtPosition(0,0)
                    text = lay.widget()
                f = open(path,"w+")
                f.write(text.text())
                f.close()
            self.timecheck()
        except Exception as e:
            print("Exception in save: ",str(sys.exc_info()))



#module for saving as file
    def saveAsFile(self,index=None):
        self.information()
        print('file save as')
        global myadd
#save as file using saveas file dialog
        try:
            #print('save as module')
#calling the file saving dialog to get the name of file and the file type to save as
            options = QFileDialog.Options()
            filename = QFileDialog.getSaveFileName(self,"SaveAsFile","","All Files (*);;Text Files (*.txt)", options=options)

            if filename:
#if filename given by user extract the filenamee by tuple and by creating the file write to the file
                #print(filename)
                truename = os.path.basename(filename[0])
                self.lexer(truename,self.globaltext)
                widget = QWidget()
                lay = QLayoutItem
#according to the index given from save all function we use given parameter index
#or the global index from information module
                if index is None:
                    self.tabs.setTabText(self.globalindex,truename)
                    widget = self.tabs.widget(self.globalindex)
                    grid = widget.layout()
                    lay = grid.itemAtPosition(0,0)
                    text = lay.widget()
                else:
                    self.tabs.setTabText(index,truename)
                    widget = self.tabs.widget(index)
                    grid = widget.layout()
                    lay = grid.itemAtPosition(0,0)
                    text = lay.widget()
                f = open(filename[0],"w+")
                f.write(text.text())
                f.close()
                myadd[truename] = filename[0]
            else:
                self.tabs.setTabText(self.globalindex,'UnTitled')
            self.timecheck()
        except Exception as e:
            print('Exception in save as:',str(sys.exc_info()))
#if file name not provided or anything goes wrong tab name goes bback to untitled
            self.tabs.setTabText(self.globalindex,'UnTitled')


#module for saving all opened files in our editor
    def saveAllFile(self):
        self.information()
        try:
            cnt = self.tabs.count()
            print(cnt)
            while cnt>-1:
                print(cnt)
                self.saveFile(cnt)
                cnt = cnt-1
            print('out of while')
            self.timecheck()
        except Exception as e:
            print('Exception in save all : ',str(sys.exc_info()))



#removing tabs using cross on each tab
    def closeTab(self, index):
        try:
#get the widget by index in tab widget
            widget = self.tabs.widget(index)
            if widget is not None:
#if the file in the tab is not saved a messgae to print if the user
#wants to save it or not
                tabName = self.tabs.tabText(index)
                if tabName.endswith('*'):
                    reply = QMessageBox.question(self,'Continue?','Do oyu want to save the file or not?', QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        if tabName.endswith('UnTitled*'):
                            self.saveAsFile()
                        elif tabName.endswith('*'):
                            self.saveFile()
                    elif QMessageBox.No:
                        self.tabs.removeTab(index)
                else:
                    self.tabs.removeTab(index)
            self.timecheck()
        except Exception as e:
            print('Exception in close : ',str(sys.exc_info()))


#removing all the opened tabs there are without
    def closeAllTabs(self):
#to close all tabs take count of the tabs opened
#then close them one by one byy calling closeTab function abovve
#where we will check if the file in the tab is saved or not
        cnt = self.tabs.count()
        while cnt>=0:
            self.closeTab(cnt)
            cnt = cnt-1
        self.timecheck()

#for closing the whole application
    def exit(self):
        print('closing bro.....')
        self.closeAllTabs()
        self.close()

    def handleExit(self):
        print('i m going to handle it')
        reply = QMessageBox.question(self,'Continue?','Do oyu want to QUIT?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
        	print('closing bro.....')
        	self.closeAllTabs()
        	self.close()


#for all the context menu options we call the information function to
#to get the text edit widget to apply the appropriate function

#undo operation module
    def opUndo(self):
        self.information()
        self.globaltext.undo()
        self.timecheck()


#redo operation module
    def opRedo(self):
        self.information()
        self.globaltext.redo()
        self.timecheck()


#copy operation module
    def opCopy(self):
        self.information()
        self.globaltext.copy()
        self.timecheck()


#cut operation module
    def opCut(self):
        self.information()
        self.globaltext.cut()
        self.timecheck()


#paste operation module
    def opPaste(self):
        self.information()
        self.globaltext.paste()
        self.timecheck()


#clear operation module
    def opClear(self):
        self.information()
        self.globaltext.clear()
        self.timecheck()


#select all operation module
    def opSelectAll(self):
        self.information()
        self.globaltext.selectAll()
        self.timecheck()


#zoom in operation module
    def opZoomIn(self):
        self.information()
        self.globaltext.zoomIn(1)
        self.timecheck()


#zoom out operation module
    def opZoomOut(self):
        self.information()
        self.globaltext.zoomOut(1)
        self.timecheck()

#opening command line promprt
    def openCmd(self):
#opening the cmd at the location where the file is saved
        os.system("start cmd .")   #after the . we can add the command
        self.timecheck()

#for find sub menu where we find a sub string in the text docuument
    def findWord(self):
        try:
            self.information()
            self.findialog = Find(self)
            self.findialog.show()
            self.timecheck()
        except Exception as e:
            print('Exception in calling find function as:',str(sys.exc_info()))

#find  and prelace stuff
    def findReplaceWord(self):
        self.frdialog = FindReplace(self)
        self.frdialog.show()
        self.timecheck()

#bazil

#aditya's function for uploading
    def uploadFile(self):
        print('uploading file')
        self.Up = UploadWindow(self)
        self.Up.show()


#aditya's end


#aditya method for voice
    def voicecode(self):
         print("voicecode")
         self.showdialog("Please See the Documentaion For Commands,To Use Feature")
         v = VoiceControl()
         text = v.voicecodeMain()
         self.information()
         self.globaltext.append(text)


    def showdialog(self,text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle("Subtle Window")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()


    def voiceoperation(self):
         print("voiceoperation")
         self.showdialog("Please See the Documentaion For Commands,To Use Feature")
         v = VoiceControl()
         string = v.voiceOperationMain()
         print(string)
         eval(string)
#aditya


#mayuresh


#selecting theme is awesome bro
    def selectTheme(self):
        print('in select theme ')
        self.theme = Themes(self)
        self.theme.show()
        self.timecheck()


# function for calling a class where we will select one from many custom themes
    def selectCustomTheme(self):
        print('selecting custom theme')
        self.themeCS = ThemeCustomSelect(self)
        self.themeCS.show()
        self.timecheck()


#function call for custom theme which intern will call a class to make one
    def createCustomTheme(self):
        print('custom theme')
        self.Customtheme = CustomThemes(self)
        self.Customtheme.show()
        self.timecheck()


#web search is in a different file where i call it up
    def webSearch(self):
#open the input dialog to get the text from user
        searchQuery, ok = QInputDialog.getText(self, 'Web Search', 'Enter search query:')
        if ok:
#call the open function to open the default browser and search for the
#user input on google
            new = 2
            tabUrl = "http://google.com/search?q="
            webbrowser.open(tabUrl+searchQuery,new=new)
        self.timecheck()


#suggestions for spotllight search
    def suggest(self):
        try:
            print('suggestion?')
            self.completer = QCompleter(wordList,self)
            self.completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
            self.spotLight.setCompleter(self.completer)
            self.completer.activated.connect(self.call)
        except Exception as e:
            print('Exception in suggestion : ',str(sys.exc_info()))

    def call(self):
        text = self.spotLight.text()

        if text=='New(File Menu)':
            self.newTab()
        elif text=='Open(File Menu)':
            self.openFile()
        elif text=='Save(File Menu)':
            self.saveFile()
        elif text=='SaveAs(File Menu)':
            self.saveAsFile()
        elif text=='SaveAll(File Menu)':
            self.saveAllFile()
        elif text=='Close(File Menu)':
            self.closeTab()
        elif text=='CloseAll(File Menu)':
            self.closeAllTabs()
        elif text=='Exit(File Menu)':
            self.exit()
        elif text=='Undo(Edit Menu)':
            self.opUndo()
        elif text=='Redo(Edit Menu)':
            self.opRedo()
        elif text=='Cut(Edit Menu)':
            self.opCut()
        elif text=='Copy(Edit Menu)':
            self.opCopy()
        elif text=='Paste(Edit Menu)':
            self.opPaste()
        elif text=='SelectAll(Edit Menu)':
            self.opSelectAll()
        elif text=='Clear(Edit Menu)':
            self.opClear()
        elif text=='ZoomIn(Edit Menu)':
            self.opZoomIn()
        elif text=='ZoomOut(Edit Menu)':
            self.opZoomOut()
        elif text=='Compile(Execute Menu)':
            self.openCmd()
        elif text=='Find(Search Menu)':
            self.findWord()
        elif text=='Find&Replace(Search Menu)':
            self.findReplaceWord()
        elif text=='Select Theme(Theme Menu)':
            self.selectTheme()
        elif text=='WebSearch(Search Menu)':
            self.webSearch()
        elif text=='Upload File(Upload Menu)':
        	self.uploadFile()
        elif text=='Code(Voice Menu)':
        	self.voicecode()
        elif text=='Operate(Voice Menu)':
        	self.voiceoperation()
        elif text=='Select Theme(Theme Menu)':
        	self.selectTheme()
        elif text=='Select Custom(Theme Menu)':
        	self.selectCustomTheme()
        elif text=='Create Custom(Theme Menu)':
        	self.createCustomTheme()
        elif text=='Help':
        	self.helpmethod()
        elif text=='About':
        	self.aboutmethod()


    def clickedDouble(self):
        try:
#to get the index of tthe item clicked so we can get the name of the item
#and set the tab ttextt accordingly
            index = self.tree.currentIndex();
            data = self.tree.model().data(index);
            file, ext = os.path.splitext(data)
            if ext in FILEEND:
#getting thhe file path of the iitem selected so we can open the file
                #print('text file')
                path = self.model.filePath(self.tree.selectionModel().currentIndex())
                #print(path)
#opening the file and some other stuff
                self.information()
                file = open(path,'r')
                data1 = file.read()
                self.globaltext.setText(data1)
                self.tabs.setTabText(self.globalindex,data)
                self.lexer(data,self.globaltext)
            else:
            	self.showdialog("File Not Supported!!")
            self.timecheck()
        except Exception as e:
            print('Exception in clicked as:',str(sys.exc_info()))
            self.tabs.setTabText(self.globalindex,'UnTitled')


#mayuresh


#bazil

#this is the event for Qtextedit where we are notified when the text is edited
#in anyway possible
    def textChange(self):
        #print('text is changed')
        self.information()
        try :
            self.timecheck()
#to add the * at the end of the tab name to indicate the file opened has been edited
            name = self.tabs.tabText(self.globalindex)
            if name.find('*') == -1:
                name = name+'*'
                self.tabs.setTabText(self.globalindex,name)
            self.timecheck()
        except Exception as e:
            print('Exception in save as:',str(sys.exc_info()))


#setting the timer for the application to make a auto save stuff
    def timecheck(self):
        try:
            global start
            if time.time()-start > 30:
                print('30 secondsdoen bro.....')
                start = time.time()
        except Exception as e:
            print('Exception in time check:',str(sys.exc_info()))


##the code was getting repeated every where so i created a module for getting the information
#and setting some self global variables so i can access them anywhere in class
    def information(self):
        try:
#found index of the file
            self.globalindex = self.tabs.currentIndex()
        #print(index)
#getting the widget on the tab
            widget = QWidget()
            widget = self.tabs.widget(self.globalindex)
#getting the grid on the widget
            grid = widget.layout()
        #print(grid)
#geting the item or widget in grid layout
            lay = QLayoutItem
            lay = grid.itemAtPosition(0,0)
        #print(lay)
#geting the textedit on the layout
            self.globaltext = lay.widget()
            self.timecheck()
        except Exception as e:
            print('Exception in info :',str(sys.exc_info()))

    def handle(self):
        print('tis button is handled')

#bazil

#aditya
    def helpmethod(self):
        self.showdialog("Please Read the Documentation and Help Yourself!")
    def aboutmethod(self):
         self.showdialog('Subtle Editor\n\n*For Love Of Coding*\n\nYou Can Give Your Feedback,Or\nIf You Face Any Issue Contact Us:\nSubtleEditor@gmail.com\n\n"Created" By Wadians\n  Aditya\n  Bazil\n  Mayuresh')
#aditya


#scintilla inside class now

    def preview(self, parent=None):
        try :
            # Set the default font
            self.font = QFont()
            self.font.setFamily('Courier')
            self.font.setFixedPitch(True)
            self.font.setPointSize(10)
            parent.setFont(self.font)
            parent.setMarginsFont(self.font)

            # Margin 0 is used for line numbers
            fontmetrics = QFontMetrics(self.font)
            parent.setMarginsFont(self.font)
            parent.setMarginWidth(0, fontmetrics.width("00000") + 6)
            parent.setMarginLineNumbers(0, True)
            parent.setMarginsBackgroundColor(QColor("#cccccc"))
            # i changed something here
            #parent.setBackgroundColor();
            #SendMessage(SCI_STYLESETBACK,33,(LPARAM)RGB(0,0,0))

#now to autocompletion stuff i.e., to get the names while we are typing stuff
#the paremeter states i m going to use the curent document and apis for auto completion
            parent.setAutoCompletionSource(QsciScintilla.AcsAll)
#the function called below takes the no. of chars. ,when this no. is achieved the auto completion window id displayed
            parent.setAutoCompletionThreshold(3)
#now the function below is to sett if the auto completion is case sensitve is not, iset it to false to indicate insensitive
            parent.setAutoCompletionCaseSensitivity(False)
#tjis function is to set if when writing the charaters to the right of the cursor are replaced by the auto completion or not
#false indicates they are not
            parent.setAutoCompletionReplaceWord(False)
#now what if there is only one option in the auto completion window do we dispaly it or not
#i m going t odisplay it
            parent.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

#to set auto indentaion so when we press enter after brackets the space goes up by a tab (maybe)
            parent.setIndentationsUseTabs(True)
            #tab width is defined by 4 wide spaces
            parent.setTabWidth(4)
            parent.setIndentationGuides(True)
            parent.setTabIndents(True)
            parent.setAutoIndent(True)


            # Clickable margin 1 for showing markers
            parent.setMarginSensitivity(1, True)
    #        self.connect(self,
    #            SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),
    #            self.on_margin_clicked)
            parent.markerDefine(QsciScintilla.RightArrow,ARROW_MARKER_NUM)
            parent.setMarkerBackgroundColor(QColor("#cccccc"),ARROW_MARKER_NUM)

            # Brace matching: enable for a brace immediately before or after
            # the current position
            #
            parent.setBraceMatching(QsciScintilla.StrictBraceMatch)

            # Current line visible with special background color
            parent.setCaretLineVisible(True)
            parent.setCaretLineBackgroundColor(QColor("#ffe4e4"))

            # Set Python lexer
            # Set style for Python comments (style number 1) to a fixed-width
            # courier.
            #

            text = bytearray(str.encode("Arial"))
    # 32, "Courier New"
            parent.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, text)

            # Don't want to see the horizontal scrollbar at all
            # Use raw message to Scintilla here (all messages are documented
            # here: http://www.scintilla.org/ScintillaDoc.html)
            parent.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
            #parent.SendMessage(SCI_STYLESETBACK, STYLE_DEFAULT, RGB(0,0,0));
        except Exception as e:
            print('Exception in preview as : ',str(sys.exc_info()))


    def lexer(self,name,parent=None):
        try:
            #print(name)
            filename, filext = os.path.splitext(name)
            print(filename)
            print(filext)
#making a dictionary to check which kind offile is opened or saved
            fileExt={
                #for batch files like system files and stuff
                '.bat':QsciLexerBatch(),
                '.cmd':QsciLexerBatch(),
                '.btm':QsciLexerBatch(),
                #for c and c++ files and header files
                '.c':QsciLexerCPP(),
                '.C':QsciLexerCPP(),
                '.cc':QsciLexerCPP(),
                '.cpp':QsciLexerCPP(),
                '.CPP':QsciLexerCPP(),
                '.c++':QsciLexerCPP(),
                '.cp':QsciLexerCPP(),
                '.cxx':QsciLexerCPP(),
                '.hpp':QsciLexerCPP(),
                '.hxx':QsciLexerCPP(),
                '.Hxx':QsciLexerCPP(),
                '.HXX':QsciLexerCPP(),
                #for csharp files
                '.cs':QsciLexerCSharp(),
                #for java language files
                '.java':QsciLexerJava(),
                #for javascript language files
                '.js':QsciLexerJavaScript(),
                #for html page files
                '.html':QsciLexerHTML(),
                #for css language files
                '.css':QsciLexerCSS(),
                #for xml language files
                '.xml':QsciLexerXML(),
                '.xrb':QsciLexerXML(),
                #for matlab files like functions and stuff
                '.m':QsciLexerMatlab(),
                '.p':QsciLexerMatlab(),
                '.mlx':QsciLexerMatlab(),
                #for perl language files
                '.pl':QsciLexerPerl(),
                '.PL':QsciLexerPerl(),
                '.pm':QsciLexerPerl(),
                #for python language files like this one
                '.py':QsciLexerPython(),
                #for ruby language files
                '.rb':QsciLexerRuby()
                }
            lexer = fileExt.get(filext)
            print(fileExt.get(filext))

            if lexer:
                lexer.setDefaultFont(self.font)
                parent.setLexer(lexer)
                #i changed heere
                #defualtcolor= QColor(0xff, 0xff, 0xff)
                #lexer.setPaper(defualtcolor)
        except Exception as e:
            print('Exception in lexer function as : ',str(sys.exc_info()))


    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)


def SELECTHEME(self):
    #you know to make the windaow same as berofe like the user selected the theme
    f = open("Data\THEME_SELECT.txt","r")
    data = f.read()
    global THEME_SELECT
    THEME_SELECT = int(data)
    f.close()
    if data == "1":
        THEME_SELECT = 1
        self.setStyleSheet(themeStyle1)
    elif data == "2":
        THEME_SELECT = 2
        self.setStyleSheet(themeStyle2)
    elif data == "3":
        THEME_SELECT = 3
        self.setStyleSheet(themeStyle3)
    elif data == "4":
        THEME_SELECT = 4
        #self.setStyleSheet(themeStyle4)
        self.setStyleSheet(None)
    else:
        f = open("Data\Custom\selected.txt","r")
        data = f.read()
        global THEME_CUSTOM_SELECT
        THEME_CUSTOM_SELECT = int(data)
        f.close()
        if THEME_CUSTOM_SELECT == 0:
            self.setStyleSheet(None)
        else:
            f = open("Data\Custom\THEME_CUSTOM_"+str(THEME_CUSTOM_SELECT)+".txt","r")
            data = f.read()
            f.close()
            self.setStyleSheet(data)

#bazil's main was here



#aditya code for voice starts here-----------------------------------------------------------------------------


class StringFromRecognizer:
      def __init__(self,GotSentence):
          self.GotSentence = GotSentence
          self.voicecontrolobject = VoiceControl()
           #writing text into file which is not code
      def JustWrite(self,GotSentence):
          #file = open("C:\\Users\\Aditya\\Desktop\\mypage1.html","a+")
          #file.write(GotSentence)
          return GotSentence

          #getting tags into file
      def ToHTMLcode(self,GotSentence):
           newformedString=""
           #file = open("C:\\Users\\Aditya\\Desktop\\mypage1.html","a+")
           HTMLstring = GotSentence.lower()
           HTMLTagsArray = {
           'comment tag':'<!--...-->',
           'doctype tag' : '<!DOCTYPE>',
           'hyperlink tag open' : '<a>',
           'hyperlink tag close' : '</a>',
           'abbreviation tag open' : '<abbr>',
           'abbreviation tag close' : '</abbr>',
           'acronym tag open': '<acronym>',
           'acronym tag close': '</acronym>',
           'address tag open' : '<address>',
           'address tag close' : '</address>',
           'applet tag open' : '<applet>',
           'applet tag close' : '</applet>',
           'area tag open' : '<area>',
           'area tag close' : '</area>',
           'article tag open' : '<article>',
           'article tag close' : '</article>',
           'aside tag open' : '<aside>',
           'aside tag close' : '</aside>',
           'audio tag open' : '<audio>',
           'audio tag close' : '</audio>',
           'bold tag open' : '<b>',
           'bold tag close' : '</b>',
           'base tag open':'<base>',
           #'base tag close':'</base>',
           'basefont tag open' : '<basefont>',
           'bidirection tag open' : '<bdi>',
           'bidirection tag close' : '</bdi>',
           'bidirection override tag open' : '<bdo>',
           'bidirection override tag close' : '</bdo>',
           'big tag open' : '<big>',
           'big tag close' : '</big>',
           'blockquote tag open' : '<blockquote>',
           'blockquote tag close' : '</blockquote>',
           'body tag open' : '<body>',
           'body tag close' : '</body>',
           'line break tag open' : '<br>',
           'button tag open' : '<button>',
           'button tag close' : '</button>',
           'canvas tag open' : '<canvas>',
           'canvas tag close' : '</canvas>',
           'caption tag open' : '<caption>',
           'caption tag close' : '</caption>',
           'center tag open' : '<center>',
           'center tag close' : '</center>',
           'citation tag open' : '<cite>',
           'citation tag close' : '</cite>',
           'code tag open' : '<code>',
           'code tag close' : '</code>',
           'column tag open' : '<col>',
           'column group tag open' : '<colgroup>',
           'column group tag close' : '</colgroup>',
           'data tag open' : '<data>',
           'data tag close' : '</data>',
           'data list tag open' : '<datalist>',
           'data list tag close' : '</datalist>',
           'descriptive tag open' : '<dd>',
           'descriptive tag close' : '</dd>',
           'delete line tag open' : '<del>',
           'delete line tag close' : '</del>',
           'detail tag open' : '<details>',
           'detail tag close' : '</details>',
           'define tag open' : '<dfn>',
           'define tag close' : '</dfn>',
           'dialog tag open' : '<dialog>',
           'dialog tag close' : '</dialog>',
           'directory tag open' : '<dir>',
           'directory tag close' : '</dir>',
           'division tag open' : '<div>',
           'division tag close' : '<div>',
           'description list tag open' : '<dl>',
           'description list tag close' : '<dl>',
           'description name tag open' : '<dt>',
           'description name tag close' : '</dt>',
           'emphasized tag open' : '<em>',
           'emphasized tag close' : '</em>',
           'embed tag open' : '<embed>',
           'embed tag close' : '</embed>',
           'field set tag open' : '<fieldset>',
           'field set tag close' : '</fieldset>',
           'figure caption tag open' : '<figcaption>',
           'figure caption tag close' : '</figcaption>',
           'figure tag open' : '<figure>',
           'figure tag close' : '</figure>',
           'font tag open' : '<font>',
           'font tag close' : '</font>',
           'footer tag open' : '<footer>',
           'footer tag close' : '</footer>',
           'form tag open' : '<form>',
           'form tag open' : '</form>',
           'frame tag open' : '<frame>',
           'frame tag close' : '</frame>',
           'frame set tag open' : '<frameset>',
           'frame set tag close' : '</frameset>',
           'h 2 tag open' : '<h2>',
           'h 2 tag close' : '</h2>',
           'h 1 tag open' : '<h1>',
           'h 1 tag close' : '</h1>',
           'h 4 tag open' : '<h4>',
           'h 4 tag close' : '</h4>',
           'h 3 tag open' : '<h3>',
           'h 3 tag close' : '</h3>',
           'h 5 tag open' : '<h5>',
           'h 5 tag close' : '</h5>',
           'h 6 tag open' : '<h6>',
           'h 6 tag close' : '</h6>',
           'head tag open' : '<head>',
           'head tag close' : '</head>',
           'header tag open' : '<header>',
           'header tag close' : '</header>',
           'thematic tag open' : '<hr>',
           'thematic tag close' : '</hr>',
           'html tag open' : '<html>',
           'html tag close' : '</html>',
           'italics tag open' : '<i>',
           'italics tag close' : '</i>',
           'inline frame tag open' : '<iframe>',
           'inline frame tag close' : '</iframe>',
           'input tag open' : '<input>',
           'input tag close' : '</input>',
           'image tag open' : '<img>',
           'image tag close' : '</img>',
           'keyboard tag open' : '<kbd>',
           'keyboard tag open' : '</kbd>',
           'inserted  tag open' : '<ins>',
           'inserted  tag close' : '</ins>',
           'label tag open' : '<label>',
           'label tag close' : '</label>',
           'legend tag open' : '<legend>',
           'legend tag close' : '</legend>',
           'list item tag open' : '<li>',
           'list item tag close' : '</li>',
           'link tag open' : '<link>',
           'link tag close' : '</link>',
           'main tag open' : '<main>',
           'main tag close' : '</main>',
           'map tag open' : '<map>',
           'map tag close' : '</map>',
           'mark tag open' : '<mark>',
           'mark tag close' : '</mark>',
           'menu tag open' : '<menu>',
           'menu tag close' : '</menu>',
           'menu item tag open' : '<menuitem>',
           'menu item tag close' : '</menuitem>',
           'meta tag open' : '<meta>',
           'meta tag close' : '</meta>',
           'meter tag open' : '<meter>',
           'meter tag close' : '</meter>',
           'navigation tag open' : '<nav>',
           'navigation tag close' : '</nav>',
           'no frame tag open' : '<noframes>',
           'no frame tag close' : '</noframes>',
           'no script tag open' : '<noscript>',
           'no script tag close' : '</noscript>',
           'object tag open' : '<object>',
           'object tag close' : '</object>',
           'ordered list tag open' : '<ol>',
           'ordered list tag close' : '</ol>',
           'option group tag open' : '<optgroup>',
           'option group tag close' : '</optgroup>',
           'option tag open' : '<option>',
           'option tag close' : '</option>',
           'output tag open' : '<output>',
           'output tag close' : '</output>',
           'paragraph tag open' : '<p>',
           'paragraph tag close' : '</p>',
           'parameter tag open' : '<param>',
           'parameter tag close' : '</param>',
           'picture tag open' : '<picture>',
           'picture tag close' : '</picture>',
           'preformatted tag open' : '<pre>',
           'preformatted tag close' : '</pre>',
           'progress tag open' : '<progress>',
           'progress tag close' : '</progress>',
           'quotaion tag open' : '<q>',
           'quotaion tag close' : '</q>',
           '' : '<rp>',
           '' : '<rt>',
           'ruby tag open' : '<ruby>',
           'ruby tag close' : '</ruby>',
           'not correct tag open' : '<s>',
           'not correct tag close' : '</s>',
           'sample tag open' : '<samp>',
           'sample tag close' : '</samp>',
           'script tag open' : '<script>',
           'script tag close' : '</script>',
           'section tag open' : '<section>',
           'section tag close' : '</section>',
           'select tag open' : '<select>',
           'select tag close' : '</select>',
           'small tag open' : '<small>',
           'small tag close' : '</small>',
           'source tag open' : '<source>',
           'source tag close' : '</source>',
           'span tag open' : '<span>',
           'span tag close' : '</span>',
           'strikethrough tag open' : '<strike>',
           'strikethrough tag close' : '</strike>',
           'important tag open' : '<strong>',
           'important tag close' : '</strong>',
           'style tag open' : '<style>',
           'style tag close' : '</style>',
           'subscripted text tag open' : '<sub>',
           'subscripted text tag close' : '</sub>',
           'summary tag open' : '<summary>',
           'summary tag close' : '</summary>',
           'super scripted text tag open' : '<sup>',
           'super scripted text tag close' : '</sup>',
           'svg graphics tag open' : '<svg>',
           'svg graphics tag close' : '</svg>',
           'table tag open' : '<table>',
           'table tag close' : '</table>',
           'table body tag open' : '<tbody>',
           'table body tag close' : '</tbody>',
           'table cell tag open' : '<td>',
           'table cell tag close' : '</td>',
           'template tag open' : '<template>',
           'template tag close' : '</template>',
           'text area tag open' : '<textarea>',
           'text area tag close' : '</textarea>',
           'table footer tag open' : '<tfoot>',
           'table footer tag close' : '</tfoot>',
           'table header cell tag open' : '<th>',
           'table header cell tag close' : '</th>',
           'table header tag open' : '<thead>',
           'table header tag close' : '</thead>',
           'time tag open' : '<time>',
           'time tag close' : '</time>',
           'title tag open' : '<title>',
           'title tag close' : '</title>',
           'table row tag open' : '<tr>',
           'table row tag close' : '</tr>',
           'tarck tag open' : '<track>',
           'teletype text tag open' : '<tt>',
           'teletype text tag close' : '</tt>',
           'stylist tag open' : '<u>',
           'stylist tag close' : '</u>',
           'unordered list tag open' : '<ul>',
           'unordered list tag close' : '</ul>',
           'variable tag open' : '<var>',
           'variable tag close' : '</var>',
           'video tag open' : '<video>',
           'video tag close' : '</video>',
           'possible line break tag open' : '<wbr>',
           'possible line break tag close' : '</wbr>'
           }

           AttributeString = {
           'accept attribute' : 'accept',
           'accept character set attribute' : 'accept-charset',
           'access key attribute' : 'accesskey',
           'action attribute' : 'action',
           'align attribute' : 'align',
           'alternate attribute' : 'alt',
           'asynchronous attribute' : 'async',
           'auto capitalize attribute' : 'autocapitalize',
           'auto complete attribute' : 'autocomplete',
           'auto focus attribute' : 'autofocus',
           'auto play attribute' : 'autoplay ',
           'background attribute' : 'bgcolor',
           'border attribute' : 'border',
           'buffer attribute' : 'buffered ',
           'challenge attribute' : 'challenge',
           'character set attribute' : 'charset',
           'checked attribute' : 'checked',
           'citation attribute' : 'cite',
           'class attribute' : 'class',
           'code attribute' : 'code',
           'code base attribute' : 'codebase',
           'color attribute' : 'color',
           'column attribute' : 'cols',
           'column span attribute' : 'colspan',
           'content attribute' : 'content ',
           'content editable' : 'contenteditable',
           'conetxt menu attribute' : 'contextmenu',
           'control attribute' : 'controls',
           'coordinate attribute' : 'coords',
           'cross origin attribute' : 'crossorigin',
           'data attribute' : 'data',
           'date time attribute' : 'datetime',
           'default attribute' : 'default',
           'deference attribute' : 'defer',
           'directory attribute' : 'dir',
           'directory name attribute' : 'dirname',
           'disable attribute' : 'disabled',
           'download attribute' : 'download',
           'draggable attribute' : 'draggable',
           'drop zone attribute' : 'dropzone',
           'encrypt type attribute' : 'enctype ',
           'for attribute' : 'for',
           'form attribute' : 'form',
           'form action attribute' : 'formaction',
           'header attribute' : 'headers',
           'height attribute' : 'height',
           'hidden attribute' : 'hidden',
           'high attribute' : 'high',
           'hyperlink reference attribute' : 'href',
           'hyperlink reference language attribute' : 'hreflang',
           'http equivalent attribute' : 'http-equiv',
           'icon attribute' : 'icon',
           'identity attribute' : 'id',
           'integrity attribute' : 'integrity',
           'is map attribute' : 'ismap ',
           'item property attribute' : 'itemprop',
           'key type attribute' : 'keytype',
           'kind attribute' : 'kind',
           'label attribute' : 'label',
           'language attribute' : 'lang',
           'script language attribute' : 'language',
           'list attribute' : 'list',
           'loop attribute' : 'loop',
           'low attribute' : 'low',
           'manifest attribute' : 'manifest',
           'max attribute' : 'max',
           'maximum length attribute' : 'maxlength',
           'minimum length attribute' : 'minlength',
           'media attribute' : 'media',
           'method attribute' : 'method',
           'min attribute' : 'min',
           'multiple attribute' : 'multiple',
           'mute attribute' : 'muted',
           'name attribute' : 'name',
           'no validate attribute' : 'novalidate',
           'open attribute' : 'open',
           'optimum attribute' : 'optimum',
           'pattern attribute' : 'pattern',
           'ping attribute' : 'ping',
           'place holder attribute' : 'placeholder',
           'poster attribute' : 'poster',
           'preload attribute' : 'preload',
           'radio group attribute' : 'radiogroup',
           'read only attribute' : 'readonly',
           'relation attribute' : 'rel',
           'required attribute' : 'required',
           'reversed attribute' : 'reversed',
           'row attribute' : 'rows',
           'row span attribute' : 'rowspan',
           'sandbox attribute' : 'sandbox',
           'table scope attribute' : 'scope',
           'style scope attribute' : 'scoped',
           'seamless attribute' : 'seamless',
           'selected attribute' : 'selected',
           'shape attribute' : 'shape',
           'size attribute' : 'size',
           'sizes attribute' : 'sizes',
           'slot attribute' : 'slot',
           'span attribute' : 'span',
           'spellcheck attribute' : 'spellcheck',
           'source' : 'src',
           'source document attribute' : 'srcdoc',
           'source language attribute' : 'srclang',
           'source set attribute' : 'srcset',
           'start attribute' : 'start',
           'step attribute' : 'step',
           'style attribute' : 'style',
           'summary attribute' : 'summary',
           'tab index attribute' : 'tabindex',
           'target attribute' : 'target',
           'title attribute' : 'title',
           'translate attribute' : 'translate',
           'type attribute' : 'type',
           'use map attribute' : 'usemap',
           'value attribute' : 'value',
           'width attribute' : 'width',
           'wrap attribute' : 'wrap'
           }

           sizeofdict=len(HTMLTagsArray)
           tag_keys = HTMLTagsArray.keys()
           attribute_keys = AttributeString.keys()

           #keys.sort()
           #Ask if user wants to add attribute
           yes_or_no = 'yes'
           #i=0
           attarr = []
           attvalue = []
           #searching through file for html inbuilt tags
           for each in tag_keys:
               i=0
               #looking if whatever said matches with html tag is present in  dictionary file
               if  each == HTMLstring:
                   if '/' in HTMLTagsArray.get(each):
                       newformedString = HTMLTagsArray.get(each)
                       yes_or_no='no'
                       break
                   else:
                       #looping until user says no to add attribute
                       HTMLTagnew = HTMLTagsArray.get(each).replace("<","")
                       HTMLTag = HTMLTagnew.replace("<","")
                       while yes_or_no == 'yes':
                         #asking user if he wants to add atribute by usig speak function,
                         #and it returns whatever said that ought to be an attribute
                         said=self.voicecontrolobject.Speak('do you want to add attribute to html tag?')
                         #if said yes again call function speak to ask user which attribute he or she wants to add
                         if said == 'yes':
                            attsaid = self.voicecontrolobject.Speak('Say the attribute command')
                            #got value from speak function which is the command for a certin attribute
                            #which we are going to find through this loop below
                            #--we created an array of attributes because we dont know how many attributes user will add to the add--
                            for attrkey in attribute_keys:
                                #storing the attribute into the array
                                print("key is ",attrkey)
                                print("what said is ",attsaid)
                                if attrkey == attsaid:
                                   print(attrkey)
                                   attarr.append(AttributeString.get(attrkey))
                                   attvaluesaid= self.voicecontrolobject.Speak('Say the attribute value')
                                   if attvaluesaid is None:
                                      attvaluesaid = self.voicecontrolobject.Speak('Say the attribute value')
                                   else:
                                      attvalue.append(attvaluesaid)
                                   i=i+1
                                   print(attarr)
                                   print(attvalue)
                                   continue
                                elif attrkey != attsaid:
                                     continue
                                else :
                                   self.voicecontrolobject.Speak(' no such attribute found in the database')
                                   break

                         elif said == 'no':
                              formedString2=""
                              chevrons="<>"
                              for char in chevrons:
                                   HTMLTag = HTMLTag.replace(char,"")
                              formedString1 = "<"+ HTMLTag + " "
                              length_of_attribute_array=len(attarr)
                              temp_value=0
                              if len(attarr) == 0:
                                  newformedString = HTMLTagsArray.get(each)
                              else:
                                  while temp_value < length_of_attribute_array:
                                       formedString2 = formedString2 + attarr[temp_value] + '="' + attvalue[temp_value]+'" '
                                       temp_value=temp_value+1
                              if len(attarr) != 0:
                                 newformedString = formedString1 + formedString2 + '>'
                              else:
                                 newformedString = HTMLTagsArray.get(each)

                              yes_or_no='no'

                         else:
                             self.voicecontrolobject.Speak('You need to say yes or no only,speak now')

                   break
               else :
                   continue

           print(newformedString)
           #file.write(newformedString)
           #file.flush()
           return newformedString



           #search ends here for tags

         #getting printable(ascii) charatcers in file
      def ToCode(self,GotSentence):
          Svariable = GotSentence.lower()
          print(Svariable)
          #space symbol
          #file = open("C:\\Users\\Aditya\\Desktop\\mypage.html","a+")
          single_characters = {
          'space symbol' : ' ',
          'exclamation mark symbol' : '!',
          'double quotes symbol' : '"',
          'quotation mark symbol' : '"',
          'speech marks symbol' : '"',
          'number sign symbol' : '#',
          'pound symbol' : '#',
          'hash symbol' : '#',
          'percent symbol' : '%',
          'dollar symbol' : '$',
          'ampersand symbol' : '&',
          'single quote symbol' : '\'',
          'apostrophe symbol' : '\'',
          'round brackets open symbol' : '(',
          'parentheses open symbol' : '(',
          'parentheses close symbol' : ')',
          'round brackets close symbol' : ')',
          'asterisk symbol' : '*',
          'star symbol' : '*',
          'plus symbol' : '+',
          'comma symbol' : ',',
          'hyphen symbol' : '-',
          'minus symbol' : '-',
          'dot symbol' : '.',
          'full stop symbol' : '.',
          'period symbol' : '.',
          'slash symbol' : '/',
          'forward slash symbol' : '/',
          'fraction bar symbol' : '/',
          'division slash symbol' : '/',
          '/ symbol' : '/',
          #  else if0 ( number zero
          #          else if2 ( number two
          #else if3 ( number three
          #else if4 ( number four
          # else if5 ( number five
          # else if6 ( number six
          # else if7 ( number seven
          # else if8 ( number eight
          # else if9 ( number nine
          #colon :
          'colon symbol' : ':',
          'semicolon symbol' : ';',
          'less than symbol' : '<',
          'equal symbol' : '=',
          'equals symbol' : '=',
          'equals to symbol' : '=',
          'greater than symbol' : '>',
          'question mark symbol' : '?',
          'at symbol' : '@',
          'at the rate symbol' : '@',
          #capital letter A to Z----------,---------------------------------------
          'capital letter a symbol' : 'A',
          'capital letter b symbol' : 'B',
          'capital letter c symbol' : 'C',
          'capital letter d symbol' : 'D',
          'capital letter e symbol' : 'E',
          'capital letter f symbol' : 'F',
          'capital letter g symbol' : 'G',
          'capital letter h symbol' : 'H',
          'capital letter i symbol' : 'I',
          'capital letter j symbol' : 'J',
          'capital letter k symbol' : 'K',
          'capital letter l symbol' : 'L',
          'capital letter m symbol' : 'M',
          'capital letter n symbol' : 'N',
          'capital letter o symbol' : 'O',
          'capital letter p symbol' : 'P',
          'capital letter q symbol' : 'Q',
          'capital letter r symbol' : 'R',
          'capital letter s symbol' : 'S',
          'capital letter t symbol' : 'T',
          'capital letter u symbol' : 'U',
          'capital letter v symbol' : 'V',
          'capital letter w symbol' : 'W',
          'capital letter x symbol' : 'X',
          'capital letter y symbol' : 'Y',
          'capital letter z symbol' : 'Z',
          #capital letter A to Z--------------------------------------------------
          #square brackets open [
          'square brackets open symbol' : '[',
          'box brackets open symbol' : '[',
          'backward slash symbol' : '\\',
          'backslash symbol' : '\\',
          'reverse slash symbol' : '\\',
          'box brackets close symbol' : ']',
          'square brackets close symbol' : ']',
          'circumflex accent symbol' : '^',
          'caret symbol' : '^',
          'underscore symbol' : '_',
          'understrike symbol' : '_',
          'underbar symbol' : '_',
          'low line symbol' : '_',
          'grave accent symbol' : '`',
          'curly brackets open symbol' : '{',
          'vertical bar symbol' : '|',
          'vbar symbol' : '|',
          'vertical line symbol' : '|',
          'vertical slash symbol' : '|',
          'curly brackets close symbol' : '}',
          'tilde symbol' : '~',
          'swung dash symbol' : '~'
          }
          charkeys = single_characters.keys()
          for key in charkeys:
              if key == Svariable:
                  chargot = single_characters.get(key)
                  print("this is key "+key)
                  print("thi is character got"+chargot)
                  return chargot
                  break
              else:
                  continue

      def ToOption(self,GotSentence):
          Svariable = GotSentence.lower()
          OptionList = {
            'New' : 'self.newTab()',
            'Open' : 'self.openFile()',
            'Save' : 'self.saveFile()',
            'Save As' : 'self.saveAsFile()',
            'Save All' : 'self.saveAllFile()',
            'Close' : 'self.closeTab()',
            'Close All' : 'self.closeAllTabs()',
            'Exit' : 'self.exit()',
            'Undo' : 'self.opUndo()',
            'Redo' : 'self.opRedo()',
            'Cut' : 'self.opCut()',
            'Copy' : 'self.opCopy()',
            'Paste' : 'self.opPaste()',
            'Select All' : 'self.opSelectAll()',
            'Clear' : 'self.opClear()',
            'Zoom In' : 'self.opZoomIn()',
            'Zoom Out' : 'self.opZoomOut()',
            'Compile' : 'self.openCmd()',
            'Find' : 'self.findWord()',
            'Find and Replace' : 'self.findReplaceWord()',
            'Web Search' : 'self.webSearch()',
            'Upload File' : 'self.uploadFile()',
            'Code' : 'self.voicecode()',
            'Operate' : 'self.voiceoperation()',
            'Select Theme' : 'self.selectTheme()',
            'Select Custom Theme' : 'self.selectCustomTheme()',
            'Create Custom Theme' : 'self.createCustomTheme()',
            'Help' : 'self.helpmethod()',
            'About' : 'self.aboutmethod()'
            }
          optionKeys = OptionList.keys()
          for each in optionKeys:
              if each.lower() == Svariable:
                  print(each)
                  print("this is"+OptionList.get(each))
                  return OptionList.get(each)
              elif each != Svariable:
                   continue
              else:
                  spokeback = self.voicecontrolobject.Speak('No Such option,speak again')
                  spokeback = Svariable
                  break


class VoiceControl :
      def __init__(self):
         print("Does nothing")

      def voicecodeMain(self):
             variable = self.SpeakRecognize()
             #print(type(r))
             #print(variable)
             object = StringFromRecognizer(variable)
             if 'exit from voice mode' == variable:
                 print("inside 1 if")
                 sys.exit()
             elif 'exit voice mode' == variable:
                   print("inside 2 if")
                   sys.exit()
             elif 'symbol' in variable:
                   print("inside 3 if")
                   code = object.ToCode(variable)
                   return code
             elif 'tag open' or 'tag close' in variable:
                   print("inside 4 if")
                   htmlcode = object.ToHTMLcode(variable)
                   return htmlcode
             else:
                   justwrite = object.JustWrite(variable)
                   return justwrite

      def voiceOperationMain(self):
            variable = self.SpeakRecognize()
            object = StringFromRecognizer(variable)
            if variable is None:
               print("inside 1 if")
               self.Speak('Say option again')

            elif 'exit from voice mode' == variable:
                  print("inside 2 if")
                  sys.exit()

            elif 'exit voice mode' == variable:
                   print("inside 3 if")
                   sys.exit()
            else:
                string = object.ToOption(variable)
                print("inside 4 if")
                print("this tooption string "+string)
                return string

    #function to reccognize speech through google speech api
      def SpeakRecognize(self):
           #obtain audio from the microphone
           #def StartFromHere():
           r = sr.Recognizer()
           with sr.Microphone() as source:
               print("Say something!")
               audio = r.listen(source)

           # recognize speech using Google Speech Recognition
           try:
              # for testing purposes, we're just using the default API key
              # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
              # instead of `r.recognize_google(audio)`
               google_voice_recognize = r.recognize_google(audio)
               print("Google Speech Recognition thinks you said " + google_voice_recognize )
               return google_voice_recognize
           except sr.UnknownValueError:
               print("Google Speech Recognition could not understand audio")
           except sr.RequestError as e:
               print("Could not request results from Google Speech Recognition service; {0}".format(e))

#here happens text to speech
      def Speak(self,spoken):
           engine = pyttsx3.init()
           engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')
           engine.say(spoken)

           if spoken == 'You need to say yes or no only,speak now':
              engine.runAndWait()
           else:
              engine.runAndWait()
              said = self.SpeakRecognize()
              return said


#aytida----------------------------------------------




#the freaking main function bro
if __name__=='__main__'    :
    process = Popen(['py', 'starter.py'], stdout=PIPE, stderr=PIPE)
    time.sleep(3)
    app = QApplication(sys.argv)
    pal = QPalette()
    pal.setColor(QPalette.Highlight,Qt.yellow)
    pal.setColor(QPalette.HighlightedText,Qt.blue)
    app.setPalette(pal)
    #Aditya
    #start = Starter()
    #aditya
#creating the objecct of App class so we can start our stuff
    ex = App()
    sys.exit(app.exec_())
