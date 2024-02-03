import tkinter as tk
import tkinter.ttk as ttk

from ctransformers import AutoModelForCausalLM

import torch

from collections import deque


class Application():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('ChatBot')
        self.window.geometry("780x550")
        self.window.resizable(width=False, height = False)

        self.model = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-13b-Chat-GGUF", model_file= 'llama-2-13b-chat.Q4_K_M.gguf', model_type="llama", gpu_layers = 100)

        self.colorMap = {
            'window' : '#53c653',
            'chatFrame' : '#79d279',
            'chatBoxText' : '#9fdf9f',
            'btn' : '#ecffe6'
            }

        self.window.configure(bg = self.colorMap['window'])
        self.window.wm_iconbitmap('icons\\ChatBot.ico') #icon: https://icon-icons.com/download/65955/ICO/512/
        self.createInterface()

        self.mode = 0
        

    def createInterface(self):
        
        self.setChatBox()
        self.setFrame2()
        self.createAIModeButton()

    def setChatBox(self):
        self.chatBoxFrame = tk.Frame(master = self.window, width= 100, height = 25, relief = tk.GROOVE, borderwidth = 2, padx= 2, pady = 2, bg = self.colorMap['chatFrame'])
        self.chatBoxFrame.grid(row = 0, column= 0, sticky = 'ew', ipadx= 5, ipady= 5, padx = 5, pady = 5)
        self.chatBoxFrame.columnconfigure(index = 0, weight = 1)

        self.chatHistory = []
        self.chatHistory.append('Let\'s start a conversation!')


        self.chatBoxText = tk.Text(master = self.chatBoxFrame, width = 80, height = 23, relief = tk.FLAT, font = 'Calibri 11 italic', wrap = 'word', background= self.colorMap['chatBoxText'])

        scrollbar = tk.Scrollbar(self.chatBoxFrame, command=self.chatBoxText.yview)
        self.chatBoxText.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row = 1, column = 2, sticky = 'nsew')
        self.chatBoxText.grid(row = 1, column = 1, sticky = 'nsew')

        self.refreshChatFrame()
    
    def refreshChatFrame(self):
        self.chatBoxText.configure(state = 'normal')
        self.chatBoxText.delete('1.0', tk.END)

        self.chatBoxText.insert(tk.END, self.chatHistory[0])
        for i in range(1, len(self.chatHistory)):
            if i % 2 == 0:
                self.chatBoxText.insert(tk.END, '\nAI:')
            else:
                self.chatBoxText.insert(tk.END, '\nYou:')
            self.chatBoxText.insert(tk.END, '\n')
            self.chatBoxText.insert(tk.END, self.chatHistory[i])

            if i % 2 == 0:
                self.chatBoxText.insert(tk.END, '\n=============================================================================\n')
        self.chatBoxText.configure(state = 'disabled')
        self.chatBoxText.yview_pickplace(tk.END)

    def refreshWindow(self):
        self.window.destroy()
        self.window = tk.Tk()
        self.window.geometry("780x550")
        self.window.resizable(width=False, height = False)


        if self.mode == 1:  #Therapist
            self.colorMap = {
            'window' : '#008ae6',
            'chatFrame' : '#33adff',
            'chatBoxText' : '#e6f3ff',
            'btn' : '#ecffe6'
            }
            self.window.title('Mental Health Therapist Bot')

            self.window.wm_iconbitmap('icons\\TherapistBot.ico')  #https://icon-icons.com/download/113675/ICO/512/

        else:               #Regular
            self.colorMap = {
            'window' : '#53c653',
            'chatFrame' : '#79d279',
            'chatBoxText' : '#9fdf9f',
            'btn' : '#ecffe6'
            }
            self.window.title('ChatBot')

            self.window.wm_iconbitmap('icons\\ChatBot.ico') #icon: https://icon-icons.com/download/65955/ICO/512/
            

        self.window.configure(bg = self.colorMap['window'])
        self.createInterface()

    def clearChatHistory(self):
        self.chatBoxText.configure(state = 'normal')
        self.chatBoxText.delete('1.0', tk.END)
        self.chatHistory = []
        self.chatHistory.append('Let\'s start a conversation!')
        self.refreshChatFrame()

    def setFrame2(self):
        self.inputText_frame = tk.Frame(master= self.window, borderwidth = 5, height = 50, width=100, bg= self.colorMap['window'])
        self.inputText_frame.columnconfigure(0, minsize = 100, weight= 1)
        self.lbl_textEntry = tk.Label(master = self.inputText_frame, text = 'Input text: ', width = 5, border = 2, relief = tk.GROOVE, bg = '#ffffe6')
        self.ent_textEntry = tk.Text(master = self.inputText_frame, background= '#d3d3d3', width = 80, height= 5, xscrollcommand= True, yscrollcommand= True, font = 'Calibri 11')
        self.ent_textEntry.bind('<Return>', self.get_input)

        self.btn_frame = tk.Frame(master = self.window, bg = self.colorMap['window'])
        self.btn_textEntry = tk.Button(master = self.btn_frame, text = 'Enter', command= self.get_input, background= self.colorMap['btn'])
        self.btn_clrChat = tk.Button(master= self.btn_frame, text = 'Clear History', command = self.clearChatHistory, background = self.colorMap['btn'])

        self.createTextScrollbar()

        self.inputText_frame.grid(row = 1, column= 0, sticky= 'ew')
        self.lbl_textEntry.grid(row = 0, column = 0, sticky= 'nsew')
        self.ent_textEntry.grid(row = 0, column = 1, sticky = 'ew')
        self.ent_textEntry.grid_columnconfigure(0, weight = 1, minsize= 500)

        self.btn_frame.grid(row = 2, column = 0, sticky = 'e')
        self.btn_clrChat.grid(row = 1, column = 1, padx = 5, pady = 5, ipadx =5, sticky= 'e')
        self.btn_clrChat.grid_columnconfigure(0, weight = 1)
        self.btn_textEntry.grid(row = 1, column = 2, padx = 5, pady = 5, ipadx= 5, sticky= 'e')
        self.btn_textEntry.grid_columnconfigure(0, weight = 1)


    def createTextScrollbar(self):
        scrollbar = tk.Scrollbar(self.ent_textEntry, command=self.ent_textEntry.yview)
        self.ent_textEntry.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(sticky = 'nsew' , column = 3)

    def createAIModeButton(self):
        self.btn_switch_frame = tk.Frame(master = self.window, bg = self.colorMap['window'])
        self.btn_regularMode = tk.Button(master = self.btn_switch_frame, text='Regular Chat Mode' ,bg = self.colorMap['btn'], command = self.createWarnWindowRegular)
        self.btn_mentalTherapistMode = tk.Button(master = self.btn_switch_frame, text='Mental Health Therapist Chat Mode' ,bg = self.colorMap['btn'], wraplength= 90, command = self.createWarnWindowTherapist)

        self.btn_switch_frame.grid(row= 0, column = 1, sticky = 'nsew')
        self.btn_regularMode.grid(row = 1,column = 0, sticky = 'ew', padx = 2, pady = 5, ipadx = 2)
        self.btn_mentalTherapistMode.grid(row = 2,column = 0, sticky = 'ew', padx = 2, pady = 5, ipadx = 2)

    def createWarnWindowRegular(self):
        self.warnWindow = tk.Tk()
        self.warnWindow.title('WARNING!')
        
        lbl_warn = tk.Label(master = self.warnWindow, text = 'WARNING! Chat history will be lost! Would you like to proceed?')
        lbl_warn.pack()

        option_frame = tk.Frame(master = self.warnWindow)
        option_frame.pack()

        btn_yes = tk.Button(master = option_frame, text = 'Yes', command= self.switchToRegular)
        btn_no = tk.Button(master = option_frame, text= 'No', command = self.destroyWarnWindow)

        btn_yes.grid(row = 0, column = 0, sticky = 'ew')
        btn_no.grid(row = 0, column = 1, sticky = 'ew')

    def createWarnWindowTherapist(self):
        self.warnWindow = tk.Tk()
        self.warnWindow.title('WARNING!')
        
        lbl_warn = tk.Label(master = self.warnWindow, text = 'WARNING! Chat history will be lost! Would you like to proceed?')
        lbl_warn.pack()

        option_frame = tk.Frame(master = self.warnWindow)
        option_frame.pack()

        btn_yes = tk.Button(master = option_frame, text = 'Yes', command= self.switchToTherapist)
        btn_no = tk.Button(master = option_frame, text= 'No', command = self.destroyWarnWindow)

        btn_yes.grid(row = 0, column = 0, sticky = 'ew')
        btn_no.grid(row = 0, column = 1, sticky = 'ew')

    def destroyWarnWindow(self):
        self.warnWindow.destroy()

    def switchToRegular(self):
        self.mode = 0
        self.refreshWindow()
        self.clearChatHistory()
        self.destroyWarnWindow()


    def switchToTherapist(self):
        self.mode = 1
        self.refreshWindow()
        self.clearChatHistory()
        self.destroyWarnWindow()
    
    def start(self):
        self.window.mainloop()

    def get_input(self, event = None):
        input_text = self.ent_textEntry.get("0.0",tk.END)

        out = self.get_model_output(input_text)
        self.refreshChatFrame()
        self.ent_textEntry.delete("0.0", tk.END)


    def get_model_output(self, input_text):

        if self.mode == 1:
            prompt = 'The following is a conversation with an AI Large Language Model as a mental health therapist. The AI has been trained to answer questions, provide recommendations, help with decision making and provide comfort. The AI follows USER requests. The AI thinks outside the box.'
        else:
            prompt = 'The following is a conversation with an AI Large Language Model. The AI has been trained to answer questions, provide recommendations, and help with decision making. The AI follows USER requests. The AI thinks outside the box.'
        
        self.chatHistory.append(input_text)
        input_text_with_history = ''.join(self.chatHistory[1:])

        decoded_out = self.model(f'{prompt}\nUSER:{input_text_with_history}\nAI:', temperature= 0.7, max_new_tokens= 512, top_p = 0.9, top_k= 2, repetition_penalty= 1.15, stop=['USER:', '\n\n\n', 'AI:'])
        self.chatHistory.append(decoded_out)
        return decoded_out

    
if __name__ == '__main__':
    Application().start()