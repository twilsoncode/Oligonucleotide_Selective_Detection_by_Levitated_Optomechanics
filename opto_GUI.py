# Module imports
import customtkinter
import opto_save

if __name__ == "__main__":
    # Setting the layout of the GUI
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    root = customtkinter.CTk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.resizable(True, True)
    root.tk.call('tk', 'scaling', 1.0)
    root.state("normal")
    root.title("")
    switch_var_bin = customtkinter.StringVar(value="off")
    switch_var_csv = customtkinter.StringVar(value="off")
    file_switch = customtkinter.StringVar(value="off")
    root.grid_columnconfigure(10, weight=1)
    root.grid_rowconfigure(10, weight=1)

    # Setting the program title
    logo_label = customtkinter.CTkLabel(master=root, text="Welcome to the Optoanalysis Tool", font=customtkinter.CTkFont(size=30, weight="bold"))
    logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), rowspan=2, columnspan=11)

    # Setting up the tabs for future expandability
    tabview = customtkinter.CTkTabview(root, width=width, height=height)
    tabview.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), columnspan=11, rowspan=10)
    tabview.add("Tab 1")
    tabview.add("Tab 2")
    tabview.tab("Tab 1").grid_columnconfigure(0, weight=1)
    tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

    # Creating a scrollable frame
    scrollable_frame = customtkinter.CTkScrollableFrame(tabview.tab("Tab 1"), height=height-300)
    scrollable_frame.grid(row=3, column=0, padx=(2, 0), pady=(20, 0), sticky="nsew")
    scrollable_frame.grid_columnconfigure(20, weight=1)
    scrollable_frame.grid_rowconfigure(50, weight=1)

    # Function to plot the R&S .csv PSD using the particular oscilloscope parameters
    # Note - change these parameters depending on your settings
    def plot_csv_PSD():
        global file_path
        file_path = opto_save.get_file()
        placeholder_box = customtkinter.CTkEntry(scrollable_frame, width = 600, height = 28)
        placeholder_box.grid(row=5, column=0, padx=20, pady=(20, 10), columnspan=1)
        placeholder_box.insert(0, file_path[0])
        placeholder_box.configure(state="disabled")
        time_start = -0.249992
        time_stop = 0.250008
        signal_record_length = 5000000
        data = opto_save.get_csv_data(file_path[0], time_start, time_stop, signal_record_length)
        opto_save.plot_default_PSD(data, scrollable_frame, file_path[0])        
        return
    
    # Function to plot the R&S .bin PSD
    def plot_bin_PSD():
        global file_path
        file_path = opto_save.get_file()
        placeholder_box = customtkinter.CTkEntry(scrollable_frame, width = 600, height = 28)
        placeholder_box.grid(row=5, column=0, padx=20, pady=(20, 10), columnspan=1)
        placeholder_box.insert(0, file_path[0])
        placeholder_box.configure(state="disabled")
        data = opto_save.get_bin_data(file_path[0])
        opto_save.plot_default_PSD(data, scrollable_frame, file_path[0])        
        return

    # Function to calculate the parameters using the entered data
    def calculate_parameters():
        particle_type = particle_box.get()
        pressure = pressure_box.get()
        f1_rough = f1_rough_box.get()
        f2_rough = f2_rough_box.get()
        f3_rough = f3_rough_box.get()
        easy_peaks = read_peaks_box.get()
        data = None

        # Checking the file type
        if file_path[0].endswith(".csv"):
            time_start = -0.249992
            time_stop = 0.250008
            signal_record_length = 5000000
            data = opto_save.get_csv_data(file_path[0], time_start, time_stop, signal_record_length)
        elif file_path[0].endswith(".bin"):
            data = opto_save.get_bin_data(file_path[0])
        else:
            print("Unsupported file type. Please use .csv or .bin.")
            return

        # Checking that the entered data is reasonable
        try:
            peak_freq = [float(f1_rough), float(f2_rough), float(f3_rough)]
            pressure = float(pressure)
            pressure_error = 1
            if data is not None:
                opto_save.save_data(data, peak_freq, pressure, pressure_error, file_path, particle_type, easy_peaks)
            else:
                print("Data is None. Unable to save.")
        except Exception as e:
            print(f"Error in processing: {e}")

    # Setting up the scaling of the GUI
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # Button for calling the plot_csv_PSD function
    button = customtkinter.CTkButton(scrollable_frame, text = "Plot R&S .csv PSD", command=plot_csv_PSD)
    button.grid(row=3, column=0, padx=20, pady=(20, 10))

    # Button for calling the plot_bin_PSD function
    button = customtkinter.CTkButton(scrollable_frame, text = "Plot R&S .bin PSD", command=plot_bin_PSD)
    button.grid(row=4, column=0, padx=20, pady=(20, 10))

    # Creating a blank plot as a placeholder
    opto_save.blank_plot(scrollable_frame)

    # Placeholder box for the file path
    placeholder_box = customtkinter.CTkEntry(scrollable_frame, width = 600, height = 28)
    placeholder_box.grid(row=5, column=0, padx=20, pady=(20, 10), columnspan=1)
    placeholder_box.configure(state="disabled")

    # Box for the entry of the pressure value
    pressure_box = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter the pressure (mbar)", width = 600, height = 28)
    pressure_box.grid(row=6, column=0, padx=20, pady=(20, 10), columnspan=1)     

    # Label text for Enter the particle type
    particle_box_label = customtkinter.CTkLabel(scrollable_frame, text="Enter the particle type:", anchor="w")
    particle_box_label.grid(row=7, column=0, padx=20, pady=(20, 10), columnspan=1)

    # Dropdown box for the selection of particle type tested
    particle_box = customtkinter.CTkComboBox(scrollable_frame, values=["SiNP", "1000uM Final ZnCl2 SiNP", "25A 1000uM Final ZnCl2 SiNP", "25A 100uM Final ZnCl2 SiNP", "25A 10uM Final ZnCl2 SiNP", "25A 1uM Final ZnCl2 SiNP", "25T 1000uM Final ZnCl2 SiNP", "25T 750uM Final ZnCl2 SiNP", "25T 500uM Final ZnCl2 SiNP", "25T 250uM Final ZnCl2 SiNP", "25T 100uM Final ZnCl2 SiNP", "25T 10uM Final ZnCl2 SiNP", "25T 1uM Final ZnCl2 SiNP", "25A-25T Duplex ZnCl2 SiNP", "25A 25T Individual ZnCl2 SiNP"])
    particle_box.grid(row=8, column=0, columnspan=1)

    # Box for the entry of the rough f1 peak frequency
    f1_rough_box = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter the f1 Rough Peak Frequency (kHz)", width = 600, height = 28)
    f1_rough_box.grid(row=9, column=0, padx=20, pady=(20, 10), columnspan=1)

    # Box for the entry of the rough f2 peak frequency
    f2_rough_box = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter the f2 Rough Peak Frequency (kHz)", width = 600, height = 28)
    f2_rough_box.grid(row=10, column=0, padx=20, pady=(20, 10), columnspan=1)

    # Box for the entry of the rough f2 peak frequency
    f3_rough_box = customtkinter.CTkEntry(scrollable_frame, placeholder_text="Enter the f3 Rough Peak Frequency (kHz)", width = 600, height = 28)
    f3_rough_box.grid(row=11, column=0, padx=20, pady=(20, 10), columnspan=1)

    # Text label saying Are the PSD peaks easy to fit?
    read_peaks_box_label = customtkinter.CTkLabel(scrollable_frame, text="Are the PSD peaks easy to fit?", anchor="w")
    read_peaks_box_label.grid(row=12, column=0, padx=20, pady=(20, 10), columnspan=1)

    # Dropdown box for Yes/No if the PSD peaks are easy to fit
    read_peaks_box = customtkinter.CTkComboBox(scrollable_frame, values=["Yes", "No"])
    read_peaks_box.grid(row=13, column=0, columnspan=1)
    
    # A button to run the calculate_parameters function
    button = customtkinter.CTkButton(scrollable_frame, text = "Calculate Parameters", command=calculate_parameters)
    button.grid(row=14, column=0, padx=20, pady=(20, 10))

    # Setting up the GUI scaling as a dropdown list
    optionmenu_var = customtkinter.StringVar(value="100%")
    root.scaling_label = customtkinter.CTkLabel(master=root, text="UI Scaling:", anchor="w")
    root.scaling_label.grid(row=0, column=0, padx=20, pady=(10, 0))
    root.scaling_optionemenu = customtkinter.CTkOptionMenu(master=root, values=["50%", "60%", "70%", "80%", "90%", "100%", "110%", "120%", "130%", "140%", "150%"],
                                                               command=change_scaling_event, variable=optionmenu_var)
    root.scaling_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 20))

    # Ending the customtkinter root main loop
    root.mainloop()