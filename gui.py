import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk

from ctransformers import AutoModelForCausalLM

import torch

class Application():
    def __init__(self):
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title('ChatBot')
        self.window.geometry("960x300")
        self.window.resizable(width=False, height = False)

        self.model = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-13b-Chat-GGUF", model_file= 'C:\\Users\\chris\\text-generation-webui\\models\\llama-2-13b-chat.Q4_K_M.gguf', model_type="llama", gpu_layers = 100)
        # self.model = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-13b-Chat-GGUF", model_file= 'llama-2-13b-chat.Q4_K_M.gguf', model_type="llama", gpu_layers = 100)
        
        self.window._set_appearance_mode('light')

        self.window.wm_iconbitmap('icons\\ChatBot.ico') #icon: https://icon-icons.com/download/65955/ICO/512/
        self.createInterface()

        self.warnWindowCounter = 0
        self.mode = 0
        self.appearanceMode = 0
        

    def createInterface(self):
        
        self.setChatBox()
        self.setFrame2()
        self.createModeButton()

    def setChatBox(self):
        self.chatBoxFrame = ctk.CTkFrame(master = self.window, width= 800, height = 50)
        self.chatBoxFrame.grid(row = 0, column= 0, sticky = 'ew', ipadx= 1, ipady= 1, padx = 1, pady = 1)
        self.chatBoxFrame.columnconfigure(index = 0, weight = 1)

        self.chatHistory = []
        self.chatHistory.append('Let\'s start a conversation!')

        self.chatBoxText = ctk.CTkTextbox(master = self.chatBoxFrame, width = 700, height = 45,  wrap = 'word', border_width=2)

        scrollbar = ctk.CTkScrollbar(self.chatBoxFrame, command=self.chatBoxText.yview)
        self.chatBoxText.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row = 1, column = 2, sticky = 'nsew')
        self.chatBoxText.grid(row = 1, column = 1, sticky = 'nsew')

        self.refreshChatFrame()
    
    def refreshChatFrame(self):
        self.chatBoxText.configure(state = 'normal')
        self.chatBoxText.delete('1.0', ctk.END)

        self.chatBoxText.insert(ctk.END, self.chatHistory[0])
        for i in range(1, len(self.chatHistory)):
            if i % 2 == 0:
                self.chatBoxText.insert(ctk.END, '\nAI:')
                self.chatBoxText.insert(ctk.END, '\n')
                self.chatBoxText.insert(ctk.END, self.chatHistory[i][4:])
            else:
                self.chatBoxText.insert(ctk.END, '\nYou:')
                self.chatBoxText.insert(ctk.END, '\n')
                self.chatBoxText.insert(ctk.END, self.chatHistory[i][6:])

            if i % 2 == 0:
                self.chatBoxText.insert(ctk.END, '\n=============================================================================\n')
        self.chatBoxText.configure(state = 'disabled')
        self.chatBoxText.yview(ctk.END)

    def refreshWindow(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        if self.mode == 1:  #Therapist
            self.window.title('Mental Health Therapist Bot')

            self.window.wm_iconbitmap('icons\\TherapistBot.ico')  #https://icon-icons.com/download/113675/ICO/512/

        else:               #Regular
            self.window.title('ChatBot')

            self.window.wm_iconbitmap('icons\\ChatBot.ico') #icon: https://icon-icons.com/download/65955/ICO/512/
            

        self.createInterface()

    def clearChatHistory(self):
        self.chatBoxText.configure(state = 'normal')
        self.chatBoxText.delete('1.0', ctk.END)
        self.chatHistory = []
        self.chatHistory.append('Let\'s start a conversation!')
        self.refreshChatFrame()

    def setFrame2(self):
        self.inputText_frame = ctk.CTkFrame(master= self.window, height = 50, width=750)
        self.inputText_frame.columnconfigure(0, minsize = 50)
        self.inputText_frame.columnconfigure(1, minsize = 100)
        self.lbl_textEntry = ctk.CTkLabel(master = self.inputText_frame, text = 'Input text: ', width = 50, height = 50)
        self.ent_textEntry = ctk.CTkTextbox(master = self.inputText_frame,  width = 700, height= 50, xscrollcommand= True, yscrollcommand= True, border_width= 2)
        self.ent_textEntry.bind('<Return>', self.get_input)

        self.btn_frame = ctk.CTkFrame(master = self.window)
        self.btn_textEntry = ctk.CTkButton(master = self.btn_frame, text = 'Enter', command= self.get_input)
        self.btn_clrChat = ctk.CTkButton(master= self.btn_frame, text = 'Clear History', command = self.clearChatHistory)

        self.createTextScrollbar()

        self.inputText_frame.grid(row = 1, column= 0, sticky= 'ew')
        self.lbl_textEntry.grid(row = 0, column = 0, sticky= 'ew', ipadx = 5)
        self.ent_textEntry.grid(row = 0, column = 1, sticky = 'ew')

        self.btn_frame.grid(row = 2, column = 0, sticky = 'e')
        self.btn_clrChat.grid(row = 1, column = 1, padx = 5, pady = 5, ipadx =5, sticky= 'e')
        self.btn_clrChat.grid_columnconfigure(0, weight = 1)
        self.btn_textEntry.grid(row = 1, column = 2, padx = 5, pady = 5, ipadx= 5, sticky= 'e')
        self.btn_textEntry.grid_columnconfigure(0, weight = 1)


    def createTextScrollbar(self):
        scrollbar = ctk.CTkScrollbar(self.inputText_frame, command=self.ent_textEntry.yview, height = 50)
        self.ent_textEntry.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(sticky = 'nsew' , row = 0, column = 3)

    def createModeButton(self):
        self.btn_switch_frame = ctk.CTkFrame(master = self.window, bg_color= 'white', width = 50, corner_radius= 0)
        self.btn_regularMode = ctk.CTkButton(master = self.btn_switch_frame, text='Regular Chat Mode', command = self.createWarnWindowRegular)
        self.btn_regularMode._text_label.configure(wraplength= 200)
        self.btn_mentalTherapistMode = ctk.CTkButton(master = self.btn_switch_frame, text='Mental Health Therapist Chat Mode' , command = self.createWarnWindowTherapist)
        self.btn_mentalTherapistMode._text_label.configure(wraplength= 200)

        self.swtch_appearance = ctk.CTkSwitch(master = self.btn_switch_frame, command = self.switch_appearance, text = 'Light Mode')

        self.btn_switch_frame.grid(row= 0, column = 1, sticky = 'nsew')
        self.btn_regularMode.grid(row = 1,column = 0, sticky = 'ew', padx = 2, pady = 5, ipadx = 2)
        self.btn_mentalTherapistMode.grid(row = 2,column = 0, sticky = 'ew', padx = 2, pady = 5, ipadx = 2)
        self.swtch_appearance.grid(row = 3, column = 0, sticky = 'nsew')

    def switch_appearance(self):
        if self.appearanceMode == 0:
            self.window._set_appearance_mode("dark")
            self.appearanceMode = 1
            self.swtch_appearance.configure(text = "Dark Mode")

            for widget in self.window.winfo_children():
                widget._set_appearance_mode("dark")

                if widget.winfo_children():
                    for w in widget.winfo_children():
                        w._set_appearance_mode("dark")

        else:
            self.window._set_appearance_mode("light")
            self.appearanceMode = 0
            self.swtch_appearance.configure(text = "Light Mode")
            for widget in self.window.winfo_children():
                widget._set_appearance_mode("light")

                if widget.winfo_children():
                    for w in widget.winfo_children():
                        w._set_appearance_mode("light")

        self.swtch_appearance.update()

    def createWarnWindowRegular(self):
        if self.warnWindowCounter == 0:
            self.warnWindow = ctk.CTkToplevel(self.window)
            self.warnWindowCounter += 1 
            self.warnWindow.wm_transient(self.window)

            self.warnWindow.title('WARNING!')
        
            lbl_warn = ctk.CTkLabel(master = self.warnWindow, text = 'WARNING! Chat history will be lost! Would you like to proceed?')
            lbl_warn.pack()

            option_frame = ctk.CTkFrame(master = self.warnWindow)
            option_frame.pack()

            btn_yes = ctk.CTkButton(master = option_frame, text = 'Yes', command= self.switchToRegular)
            btn_no = ctk.CTkButton(master = option_frame, text= 'No', command = self.destroyWarnWindow)

            btn_yes.grid(row = 0, column = 0, sticky = 'ew')
            btn_no.grid(row = 0, column = 1, sticky = 'ew')
        else:
            self.warnWindow.focus()
            
        

    def createWarnWindowTherapist(self):
        if self.warnWindowCounter == 0:
            self.warnWindow = ctk.CTkToplevel(self.window)
            self.warnWindowCounter += 1
            self.warnWindow.title('WARNING!')
            self.warnWindow.wm_transient(self.window)
            
            lbl_warn = ctk.CTkLabel(master = self.warnWindow, text = 'WARNING! Chat history will be lost! Would you like to proceed?')
            lbl_warn.pack()

            option_frame = ctk.CTkFrame(master = self.warnWindow)
            option_frame.pack()

            btn_yes = ctk.CTkButton(master = option_frame, text = 'Yes', command= self.switchToTherapist)
            btn_no = ctk.CTkButton(master = option_frame, text= 'No', command = self.destroyWarnWindow)

            btn_yes.grid(row = 0, column = 0, sticky = 'ew')
            btn_no.grid(row = 0, column = 1, sticky = 'ew')
        else:
            self.warnWindow.focus()
        

    def destroyWarnWindow(self):
        self.warnWindow.destroy()
        self.warnWindowCounter -= 1

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
        
        input_text = "USER: " + input_text
        self.chatHistory.append(input_text)
        input_text_with_history = ''.join(self.chatHistory[1:])

        decoded_out = self.model(f'{prompt}\nUSER:{input_text_with_history}\nAI:', temperature= 0.7, max_new_tokens= 1024, top_p = 0.9, top_k= 2, repetition_penalty= 1.15, stop=['USER:', '\n\n\n', 'AI:'])
        temp = "AI: " + decoded_out
        self.chatHistory.append(temp)
        return decoded_out

    
if __name__ == '__main__':
    Application().start()