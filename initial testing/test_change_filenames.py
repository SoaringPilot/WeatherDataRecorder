import os
t_path = "../maps/2020-06-01/"

filename_list = os.listdir(t_path)
print("File Name Length: " + str(len(filename_list)))
counter = 0
for filename in filename_list:
    if filename.find("cc_") >= 0:
        print(filename)
    elif filename.find(".png") >= 0:
        os.rename(t_path + filename, t_path + filename.replace(".png", ".PNG"))
        counter += 1
    elif filename.find(".PNG"):
        print("Ready: " + filename)
        counter += 1
print(counter)
