# ELEN4022 - Project - Group 01
# 09/05/2022
# Jesse Van Der Merwe (1829172)
# Keri-Lee Carstens (1384538)
# Tshegofatso Kale (1600916)

# - - - - - - - - - - IMPORTS - - - - - - - - - - #
from tkinter import *
from tkinter import ttk

from matplotlib.font_manager import FontProperties
from Classical import *
from Quantum import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

# - - - - - - - - - - FUNCTIONS - - - - - - - - - - #
def on_combobox_change(event):
    """Updates the GUI according to which running option the user has selected."""
    if running_options_selected.get() == running_options[0]:
        label_z_qubits.grid_remove()
        entry_z_qubits.grid_remove()
        label_z_warning_slow_results_hardware.grid_remove()
        label_z_warning_limited_qubits.grid_remove()
        entry_z_qubits.config(state = "normal")
        label_z_error.grid_remove()

    if running_options_selected.get() == running_options[1]:
        label_z_qubits.grid()
        entry_z_qubits.grid()
        label_z_warning_slow_results_hardware.grid_remove()
        label_z_warning_limited_qubits.grid_remove()
        entry_z_qubits.config(state = "normal")
    if running_options_selected.get() == running_options[2]:
        label_z_qubits.grid()
        entry_z_qubits.grid()
        label_z_warning_slow_results_hardware.grid()
        label_z_warning_limited_qubits.grid()
        entry_z_qubits.config(state = "disabled")
        entry_z_qubits_var.set("1")

def calculate_total_expected_loss():
    '''
    Performs input validation and runs the Quantum or Classical code according to the option selected.

        Parameters: 
            my_classical (Classical): An instance of the Classical class, created according to the running option selected.
            my_quantum_simulated (Quantum): An instance of the Quantum class, created according to the running option selected.
            values (list): A list of the loss values that occur for the inputted default probabilities of the two assets.
            probs (list): A list of the probabilities of each loss value for the inputted default probabilities of the two assets.
            total_expected_loss_exact (float): The calculated exact total expected loss value.
            total_expected_loss_estimate (float): The estimated total expected loss value. 

    '''
    input_valid = True
    default_probability_1 = entry_default_probability_1.get()
    default_probability_2 = entry_default_probability_2.get()
    z_qubits = entry_z_qubits.get()

    # Input validation for float default probability 1 
    try:
        default_probability_1 = float(default_probability_1)
        label_default_probability_1_error.grid_remove()
        if(default_probability_1 >= 1 or default_probability_1 <= 0):
            input_valid = False
            label_default_probability_1_error.grid()
    except:
        input_valid = False
        label_default_probability_1_error.grid()

    # Input validation for float default probability 2
    try:
        default_probability_2 = float(default_probability_2)
        label_default_probability_2_error.grid_remove()
        if(default_probability_2 >= 1 or default_probability_2 <= 0):
            input_valid = False
            label_default_probability_2_error.grid()
    except:
        input_valid = False
        label_default_probability_2_error.grid()

    # Input validation for integer Z value if required (i.e. for quantum code)
    if running_options_selected.get() == running_options[1] or running_options_selected.get() == running_options[2]:       
        try:
            z_qubits = int(z_qubits)
            label_z_error.grid_remove()
            # Warning for user if Z value is too large (might take too long for user's PC to run)
            if(z_qubits > 5):
                label_z_warning_slow_results_simulations.grid()
            else:
                label_z_warning_slow_results_simulations.grid_remove()
        except:
            input_valid = False
            label_z_error.grid()

    if input_valid:
        values, probs = 0, 0
        total_expected_loss_exact = 0
        total_expected_loss_estimated = 0
        if(running_options_selected.get() == running_options[0]): # CLASSICAL 
            my_classical = Classical(default_probability_1, default_probability_2, 10000)
            values, probs = my_classical.get_probabilities()
            total_expected_loss_exact = my_classical.get_total_expected_loss()

            label_total_expected_loss_exact['text'] = "Total expected loss: {}".format(total_expected_loss_exact)
            label_total_expected_loss_exact.grid(row = 6, column=0, padx=10, pady=10, sticky=W)
            label_total_expected_loss_estimated['text'] = ""

        elif(running_options_selected.get() == running_options[1]): # QUANTUM SIMULATED
            my_quantum_simulated = Quantum(default_probability_1, default_probability_2, z_qubits, "S")
            values, probs = my_quantum_simulated.get_probabilities_simulated()
            total_expected_loss_exact = my_quantum_simulated.get_total_expected_loss_exact()
            total_expected_loss_estimated = my_quantum_simulated.get_total_expected_loss_estimated()

            label_total_expected_loss_exact['text'] = "Total exact expected loss: {}".format(total_expected_loss_exact)
            label_total_expected_loss_exact.grid(row = 6, column=0, padx=10, sticky=W)

            label_total_expected_loss_estimated['text'] = "Total estimated expected loss: {}".format(total_expected_loss_estimated)
            label_total_expected_loss_estimated.grid(row = 7, column=0, padx=10, sticky=W)

        elif(running_options_selected.get() == running_options[2]): # QUANTUM HARDWARE
            my_quantum_simulated = Quantum(default_probability_1, default_probability_2, z_qubits, "Q")
            values, probs = my_quantum_simulated.get_probabilities_simulated()
            total_expected_loss_exact = my_quantum_simulated.get_total_expected_loss_exact()
            total_expected_loss_estimated = my_quantum_simulated.get_total_expected_loss_estimated()

            label_total_expected_loss_exact['text'] = "Total exact expected loss: {}".format(total_expected_loss_exact)
            label_total_expected_loss_exact.grid(row = 6, column=0, padx=10, pady=10, sticky=W)

            label_total_expected_loss_estimated['text'] = "Total estimated expected loss: {}".format(total_expected_loss_estimated)
            label_total_expected_loss_estimated.grid(row = 7, column=0, padx=10, pady=10, sticky=W)
        
        figure = plt.figure(figsize=(4, 3))
        plt.bar(x=values, height=probs)
        plt.xlabel("Loss")
        plt.ylabel("Probability (%)")
        plt.title("{}: Total Loss Distribution".format(running_options_selected.get()), fontsize=10)

        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 10, column=0, columnspan=3, ipadx=50, ipady=50, sticky=W)

