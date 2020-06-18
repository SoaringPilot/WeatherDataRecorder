from tkinter import *

label_text = ["Overall Rating", "Clouds", "Cloudbase", "Average Thermal", "Max on Vario", "Overdeveloped", "Wind Strength",
              "Wind Direction"]
label_units = ["", "", "ft MSL", "knots", "knots", "", "knots", "deg"]
label_widgets = []
main_widgets = []

root = Tk()
frame = Frame(height=2, bd=15, )
frame.grid(row=0,column=0)
for i in range(len(label_text)):
    print(i)
    label_widgets.append(Label(frame, text=label_text[i]).grid(row=i, column=0))
clouds = IntVar()
odev = IntVar()
row_var=0
vert_pad = 10
main_widgets.append(Scale(frame, from_=0, to=10, orient=HORIZONTAL, resolution=0.1).grid(row=row_var,column=1,columnspan=2, pady=vert_pad))
row_var +=1
main_widgets.append(Radiobutton(frame, text="YES", variable=clouds, value=1).grid(row=row_var, column=1, pady=vert_pad, sticky="E"))
main_widgets.append(Radiobutton(frame, text="NO", variable=clouds, value=2).grid(row=row_var, column=2, sticky="W"))
row_var +=1
main_widgets.append(Scale(frame, from_=3000, to=9000, orient=HORIZONTAL, resolution=50).grid(row=row_var,column=1,columnspan=2, pady=vert_pad))
row_var +=1
main_widgets.append(Scale(frame, from_=1, to=10, orient=HORIZONTAL, resolution=0.1).grid(row=row_var,column=1,columnspan=2, pady=vert_pad))
row_var +=1
main_widgets.append(Scale(frame, from_=1, to=10, orient=HORIZONTAL, resolution=0.1).grid(row=row_var,column=1,columnspan=2, pady=vert_pad))
row_var +=1
main_widgets.append(Radiobutton(frame, text="YES", variable=odev, value=1).grid(row=row_var, column=1, pady=vert_pad, sticky="E"))
main_widgets.append(Radiobutton(frame, text="NO", variable=odev, value=2).grid(row=row_var, column=2, sticky="W"))
row_var +=1
main_widgets.append(Scale(frame, from_=1, to=25, orient=HORIZONTAL, resolution=1).grid(row=row_var,column=1,columnspan=2, pady=vert_pad))
row_var +=1
main_widgets.append(Scale(frame, from_=0, to=359, orient=HORIZONTAL, resolution=1).grid(row=row_var,column=1,columnspan=2, pady=vert_pad))
row_var +=1
main_widgets.append(Text(frame, height=6, width=50).grid(row=row_var,column=0,columnspan=3, pady=vert_pad))
# file = open("./test.txt", "w")
# file.write("test sentence")
root.mainloop()
