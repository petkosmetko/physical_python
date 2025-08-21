import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("This or that")
        self.geometry(f"{800}x{450}")
        self.grid_rowconfigure((0,1,2,3),weight = 1)
        self.grid_columnconfigure((0,1),weight = 1)

    
        
        buttonA = customtkinter.CTkButton(self, text='Image1', width=200, height=700,command = self.buttonA_event)
        buttonA.grid(column = 0,rowspan = 3)
        buttonB = customtkinter.CTkButton(self, text='Image2', width=200, height=700,command = self.buttonB_event)
        buttonB.grid(column = 1,rowspan = 3)
        
    def buttonA_event(self):
        print("key 1 pressed")
    def buttonB_event(self):
        print("key 2 pressed")



if __name__ == "__main__":
    app = App()
    app.mainloop()
