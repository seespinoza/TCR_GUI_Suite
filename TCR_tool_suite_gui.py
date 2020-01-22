#!/usr/bin/env python3

import os
import re
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from PIL import Image as Imag
from PIL import ImageTk

from descriptions import Desc

DOCKER_CMD = 'docker run -it -v /home:/home seespinoza/memecos:latest /bin/bash -c '

# Global functions
def pop_up_msg(text_desc):

    def exit_out_of_focus(event):
        if event.widget == popup:
            popup.destroy()

    popup = Tk()
    popup.focus_force()
    Tk.wm_geometry(popup)
    popupFrame = Frame(popup, relief=GROOVE, bd=10)
    popupFrame.pack(fill=Y)

    popupLabelTitle = Label(popupFrame, text=text_desc[0], justify=LEFT, font=('OpenSymbol', 10, 'bold'))
    popupLabelTitle.pack()

    popupLabelDesc = Label(popupFrame, text=text_desc[1], justify=LEFT)
    popupLabelDesc.pack()

    popup.wm_attributes('-type', 'splash')
    popup.bind('<FocusOut>', exit_out_of_focus)
    popup.mainloop()


def pop_up_img(plot):

    popup = Toplevel()

    popup.wm_title('Circos Plot Preview')

    circosPlotImage = Label(popup, image=plot)
    circosPlotImage.pack(fill=BOTH)
    popup.mainloop()


def get_File_Name(updateLabelText):
    home = os.path.expanduser('~')
    filename = filedialog.askopenfilename(initialdir=home)
    if filename:
        updateLabelText.set(filename)


def num_only(input):
    try:
        if input is '' or int(input) >= 0:
            return True
    except ValueError:
        return False


def save_dir(OutputDir):
    home = os.path.expanduser('~')
    dirName = filedialog.askdirectory(initialdir=home)

    if dirName:
        os.system('cp ' + OutputDir + '* ' + dirName)


def set_up_loading_screen(self):

    clear_current_frame(self)

    self.loadingLabel = ttk.Label(self, text='Loading...')
    self.loadingLabel.grid(row=0, column=0, padx=225, pady=(200, 0))

    self.loadingBar = ttk.Progressbar(self, orient=HORIZONTAL, mode='determinate', length=300)
    self.loadingBar.grid(row=1, column=0, pady=0, padx=225, sticky='w')

    return self.loadingBar, self.loadingLabel


def clear_current_frame(self):
    for widget in self.winfo_children():
        widget.grid_forget()


def restore_current_frame(self):
    for widget in self.winfo_children():
        widget.grid(pady=2, padx=2, sticky='w')


def increase_loadbar(loadBar, increment=25):

    loadBar['value'] += increment
    loadBar.update_idletasks()


# Main GUI Class
class FUSE_GUI(Tk):

    def __init__(self, *args, **kwargs):

        # Initialize Root Window
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, 'MEMEcos')
        Tk.wm_geometry(self, '750x500')

        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        # Initialize all GUI frames
        for F in (StartPage, MEMEStart, CircosStart, TCR_Dist):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


        # Change window size depending on page shown
        if cont.__name__ == 'StartPage':
            Tk.wm_geometry(self, '750x500')
        elif cont.__name__ == 'CircosStart':
            Tk.wm_geometry(self, '750x415')


# GUI Splash page
class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = ttk.Label(self, text='FUSE GUI', font=('OpenSymbol', 10, 'bold'))
        label.pack(pady=0,padx=0)

        # Visit MEME button
        self.photoM = PhotoImage(file='MEME.png')
        MEMEButton = Button(self, text='Visit MEME', command=lambda: controller.show_frame(MEMEStart),
                            height=150, width=500, image=self.photoM)
        MEMEButton.pack()

        # Visit Circos button
        self.photoC = PhotoImage(file='CIRCOS.png')
        CIRCOSButton = Button(self, text='Visit Circos', command=lambda: controller.show_frame(CircosStart),
                              height=150, width=500, image=self.photoC)
        CIRCOSButton.pack()

        # Visit TCRDist button
        TCRDistButton = Button(self, text='Visit TCR-Dist', command=lambda: controller.show_frame(TCR_Dist),
                               height=150, width=500)
        TCRDistButton.pack()


