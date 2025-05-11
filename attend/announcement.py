import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

class AnnouncementImageCreator:
    WIDTH = 800
    HEIGHT = 480
    ARABIC_FONT_PATH = os.path.join(settings.STATIC_ROOT, "webfont/Almarai-Regular.ttf")
    BACKGROUND_IMAGE_PATH = os.path.join(settings.STATIC_ROOT, "dwin/bg.jpg")
    FRAME_COLOR = (0, 0, 0)  # RGB for black
    FRAME_WIDTH = 5
    FONT_SIZE_MEDIUM = 26
    FONT_SIZE_LARGE = 28
    TEXT_FILL_COLOR = (0, 0, 0)  # RGB for black text
    PICTURE_SIZE = (170, 210)
    PICTURE_POSITION = (WIDTH * 0.67, HEIGHT * 0.37)
    DESTINATION_PATH = os.path.join(settings.STATIC_ROOT, "room")
    MAX_TEXT_LENGTH = 44
    MAX_DOCTOR_NAME_LENGTH = 20

    def __init__(self):
        if not os.path.exists(self.DESTINATION_PATH):
            os.makedirs(self.DESTINATION_PATH)

    def _load_image(self, path, size):
        """Helper to load and resize images."""
        try:
            image = Image.open(path)
            image = image.resize(size, Image.LANCZOS)
            return image
        except IOError:
            print(f"Unable to load image at {path}")
            return None

    def _add_text(self, draw, text, font, position):
        """Helper to add text to the image."""
        draw.text(position, text, fill=self.TEXT_FILL_COLOR, font=font)

    def _add_multiline_text(self, draw, text, font, start_x, start_y):
        """Helper to add multiline text with automatic line breaks."""
        line_y = start_y
        max_line_length = self.MAX_TEXT_LENGTH
        lines = 0
        for line in self._wrap_text(text, max_line_length):
            self._add_text(draw, line, font, (start_x, line_y))
            line_y += font.size + 8  # Line spacing
            lines += 1
        return lines - 1

    def _wrap_text(self, text, max_length):
        """Helper to wrap text into lines of a maximum length."""
        words = text.split()
        line, wrapped_text = "", []
        for word in words:
            if len(line) + len(word) + 1 <= max_length:
                line += (word + " ")
            else:
                wrapped_text.append(line.strip())
                line = word + " "
        if line:
            wrapped_text.append(line.strip())
        return wrapped_text

    def _draw_doctor_image(self, img, doctor_image_path):
        """Helper to load, frame, and paste doctor image."""
        doctor_image = self._load_image(doctor_image_path, self.PICTURE_SIZE)
        if doctor_image:
            frame = Image.new(
                "RGB", 
                (doctor_image.width + 2 * self.FRAME_WIDTH, doctor_image.height + 2 * self.FRAME_WIDTH), 
                color=self.FRAME_COLOR
            )
            frame.paste(doctor_image, (self.FRAME_WIDTH, self.FRAME_WIDTH))
            img.paste(frame, (int(self.PICTURE_POSITION[0] - self.FRAME_WIDTH), int(self.PICTURE_POSITION[1] - self.FRAME_WIDTH)))

    def _get_font(self, size):
        """Helper to load the Arabic font."""
        return ImageFont.truetype(self.ARABIC_FONT_PATH, size)

    def create_lecture_announcement(self, event, data, destination=None):
        department_name = data["department_name"] 
        college_name = data["college_name"] 
        doctor_name = data["doctor_name"] 
        subject_name = data["subject_name"] 
        time = data["time"] 
        students = data["students"] 
        """Creates an announcement image for a lecture."""
        img = Image.new("RGB", (self.WIDTH, self.HEIGHT), color=(255, 255, 255))
        bg_image = self._load_image(self.BACKGROUND_IMAGE_PATH, (self.WIDTH, self.HEIGHT))
        if bg_image:
            img.paste(bg_image)

        doctor_image_path = (settings.MEDIA_ROOT + event.doctor.image.url[6:] if event.doctor.image else os.path.join(settings.STATIC_ROOT, "dwin/Blank.jpg"))
        self._draw_doctor_image(img, doctor_image_path)

        draw = ImageDraw.Draw(img)
        font_medium = self._get_font(self.FONT_SIZE_MEDIUM)
        font_large = self._get_font(self.FONT_SIZE_LARGE)

        texts = [college_name, department_name, subject_name, students, time]
        start_x, line_y = self.WIDTH * 0.035, self.HEIGHT * 0.35
        for text in texts:
            if text:
                lines = self._add_multiline_text(draw, text, font_medium, start_x, line_y)
                line_y += 45 + (lines * (font_medium.size + 8))

        self._add_centered_text(draw, doctor_name, font_large)
        # self._add_centered_text(draw, 'docc', font_large)

        file_path = os.path.join(self.DESTINATION_PATH, "final_image.jpg") if not destination else destination
        img.save(file_path)
        return file_path

    def create_doctor_announcement(self, doctor, destination=None):
        """Creates an announcement image for a doctor."""
        img = Image.new("RGB", (self.WIDTH, self.HEIGHT), color=(255, 255, 255))
        bg_image = self._load_image(self.BACKGROUND_IMAGE_PATH, (self.WIDTH, self.HEIGHT))
        if bg_image:
            img.paste(bg_image)

        doctor_image_path = (settings.MEDIA_ROOT + doctor.image.url[6:] if doctor.image else os.path.join(settings.STATIC_ROOT, "dwin/Blank.jpg"))
        self._draw_doctor_image(img, doctor_image_path)

        draw = ImageDraw.Draw(img)
        font_large = self._get_font(self.FONT_SIZE_LARGE)
        self._add_centered_text(draw, str(doctor), font_large)
        # self._add_centered_text(draw, 'docc', font_large)

        file_path = os.path.join(self.DESTINATION_PATH, "doc_image.jpg") if not destination else destination
        img.save(file_path)
        return file_path

    def _add_centered_text(self, draw, text, font, max_line_length=22):
        """Adds centered text under the doctor image at a specified Y position.
        Breaks long text into two lines if needed, centering each line."""
        
        # X-coordinate reference for doctor image (adjust as needed)
        pic_center_x = self.WIDTH * 0.776  # Example center point for doctor image area
        y_position = self.HEIGHT * 0.82
        # Check if text fits within the max line length; if not, split it
        if len(text) > max_line_length:
            words = text.split()
            lines = []
            current_line = ""

            # Split text into two lines if necessary
            for word in words:
                if len(current_line) + len(word) + 1 <= max_line_length:  # +1 for space
                    current_line += (word + " ")
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            lines.append(current_line.strip())  # Append last line

        else:
            lines = [text]

        y_position = self.HEIGHT * (0.85 - (len(lines) / 100))

        # Draw each line centered below the doctor image
        for i, line in enumerate(lines):
            text_width = draw.textbbox((0, 0), line, font=font)[2]
            line_x = pic_center_x - text_width / 2
            line_y = y_position + (i * font.size * 1.2)  # Adjust vertical spacing
            self._add_text(draw, line, font, (line_x, line_y))
