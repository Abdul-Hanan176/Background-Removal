import tkinter as tk
from tkinter import filedialog, messagebox
import os
from rembg import remove
from PIL import Image
import cv2
import numpy as np
import io

# Function to remove background (without replacing it)
def remove_background(input_path, output_path):
    try:
        # Load the input image
        input_image = Image.open(input_path)
        
        # Remove background using rembg
        output_data = remove(input_image)  # This returns an image, not bytes
        
        # Convert the output image (rembg result) to RGBA
        output_image = output_data.convert("RGBA")
        
        # Save the output image with the background removed
        output_image.save(output_path)

        print(f"Background removed successfully! Output saved at: {output_path}")
        messagebox.showinfo("Success", f"Background removed successfully! Output saved at: {output_path}")
    
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to remove background and replace it with a new background (from Option 1)
def remove_background_and_replace(input_path, background_path, output_path):
    try:
        # Load the input image
        input_image = Image.open(input_path)
        
        # Remove background using rembg
        output_data = remove(input_image)  # This returns an image, not bytes
        
        # Convert the output image (rembg result) to RGBA
        output_image = output_data.convert("RGBA")
        output_array = np.array(output_image)

        # Load the background image
        background_image = Image.open(background_path)
        
        # Resize the background image to match the input image size
        background_image = background_image.resize(input_image.size)
        background_array = np.array(background_image)

        # Create a mask from the alpha channel of the output image (background removed area)
        mask = output_array[:, :, 3]  # Alpha channel
        mask = np.stack([mask] * 3, axis=-1)  # Make a 3-channel mask (RGB)
        mask = mask / 255  # Normalize to [0, 1] range

        # Replace the background with the new background
        final_image = output_array[:, :, :3] * mask + background_array * (1 - mask)

        # Convert final image back to PIL Image and save
        final_image = Image.fromarray(final_image.astype(np.uint8))
        final_image.save(output_path)

        print(f"Background replaced successfully! Output saved at: {output_path}")
        messagebox.showinfo("Success", f"Background replaced successfully! Output saved at: {output_path}")
    
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function for webcam feed and background removal (updated)
def capture_and_modify_background():
    # Open webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open webcam.")
        return

    print("Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to an image
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Remove background using rembg
        output = remove(pil_img)
        output_np = np.array(output)

        # Convert back to BGR for OpenCV
        frame_no_bg = cv2.cvtColor(output_np, cv2.COLOR_RGB2BGR)

        # Display the processed frame
        cv2.imshow('No Background', frame_no_bg)

        # Press Q to quit the webcam feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main menu in Tkinter
def main_menu():
    root = tk.Tk()
    root.title("Background Removal Tool")

    # Set window size
    root.geometry("400x300")

    # Title label
    title_label = tk.Label(root, text="Choose an Option", font=("Arial", 18))
    title_label.pack(pady=20)

    # Button for Image Background Removal
    def open_image_removal():
        input_path = filedialog.askopenfilename(title="Select Image for Background Removal", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if not input_path:
            return

        background_path = filedialog.askopenfilename(title="Select Background Image", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if not background_path:
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if not output_path:
            return

        remove_background_and_replace(input_path, background_path, output_path)

    button_image_removal = tk.Button(root, text="Image Background Removal", width=30, command=open_image_removal)
    button_image_removal.pack(pady=10)

    # Button for Camera Background Removal (Updated to use the new code)
    def open_camera_removal():
        capture_and_modify_background()

    button_camera_removal = tk.Button(root, text="Open the Camera", width=30, command=open_camera_removal)
    button_camera_removal.pack(pady=10)

    # Button for Remove Background (New Option)
    def open_background_removal():
        input_path = filedialog.askopenfilename(title="Select Image for Background Removal", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if not input_path:
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if not output_path:
            return

        remove_background(input_path, output_path)

    button_remove_background = tk.Button(root, text="Remove Background", width=30, command=open_background_removal)
    button_remove_background.pack(pady=10)

    # Start the Tkinter main loop
    root.mainloop()

# Run the main menu
if __name__ == "__main__":
    main_menu()