# MEME main Page
class MEMEStart(Frame):

    def run_MEME(self, disMode, alpha, filePath, site, motifNo):

        loading_elements = set_up_loading_screen(self)

        increase_loadbar(loading_elements[0], 50)

        # Run MEME
        siteVar = site.get().split('(')[1][:-1]
        memeOutDir = os.getcwd() + '/temp_meme_out'

        memeCMD = '"./opt/meme/bin/meme -oc ' + memeOutDir + ' -objfun ' + disMode.get() + ' -' \
                  + alpha.get() + ' -mod ' + siteVar + ' -nmotifs ' + str(motifNo.get()) + ' ' + filePath.get() + '"'

        os.system(DOCKER_CMD + memeCMD)

        increase_loadbar(loading_elements[0], 50)

        loading_elements[0].destroy()
        loading_elements[1].destroy()

        # Restore current window
        restore_current_frame(self)


    def append_weights(self, filePath, weightList):

        weightString = '>WEIGHTS '

        with open(filePath, 'a') as f:

            # Add all weights to one string
            for weight in weightList:
                weightString += ' ' + str(weight)

            # Append weights to last line of FASTA file
            f.write(weightString)

    def increaseArrow(self, num):
        try:
            num.set(num.get() + 1)
        except TclError:
            pass

    def decreaseArrow(self, num):
        try:
            if num_only(num.get() - 1):
                num.set(num.get() -1)
        except TclError:
            pass

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)


        # Motif discovery label frame
        motifDiscovery = ttk.LabelFrame(self, text='Motif discovery mode')
        motifDiscovery.grid(row=1, column=0, padx=2, pady=2, sticky='w')

        # Motif discovery mode radio buttons and variable
        self.disModeVar = StringVar()
        self.disModeVar.set('classic')

        classicRadio = ttk.Radiobutton(motifDiscovery, text='Classic mode', var=self.disModeVar, val='classic')
        classicRadio.grid(row=2, column=1, pady=10, padx=2)

        discrimRadio = ttk.Radiobutton(motifDiscovery, text='Discriminative mode', var=self.disModeVar, val='dis')
        discrimRadio.grid(row=2, column=2, pady=10, padx=2)
        discrimRadio.configure(state=DISABLED)

        diffEnrichRadio = ttk.Radiobutton(motifDiscovery, text='Differential Enrichment mode',
                                          var=self.disModeVar, val='de')
        diffEnrichRadio.grid(row=2, column=3, pady=10, padx=2)
        diffEnrichRadio.configure(state=DISABLED)

        moreInfo = ttk.Button(motifDiscovery, text='?', command=lambda: pop_up_msg(Desc.classic()))
        moreInfo.grid(row=2, column=4)

        # Sequence alphabet label frame
        sequenceAlpha = ttk.LabelFrame(self, text='Sequence alphabet')
        sequenceAlpha.grid(row=2, column=0, padx=2, pady=2, sticky='w')

        self.alphaVar = StringVar()
        self.alphaVar.set('protein')

        # Sequence alphabet Radio Buttons
        proteinAlphaRadio = ttk.Radiobutton(sequenceAlpha, text='Protein', var=self.alphaVar, val='protein')
        proteinAlphaRadio.grid(row=2, column=1, pady=10, padx=2)

        dnaAlphaRadio = ttk.Radiobutton(sequenceAlpha, text='DNA', var=self.alphaVar, val='dna')
        dnaAlphaRadio.grid(row=2, column=2, pady=10, padx=2)

        rnaAlphaRadio = ttk.Radiobutton(sequenceAlpha, text='RNA', var=self.alphaVar, val='rna')
        rnaAlphaRadio.grid(row=2, column=3, pady=10, padx=2)

        CustomAlphaRadio = ttk.Radiobutton(sequenceAlpha, text='Custom...', var=self.alphaVar, val='alph')
        CustomAlphaRadio.grid(row=2, column=4, pady=10, padx=2)

        # Primary sequence label frame
        primarySequences = ttk.LabelFrame(self, text='Primary sequences')
        primarySequences.grid(row=3, column=0, pady=2, padx=2, sticky='w')

        # Primary sequence labels
        primarySeqLabel = ttk.Label(primarySequences, text='Enter sequences in which you want to find motifs.')
        primarySeqLabel.grid(row=1, column=0, pady=2, padx=2, sticky='w')

        self.filePathVar = StringVar()
        self.filePathVar.set('No file selected.')

        fileLabel = Label(primarySequences, textvariable=self.filePathVar, bg='gray')
        fileLabel.grid(row=2, column=0, pady=2, padx=2, sticky='w')

        primarySeqButtom = ttk.Button(primarySequences, text='Browse...',
                                      command=lambda: get_File_Name(self.filePathVar))
        primarySeqButtom.grid(row=2, column=2, pady=2, padx=2, sticky='e')

        # Site distribution label frame
        SiteDistribution = ttk.LabelFrame(self, text='Site distribution')
        SiteDistribution.grid(row=4, column=0, pady=2, padx=2, sticky='w')

        # Site distribution label
        siteDisLabel = Label(SiteDistribution, text='How do you expect motif sites to be distributed in sequences.')
        siteDisLabel.grid(row=0, column=0, pady=2, padx=2, sticky='w')

        # Site distribution optionMenu
        self.siteVar = StringVar()
        self.siteVar.set('Zero or One Occurrence Per Sequence (zoops)')

        self.siteLst = ['Zero or One Occurrence Per Sequence (zoops)',
                        'One Occurrence Per Sequence (oops)',
                        'Any Number of Repetitions (anr)']

        siteDisMenu = ttk.OptionMenu(SiteDistribution, self.siteVar, self.siteLst[0], *self.siteLst)
        siteDisMenu.grid(row=1, column=0, pady=2, padx=2, sticky='w')

        # Number of motifs label frame
        noMotifs = ttk.LabelFrame(self, text='Number of motifs')
        noMotifs.grid(row=5, column=0, pady=2, padx=2, sticky='w')

        # Number of motifs label
        noMotifsLabel = ttk.Label(noMotifs, text='How many motifs should MEME find?')
        noMotifsLabel.grid(row=0, column=0, padx=2, pady=2, sticky='w')

        # Number of motifs entry with up/down buttons
        self.noMotifVar = IntVar()
        self.noMotifVar.set(3)

        noMotifEntry = ttk.Entry(noMotifs, width=3, textvariable=self.noMotifVar)
        noMotifEntry.grid(row=1, column=0, pady=2, sticky='w')

        motifReg = self.register(num_only)
        noMotifEntry.config(validate='key', validatecommand=(motifReg, '%P'))

        noMotifButtonUp = Button(noMotifs, text='↑', width=1, height=1, repeatdelay=350, repeatinterval=25,
                                 command=lambda: self.increaseArrow(self.noMotifVar))
        noMotifButtonUp.grid(row=1, column=1, sticky='w')

        noMotifButtonDown = Button(noMotifs, text='↓', width=1, height=1, repeatdelay=350, repeatinterval=25,
                                   command=lambda: self.decreaseArrow(self.noMotifVar))
        noMotifButtonDown.grid(row=1, column=2, sticky='w')

        # Motif width Label Frame
        widthMotif = ttk.LabelFrame(self, text='Motif width')
        widthMotif.grid(row=6, column=0, padx=2, pady=2, sticky='w')

        # Motif width labels
        minWidthLabel = Label(widthMotif, text='Minimum width')
        minWidthLabel.grid(row=0, column=0, padx=2, pady=2)

        self.motifWidthVar = IntVar()
        self.motifWidthVar.set(8)

        motifWidthEntry = ttk.Entry(widthMotif, width=3, textvariable=self.motifWidthVar)
        motifWidthEntry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        motifWidthReg = self.register(num_only)
        motifWidthEntry.config(validate='key', validatecommand=(motifWidthReg, '%P'))

        # Run MEME Button
        runMeme = ttk.Button(self, text='Run MEME', command=lambda: self.run_MEME(self.disModeVar, self.alphaVar,
                                                                                  self.filePathVar, self.siteVar,
                                                                                  self.noMotifVar))
        runMeme.grid(row=1000, column=0, pady=20, sticky='w')

        # Back home button at bottom of page
        backHomeMEME = ttk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        backHomeMEME.grid(row=1000, column=1, pady=20)

