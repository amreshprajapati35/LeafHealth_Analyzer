import cv2
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import sys

def process_image():
    global alpha

    original_image = cv2.imread(filename, 1)
    cv2.imshow("Original Image", original_image)

    blue_channel = original_image[:, :, 0]
    green_channel = original_image[:, :, 1]
    red_channel = original_image[:, :, 2]

    disease_image = red_channel - green_channel
    alpha = blue_channel
    get_alpha(original_image)

    for i in range(original_image.shape[0]):
        for j in range(original_image.shape[1]):
            if int(green_channel[i, j]) > green_threshold:
                disease_image[i, j] = 255

    cv2.imshow("Disease Image", disease_image)
    display_disease_percentage(disease_image)
    main_window.bind('<ButtonRelease-1>', process_image)

def get_alpha(original_image):
    global alpha
    alpha = (original_image[:, :, 0] > 200) & (original_image[:, :, 1] > 200) & (original_image[:, :, 2] > 200)
    alpha = alpha.astype(int) * 255

def get_file():
    return filedialog.askopenfilename(title="Select Image")


def display_disease_percentage(disease_image):
    global alpha
    disease_status = ""
    count = 0
    res = 0
    for i in range(disease_image.shape[0]):
        for j in range(disease_image.shape[1]):
            if alpha[i, j] == 0:
                res += 1
            if disease_image[i, j] < green_threshold:
                count += 1
    
    percent = (count / res) * 100
    disease_status = "Diseased" if percent > 10 else "Healthy"
    
    disease_percent.set("Percentage Disease: {:.2f}%".format(percent))
    disease_status_label.config(text=disease_status)
    disease_status_label.config(fg="green" if disease_status == "Healthy" else "red")
    disease_status_label.config(font=("Helvetica", 16, "bold"))

alpha = None
main_window = tk.Tk()

# ------------------------------------------
main_window.geometry("1500x1000")
bg_image = Image.open("background.jpg")
background = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(image=background)
background_label.place(x=0, y=0)

# -------------------------------------
main_window.title("Plant Disease Detector")

filename = get_file()
green_threshold = 130  #  Desired green threshold value

disease_percent = tk.StringVar()
disease_percent_label = tk.Label(main_window, textvariable=disease_percent)
disease_percent_label.pack(pady=20)  # Add padding to center the label

disease_status_label = tk.Label(main_window, text="", font=("Helvetica", 16, "bold"))
disease_status_label.pack()

if filename != "":
    process_image()
else:
    print("No File!")
    exit(0)

main_window.mainloop()
