import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import os.path
import imghdr
import tomograph as tgraph


def image_from_array(image_array, size=None):
    image = Image.fromarray(np.uint8(image_array))
    if size is not None:
        image = image.resize(size, Image.ANTIALIAS)
    photo_image = ImageTk.PhotoImage(image)
    return photo_image


class TomographApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True,
                            padx=40, pady=40)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.title("Tomograph simulator")
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.quit_app)
        self.bind(sequence='<Escape>', func=self.quit_app)

        self.show_frame(StartPage(self, self.container))

    def show_frame(self, frame):
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def quit_app(self, event=None):
        self.quit()


class StartPage(tk.Frame):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        self.alpha_valid = False
        self.detectors_number_valid = False
        self.detectors_range_valid = False
        self.image_valid = False

        tk_frame_inputs = tk.Frame(self)
        tk_frame_inputs.pack(side="top", padx=10, pady=5)

        tk.Label(tk_frame_inputs, text="Alpha").grid(row=0, column=0)
        validate_alpha_command = self.register(self.validate_alpha)
        self.alpha_entry = tk.Entry(tk_frame_inputs, background='white',
                                    validate='key', validatecommand=(validate_alpha_command, '%P'))
        self.alpha_entry.grid(row=0, column=1, sticky='w')

        tk.Label(tk_frame_inputs, text="Detectors number").grid(row=1, column=0)
        validate_detectors_number_command = self.register(self.validate_detectors_number)
        self.detectors_number_entry = tk.Entry(tk_frame_inputs, background='white',
                                               validate='key',
                                               validatecommand=(validate_detectors_number_command, '%P'))
        self.detectors_number_entry.grid(row=1, column=1, sticky='w')

        tk.Label(tk_frame_inputs, text="Detectors range").grid(row=2, column=0)
        validate_detectors_range_command = self.register(self.validate_detectors_range)
        self.detectors_range_entry = tk.Entry(tk_frame_inputs, background='white',
                                              validate='key', validatecommand=(validate_detectors_range_command, '%P'))
        self.detectors_range_entry.grid(row=2, column=1, sticky='w')

        tk.Label(tk_frame_inputs, text="Image path").grid(row=3, column=0)
        validate_image_command = self.register(self.validate_image)
        self.image_entry = tk.Entry(tk_frame_inputs, background='white',
                                    validate='key', validatecommand=(validate_image_command, '%P'))
        self.image_entry.grid(row=3, column=1, sticky='w')

        tk_frame_menu = tk.Frame(self)
        tk_frame_menu.pack(side="bottom", pady=(15, 0))

        self.full_tomography_button = tk.Button(tk_frame_menu, text="Full tomography",
                                                command=lambda: self.start_app(FinalResultPage), state='disabled')
        self.full_tomography_button.pack(side="left", padx=3)
        self.iteration_tomography_button = tk.Button(tk_frame_menu, text="Iteration tomography",
                                                     command=lambda: self.start_app(IterationResultPage),
                                                     state='disabled')
        self.iteration_tomography_button.pack(side="left", padx=3)

        tk.Button(tk_frame_menu, text='Quit', command=controller.quit_app) \
            .pack(side="left", padx=10)

    def start_app(self, ResultPage):
        self.controller.show_frame(
            ResultPage(float(self.alpha_entry.get()), int(self.detectors_number_entry.get()),
                       float(self.detectors_range_entry.get()), self.image_entry.get(),
                       self.controller, self.parent)
        )

    def validate_alpha(self, value):
        try:
            float(value)
            self.alpha_valid = True
            if (self.alpha_valid and self.detectors_number_valid
                and self.detectors_range_valid and self.image_valid):
                self.form_valid()
        except ValueError:
            self.alpha_valid = False
            self.form_invalid()
        return True

    def validate_detectors_number(self, value):
        try:
            int(value)
            self.detectors_number_valid = True
            if (self.alpha_valid and self.detectors_number_valid
                and self.detectors_range_valid and self.image_valid):
                self.form_valid()
        except ValueError:
            self.detectors_number_valid = False
            self.form_invalid()
        return True

    def validate_detectors_range(self, value):
        try:
            float(value)
            self.detectors_range_valid = True
            if (self.alpha_valid and self.detectors_number_valid
                and self.detectors_range_valid and self.image_valid):
                self.form_valid()
        except ValueError:
            self.detectors_range_valid = False
            self.form_invalid()
        return True

    def validate_image(self, value):
        if os.path.isfile(value) and imghdr.what(value):
            self.image_valid = True
            if (self.alpha_valid and self.detectors_number_valid
                and self.detectors_range_valid and self.image_valid):
                self.form_valid()
        else:
            self.image_valid = False
            self.form_invalid()
        return True

    def form_invalid(self):
        self.full_tomography_button['state'] = 'disabled'
        self.iteration_tomography_button['state'] = 'disabled'

    def form_valid(self):
        self.full_tomography_button['state'] = 'active'
        self.iteration_tomography_button['state'] = 'active'