class CircosStart(Frame):
    def save_circos_plot(self, initialFileName):
        outputDir = '/memecos/circos_output/img/'
        home = os.path.expanduser('~')
        files = [('PNG Files', '*.png'), ('SVG Files', '*.svg')]


        dirName = filedialog.asksaveasfile(initialdir=home, filetypes=files, initialfile=initialFileName)

        if dirName.name[-3:] == 'svg':
            os.system('cp ' + outputDir + '*.svg ' + dirName.name)
        elif dirName.name[-3:] == 'png':
            os.system('cp ' + outputDir + '*.png ' + dirName.name)

    def run_Circos(self):

        # No TSV file selected to plot
        if self.cirFilePathVar.get() == 'No file selected.':
            self.runStatusLabel.config(bg='red')
            self.circosStatus.set('Please select a file first.')


        # Else if a TSV file is selected edit conf files and run Circos
        else:

            # Create Progress bar and label
            loading_elements = set_up_loading_screen(self)

            increase_loadbar(loading_elements[0])

            # Clear out any error message
            self.circosStatus.set('')
            self.runStatusLabel.config(bg='#d9d9d9')

            os.system(DOCKER_CMD + '"python3 /memecos/circos.py -i ' + self.cirFilePathVar.get() +
                      ' -s ' + str(self.labelSize.get()) + ' -o ' + self.labelOri.get() + ' -t ' +
                      str(self.ideoThickness.get()) + ' -l ' + str(self.labelPosition.get()) +
                      ' -i ' + str(self.linkSize.get()) + ' -c ' + os.getcwd() + '"')

            print(DOCKER_CMD + '"python3 /memecos/circos.py -i ' + self.cirFilePathVar.get() +
                      ' -s ' + str(self.labelSize.get()) + ' -o ' + self.labelOri.get() + ' -t ' +
                      str(self.ideoThickness.get()) + ' -l ' + str(self.labelPosition.get()) +
                      ' -i ' + str(self.linkSize.get()) + ' -c ' + os.getcwd() + '"')

            increase_loadbar(loading_elements[0])

            # Destroy the loading screen frame after the process has finished
            loading_elements[1].destroy()
            loading_elements[0].destroy()

            # Repopulate current window
            restore_current_frame(self)

            try:
                circosPlotDir = os.getcwd() + '/temp_circos_out/tableview.png'

                self.circosPlot = ImageTk.PhotoImage(Imag.open(circosPlotDir).resize((1100, 1100),Imag.ANTIALIAS))

                plotPreviewButton = Button(self.circosPlotFiles, text='Preview Circos Plot in New Window',
                                              command=lambda: pop_up_img(self.circosPlot))

                plotPreviewButton.grid(row=0, column=0, pady=2, padx=2, sticky='w')

                plotSaveButton = Button(self.circosPlotFiles, text='Save File',
                                        command=lambda: self.save_circos_plot(self, circosPlotDir),
                                        bg='medium sea green')
                plotSaveButton.grid(row=1, column=0, pady=2, padx=2, sticky='w')

            except FileNotFoundError:
                print('error')
                pass

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Circos Default label frame
        circosFileSelect = ttk.LabelFrame(self, text='File to be plotted')
        circosFileSelect.grid(row=0, column=0, pady=2, padx=2, sticky='w')

        circosFileLabel = ttk.Label(circosFileSelect, text='Choose the .tsv file you want to plot.')
        circosFileLabel.grid(row=0, column=0, padx=2, pady=2, sticky='w')

        self.cirFilePathVar = StringVar()
        self.cirFilePathVar.set('No file selected.')

        circosFileLabelStatus = Label(circosFileSelect, textvariable=self.cirFilePathVar, bg='gray')
        circosFileLabelStatus.grid(row=1, column=0, padx=2, pady=2, sticky='w')

        circosFileButton = ttk.Button(circosFileSelect, text='Browse...',
                                      command=lambda: get_File_Name(self.cirFilePathVar))

        circosFileButton.grid(row=1, column=1, pady=2, padx=2, sticky='e')

        # Advanced settings label frame
        advancedCircosSettings = ttk.LabelFrame(self, text='Advanced Settings')
        advancedCircosSettings.grid(row=1, column=0, pady=2, padx=2, sticky='w')

        # Label size
        self.labelSize = IntVar()
        self.labelSize.set(20)

        labelSizeLable = ttk.Label(advancedCircosSettings, text='Enter label font size: ')
        labelSizeLable.grid(row=0, column=0, pady=2, padx=2, sticky='w')

        labelSizeEntry = ttk.Entry(advancedCircosSettings, width=3, textvariable=self.labelSize)
        labelSizeEntry.grid(row=0, column=1, pady=2, padx=10, sticky='w')

        sizeReg = self.register(num_only)
        labelSizeEntry.config(validate='key', validatecommand=(sizeReg, '%P'))

        # Label Orientation
        self.labelOri = StringVar()
        self.labelOri.set('no')

        labelOrientationLabel = ttk.Label(advancedCircosSettings, text='Choose label orientation: ')
        labelOrientationLabel.grid(row=1, column=0, pady=2, padx=2, sticky='w')

        radioParallel = ttk.Radiobutton(advancedCircosSettings, text='Parallel', var=self.labelOri, val='yes')
        radioParallel.grid(row=1, column=1, pady=2, padx=2, sticky='w')

        radioNonParallel = ttk.Radiobutton(advancedCircosSettings, text='Not parallel', var=self.labelOri, val='no')
        radioNonParallel.grid(row=1, column=2, pady=2, padx=2, sticky='e')

        # Label thickness
        self.ideoThickness = IntVar()
        self.ideoThickness.set(25)

        labelIdeogramThickness = ttk.Label(advancedCircosSettings, text='Enter ideogram thickness: ')
        labelIdeogramThickness.grid(row=2, column=0, pady=2, padx=2, sticky='w')

        entryIdeogramThickness = ttk.Entry(advancedCircosSettings, width=3, textvariable=self.ideoThickness)
        entryIdeogramThickness.grid(row=2, column=1, pady=2, padx=2, sticky='w')

        ideoThicknessReg = self.register(num_only)
        entryIdeogramThickness.config(validate='key', validatecommand=(ideoThicknessReg, '%P'))

        # Label Position
        self.labelPosition = IntVar()
        self.labelPosition.set(10)

        labelPositionLabel = ttk.Label(advancedCircosSettings, text='Enter the label position: ')
        labelPositionLabel.grid(row=3, column=0, pady=2, padx=2, sticky='w')

        entryPositionLabel = ttk.Entry(advancedCircosSettings, width=5, textvariable=self.labelPosition)
        entryPositionLabel.grid(row=3, column=1, pady=2, padx=2, sticky='w')

        labelPositionReg = self.register(num_only)
        entryPositionLabel.config(validate='key', validatecommand=(labelPositionReg, '%P'))

        # Minimum link size filter
        self.linkSize = IntVar()
        self.linkSize.set(0)
        labelLinkSize = ttk.Label(advancedCircosSettings, text='Enter minimum link size: ')
        labelLinkSize.grid(row=4, column=0, pady=2, padx=2, sticky='w')

        entryLinkSize = ttk.Entry(advancedCircosSettings, width=5, textvariable=self.linkSize)
        entryLinkSize.grid(row=4, column=1, pady=2, padx=2, sticky='w')

        linkSizeReg = self.register(num_only)
        entryLinkSize.config(validate='key', validatecommand=(linkSizeReg, '%P'))

        # Run Circos button
        self.circosStatus = StringVar()

        self.runStatusLabel = Label(self, textvariable=self.circosStatus)
        self.runStatusLabel.grid(row=3, column=1, pady=2, padx=10)

        # Circos Plot Files label frame
        self.circosPlotFiles = ttk.LabelFrame(self, text='Circos Plot Files')
        self.circosPlotFiles.grid(row=3, column=0, pady=2, padx=2, sticky='w')

        runCircos = ttk.Button(self, text='Run Circos', command=lambda: self.run_Circos())

        runCircos.grid(row=2, column=0, pady=2, padx=2, sticky='w')

        backHomeCircos = ttk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        backHomeCircos.grid(row=4, column=0, pady=2, padx=2, sticky='w')

