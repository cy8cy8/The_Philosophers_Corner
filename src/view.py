import tkinter as tk
from tkinter import ttk

class HomePage(tk.Frame):
    def __init__(self, parent, viewmodel, bg):
        super().__init__(parent)
        self.viewmodel = viewmodel
        self["background"] = bg
        style = ttk.Style()

        self.wisdom_lbl = self.create_wisdom_lbl()
        self.wisdom_lbl.pack(padx=150, pady=70)

        self.btns_and_dropdown_frame = ttk.Frame(self)
        self.category_dropdown = self.create_cateogry_dropdown()
        self.category_dropdown.pack(pady=25)
        self.btns = self.create_show_and_add_wisdom_btn(style)
        self.btns.pack()
        self.btns_and_dropdown_frame.pack(padx=50)

    def create_cateogry_dropdown(self) -> ttk.Combobox:
        category_dropdown = ttk.Combobox(self, textvariable=self.viewmodel.category_var)
        category_dropdown["values"] = self.viewmodel.categories
        category_dropdown.bind("<<ComboboxSelected>>", func=lambda e: self.update_wisdom(self.viewmodel.category_var.get()))
        category_dropdown.bind("<<ComboboxSelected>>", func=lambda e: e.widget.select_clear(), add="+") #add="+"  for multiple binding
        return category_dropdown

    def create_wisdom_lbl(self):
        wisdom = tk.Text(self,
                        wrap=tk.WORD, 
                        borderwidth=0, 
                        font=("Arial", 15, "bold"), 
                        background="black", 
                        foreground="white", 
                        highlightthickness=0,
                        height=20 #20 lines
        )
        wisdom.insert(tk.END, self.viewmodel.display_all_wisdom())
        wisdom["state"] = "disabled"
        return wisdom

    def create_show_and_add_wisdom_btn(self, style):
        btn_frame = ttk.Frame(self)
        style.configure("Show.TButton", 
                        font=("Arial", 14), 
                        background="lightgreen", 
                        foreground="black", 
                        borderwidth=0, 
                        padding=10, 
                        focuscolor="black", 
                        bordercolor="white", 
                        hightlightthickness=0
        )
        style.configure("Add.TButton", 
                        font=("Arial", 14), 
                        background="black", 
                        foreground="darkgreen",
                        borderwidth=0, 
                        padding=10, 
                        focuscolor="black", 
                        bordercolor="white"
        )
        show_wisdom_btn = ttk.Button(btn_frame, 
                                     text="Show Wisdom", 
                                     command=lambda: self.update_wisdom(category=self.viewmodel.category_var.get()), 
                                     style="Show.TButton"
        )
        show_wisdom_btn.pack(fill="both", expand=True, side="left")
        add_wisdom_btn = ttk.Button(btn_frame, 
                                    text="Add Wisdom", 
                                    style="Add.TButton", 
                                    command=self.open_add_window
        )
        add_wisdom_btn.pack(fill="both", expand=True, side="left")
        return btn_frame

    def update_wisdom(self, category:str):
        self.wisdom_lbl["state"] = "normal"
        if self.viewmodel.category_var.get() == "":
            self.wisdom_lbl.delete("1.0", tk.END)
            self.wisdom_lbl.insert(tk.END, self.viewmodel.display_all_wisdom())
            self.wisdom_lbl["state"] = "disabled"
        elif self.viewmodel.category_var.get()== category:
            self.wisdom_lbl.delete("1.0", tk.END)
            self.wisdom_lbl.insert(tk.END, self.viewmodel.display_wisdom_from_a_category(category))
            self.wisdom_lbl["state"] = "disabled"
    
    def open_add_window(self):
        add_window = AddWisdomPage(self, self.viewmodel)
        add_window.grab_set()


class AddWisdomPage(tk.Toplevel):
    def __init__(self, parent, viewmodel):
        super().__init__(parent)
        self.viewmodel = viewmodel
        self.minsize(width=700, height=550)
        self.maxsize(width=700, height=550)
        style = ttk.Style()

        style.configure("TLabel", font="Arial 20 bold")
        add_wisdom_label = ttk.Label(self, text="Add Your Wisdom")
        add_wisdom_label.pack(pady=25)
        self.add_wisdom_entry = tk.Text(self, height=10, width=60, font="Arial 14")
        self.add_wisdom_entry.pack(pady=15)
        self.create_add_cateogory_dropdown().pack()
        self.create_submit_and_cancel_btn(style=style).pack(pady=25, padx=25)

    def create_submit_and_cancel_btn(self, style:ttk.Style) -> tk.Frame:
        style.configure("Submit.TButton", 
                        font="Arial 14", 
                        padding=5, 
                        background="lightgreen", 
                        foreground="black"
        )
        style.configure("Cancel.TButton", 
                        font="Arial 14", 
                        padding=5, 
                        background="red", 
                        foreground="black"
        )
        add_wisdom_btns = tk.Frame(self)
        ttk.Button(add_wisdom_btns, 
                                text="Submit", 
                                command=self.on_submit, 
                                style="Submit.TButton"
        ).grid(row=0, column=0, padx=10)
        ttk.Button(add_wisdom_btns, 
                                text="Cancel", 
                                command=self.destroy, 
                                style="Cancel.TButton"
        ).grid(row=0, column=1, padx=10)
        return add_wisdom_btns

    def create_add_cateogory_dropdown(self) -> ttk.Combobox:
        category_dropdown = ttk.Combobox(self, textvariable=self.viewmodel.category_var)
        category_dropdown["values"] = self.viewmodel.categories
        category_dropdown.bind("<<ComboboxSelected>>", func=self.viewmodel.category_var.get())
        return category_dropdown
    
    def on_submit(self):
        new_wisdom = self.add_wisdom_entry.get("1.0", tk.END).strip()
        self.viewmodel.insert_new_wisdom(self.viewmodel.category_var.get(), new_wisdom)
        self.destroy()