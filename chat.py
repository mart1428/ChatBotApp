import tkinter as tk
import customtkinter as ctk


class Chat():
    def __init__(self):
        self.id = None
        self.summary = None
        self.prompt = None
        self.history = []

        self.mode = 0