class TCR_Dist(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        pairSeqLabelFrame = ttk.LabelFrame(self, text='Choose a pair sequences file')
        pairSeqLabelFrame.grid(row=0, column=0, pady=2, padx=2)

        self.pairSeqPathVar = StringVar()
        self.pairSeqPathVar.set('No file selected.')

        circosFileLabelStatus = Label(pairSeqLabelFrame, textvariable=self.pairSeqPathVar, bg='gray')
        circosFileLabelStatus.grid(row=0, column=0, padx=2, pady=2, sticky='w')

        pairSeqFileButton = ttk.Button(pairSeqLabelFrame, text='Browse...',
                                       command=lambda: get_File_Name(self.pairSeqPathVar))
        pairSeqFileButton.grid(row=0, column=1, pady=2, padx=2, sticky='e')

        self.pairSeqAmount = IntVar()
        self.pairSeqAmount.set(100)
        pairSeqScale = Scale(pairSeqLabelFrame, label='Select amount of sequence to analyze',
                             variable=self.pairSeqAmount, sliderlength=20, orient=HORIZONTAL,
                             to=1000, length=300, repeatinterval=10, repeatdelay=10, resolution=100)
        pairSeqScale.grid(column=0, row=1, pady=2)

        backHomeTCR = ttk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        backHomeTCR.grid(row=1000, column=0, pady=2)

# Main program
if __name__ == '__main__':
    app = FUSE_GUI()
    app.mainloop()
