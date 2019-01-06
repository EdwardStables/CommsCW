from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import math
import cmath
import numpy as np 
import pandas as pd
import os

class guiLayout:
    diagramState = 1
    def __init__(self, master):
        self.master = master

        #----------Window Options----------
        self.master.title("QPSK Communication System")
        windowWidth = 1000
        windowHeight = 800
        self.master.geometry('{}x{}'.format(windowWidth, windowHeight))
        self.master.resizable(width=False, height=False)
        #----------Create Frames----------
        #Top Level
        self.diagramFrame = Frame(self.master, width = 600, height = 600)
        self.blockFrame = Frame(self.master, width = 400, height = 600, bg = "red")
        self.descriptionFrame = Frame(self.master, width = 600, height = 200)
        self.outputFrame = Frame(self.master, width = 400, height = 200)
        #(0,0): diagramFrame
        self.systemFrame = Frame(self.diagramFrame, width = 600, height = 550)
        self.taskFrame = Frame(self.diagramFrame, width = 600, height = 50)
        #(0,1): blockFrame:
        #(1,0): descriptionFrame
        #(1,1): outputFrame
        #----------Position Frames & Separators----------
        self.diagramFrame.grid(column = 0, row = 0, sticky = "nsew")
        self.blockFrame.grid(column = 2, row = 0, sticky = "nsew")
        self.descriptionFrame.grid(column = 0, row = 2, sticky = "nsew")
        self.outputFrame.grid(column = 2, row = 2, sticky = "nsew")
        #(0,0): diagramFrame
        self.taskFrame.grid(column = 0, row = 2, sticky = "ew")
        #(0,1): blockFrame:
        #(1,0): descriptionFrame
        #(1,1): outputFrame
        #----------Configure----------
        self.blockFrame.columnconfigure(0, weight = 2)
        self.blockFrame.rowconfigure(0, weight = 1)
        self.blockFrame.rowconfigure(1, weight = 1)
        self.blockFrame.rowconfigure(2, weight = 1)

        self.taskFrame.columnconfigure(0, weight = 1)
        self.taskFrame.columnconfigure(1, weight = 1)
        self.taskFrame.columnconfigure(2, weight = 1)
        self.taskFrame.columnconfigure(3, weight = 1)
        self.taskFrame.columnconfigure(4, weight = 1)
        self.taskFrame.columnconfigure(5, weight = 1)
        self.taskFrame.columnconfigure(6, weight = 1)
        #----------Separators----------
        self.blockFrameSeparator = ttk.Separator(self.blockFrame, orient = HORIZONTAL)
        self.blockFrameSeparator.grid(row = 1, column = 0, sticky = "ew")

        self.verticalSeparator = ttk.Separator(self.master, orient = VERTICAL)
        self.verticalSeparator.grid(row = 0, column = 1, rowspan = 3, sticky = "ns")
        self.horizontalSeparator = ttk.Separator(self.master, orient = HORIZONTAL)
        self.horizontalSeparator.grid(row = 1, column = 0, columnspan = 3, sticky = "ew")

        self.taskSeparator = ttk.Separator(self.diagramFrame, orient = HORIZONTAL)
        self.taskSeparator.grid(column = 0, row = 1, columnspan = 7, sticky = "ew")
        #----------Create Buttons----------
        self.task1Button = Button(self.taskFrame, text = "Task 1", command = self.task1Function)
        self.task2Button = Button(self.taskFrame, text = "Task 2", command = self.task2Function)
        self.task3Button = Button(self.taskFrame, text = "Task 3", command = self.task3Function)
        self.task4Button = Button(self.taskFrame, text = "Task 4", command = self.task4Function)
        self.task5Button = Button(self.taskFrame, text = "Task 5", command = self.task5Function)
        self.task6Button = Button(self.taskFrame, text = "Task 6", command = self.task6Function)
        self.task7Button = Button(self.taskFrame, text = "Task 7", command = self.task7Function)
        self.buttonList = [self.task1Button, self.task2Button, self.task3Button, self.task4Button, self.task5Button, self.task6Button, self.task7Button]
        #----------Position Buttons----------
        self.task1Button.grid(column = 0, row = 1, padx = 5, pady = 5, sticky = "ew")
        self.task2Button.grid(column = 1, row = 1, padx = 5, pady = 5, sticky = "ew")
        self.task3Button.grid(column = 2, row = 1, padx = 5, pady = 5, sticky = "ew")
        self.task4Button.grid(column = 3, row = 1, padx = 5, pady = 5, sticky = "ew")
        self.task5Button.grid(column = 4, row = 1, padx = 5, pady = 5, sticky = "ew")
        self.task6Button.grid(column = 5, row = 1, padx = 5, pady = 5, sticky = "ew")
        self.task7Button.grid(column = 6, row = 1, padx = 5, pady = 5, sticky = "ew")
        #----------Block Code Box----------
        self.code = Label(self.blockFrame, text = "Select a block to see the corresponding code", wrap = 400, justify = LEFT)
        self.code.grid(column = 0, row = 0, sticky = "nsew")
        #----------Block Description Box----------
        self.description = Label(self.blockFrame, text = "Select a module to see its description", wrap = 400, justify = LEFT)
        self.description.grid(column = 0, row = 2, sticky = "nsew")
        #----------Diagram Canvas----------
        self.diagramCanvas = Canvas(self.diagramFrame, height = 550, width = 600)
        self.diagramCanvas = self.diagram(self.diagramCanvas)
        self.diagramCanvas.grid(column = 0, row = 0)
        #----------Task Descriptions----------
        self.taskDescriptionLabel = Label(self.descriptionFrame, wrap = 600, justify = LEFT)
        self.tasks = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "\\taskDescriptions.csv")
        pd.set_option('display.max_colwidth', -1)
        self.taskDescriptionLabel.pack(side = TOP, expand = False, fill = 'y')
        #----------Graph----------
        #fig = Figure(figsize=(5,5), dpi = 100)
        #canvas = FigureCanvasTkAgg(fig, self)
        #canvas.show()
        #canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

        #----------Setup----------
        self.task1Function()
        #self.initialMessage = messagebox.showinfo("App Usage" , "Use the task buttons to view the description of each task, as well as the output information (constellation diagram, BER etc.). \n\nEach time the task button is pressed, a simulation is run, leading to different output values. \n\nSelect each block in the system diagram to see a description of the function it provides.")


    #System Blocks
    def sourceClicked(self, event):
        text = "The source is a string of text in unicode format (Python default). The text is a semi-random latin passage."
        self.description.config(text = text)
    def encoderClicked(self, event):
        text = "The text input is interpreted as a UTF-8 formatted string (applicable for normal text), which is converted into an array of 300 8-bit symbols. As the conversion automatically truncates any 0s beyond the largest 1, all bytes are formatted as strings, have the leading '0b' removed and are zero-extended to ensure all entries are 8-bits long"
        self.description.config(text = text)
    def digitalModulatorClicked(self, event):
        code = """
            def digitalModulator(self, inp, phi=cmath.pi/4):
                output = []
                symbols = {
                    "00":cmath.rect(math.sqrt(2), phi),
                    "01":cmath.rect(math.sqrt(2), phi + cmath.pi/2),
                    "11":cmath.rect(math.sqrt(2), phi + cmath.pi),
                    "10":cmath.rect(math.sqrt(2), phi + 3*cmath.pi/2)
                }
                for i in inp:
                    output.append(symbols[i[0:2]])
                    output.append(symbols[i[2:4]])
                    output.append(symbols[i[4:6]])
                    output.append(symbols[i[6:8]])
                return output
        """
        text = "Each of the 8-bit characters is split into 4 2-bit symbols, each of these is mapped to one of the defined symbols and outputs 1200 symbols (for the 300 character input)"
        self.description.config(text = text)
        self.code.config(text = code)
    def spreaderClicked(self, event):
        text = "The gold code is applied to the signal with an assumption of Tcs=Tc. Therefore the length 31 gold code is repeated multiple times along the whole length of the length 1200 message."
        self.description.config(text = text)
    def attenuatorClicked(self, event):
        text = "attenuation, to be removed"
        self.description.config(text = text)
    def channelNoiseClicked(self, event):
        text = "The noise is simulated by measuring the power of the signal, followed by calculating the relative power of the noise from the "
        self.description.config(text = text)
    def channelJammerClicked(self, event):
        print("channel jammer")
    def despreaderClicked(self, event):
        print("despreader")
    def digitalDemodulatorClicked(self, event):
        print("digitaldemodulator")
    def sourceDecoderClicked(self, event):
        print("source decoder")
    def sinkClicked(self, event):
        print("sink")

    #Task Buttons
    def task1Function(self):
        self.diagramCanvas.delete("all")
        self.diagramCanvas = self.diagram(self.diagramCanvas)
        self.diagramCanvas.grid(column = 0, row = 0)
        self.makeButtonBold(self.task1Button)
        self.taskDescriptionLabel.config(text = str(self.tasks['Descriptions'].iloc[0]))
        task1 = QPSK()
        task1.run()
        self.setPlot(task1.symbols)

    def task2Function(self):
        self.diagramCanvas.delete("all")
        self.diagramCanvas = self.diagramNoise(self.diagramCanvas)
        self.diagramCanvas.grid(column = 0, row = 0)
        self.makeButtonBold(self.task2Button)
        self.taskDescriptionLabel.config(text = str(self.tasks['Descriptions'].iloc[1]))
    def task3Function(self):
        self.diagramCanvas.delete("all")
        self.diagramCanvas = self.diagramNoise(self.diagramCanvas)
        self.diagramCanvas.grid(column = 0, row = 0)
        self.makeButtonBold(self.task3Button)
        self.taskDescriptionLabel.config(text = str(self.tasks['Descriptions'].iloc[2]))
    def task4Function(self):
        self.diagramCanvas.delete("all")
        self.diagramCanvas = self.diagramNoise(self.diagramCanvas)
        self.diagramCanvas.grid(column = 0, row = 0)
        self.makeButtonBold(self.task4Button)
        self.taskDescriptionLabel.config(text = str(self.tasks['Descriptions'].iloc[3]))
    def task5Function(self):
        self.diagramCanvas.delete("all")
        self.diagramCanvas = self.diagramNoise(self.diagramCanvas)
        self.diagramCanvas.grid(column = 0, row = 0)
        self.makeButtonBold(self.task5Button)
        self.taskDescriptionLabel.config(text = str(self.tasks['Descriptions'].iloc[4]))
    def task6Function(self):
        self.diagramCanvas.delete("all")
        self.diagramCanvas = self.diagramJammerNoise(self.diagramCanvas)
        self.diagramCanvas.grid(column = 0, row = 0)
        self.makeButtonBold(self.task6Button)
        self.taskDescriptionLabel.config(text = str(self.tasks['Descriptions'].iloc[5]))
    def task7Function(self):
        self.diagramCanvas.delete("all")
        self.diagramCanvas = self.diagramSpreadJammerNoise(self.diagramCanvas)
        self.diagramCanvas.grid(column = 0, row = 0)
        self.makeButtonBold(self.task7Button)
        self.taskDescriptionLabel.config(text = str(self.tasks['Descriptions'].iloc[6]))
    
    #Utility Functions
    def makeButtonBold(self, buttonBold):
        normalFont = font.Font(family='Helvetica', size=12, weight = "normal")
        boldFont = font.Font(family='Helvetica', size=12, weight = "bold")
        for button in self.buttonList:
            button.config(font = normalFont)
        buttonBold.config(font = boldFont)
    
    def setPlot(self, symbols):
        fig = Figure(figsize=(2,2), dpi = 100)
        plot = fig.add_subplot(111)
        plot.plot(symbols[0], symbols[1])

        graphCanvas = FigureCanvasTkAgg(fig, master = self.outputFrame)
        graphCanvas.draw()
        graphCanvas.get_tk_widget().grid(column = 0, row = 0)
        testlab = Label(self.outputFrame, text = "hellow there ")
        testlab.grid(column = 1, row = 0)

    #Canvas Functions
    def diagramSpreadJammerNoise(self, system):
        self.system = system
        #Tx Blocks
        self.source = self.system.create_rectangle(20, 30, 100, 80, fill = "green")
        self.sourceLabel = self.system.create_text(60, 55, text = "Source", state = DISABLED)
        self.encoder = self.system.create_rectangle(140, 30, 220, 80, fill = "green")
        self.encoderLabel = self.system.create_text(180, 55, text = "Encoder", state = DISABLED)
        self.digitalModulator = self.system.create_rectangle(260, 30, 340, 80, fill = "green")
        self.digitalModulatorLabel_1 = self.system.create_text(300, 45, text = "Digital", state = DISABLED)
        self.digitalModulatorLabel_2 = self.system.create_text(300, 65, text = "Modulator", state = DISABLED)
        self.spreader = self.system.create_rectangle(380, 30, 460, 80, fill = "green")
        self.spreaderLabel = self.system.create_text(420, 55, text = "Spreader", state = DISABLED)
        #Channel Blocks
        self.channelNoise = self.system.create_rectangle(480, 185, 560, 235, fill = "green")
        self.channelNoiseLabel_1 = self.system.create_text(520, 200, text = "Channel", state = DISABLED)
        self.channelNoiseLabel_2 = self.system.create_text(520, 220, text = "Noise", state = DISABLED)
        self.channelJammer = self.system.create_rectangle(480, 315, 560, 365, fill = "green")
        self.channelJammerLabel_1 = self.system.create_text(520, 330, text = "Channel", state = DISABLED)
        self.channelJammerLabel_2 = self.system.create_text(520, 350, text = "Jammer", state = DISABLED)
         #Rx Blocks
        self.despreader = self.system.create_rectangle(380, 470, 460, 520, fill = "green")
        self.despreaderLabel = self.system.create_text(420, 495, text = "Despreader", state = DISABLED)
        self.digitalDemodulator = self.system.create_rectangle(260, 470, 340, 520, fill = "green")
        self.digitalDemodulatorLabel_1 = self.system.create_text(300, 485, text = "Digital", state = DISABLED)
        self.digitalDemodulatorLabel_2 = self.system.create_text(300, 505, text = "Demodulator", state = DISABLED)
        self.sourceDecoder = self.system.create_rectangle(140, 470, 220, 520, fill = "green")
        self.sourceDecoderLabel_1 = self.system.create_text(180, 485, text = "Source", state = DISABLED)
        self.sourceDecoderLabel_2 = self.system.create_text(180, 505, text = "Decoder", state = DISABLED)
        self.sink = self.system.create_rectangle(20, 470, 100, 520, fill = "green")
        self.sinkLabel = self.system.create_text(60, 495, text = "Sink", state = DISABLED)

        #Channel Marker
        self.channelMarker = self.system.create_rectangle(460, 110, 580, 440, dash = True)
        self.channelText = self.system.create_text(450, 275, text = "CHANNEL", angle = 90)

        #Arrows
        self.arrow1 = self.system.create_line(100, 55, 140, 55, arrow=LAST)
        self.arrow2 = self.system.create_line(220, 55, 260, 55, arrow=LAST)
        self.arrow3 = self.system.create_line(340, 55, 380, 55, arrow=LAST)
        self.arrow4 = self.system.create_line(460, 55, 520, 55)
        self.arrow5 = self.system.create_line(520, 55, 520, 185, arrow=LAST)
        self.arrow5 = self.system.create_line(520, 235, 520, 315, arrow=LAST)
        self.arrow5 = self.system.create_line(520, 365, 520, 495)
        self.arrow5 = self.system.create_line(520, 495, 460, 495, arrow=LAST)
        self.arrow5 = self.system.create_line(380, 495, 340, 495, arrow=LAST)
        self.arrow5 = self.system.create_line(260, 495, 220, 495, arrow=LAST)
        self.arrow5 = self.system.create_line(140, 495, 100, 495, arrow=LAST)

        #Clicking
        self.system.tag_bind(self.source, '<Button-1>', self.sourceClicked)
        self.system.tag_bind(self.encoder, '<Button-1>', self.encoderClicked)
        self.system.tag_bind(self.digitalModulator, '<Button-1>', self.digitalModulatorClicked)
        self.system.tag_bind(self.spreader, '<Button-1>', self.spreaderClicked)
        self.system.tag_bind(self.channelNoise, '<Button-1>', self.channelNoiseClicked)
        self.system.tag_bind(self.channelJammer, '<Button-1>', self.channelJammerClicked)
        self.system.tag_bind(self.despreader, '<Button-1>', self.despreaderClicked)
        self.system.tag_bind(self.digitalDemodulator, '<Button-1>', self.digitalDemodulatorClicked)
        self.system.tag_bind(self.sourceDecoder, '<Button-1>', self.sourceDecoderClicked)
        self.system.tag_bind(self.sink, '<Button-1>', self.sinkClicked)
        return self.system
    def diagramJammerNoise(self, system):
        self.system = system

        #Tx Blocks
        self.source = self.system.create_rectangle(20, 30, 100, 80, fill = "green")
        self.sourceLabel = self.system.create_text(60, 55, text = "Source", state = DISABLED)
        self.encoder = self.system.create_rectangle(140, 30, 220, 80, fill = "green")
        self.encoderLabel = self.system.create_text(180, 55, text = "Encoder", state = DISABLED)
        self.digitalModulator = self.system.create_rectangle(260, 30, 340, 80, fill = "green")
        self.digitalModulatorLabel_1 = self.system.create_text(300, 45, text = "Digital", state = DISABLED)
        self.digitalModulatorLabel_2 = self.system.create_text(300, 65, text = "Modulator", state = DISABLED)
        #Channel Blocks
        self.channelNoise = self.system.create_rectangle(480, 185, 560, 235, fill = "green")
        self.channelNoiseLabel_1 = self.system.create_text(520, 200, text = "Channel", state = DISABLED)
        self.channelNoiseLabel_2 = self.system.create_text(520, 220, text = "Noise", state = DISABLED)
        self.channelJammer = self.system.create_rectangle(480, 315, 560, 365, fill = "green")
        self.channelJammerLabel_1 = self.system.create_text(520, 330, text = "Channel", state = DISABLED)
        self.channelJammerLabel_2 = self.system.create_text(520, 350, text = "Jammer", state = DISABLED)
        #Rx Blocks
        self.digitalDemodulator = self.system.create_rectangle(260, 470, 340, 520, fill = "green")
        self.digitalDemodulatorLabel_1 = self.system.create_text(300, 485, text = "Digital", state = DISABLED)
        self.digitalDemodulatorLabel_2 = self.system.create_text(300, 505, text = "Demodulator", state = DISABLED)
        self.sourceDecoder = self.system.create_rectangle(140, 470, 220, 520, fill = "green")
        self.sourceDecoderLabel_1 = self.system.create_text(180, 485, text = "Source", state = DISABLED)
        self.sourceDecoderLabel_2 = self.system.create_text(180, 505, text = "Decoder", state = DISABLED)
        self.sink = self.system.create_rectangle(20, 470, 100, 520, fill = "green")
        self.sinkLabel = self.system.create_text(60, 495, text = "Sink", state = DISABLED)

        #Channel Marker
        self.channelMarker = self.system.create_rectangle(460, 110, 580, 440, dash = True)
        self.channelText = self.system.create_text(450, 275, text = "CHANNEL", angle = 90)

        #Arrows
        self.arrow1 = self.system.create_line(100, 55, 140, 55, arrow=LAST)
        self.arrow2 = self.system.create_line(220, 55, 260, 55, arrow=LAST)
        self.arrow4 = self.system.create_line(340, 55, 520, 55)
        self.arrow5 = self.system.create_line(520, 55, 520, 185, arrow=LAST)
        self.arrow5 = self.system.create_line(520, 235, 520, 315, arrow=LAST)
        self.arrow5 = self.system.create_line(520, 365, 520, 495)
        self.arrow5 = self.system.create_line(520, 495, 340, 495, arrow=LAST)
        self.arrow5 = self.system.create_line(260, 495, 220, 495, arrow=LAST)
        self.arrow5 = self.system.create_line(140, 495, 100, 495, arrow=LAST)

        #Clicking
        self.system.tag_bind(self.source, '<Button-1>', self.sourceClicked)
        self.system.tag_bind(self.encoder, '<Button-1>', self.encoderClicked)
        self.system.tag_bind(self.digitalModulator, '<Button-1>', self.digitalModulatorClicked)
        self.system.tag_bind(self.channelNoise, '<Button-1>', self.channelNoiseClicked)
        self.system.tag_bind(self.channelJammer, '<Button-1>', self.channelJammerClicked)
        self.system.tag_bind(self.digitalDemodulator, '<Button-1>', self.digitalDemodulatorClicked)
        self.system.tag_bind(self.sourceDecoder, '<Button-1>', self.sourceDecoderClicked)
        self.system.tag_bind(self.sink, '<Button-1>', self.sinkClicked)
        return self.system
    def diagramNoise(self, system):
        self.system = system

        #Tx Blocks
        self.source = self.system.create_rectangle(20, 30, 100, 80, fill = "green")
        self.sourceLabel = self.system.create_text(60, 55, text = "Source", state = DISABLED)
        self.encoder = self.system.create_rectangle(140, 30, 220, 80, fill = "green")
        self.encoderLabel = self.system.create_text(180, 55, text = "Encoder", state = DISABLED)
        self.digitalModulator = self.system.create_rectangle(260, 30, 340, 80, fill = "green")
        self.digitalModulatorLabel_1 = self.system.create_text(300, 45, text = "Digital", state = DISABLED)
        self.digitalModulatorLabel_2 = self.system.create_text(300, 65, text = "Modulator", state = DISABLED)
        #Channel Blocks
        self.channelNoise = self.system.create_rectangle(480, 185, 560, 235, fill = "green")
        self.channelNoiseLabel_1 = self.system.create_text(520, 200, text = "Channel", state = DISABLED)
        self.channelNoiseLabel_2 = self.system.create_text(520, 220, text = "Noise", state = DISABLED)
         #Rx Blocks
        self.digitalDemodulator = self.system.create_rectangle(260, 470, 340, 520, fill = "green")
        self.digitalDemodulatorLabel_1 = self.system.create_text(300, 485, text = "Digital", state = DISABLED)
        self.digitalDemodulatorLabel_2 = self.system.create_text(300, 505, text = "Demodulator", state = DISABLED)
        self.sourceDecoder = self.system.create_rectangle(140, 470, 220, 520, fill = "green")
        self.sourceDecoderLabel_1 = self.system.create_text(180, 485, text = "Source", state = DISABLED)
        self.sourceDecoderLabel_2 = self.system.create_text(180, 505, text = "Decoder", state = DISABLED)
        self.sink = self.system.create_rectangle(20, 470, 100, 520, fill = "green")
        self.sinkLabel = self.system.create_text(60, 495, text = "Sink", state = DISABLED)

        #Channel Marker
        self.channelMarker = self.system.create_rectangle(460, 110, 580, 440, dash = True)
        self.channelText = self.system.create_text(450, 275, text = "CHANNEL", angle = 90)

        #Arrows
        self.arrow1 = self.system.create_line(100, 55, 140, 55, arrow=LAST)
        self.arrow2 = self.system.create_line(220, 55, 260, 55, arrow=LAST)
        self.arrow4 = self.system.create_line(340, 55, 520, 55)
        self.arrow5 = self.system.create_line(520, 55, 520, 185, arrow=LAST)
        self.arrow5 = self.system.create_line(520, 235, 520, 495)
        self.arrow5 = self.system.create_line(520, 495, 340, 495, arrow=LAST)
        self.arrow5 = self.system.create_line(260, 495, 220, 495, arrow=LAST)
        self.arrow5 = self.system.create_line(140, 495, 100, 495, arrow=LAST)

        #Clicking
        self.system.tag_bind(self.source, '<Button-1>', self.sourceClicked)
        self.system.tag_bind(self.encoder, '<Button-1>', self.encoderClicked)
        self.system.tag_bind(self.digitalModulator, '<Button-1>', self.digitalModulatorClicked)
        self.system.tag_bind(self.channelNoise, '<Button-1>', self.channelNoiseClicked)
        self.system.tag_bind(self.digitalDemodulator, '<Button-1>', self.digitalDemodulatorClicked)
        self.system.tag_bind(self.sourceDecoder, '<Button-1>', self.sourceDecoderClicked)
        self.system.tag_bind(self.sink, '<Button-1>', self.sinkClicked)
        return self.system
    def diagram(self, system):
        self.system = system

        #Tx Blocks
        self.source = self.system.create_rectangle(20, 30, 100, 80, fill = "green")
        self.sourceLabel = self.system.create_text(60, 55, text = "Source", state = DISABLED)
        self.encoder = self.system.create_rectangle(140, 30, 220, 80, fill = "green")
        self.encoderLabel = self.system.create_text(180, 55, text = "Encoder", state = DISABLED)
        self.digitalModulator = self.system.create_rectangle(260, 30, 340, 80, fill = "green")
        self.digitalModulatorLabel_1 = self.system.create_text(300, 45, text = "Digital", state = DISABLED)
        self.digitalModulatorLabel_2 = self.system.create_text(300, 65, text = "Modulator", state = DISABLED)
        #Channel Blocks
        
        #Rx Blocks
        self.digitalDemodulator = self.system.create_rectangle(260, 470, 340, 520, fill = "green")
        self.digitalDemodulatorLabel_1 = self.system.create_text(300, 485, text = "Digital", state = DISABLED)
        self.digitalDemodulatorLabel_2 = self.system.create_text(300, 505, text = "Demodulator", state = DISABLED)
        self.sourceDecoder = self.system.create_rectangle(140, 470, 220, 520, fill = "green")
        self.sourceDecoderLabel_1 = self.system.create_text(180, 485, text = "Source", state = DISABLED)
        self.sourceDecoderLabel_2 = self.system.create_text(180, 505, text = "Decoder", state = DISABLED)
        self.sink = self.system.create_rectangle(20, 470, 100, 520, fill = "green")
        self.sinkLabel = self.system.create_text(60, 495, text = "Sink", state = DISABLED)

        #Channel Marker
        self.channelMarker = self.system.create_rectangle(460, 110, 580, 440, dash = True)
        self.channelText = self.system.create_text(450, 275, text = "CHANNEL", angle = 90)

        #Arrows
        self.arrow1 = self.system.create_line(100, 55, 140, 55, arrow=LAST)
        self.arrow2 = self.system.create_line(220, 55, 260, 55, arrow=LAST)
        self.arrow4 = self.system.create_line(340, 55, 520, 55)
        self.arrow5 = self.system.create_line(520, 55, 520, 495)
        self.arrow5 = self.system.create_line(520, 495, 340, 495, arrow=LAST)
        self.arrow5 = self.system.create_line(260, 495, 220, 495, arrow=LAST)
        self.arrow5 = self.system.create_line(140, 495, 100, 495, arrow=LAST)

        #Clicking
        self.system.tag_bind(self.source, '<Button-1>', self.sourceClicked)
        self.system.tag_bind(self.encoder, '<Button-1>', self.encoderClicked)
        self.system.tag_bind(self.digitalModulator, '<Button-1>', self.digitalModulatorClicked)
        self.system.tag_bind(self.digitalDemodulator, '<Button-1>', self.digitalDemodulatorClicked)
        self.system.tag_bind(self.sourceDecoder, '<Button-1>', self.sourceDecoderClicked)
        self.system.tag_bind(self.sink, '<Button-1>', self.sinkClicked)
        return self.system

