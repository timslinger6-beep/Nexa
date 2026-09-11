import tkinter as tk


class GameRuntime:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.width = 800
        self.height = 600
        self.background = "black"
        self.keys = set()

    def window(self, title, width, height):
        if not isinstance(title, str):
            raise RuntimeError("window() ben?tigt einen String als Titel.")

        if not isinstance(width, int) or isinstance(width, bool):
            raise RuntimeError("window() ben?tigt eine Ganzzahl f?r die Breite.")

        if not isinstance(height, int) or isinstance(height, bool):
            raise RuntimeError("window() ben?tigt eine Ganzzahl f?r die H?he.")

        if width <= 0 or height <= 0:
            raise RuntimeError("Fenstergr??e muss gr??er als 0 sein.")

        self.width = width
        self.height = height

        if self.root is not None:
            try:
                self.root.destroy()
            except tk.TclError:
                pass

        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            raise RuntimeError(
                f"Grafikfenster konnte nicht erstellt werden: {error}"
            )

        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            highlightthickness=0,
            bg=self.background
        )

        self.canvas.pack()

        self.root.bind("<KeyPress>", self._key_down)
        self.root.bind("<KeyRelease>", self._key_up)

        self.root.focus_force()

    def _key_down(self, event):
        self.keys.add(event.keysym.lower())

    def _key_up(self, event):
        self.keys.discard(event.keysym.lower())

    def require_window(self):
        if self.root is None or self.canvas is None:
            raise RuntimeError(
                "Kein Spielfenster vorhanden. "
                "Rufe zuerst window() auf."
            )

    def clear(self, color="black"):
        self.require_window()

        if not isinstance(color, str):
            raise RuntimeError("clear() ben?tigt eine Farbe als String.")

        self.background = color
        self.canvas.configure(bg=color)
        self.canvas.delete("all")

    def rect(self, x, y, width, height, color="white"):
        self.require_window()

        values = [x, y, width, height]

        if not all(isinstance(value, int) and not isinstance(value, bool)
                   for value in values):
            raise RuntimeError(
                "rect() ben?tigt x, y, width und height als Ganzzahlen."
            )

        if not isinstance(color, str):
            raise RuntimeError("rect() ben?tigt eine Farbe als String.")

        self.canvas.create_rectangle(
            x,
            y,
            x + width,
            y + height,
            fill=color,
            outline=color
        )

    def circle(self, x, y, radius, color="white"):
        self.require_window()

        values = [x, y, radius]

        if not all(isinstance(value, int) and not isinstance(value, bool)
                   for value in values):
            raise RuntimeError(
                "circle() ben?tigt x, y und radius als Ganzzahlen."
            )

        if radius < 0:
            raise RuntimeError("circle() ben?tigt einen Radius >= 0.")

        if not isinstance(color, str):
            raise RuntimeError("circle() ben?tigt eine Farbe als String.")

        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=color,
            outline=color
        )

    def text(self, x, y, value, size=24, color="white"):
        self.require_window()

        if not isinstance(x, int) or isinstance(x, bool):
            raise RuntimeError("text() ben?tigt x als Ganzzahl.")

        if not isinstance(y, int) or isinstance(y, bool):
            raise RuntimeError("text() ben?tigt y als Ganzzahl.")

        if not isinstance(value, str):
            value = str(value)

        if not isinstance(size, int) or isinstance(size, bool):
            raise RuntimeError("text() ben?tigt size als Ganzzahl.")

        if not isinstance(color, str):
            raise RuntimeError("text() ben?tigt eine Farbe als String.")

        self.canvas.create_text(
            x,
            y,
            text=value,
            fill=color,
            font=("Arial", size),
            anchor="nw"
        )

    def present(self):
        self.require_window()

        self.root.update_idletasks()
        self.root.update()

    def key_down(self, key):
        self.require_window()

        if not isinstance(key, str):
            raise RuntimeError("key_down() ben?tigt einen String.")

        return key.lower() in self.keys

    def wait(self):
        self.require_window()

        self.root.mainloop()

    def close(self):
        if self.root is not None:
            try:
                self.root.destroy()
            except tk.TclError:
                pass

            self.root = None
            self.canvas = None
