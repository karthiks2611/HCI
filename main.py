import time
import tkinter
from PIL import ImageTk, Image
import cv2
from menu import Menu


class App:
    def __init__(self):
        self.source = 0
        self.cam = cv2.VideoCapture(self.source)
        self.frame = None
        self.cam.set(3, 1270)
        self.cam.set(4, 720)

        self.menu = Menu()
        self.start = time.time()

        # Creating Tkinter window
        self.window = tkinter.Tk()
        self.window.title("Application")
        self.window.protocol('WM_DELETE_WINDOW', self.destructor)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.window, width=1270, height=720)
        self.canvas.pack()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        # self.window.mainloop()

    def update(self):
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            if not ret:
                return
            frame = cv2.flip(frame, 1)

            self.frame = self.menu.menu(frame)

            cv2.putText(self.frame, f"fps: {round(1 / (time.time() - self.start))}", (50, 50), cv2.FONT_HERSHEY_PLAIN,
                        1.5, (255, 0, 0), 1)
            self.start = time.time()

            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.frame, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

    def destructor(self):
        """ Destroy the root object and release all resources """
        self.window.destroy()
        self.cam.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application

    def camera(self):

        while self.cam.isOpened():
            ret, frame = self.cam.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            frame = self.menu.menu(frame)

            cv2.putText(frame, f"fps: {round(1 / (time.time() - self.start))}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1.5,
                        (255, 0, 0), 2)
            self.start = time.time()
            cv2.imshow("Video", frame)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

        self.cam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = App()
    app.window.mainloop()