class QPSK:
    #Hardcoded input text and jamming message
    inputText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse non orci sem. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas tempor et urna sit amet ornare. Maecenas mattis ligula eleifend, ultrices lacus a, pellentesque nisl. Vestibulum tel"
    jammingText = "Mauris interdum tempor neque, eget ornare erat eleifend luctus. In quis arcu cursus, lobortis leo sit amet, dignissim odio. Mauris molestie vel orci et consequat. Nunc nec sapien eu purus tempor vulputate. Donec in tristique lectus, a interdum orci. Cras rhoncus sapien nec aliquet egestas. Donec ege"

    #Hardcoded LFSR polynomials, number describes power of each entry, each is assumed to also have the 1 entry following
    signalPolynomial_1 = [5,2]
    signalPolynomial_2 = [5,3,2,1]
    jammerPolynomial_1 = [5,3]
    jammerPolynomial_2 = [5,4,2,1]
    
    #System Variables
    phi_degrees = 43
    phi_radians = math.radians(phi_degrees)
    offset = 24
    attenuation = 1

    

    def __init__(self, spreadSpectrum=False, SNRin=False, jammer=False):
        #If instantiated with no values it is assumed to be operating in the presence of no noise and no jammer
        self.symbols = [[0],[0]]
        self.SNRin = SNRin
        self.spreadSpectrum = spreadSpectrum
        self.jammer = jammer
        
        if jammer != False:
            jammerEncoded = self.sourceEncoder(self.jammingText)
            self.jammingSignal = self.digitalModulator(jammerEncoded, self.phi_radians)

        if spreadSpectrum:
            self.goldCodeSignal = self.utility_generateGoldCode(self.signalPolynomial_1, self.signalPolynomial_2, self.offset)
            self.goldCodeJammer = self.utility_generateGoldCode(self.jammerPolynomial_1, self.jammerPolynomial_2, self.offset)
            self.jammingSignal = self.spreader(self.jammingSignal, self.goldCodeJammer)

    def run(self):
        print("Running sim")
        """ 
        B = self.sourceEncoder(self.inputText)
        T = self.digitalModulator(B, self.phi_radians)
        if self.spreadSpectrum:
            T = self.spreader(T, self.goldCodeSignal)
        if self.SNRin != False:
            T = self.channelNoise(T, self.SNRin)
        if self.jammer != False:
            T = self.channelJammer(T, self.jammingSignal)
        if self.spreadSpectrum:
            T_ = self.despreader(T, )
        """
    
    def sourceEncoder(self, inp):
        output = list(map(bin, bytearray(inp, 'UTF-8')))
        output = [str(i[2:]) for i in output]
        for i in range(len(output)):
            while len(output[i]) < 8:
                output[i] = "0" + output[i]
        return output

    def digitalModulator(self, inp, phi=cmath.pi/4):
        output = []
        symbols = {
            "00":cmath.rect(math.sqrt(2), phi),
            "01":cmath.rect(math.sqrt(2), phi + cmath.pi/2),
            "11":cmath.rect(math.sqrt(2), phi + cmath.pi),
            "10":cmath.rect(math.sqrt(2), phi + 3*cmath.pi/2)
        }
        for i in inp:
            output.append(symbols[i[0:2]])
            output.append(symbols[i[2:4]])
            output.append(symbols[i[4:6]])
            output.append(symbols[i[6:8]])
        return output

    def spreader(self, inp, goldCode):
        #assumes T_cs = T_c, ie, 1 PN symbol per channel symbol
        output = []

        for i in range(len(inp)):
            
            output.append(inp[i] * goldCode[i%len(goldCode)])
        return output

    def channelNoise(self, inp, noisePower):
        #Takes the input and applies AWGN to every sample
        noise_real = []
        noise_imaginary = []
        for i in inp:
            noise_real.append(np.random.normal(scale = math.sqrt(noisePower)))
            noise_imaginary.append(np.random.normal(scale = math.sqrt(noisePower)))
        output = [s + complex(r,i) for s, r, i in list(zip(inp, noise_real, noise_imaginary))]
        return output

    def channelJammer(self, inp, jammingSignal):
        output = [s + i for s, i in list(zip(inp, jammingSignal))]
        return output

    def digitalDemodulator(self, inp):
        output = [utility_decision(i) for i in inp]
        return output
    
    def sourceDecoder(self, inp):
        byteList = []
        output = ""
        inp_copy = inp.copy()
        while len(inp_copy) > 0:
            symbol = inp_copy[0] + inp_copy[1] + inp_copy[2] + inp_copy[3]
            del inp_copy[0:4]
            byteList.append(symbol)
        
        for byte in byteList:
            temp = int(byte, 2).to_bytes(1, byteorder = "big")
            output += temp.decode()
        return output

    def utility_decision(self, inp):
        #A decision device that provides the output value with minimum distance to any of the defined symbols
        symbols = {
            "00":cmath.rect(math.sqrt(2), phi),
            "01":cmath.rect(math.sqrt(2), phi + cmath.pi/2),
            "11":cmath.rect(math.sqrt(2), phi + cmath.pi),
            "10":cmath.rect(math.sqrt(2), phi + 3*cmath.pi/2)
        }
        distances["00"] = abs(inp - symbols["00"])
        distances["01"] = abs(inp - symbols["01"])
        distances["11"] = abs(inp - symbols["11"])
        distances["10"] = abs(inp - symbols["10"])

        output = min(distances, key = distances.get)
        return output
    def utility_signalPower(self, inp):
        pass
    def utility_generateGoldCode(self, primitivePolynomial_1, primitivePolynomial_2, offset):
        #Generates and returns the gold code from the modulo-2 addition of the PN codes generated from the 2 passed primitive polynomials with the passed offset
        #Requires the 2 passed polynomials to have the same amount of stages
        PN_1 = self.utility_generatePNcode(primitivePolynomial_1)
        PN_2 = self.utility_generatePNcode(primitivePolynomial_2)
        goldCode = [0] * len(PN_1)

        for i in range(len(PN_1)):
            new = PN_1[i]
            if i+self.offset < len(PN_2):
                new += PN_2[i+self.offset]
            else:
                new += PN_2[i+self.offset - len(PN_2)]
            goldCode[i] = new % 2
        goldCode = [1-2*i for i in goldCode]
        return goldCode
    def utility_generatePNcode(self, primitivePolynomial):
        #Generates and returns the PN code from the passed polynomial
        PN = [1] #The PN code is formed as a list with initial value 1
        M = max(primitivePolynomial) #the number of stages of the LFSR is determined by the maximum value in the primitive polynomial
        initialState = [1] * M #the initial state is defined as all registers having value 1
        currentState = [1] * M
        workingPolynomial = primitivePolynomial[1:] #working polynomial is defined to allow the generation algorithm to work
        workingPolynomial = [i+1 for i in workingPolynomial]

        while True:
            new = currentState[-1]
            for i in workingPolynomial:
                new += currentState[-i]
            currentState.insert(0, new % 2)
            currentState.pop(-1)
            if currentState == initialState:
                break
            PN.append(currentState[-1])
        return PN
    
        output = 0
        for i in inp:
            output += (abs(i))**2
        return output/len(inp)

if __name__ == '__main__':
    root = Tk() 
    gui = guiLayout(root)
    root.mainloop()