def close_application():
    """Closes the tkinter window and ensures the program is terminated."""
    root.quit()
    root.destroy()

# - - - - - - - - - - GUI ELEMENTS AND OBJECTS - - - - - - - - - - #
root = Tk()
root.title('ELEN4022 Project: Quantum vs Classical Estimated Expected Loss')
root.geometry("750x700")

label_running_option = Label(root, text="Choose how to run this program: ")
label_running_option.grid(row=0, column=0, padx=10, pady=10, sticky=W)
running_options = ["Classical Code", "Quantum Simulation", "Quantum Hardware"]
running_options_selected = StringVar()
running_option_combobox = ttk.Combobox(root, textvariable = running_options_selected, values=running_options, state='readonly')
running_option_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=W)
running_option_combobox.current(0)
running_option_combobox.bind("<<ComboboxSelected>>", on_combobox_change)
running_options_selected.set(running_options[0])

label_default_probability_1 = Label(root, text = "Enter the default probability of asset 1: ")
label_default_probability_1.grid(row=1, column=0, padx=10, sticky=W)
label_default_probability_1_error = Label(root, text = "Please enter a decimal between 0 and 1.", fg='red')
label_default_probability_1_error.grid(row=1, column=2, padx=10, sticky=W)
label_default_probability_1_error.grid_remove()
entry_default_probability_1 = Entry(root, width = 20) # NB!! NEED to add input data validation
entry_default_probability_1.grid(row=1, column=1, padx=10, sticky=W)

label_default_probability_2 = Label(root, text = "Enter the default probability of asset 2: ")
label_default_probability_2.grid(row=2, column=0, padx=10, sticky=W)
label_default_probability_2_error = Label(root, text = "Please enter a decimal between 0 and 1.", fg='red')
label_default_probability_2_error.grid(row=2, column=2, padx=10, sticky=W)
label_default_probability_2_error.grid_remove()
entry_default_probability_2 = Entry(root, width = 20) # NB!! NEED to add input data validation
entry_default_probability_2.grid(row=2, column=1, padx=10, sticky=W)

label_z_qubits = Label(root, text = "Enter the number of qubits to represent Z: ")
label_z_qubits.grid(row=3, column=0, padx=10, sticky=W)
label_z_qubits.grid_remove()

label_z_error = Label(root, text = "Please enter an interger.", fg='red')
label_z_error.grid(row=3, column=2, padx=10, sticky=W)
label_z_error.grid_remove()

label_z_warning_limited_qubits = Label(root, text = "Set to 1 due to limited quantum hardware.", fg='red')
label_z_warning_limited_qubits.grid(row=3, column=2, padx=10, sticky=W)
label_z_warning_limited_qubits.grid_remove()

label_z_warning_slow_results_simulations = Label(root, text = "Note: Large number of qubits will take long to run.", fg='red')
label_z_warning_slow_results_simulations.grid(row=3, column=2, columnspan=3, padx=10, sticky=W)
label_z_warning_slow_results_simulations.grid_remove()

label_z_warning_slow_results_hardware = Label(root, text = "Note: This process could take upwards of 1 hour to complete due to IBMQ quantum hardware queue times.", fg='red')
label_z_warning_slow_results_hardware.grid(row=4, column=0, columnspan=3, padx=10, sticky=W)
label_z_warning_slow_results_hardware.grid_remove()

entry_z_qubits_var = StringVar()
entry_z_qubits_var.set("")
entry_z_qubits = Entry(root, width = 20, textvariable=entry_z_qubits_var) # NB!! NEED to add input data validation
entry_z_qubits.config(state = "normal")
entry_z_qubits.grid(row=3, column=1, padx=10, pady=10, sticky=W)
entry_z_qubits.grid_remove()

label_total_expected_loss_exact = Label(root, text = "")
label_total_expected_loss_estimated = Label(root, text = "")

button_calculate = Button(root, text = "Calculate", command = calculate_total_expected_loss)
button_calculate.grid(row=5, column=1, padx=10, pady=10, sticky=W)

root.protocol("WM_DELETE_WINDOW", close_application)
root.mainloop()