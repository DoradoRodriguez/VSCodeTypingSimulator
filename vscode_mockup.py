import pygame
import time
import sys
import numpy as np
import cv2

# Colores
BACKGROUND = (30, 30, 30)  # Fondo oscuro de VSCode
TEXT_COLOR = (220, 220, 220)  # Color del texto
LINE_NUMBER_COLOR = (100, 100, 100)  # Color de números de línea
TITLE_BAR_COLOR = (50, 50, 50)  # Color de la barra de título
DESKTOP_COLOR = (0, 122, 204)  # Color azul característico de Windows/macOS

class VSCodeMockup:
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Visual Studio Code")
        
        # Load and scale Windows XP background
        try:
            self.background = pygame.image.load('./media/windows-xp-wallpaper.jpeg')
            self.background = pygame.transform.scale(self.background, (width, height))
        except pygame.error:
            print("Could not load background image, using solid color")
            self.background = None
        
        # VSCode window dimensions
        self.window_margin = 100
        self.title_bar_height = 30
        self.window_width = width - (self.window_margin * 2)
        self.window_height = height - (self.window_margin * 1.5)
        
        # Try to load Cascadia Code font
        try:
            font_path = './media/CascadiaCode.ttf'
            self.font = pygame.font.Font(font_path, 14)
        except:
            print("Could not load Cascadia Code, using fallback font")
            self.font = pygame.font.SysFont('Consolas', 14)
        
        self.title_font = pygame.font.SysFont('Segoe UI', 12)
        self.line_height = 20
        self.char_width = 8
        self.left_margin = 50
        
        # Text buffer
        self.text_buffer = []
        self.current_line = 0
        
        # Window control buttons colors
        self.close_button_color = (232, 17, 35)
        self.minimize_button_color = (255, 185, 0)
        self.maximize_button_color = (0, 204, 0)
    
    def draw_window_chrome(self):
        # Draw desktop background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(DESKTOP_COLOR)
        
        # Draw VSCode window with shadow effect
        shadow_offset = 5
        shadow_color = (0, 0, 0, 128)
        
        # Draw shadow
        shadow_surface = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        shadow_surface.fill(shadow_color)
        self.screen.blit(shadow_surface, 
                         (self.window_margin + shadow_offset, 
                          self.window_margin + shadow_offset))
        
        # Draw main window
        pygame.draw.rect(self.screen, BACKGROUND, 
                        (self.window_margin, 
                         self.window_margin, 
                         self.window_width, 
                         self.window_height))
        
        # Draw title bar and buttons
        self.draw_title_bar()

    def draw_title_bar(self):
        pygame.draw.rect(self.screen, TITLE_BAR_COLOR,
                        (self.window_margin, 
                         self.window_margin, 
                         self.window_width, 
                         self.title_bar_height))
        
        # Window control buttons
        button_size = 12
        button_margin = 8
        button_y = self.window_margin + (self.title_bar_height - button_size) // 2
        
        # Draw buttons
        self.draw_window_buttons(button_size, button_margin, button_y)
        
        # Window title
        title = self.title_font.render("Visual Studio Code", True, TEXT_COLOR)
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 
                                self.window_margin + (self.title_bar_height - title.get_height())//2))

    def draw_window_buttons(self, button_size, button_margin, button_y):
        # Close button
        pygame.draw.circle(self.screen, self.close_button_color,
                          (self.window_margin + 20, button_y + button_size//2), button_size//2)
        
        # Minimize button
        pygame.draw.circle(self.screen, self.minimize_button_color,
                          (self.window_margin + 20 + button_size + button_margin, 
                           button_y + button_size//2), button_size//2)
        
        # Maximize button
        pygame.draw.circle(self.screen, self.maximize_button_color,
                          (self.window_margin + 20 + (button_size + button_margin) * 2, 
                           button_y + button_size//2), button_size//2)

    def draw_line_numbers(self):
        editor_y = self.window_margin + self.title_bar_height + 10
        for i in range(len(self.text_buffer) + 1):
            number = self.font.render(str(i + 1), True, LINE_NUMBER_COLOR)
            self.screen.blit(number, (self.window_margin + 10, 
                                    editor_y + i * self.line_height))

    def write_char(self, char):
        if char == '\n':
            self.text_buffer.append("")
            self.current_line += 1
        else:
            if self.current_line >= len(self.text_buffer):
                self.text_buffer.append("")
            self.text_buffer[self.current_line] += char

    def capture_frame(self):
        string_image = pygame.image.tostring(self.screen, 'RGB')
        temp_surface = pygame.image.fromstring(string_image, (self.width, self.height), 'RGB')
        
        frame = pygame.surfarray.array3d(temp_surface)
        frame = frame.swapaxes(0, 1)
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    def simulate_typing(self, text, video_writer, delay=0.1):
        for char in text:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            self.screen.fill(BACKGROUND)
            self.draw_window_chrome()
            
            self.write_char(char)
            self.draw_line_numbers()
            
            editor_y = self.window_margin + self.title_bar_height + 10
            for i, line in enumerate(self.text_buffer):
                text_surface = self.font.render(line, True, TEXT_COLOR)
                self.screen.blit(text_surface, 
                               (self.window_margin + self.left_margin, 
                                editor_y + i * self.line_height))
            
            pygame.display.flip()
            
            frame = self.capture_frame()
            video_writer.write(frame)
            
            time.sleep(delay) 