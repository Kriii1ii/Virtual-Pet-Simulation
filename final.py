import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

ctk.set_appearance_mode("dark")
background_color = "#FFFECE"
secondary_color = "#FFD0C7"
primary_color = "#E69DB8"
accent_color = "#F1E7E7"
text_color = "#000000"
white_color = "#FFFFFF"


class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self._hunger = 5
        self._energy = 5
        self._happiness = 5
        self.max_hunger = 10
        self.max_energy = 10
        self.max_happiness = 10

    def feed(self):
        if self._hunger > 0:
            self._hunger -= 1
            self.show_message(f"{self.name} ate some food!")

    def rest(self):
        if self._energy < self.max_energy:
            self._energy += 1
            self.show_message(f"{self.name} took a nap!")

    def play(self):
        if self._energy > 0:
            self._energy -= 1
            if self._happiness < self.max_happiness:
                self._happiness += 1
            self.show_message(f"{self.name} played with you!")

    def get_status(self):
        return {
            "Hunger": self._hunger,
            "Energy": self._energy,
            "Happiness": self._happiness,
        }

    def make_sound(self):
        return f"{self.name} makes a sound."

    def get_emotion(self):
        if self._hunger >= 8 or self._energy <= 2:
            return "crying"
        elif self._happiness >= 8:
            return "happy"
        else:
            return "neutral"

    def show_message(self, text):
        if hasattr(self, 'message_label'):
            self.message_label.configure(text=text)
            self.root.after(3000, self.clear_message)

    def clear_message(self):
        if hasattr(self, 'message_label'):
            self.message_label.configure(text="")


class Dog(Pet):
    def __init__(self, name):
        super().__init__(name, "dog")

    def make_sound(self):
        return f"{self.name} says: Woof!"


class Cat(Pet):
    def __init__(self, name):
        super().__init__(name, "cat")

    def make_sound(self):
        return f"{self.name} says: Meow!"


class Rabbit(Pet):
    def __init__(self, name):
        super().__init__(name, "rabbit")

    def make_sound(self):
        return f"{self.name} says: Squeak!"

    def hop(self):
        self.show_message(f"{self.name} hops around!")


class Hamster(Pet):
    def __init__(self, name):
        super().__init__(name, "hamster")

    def make_sound(self):
        return f"{self.name} says: *Cheep*!"

    def run_on_wheel(self):
        self.show_message(f"{self.name} is running on the wheel!")


