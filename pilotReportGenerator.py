from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import *
import os
import os.path

label_text = ["Location",
              "Day",
              "User Account",
              "Overall Rating",
              "Cumulus Clouds",
              "Cumulus Cloudbase",
              "Cloud Honesty",
              "Average Thermal",
              "Thermal Turbulence",
              "Thermal Spacing",
              "Max on Vario",
              "Overdeveloped",
              "Wind Strength",
              "Wind Direction"]

label_units = ["",
               "",
               "",
               "",
               "",
               "(ft MSL)",
               "",
               "(knots)",
               "",
               "(miles)",
               "(knots)",
               "",
               "(knots)",
               "(deg)"]


label_widgets_text = []
main_widgets = []
label_widgets_units = []


root = Tk()
root.title("Pilot Report Soaring")


def write_pirep_file():
    # Check if any unanswered questions
    if clouds.get() == 0:
        messagebox.showerror(title="Incomplete Entry", message="Select if clouds present")
        return
    if over_dev.get() == 0:
        messagebox.showerror(title="Incomplete Entry", message="Select if overdevelopment happened")
        return
    if honesty.get() == "":
        messagebox.showerror(title="Incomplete Entry", message="Specify cloud honesty")
        return

    # Open a text file to record the PIREP for soaring
    pirep_dir = "./maps/" + day.get() + "/"
    filename = pirep_dir + "PIREP-" + str(datetime.now().date()) + "_r0" + ".txt"
    try:
        file = open(filename, "x")
    except FileExistsError:
        # Get revision number
        start = filename.find("_r") + 2
        end = filename.find(".", start, -1)
        rev = filename[start:end]
        # Create new file
        while os.path.isfile(filename):
            new_rev = str(int(rev) + 1)
            filename = filename.replace("_r" + rev, "_r" + new_rev)
            rev = new_rev
        file = open(filename, "x")
    file.write(" PIREP ".center(50, '#') + "\n")
    # Record the results from the survey
    for t in range(len(label_widgets_text)):
        if t is 3 or t is 4:
            file.write("".center(50, '#') + "\n")
        file.write(label_text[t] + " " + label_units[t] + ": " + var_list[t].get() + "\n")
    file.write("".center(50, '#') + "\n")
    file.write("NOTES:\n")
    file.write(main_widgets[-2].get("1.0",'end-1c'))
    messagebox.showinfo(title="Entry Complete", message="Thank you for your PIREP")
    file.close()

    return


frame = Frame(height=2, bd=10, )
frame.grid(row=0, column=0)
# Populate the labels on the left and right
for i in range(len(label_text)):
    label_widgets_text.append(Label(frame, text=label_text[i]).grid(row=i, column=0, sticky=E))
    label_widgets_units.append(Label(frame, text=label_units[i]).grid(row=i, column=3,  sticky=W))


location = StringVar()
day = StringVar()
user = StringVar()
rating = StringVar()
clouds = StringVar()
cloudbase = StringVar()
honesty = StringVar()
average_thermal = StringVar()
turbulence = StringVar()
thermal_spacing = StringVar()
max_thermal = StringVar()
over_dev = StringVar()
wind_speed = StringVar()
wind_dir = StringVar()

var_list = [location,
            day,
            user,
            rating,
            clouds,
            cloudbase,
            honesty,
            average_thermal,
            turbulence,
            thermal_spacing,
            max_thermal,
            over_dev,
            wind_speed,
            wind_dir]

row_var = 0
index_var = 0
vert_pad = 5

# Populate main widgets in the center of the window
main_widgets.append(Entry(frame, textvariabl = location, width=10))
location.set("PSS")
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
row_var += 1
index_var += 1
main_widgets.append(Entry(frame, textvariabl = day, width=10))
day.set(str(datetime.now().date()))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
row_var += 1
index_var += 1
main_widgets.append(ttk.Combobox(frame, values=["T CLARK","C COOK","B HILLS", "J ALSPAUGH", "G GARAVAGLIA","E WHITE"], width=15, textvariable=user))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
main_widgets[index_var].bind("<<ComboboxSelected>>",lambda e: frame.focus())
main_widgets[index_var].current(0)
row_var += 1
index_var += 1
main_widgets.append(Scale(frame, from_=0, to=10, orient=HORIZONTAL, resolution=0.1, variable=rating))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
row_var += 1
index_var += 1
main_widgets.append(Radiobutton(frame, text="YES", variable=clouds, value="YES"))
main_widgets[index_var].grid(row=row_var, column=1, pady=vert_pad, sticky="E")
index_var += 1
main_widgets.append(Radiobutton(frame, text="NO", variable=clouds, value="NO"))
main_widgets[index_var].grid(row=row_var, column=2, sticky="W")
clouds.set(0)
row_var += 1
index_var += 1
main_widgets.append(Scale(frame, from_=3000, to=9000, orient=HORIZONTAL, resolution=50, variable=cloudbase))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
row_var += 1
index_var += 1
main_widgets.append(ttk.Combobox(frame, values=["SUBURB","GOOD","OK", "NOT GREAT"], width=15, textvariable=honesty))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
main_widgets[index_var].bind("<<ComboboxSelected>>",lambda e: frame.focus())
row_var += 1
index_var += 1
main_widgets.append(Scale(frame, from_=.1, to=10, orient=HORIZONTAL, resolution=0.1, variable=average_thermal))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
row_var += 1
index_var += 1
main_widgets.append(ttk.Combobox(frame, values=["VERY HIGH","HIGH","MEDIUM", "LOW"], width=15, textvariable=turbulence))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
main_widgets[index_var].bind("<<ComboboxSelected>>",lambda e: frame.focus())
row_var += 1
index_var += 1
main_widgets.append(Scale(frame, from_=0.5, to=10, orient=HORIZONTAL, resolution=0.1, variable=thermal_spacing))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
row_var += 1
index_var += 1
main_widgets.append(Scale(frame, from_=1, to=10, orient=HORIZONTAL, resolution=0.1, variable=max_thermal))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
row_var += 1
index_var += 1
main_widgets.append(Radiobutton(frame, text="YES", variable=over_dev, value="YES"))
main_widgets[index_var].grid(row=row_var, column=1, pady=vert_pad, sticky="E")
index_var += 1
main_widgets.append(Radiobutton(frame, text="NO", variable=over_dev, value="NO"))
main_widgets[index_var].grid(row=row_var, column=2, sticky="W")
over_dev.set(0)
row_var += 1
index_var += 1
main_widgets.append(Scale(frame, from_=1, to=30, orient=HORIZONTAL, resolution=1, variable=wind_speed))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
row_var += 1
index_var += 1
main_widgets.append(Scale(frame, from_=0, to=359, orient=HORIZONTAL, resolution=1, variable=wind_dir))
main_widgets[index_var].grid(row=row_var, column=1, columnspan=2, pady=vert_pad)
row_var += 1
index_var += 1
main_widgets.append(Text(frame, height=4, width=50))
main_widgets[index_var].grid(row=row_var, column=0, columnspan=4, pady=vert_pad)
row_var += 1
index_var += 1
main_widgets.append(Button(frame, text="CREATE", command=write_pirep_file))
main_widgets[index_var].grid(row=row_var, column=0, columnspan=4, pady=vert_pad)


root.mainloop()
