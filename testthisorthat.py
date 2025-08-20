import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("This or that")
        self.geometry(f"{800}x{450}")
        self.grid_rowconfigure((0,1,2,3),weight = 1)
        self.grid_columnconfigure((0,1),weight = 1)
        

        


if __name__ == "__main__":
    app = App()
    app.mainloop()