#GUI Class: user interface 
class PetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet Simulator")
        self.pet = None
        self.image_label = None
        self.root.geometry("500x500")
        self.root.configure(bg=background_color)

        self.frame = ctk.CTkFrame(root, corner_radius=20, bg_color=secondary_color,
                                 fg_color=secondary_color)
        self.frame.pack(padx=20, pady=20)

        self.title = ctk.CTkLabel(self.frame, text="Purrfect Pets", font=("Serif", 30),
                                  text_color=text_color)
        self.title.grid(row=0, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self.frame, text="Pet Name:", text_color=text_color).grid(row=1, column=0,
                                                                           sticky="e")
        self.name_entry = ctk.CTkEntry(self.frame, bg_color=secondary_color,
                                       text_color=white_color)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.frame, text="Pet Type:", text_color=text_color).grid(row=2, column=0,
                                                                           sticky="e")
        self.pet_type = ctk.CTkOptionMenu(self.frame,
                                          values=["dog", "cat", "rabbit", "hamster"],
                                          bg_color=secondary_color, text_color=text_color,
                                          button_color=primary_color,
                                          dropdown_fg_color=secondary_color,
                                          dropdown_text_color=text_color)
        self.pet_type.grid(row=2, column=1, padx=5, pady=5)

        self.start_button = ctk.CTkButton(self.frame, text="Start Game",
                                          command=self.start_game,
                                          bg_color=accent_color, fg_color=text_color,
                                          hover_color=primary_color)
        self.start_button.grid(row=3, columnspan=2, pady=10)

        # Progress bars to show hunger, energy, ani happiness
        self.hunger_label = ctk.CTkLabel(self.frame, text="Hunger:",
                                         text_color=text_color)
        self.hunger_label.grid(row=4, column=0, sticky="e", padx=5, pady=2)
        self.hunger_bar = ctk.CTkProgressBar(self.frame, progress_color="green",
                                             fg_color=white_color)
        self.hunger_bar.grid(row=4, column=1, padx=5, pady=2)

        self.energy_label = ctk.CTkLabel(self.frame, text="Energy:",
                                         text_color=text_color)
        self.energy_label.grid(row=5, column=0, sticky="e", padx=5, pady=2)
        self.energy_bar = ctk.CTkProgressBar(self.frame, progress_color="blue",
                                             fg_color=white_color)
        self.energy_bar.grid(row=5, column=1, padx=5, pady=2)

        self.happiness_label = ctk.CTkLabel(self.frame, text="Happiness:",
                                            text_color=text_color)
        self.happiness_label.grid(row=6, column=0, sticky="e", padx=5, pady=2)
        self.happiness_bar = ctk.CTkProgressBar(self.frame,
                                                 progress_color="yellow",
                                                 fg_color=white_color)
        self.happiness_bar.grid(row=6, column=1, padx=5, pady=2)

        self.status_label = ctk.CTkLabel(self.frame, text="", font=("Serif", 14),
                                         text_color=text_color)
        self.status_label.grid_forget()

        self.feed_btn = ctk.CTkButton(self.frame, text="Feed",
                                      command=self.feed_pet, state="disabled",
                                      bg_color=accent_color, fg_color=text_color,
                                      hover_color=primary_color)
        self.feed_btn.grid(row=7, column=0, padx=5, pady=5)
        self.play_btn = ctk.CTkButton(self.frame, text="Play",
                                     command=self.play_pet, state="disabled",
                                     bg_color=accent_color, fg_color=text_color,
                                     hover_color=primary_color)
        self.play_btn.grid(row=7, column=1, padx=5, pady=5)
        self.rest_btn = ctk.CTkButton(self.frame, text="Rest",
                                     command=self.rest_pet, state="disabled",
                                     bg_color=accent_color, fg_color=text_color,
                                     hover_color=primary_color)
        self.rest_btn.grid(row=8, column=0, padx=5, pady=5)
        self.sound_btn = ctk.CTkButton(self.frame, text="Hear Sound",
                                      command=self.hear_pet, state="disabled",
                                      bg_color=accent_color, fg_color=text_color,
                                      hover_color=primary_color)
        self.sound_btn.grid(row=8, column=1, padx=5, pady=5)

        self.extra_action_btn = None

        self.pet_image_label = ctk.CTkLabel(self.frame, text="")
        self.pet_image_label.grid(row=9, columnspan=2, pady=10)

        self.message_label = ctk.CTkLabel(self.frame, text="",
                                         font=("Serif", 12, "italic"),
                                         text_color=text_color)
        self.message_label.grid(row=10, columnspan=2, pady=5)
        self.root.message_label = self.message_label

    def start_game(self):
        name = self.name_entry.get()
        ptype = self.pet_type.get()

        if not name:
            messagebox.showerror("Error", "Please enter a name for your pet.")
            return

        if ptype == "dog":
            self.pet = Dog(name)
        elif ptype == "cat":
            self.pet = Cat(name)
        elif ptype == "rabbit":
            self.pet = Rabbit(name)
        elif ptype == "hamster":
            self.pet = Hamster(name)
        else:
            messagebox.showerror("Error", "Invalid pet type.")
            return

        self.pet.root = self.root
        self.update_status()
        self.update_pet_image()
        self.enable_buttons()
        self.configure_extra_button()

    def configure_extra_button(self):
        if self.extra_action_btn:
            self.extra_action_btn.destroy()

        if isinstance(self.pet, Rabbit):
            self.extra_action_btn = ctk.CTkButton(self.frame, text="Hop",
                                                 command=self.pet.hop,
                                                 bg_color=accent_color,
                                                 fg_color=text_color,
                                                 hover_color=primary_color)
            self.extra_action_btn.grid(row=8, column=1, padx=5, pady=5)
        elif isinstance(self.pet, Hamster):
            self.extra_action_btn = ctk.CTkButton(self.frame, text="Run on Wheel",
                                                 command=self.pet.run_on_wheel,
                                                 bg_color=accent_color,
                                                 fg_color=text_color,
                                                 hover_color=primary_color)
            self.extra_action_btn.grid(row=8, column=1, padx=5, pady=5)

    def update_status(self):
        if self.pet:
            status = self.pet.get_status()
            self.hunger_bar.set(status['Hunger'] / self.pet.max_hunger)
            self.energy_bar.set(status['Energy'] / self.pet.max_energy)
            self.happiness_bar.set(
                status['Happiness'] / self.pet.max_happiness)
            self.update_pet_image()

    def update_pet_image(self):
        if self.pet:
            emotion = self.pet.get_emotion()
            pet_type = self.pet.species
            image_path = f"{pet_type}_{emotion}.png"
            display_size = (200, 200)

            if os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    img = img.resize((300, 300))
                    self.pet_image = ctk.CTkImage(light_image=img,
                                                  dark_image=img,
                                                  size=display_size)
                    self.pet_image_label.configure(image=self.pet_image,
                                                   text="")
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
                    self.pet_image_label.configure(
                        text=f"[Error loading {pet_type} {emotion} image]",
                        image="")
            else:
                self.pet_image_label.configure(
                    text=f"[{pet_type} {emotion} image missing]", image="")

    def enable_buttons(self):
        self.feed_btn.configure(state="normal")
        self.play_btn.configure(state="normal")
        self.rest_btn.configure(state="normal")
        self.sound_btn.configure(state="normal")

    def feed_pet(self):
        if self.pet:
            self.pet.feed()
            self.update_status()

    def play_pet(self):
        if self.pet:
            self.pet.play()
            self.update_status()

    def rest_pet(self):
        if self.pet:
            self.pet.rest()
            self.update_status()

    def hear_pet(self):
        if self.pet:
            messagebox.showinfo("Pet Sound", self.pet.make_sound())


if __name__ == "__main__":
    root = ctk.CTk()
    app = PetApp(root)
    root.mainloop()