class FinalResultPage(tk.Frame):
    def __init__(self, alpha, detectors_number, detectors_range, image_path, controller, parent=None):
        super().__init__(parent)

        image = tgraph.imread_square(image_path)
        sinogram = tgraph.radon_transform(alpha, detectors_number, detectors_range, image)

        tk_frame_images = tk.Frame(self)
        tk_frame_images.pack(side="top")

        tk_frame_input = tk.Frame(tk_frame_images)
        tk_frame_input.pack(side="left", padx=10, pady=10)
        input_image = image_from_array(image, size=(300, 300))
        tk.Label(tk_frame_input, text="Input image") \
            .pack(side="top", fill=tk.X)
        tk_input_image = tk.Label(tk_frame_input, image=input_image, width=300, height=300)
        tk_input_image.image = input_image
        tk_input_image.pack(side="bottom")

        tk_frame_sinogram = tk.Frame(tk_frame_images)
        tk_frame_sinogram.pack(side="left", padx=10, pady=10)
        sinogram_image = image_from_array(sinogram, size=(150, 600))
        tk.Label(tk_frame_sinogram, text="Sinogram") \
            .pack(side="top")
        tk_sinogram_image = tk.Label(tk_frame_sinogram, image=sinogram_image, width=150, height=600)
        tk_sinogram_image.image = sinogram_image
        tk_sinogram_image.pack(side="bottom")

        tk_frame_output = tk.Frame(tk_frame_images)
        tk_frame_output.pack(side="left", padx=10, pady=10)
        output = tgraph.image_reconstruction(alpha, detectors_number, detectors_range, sinogram,
                                             image.shape[0])
        output_image = image_from_array(output, size=(300, 300))
        tk.Label(tk_frame_output, text="Output image") \
            .pack(side="top")
        tk_output_image = tk.Label(tk_frame_output, image=output_image, width=300, height=300)
        tk_output_image.image = output_image
        tk_output_image.pack(side="bottom")

        tk_frame_menu = tk.Frame(self)
        tk_frame_menu.pack(side="bottom", fill=tk.X)
        tk.Button(tk_frame_menu, text="Quit", command=controller.quit_app) \
            .pack(side="right")


class IterationResultPage(tk.Frame):
    def __init__(self, alpha, detectors_number, detectors_range, image_path, controller, parent=None):
        super().__init__(parent)
        self.alpha = alpha
        self.detectors_number = detectors_number
        self.detectors_range = detectors_range
        self.image = tgraph.imread_square(image_path)

        tk_frame_images = tk.Frame(self)
        tk_frame_images.pack(side="top")

        tk_frame_input = tk.Frame(tk_frame_images)
        tk_frame_input.pack(side="left", padx=10, pady=10)
        input_image = image_from_array(self.image, (300, 300))
        tk.Label(tk_frame_input, text="Input image") \
            .pack(side="top", fill=tk.X)
        tk_input_image = tk.Label(tk_frame_input, image=input_image, width=300, height=300)
        tk_input_image.image = input_image
        tk_input_image.pack(side="bottom")

        tk_frame_sinogram = tk.Frame(tk_frame_images)
        tk_frame_sinogram.pack(side="left", padx=10, pady=10)
        sinogram_image = image_from_array(np.zeros((600, 150)))
        tk.Label(tk_frame_sinogram, text="Sinogram") \
            .pack(side="top")
        self.tk_sinogram_image = tk.Label(tk_frame_sinogram, image=sinogram_image, width=150, height=600)
        self.tk_sinogram_image.image = sinogram_image
        self.tk_sinogram_image.pack(side="bottom")

        tk_frame_output = tk.Frame(tk_frame_images)
        tk_frame_output.pack(side="left", padx=10, pady=10)
        output_image = image_from_array(np.zeros((300, 300)))
        tk.Label(tk_frame_output, text="Output image") \
            .pack(side="top")
        self.tk_output_image = tk.Label(tk_frame_output, image=output_image, width=300, height=300)
        self.tk_output_image.image = output_image
        self.tk_output_image.pack(side="bottom")

        tk_frame_menu = tk.Frame(self)
        tk_frame_menu.pack(side="bottom", pady=30, fill=tk.X)
        tk.Label(tk_frame_menu, text="Progress [%]")\
            .pack(side="left")
        self.tk_percentage_scale = tk.Scale(tk_frame_menu, from_=0, to=100, length=300, orient=tk.HORIZONTAL)
        self.tk_percentage_scale.pack(side="left")
        tk.Button(tk_frame_menu, text="Run", command=self.update_output) \
            .pack(side="left", padx=10)
        tk.Button(tk_frame_menu, text="Quit", command=controller.quit_app) \
            .pack(side="right")

    def update_output(self):
        percentage = int(self.tk_percentage_scale.get())
        sinogram = tgraph.radon_transform(self.alpha, self.detectors_number,
                                          self.detectors_range, self.image,
                                          percentage)
        sinogram_image = image_from_array(sinogram, (150, 600))
        self.tk_sinogram_image.configure(image=sinogram_image)
        self.tk_sinogram_image.image = sinogram_image

        output = tgraph.image_reconstruction(self.alpha, self.detectors_number,
                                             self.detectors_range, sinogram,
                                             self.image.shape[0], percentage)
        output_image = image_from_array(output, (300, 300))
        self.tk_output_image.configure(image=output_image)
        self.tk_output_image.image = output_image












