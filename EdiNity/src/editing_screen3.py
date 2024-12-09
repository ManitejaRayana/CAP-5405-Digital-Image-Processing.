import tkinter as tk
from tkinter import messagebox, Toplevel, Scale, HORIZONTAL
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageFilter
from shared import add_logo, create_menu  # Import shared utilities

class EditingScreen:
    def __init__(self, root, uploaded_image_path=None):
        self.root = root
        self.canvas = None
        self.image_label = None
        self.uploaded_image_path = uploaded_image_path
        self.original_image = None
        self.current_image = None
        self.history = []  # Stack for Undo/Redo functionality
        self.future = []
        self.init_ui()

    def init_ui(self):
        """Initialize the editing screen UI."""
        self.root.config(bg="#EEECE7")
        for widget in self.root.winfo_children():
            widget.destroy()

        # === Top Buttons ===
        self.add_top_buttons()

        # === Canvas Layout ===
        self.canvas = tk.Canvas(self.root, width=1400, height=650, bg="#EEECE7", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # === Bottom Toolbar ===
        self.add_toolbar()

        # === Center Area for Image Display ===
        self.root.after(100, self.display_image)  # Delay to ensure canvas dimensions are initialized

    def add_top_buttons(self):
        """Add top buttons in the logo row for navigation and actions."""
        # Create a frame for the top buttons
        top_buttons_frame = tk.Frame(self.root, bg="#EEECE7")
        top_buttons_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Add Logo
        logo_path = "assets/logo_head.png"
        logo_label = tk.Label(top_buttons_frame, bg="#EEECE7")
        logo_image = Image.open(logo_path).resize((100, 50), Image.ANTIALIAS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label.config(image=logo_photo)
        logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        logo_label.pack(side=tk.LEFT, padx=10)

        # Add buttons on the right side of the frame
        button_config = {
            "bg": "#444",
            "fg": "white",
            "font": ("Arial", 12, "bold"),
            "padx": 10,
        }

        # Undo Button
        undo_button = tk.Button(
            top_buttons_frame, text="Undo", command=self.undo_action, **button_config
        )
        undo_button.pack(side=tk.RIGHT, padx=10)

        # Redo Button
        redo_button = tk.Button(
            top_buttons_frame, text="Redo", command=self.redo_action, **button_config
        )
        redo_button.pack(side=tk.RIGHT, padx=10)

        # Save Button
        save_button = tk.Button(
            top_buttons_frame, text="Save", command=lambda: print("Save clicked"), **button_config
        )
        save_button.pack(side=tk.RIGHT, padx=10)

        # Menu Button
        menu_canvas = tk.Canvas(top_buttons_frame, width=30, height=30, bg="#EEECE7", bd=0, highlightthickness=0)
        menu_canvas.create_line(5, 7, 25, 7, fill="black", width=3)
        menu_canvas.create_line(5, 15, 25, 15, fill="black", width=3)
        menu_canvas.create_line(5, 23, 25, 23, fill="black", width=3)
        menu_canvas.pack(side=tk.RIGHT, padx=10)

        menu_canvas.bind(
            "<Button-1>",
            lambda e: create_menu(self.root, x=menu_canvas.winfo_rootx(), y=menu_canvas.winfo_rooty() + 40),
        )

    def display_image(self):
        """Display the uploaded image on the canvas without overlapping buttons or toolbars."""
        if self.uploaded_image_path:
            try:
                # Open and resize the uploaded image
                self.original_image = Image.open(self.uploaded_image_path)
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()

                # Adjust dimensions to fit within the canvas
                image_width, image_height = self.original_image.size
                max_width = canvas_width
                max_height = canvas_height - 100  # Leave space for buttons and toolbar

                resize_ratio = min(max_width / image_width, max_height / image_height, 1)
                new_width = int(image_width * resize_ratio)
                new_height = int(image_height * resize_ratio)

                resized_image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)
                self.current_image = resized_image  # Save the resized image
                self.history.append(resized_image.copy())  # Add to history for undo functionality

                # Convert to PhotoImage and display centered
                tk_image = ImageTk.PhotoImage(resized_image)
                x_offset = (canvas_width - new_width) // 2
                y_offset = (canvas_height - new_height) // 2

                self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=tk_image)
                self.canvas.image = tk_image  # Keep reference to avoid garbage collection
            except FileNotFoundError:
                tk.Label(self.canvas, text="Image Not Found", font=("Arial", 16), fg="black", bg="#EEECE7").place(x=50, y=50)
        else:
            tk.Label(self.canvas, text="No Image Uploaded", font=("Arial", 16), fg="black", bg="#EEECE7").place(x=50, y=50)

    def add_toolbar(self):
        """Add the toolbar with editing tools."""
        toolbar_height = 50  # Fixed height for the toolbar
        self.canvas.config(height=600 - toolbar_height)  # Adjust canvas height to fit toolbar

        # Create the toolbar frame
        toolbar_frame = tk.Frame(self.root, bg="#2D3030", height=toolbar_height)
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Define the tools with their actions and icons
        tools = [
            ("Crop", self.crop_tool, "assets/crop.png"),
            ("Adjust", self.adjust_tool, "assets/controller.png"),
            ("Filters", self.filters_tool, "assets/filter.png"),
            ("Effects", self.effects_tool, "assets/beauty.png"),
            ("Reset", self.reset_tool, "assets/circular.png"),
        ]

        for tool_name, tool_action, icon_path in tools:
            try:
                # Load and resize tool icon
                icon = Image.open(icon_path).resize((40, 40), Image.ANTIALIAS)
                icon_photo = ImageTk.PhotoImage(icon)

                # Create a button for the tool
                tool_button = tk.Button(
                    toolbar_frame,
                    image=icon_photo,
                    command=tool_action,
                    bg="#2D3030",
                    activebackground="#3A3A3A",
                    borderwidth=0,
                )
                tool_button.image = icon_photo  # Keep a reference to avoid garbage collection
                tool_button.pack(side=tk.LEFT, padx=20, pady=5)
            except FileNotFoundError:
                print(f"Icon not found for tool: {tool_name}")





    def crop_tool(self):
        """Activate cropping functionality."""
        self.canvas.bind("<Button-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.finish_crop)
        messagebox.showinfo("Crop", "Drag to select the area to crop.")

    def start_crop(self, event):
        """Start the cropping rectangle."""
        self.start_x, self.start_y = event.x, event.y
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2
        )

    def update_crop(self, event):
        """Update the cropping rectangle as the user drags."""
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def finish_crop(self, event):
        """Finalize cropping and update the image."""
        end_x, end_y = event.x, event.y
        crop_box = (
            min(self.start_x, end_x),
            min(self.start_y, end_y),
            max(self.start_x, end_x),
            max(self.start_y, end_y),
        )

        if self.current_image:
            # Convert crop_box to relative coordinates in the image
            image_width, image_height = self.original_image.size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            x_ratio = image_width / canvas_width
            y_ratio = image_height / canvas_height

            adjusted_box = (
                int(crop_box[0] * x_ratio),
                int(crop_box[1] * y_ratio),
                int(crop_box[2] * x_ratio),
                int(crop_box[3] * y_ratio),
            )

            cropped = self.original_image.crop(adjusted_box)
            self.current_image = cropped
            self.history.append(cropped.copy())

            resized_cropped = cropped.resize((500, 400), Image.ANTIALIAS)
            tk_cropped = ImageTk.PhotoImage(resized_cropped)

            self.image_label.config(image=tk_cropped)
            self.image_label.image = tk_cropped  # Update reference to avoid garbage collection
            messagebox.showinfo("Crop", "Image cropped successfully.")


    def adjust_tool(self):
        """Adjust the image."""
        adjust_window = Toplevel(self.root)
        adjust_window.title("Adjust Image")

        tk.Label(adjust_window, text="Brightness").pack()
        brightness_slider = Scale(adjust_window, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL)
        brightness_slider.set(1.0)
        brightness_slider.pack()

        tk.Label(adjust_window, text="Contrast").pack()
        contrast_slider = Scale(adjust_window, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL)
        contrast_slider.set(1.0)
        contrast_slider.pack()

        tk.Label(adjust_window, text="Saturation").pack()
        saturation_slider = Scale(adjust_window, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL)
        saturation_slider.set(1.0)
        saturation_slider.pack()

        def apply_adjustments():
            """Apply adjustments to the current image."""
            brightness = brightness_slider.get()
            contrast = contrast_slider.get()
            saturation = saturation_slider.get()

            if self.current_image:
                enhanced_image = self.original_image.copy()
                enhancer = ImageEnhance.Brightness(enhanced_image)
                enhanced_image = enhancer.enhance(brightness)

                enhancer = ImageEnhance.Contrast(enhanced_image)
                enhanced_image = enhancer.enhance(contrast)

                enhancer = ImageEnhance.Color(enhanced_image)
                enhanced_image = enhancer.enhance(saturation)

                self.current_image = enhanced_image
                self.history.append(enhanced_image.copy())
                resized_enhanced = enhanced_image.resize((500, 400), Image.ANTIALIAS)
                tk_enhanced = ImageTk.PhotoImage(resized_enhanced)

                self.image_label.config(image=tk_enhanced)
                self.image_label.image = tk_enhanced  # Update reference to avoid garbage collection
                messagebox.showinfo("Adjust", "Adjustments applied successfully.")
                adjust_window.destroy()

        apply_button = tk.Button(adjust_window, text="Apply", command=apply_adjustments)
        apply_button.pack()

    def filters_tool(self):
        """Apply filters to the image."""
        filter_window = Toplevel(self.root)
        filter_window.title("Filters")

        def apply_filter(filter_type):
            """Apply the selected filter."""
            if self.current_image:
                filtered_image = self.current_image.copy()
                if filter_type == "Black & White":
                    filtered_image = ImageOps.grayscale(filtered_image)
                elif filter_type == "Sepia":
                    sepia_image = ImageOps.colorize(ImageOps.grayscale(filtered_image), "#704214", "#C0A080")
                    filtered_image = sepia_image
                elif filter_type == "Vintage":
                    filtered_image = filtered_image.filter(ImageFilter.CONTOUR)

                self.current_image = filtered_image
                self.history.append(filtered_image.copy())
                resized_filtered = filtered_image.resize((500, 400), Image.ANTIALIAS)
                tk_filtered = ImageTk.PhotoImage(resized_filtered)

                self.image_label.config(image=tk_filtered)
                self.image_label.image = tk_filtered  # Update reference to avoid garbage collection
                messagebox.showinfo("Filters", f"{filter_type} filter applied successfully.")
                filter_window.destroy()

        tk.Button(filter_window, text="Black & White", command=lambda: apply_filter("Black & White")).pack(pady=10)
        tk.Button(filter_window, text="Sepia", command=lambda: apply_filter("Sepia")).pack(pady=10)
        tk.Button(filter_window, text="Vintage", command=lambda: apply_filter("Vintage")).pack(pady=10)

    def effects_tool(self):
        """Apply effects to the image."""
        effects_window = Toplevel(self.root)
        effects_window.title("Effects")

        def apply_effect(effect_type):
            """Apply the selected effect."""
            if self.current_image:
                effected_image = self.current_image.copy()
                if effect_type == "Blur":
                    effected_image = effected_image.filter(ImageFilter.BLUR)
                elif effect_type == "Sharpen":
                    effected_image = effected_image.filter(ImageFilter.SHARPEN)
                elif effect_type == "Vignette":
                    mask = Image.new("L", effected_image.size, 0)
                    for x in range(mask.width):
                        for y in range(mask.height):
                            d = min(x, mask.width - x, y, mask.height - y)
                            mask.putpixel((x, y), int(255 * (d / (min(mask.size) // 2))))
                    effected_image.putalpha(mask)

                self.current_image = effected_image
                self.history.append(effected_image.copy())
                resized_effected = effected_image.resize((500, 400), Image.ANTIALIAS)
                tk_effected = ImageTk.PhotoImage(resized_effected)

                self.image_label.config(image=tk_effected)
                self.image_label.image = tk_effected  # Update reference to avoid garbage collection
                messagebox.showinfo("Effects", f"{effect_type} effect applied successfully.")
                effects_window.destroy()

        tk.Button(effects_window, text="Blur", command=lambda: apply_effect("Blur")).pack(pady=10)
        tk.Button(effects_window, text="Sharpen", command=lambda: apply_effect("Sharpen")).pack(pady=10)
        tk.Button(effects_window, text="Vignette", command=lambda: apply_effect("Vignette")).pack(pady=10)

    def reset_tool(self):
        """Reset the image to its original state."""
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.history = [self.original_image.copy()]  # Reset history
            resized_original = self.original_image.resize((500, 400), Image.ANTIALIAS)
            tk_original = ImageTk.PhotoImage(resized_original)

            self.image_label.config(image=tk_original)
            self.image_label.image = tk_original  # Update reference to avoid garbage collection
            messagebox.showinfo("Reset", "Image reset to original.")

    def undo_action(self):
        """Undo the last action."""
        if len(self.history) > 1:
            self.future.append(self.history.pop())  # Move current state to future stack
            self.current_image = self.history[-1]
            resized_image = self.current_image.resize((500, 400), Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(resized_image)

            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image  # Update reference to avoid garbage collection
        else:
            messagebox.showinfo("Undo", "No more actions to undo.")

    def redo_action(self):
        """Redo the last undone action."""
        if self.future:
            self.current_image = self.future.pop()
            self.history.append(self.current_image)
            resized_image = self.current_image.resize((500, 400), Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(resized_image)

            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image  # Update reference to avoid garbage collection
        else:
            messagebox.showinfo("Redo", "No more actions to redo.")
