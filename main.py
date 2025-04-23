from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

# ---------------------------- IMAGE WATERMARK ------------------------------- #

image_path = None
img = None
tk_img = None

def upload_image():
    # Opens file picker with askopenfilename()
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("PNG Files", "*.png"),
            ("JPEG Files", "*.jpg"),
            ("JPEG Files", "*.jpeg"),
            ("BMP Files", "*.bmp"),
            ("GIF Files", "*.gif"),
            ("All Files", "*.*")
        ]
    )
    # Converts selected image to RGBA (for transparency support)
    if file_path:
        global image_path, img
        image_path = file_path
        #Stores it in img and displays it in the canvas via display_image.
        img = Image.open(file_path).convert("RGBA")
        display_image(img)
        #Updates the entry box with the filename.
        photo_entry.delete(0, END)
        photo_entry.insert(0, file_path.split("/")[-1])
    else:
        messagebox.showwarning("Warning", "No File Selected!")

def display_image(pil_img):
    global tk_img
    #Takes image and resizes it to fit inside the canvas
    pil_img.thumbnail((400, 400))
    #Converts it to a Tkinter-compatible image
    tk_img = ImageTk.PhotoImage(pil_img)
    canvas.create_image(0, 0, anchor="nw", image=tk_img)
    canvas.image = tk_img

def generate_watermark():
    global img

    if not img:
        messagebox.showerror("Error", "No image uploaded.")
        return

    watermark_text = watermark_entry.get()
    if not watermark_text.strip():
        messagebox.showerror("Error", "Please enter watermark text.")
        return

    # Creates a transparent image layer the same size as the image
    watermark_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    #Uses ImageDraw to draw the text on this transparent layer
    draw = ImageDraw.Draw(watermark_layer)

    font_size = int(min(img.size) / 15)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    #Places the text in the bottom-right corner
    text_width = draw.textlength(watermark_text, font=font)
    text_height = font_size
    x = img.width - text_width - 10
    y = img.height - text_height - 10

    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

    # Blends the watermark layer and the image using Image.alpha_composite.
    watermarked = Image.alpha_composite(img, watermark_layer)

    # Save result
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Files", "*.png"),
            ("JPEG Files", "*.jpg"),
            ("All Files", "*.*")
        ]
    )
    if save_path:
        watermarked.convert("RGB").save(save_path)
        messagebox.showinfo("Success", f"Image saved to:\n{save_path}")
        display_image(watermarked)
    else:
        messagebox.showwarning("Warning", "Save operation canceled!")

# ---------------------------- USER INTERFACE ------------------------------- #

window = Tk()
window.title("Watermarks The Spot")
window.configure(padx=50, pady=50, bg='#c3e7d5', borderwidth=0, highlightthickness=0)

# Logo
logo_img = Image.open('watermark_logo.png').resize((200, 200))
tk_logo = ImageTk.PhotoImage(logo_img)
canvas = Canvas(width=200, height=200, bg='#c3e7d5', borderwidth=0, highlightthickness=0)
canvas.grid(row=0, column=0)
canvas.create_image(0, 0, anchor="nw", image=tk_logo)

# UI Text
welcome_message = Label(text="Welcome to Watermarks The Spot! \n"
                             "Select a photo you would like to watermark \n "
                             "and the text you would like to place on the image.",
                             bg='#c3e7d5', borderwidth=0, highlightthickness=0)
welcome_message.grid(row=1, column=0)

photo_title = Label(text='Photo:', bg='#c3e7d5')
photo_title.grid(row=2, column=0)

photo_entry = Entry(width=30)
photo_entry.grid(row=3, column=0)

upload_button = Button(text='Upload', width=13, bg='#c3e7d5',
                       borderwidth=0, highlightthickness=0, command=upload_image)
upload_button.grid(row=4, column=0)

watermark_title = Label(text='Watermark Text:', bg='#c3e7d5')
watermark_title.grid(row=6, column=0)

watermark_entry = Entry(width=30)
watermark_entry.grid(row=7, column=0)

submit_button = Button(text='Submit', bg='#c3e7d5',
                       borderwidth=0, highlightthickness=0, command=generate_watermark)
submit_button.grid(row=8, column=0)

window.mainloop()