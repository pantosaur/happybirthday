#!/usr/bin/env python3
import os
import random
import time
import sys

# Terminal handling
if os.name == 'nt':
    import msvcrt
else:
    import select
    import termios
    import tty

# Terminal color codes
class Color:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"

def get_terminal_size():
    """Get terminal size reliably"""
    try:
        if os.name == 'nt':
            from ctypes import windll, create_string_buffer
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            cols = csbi[10] - csbi[8] + 1
            rows = csbi[12] - csbi[6] + 1
            return rows, cols
        else:
            import fcntl
            import struct
            from termios import TIOCGWINSZ
            
            for fd in (0, 1, 2):
                try:
                    dims = struct.unpack('hh', fcntl.ioctl(fd, TIOCGWINSZ, '1234'))
                    return dims[0], dims[1]
                except:
                    pass
            
            return int(os.environ.get('LINES', 25)), int(os.environ.get('COLUMNS', 80))
    except:
        return 40, 100

class FallingObject:
    def __init__(self, x, speed, is_balloon=True):
        self.x = x
        self.y = -random.randint(5, 20)  # Start above screen
        self.speed = speed
        self.is_balloon = is_balloon
        
        if is_balloon:
            # Balloon characters - mix of emoji and circles
            self.char_options = [
                ('🎈', 2, 'emoji'),
                ('○', 1, 'circle'),
                ('●', 1, 'circle'),
                ('◉', 1, 'circle'),
                ('⬤', 1, 'circle'),
                ('⭕', 1, 'circle'),
            ]
            
            char, width, char_type = random.choice(self.char_options)
            self.char = char
            self.width = width
            self.char_type = char_type
            
            # Assign color
            if self.char == '🎈':
                self.color = random.choice([Color.RED, Color.BRIGHT_RED, Color.BLUE, 
                                           Color.GREEN, Color.YELLOW, Color.MAGENTA])
            elif self.char in ['○', '●', '◉', '⬤', '⭕']:
                self.color = random.choice([Color.RED, Color.BRIGHT_RED, Color.GREEN,
                                           Color.BRIGHT_GREEN, Color.BLUE, Color.BRIGHT_BLUE,
                                           Color.YELLOW, Color.BRIGHT_YELLOW])
            else:
                self.color = random.choice([Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW])
            
            # Cord/string BELOW the balloon - simple vertical line
            self.cord_length = random.randint(1, 3)
            self.cord_char = '│'  # Simple vertical line
            
            # For 2-width emoji, cord is centered
            # For 1-width circles, cord is directly below
            self.cord_offset = 1 if width == 2 else 0
            
        else:
            # Confetti - all single width
            self.char = random.choice(['*', '+', '·', '✦', '✧', '❉', '❊', '✶', '✴', '✨', '⭐'])
            self.width = 1
            self.char_type = 'confetti'
            self.color = random.choice([Color.WHITE, Color.YELLOW, Color.BRIGHT_YELLOW, 
                                       Color.BRIGHT_CYAN, Color.BRIGHT_MAGENTA])
            self.cord_length = 0
            self.cord_char = ''
            self.cord_offset = 0
    
    def update(self, speed_factor, rows):
        self.y += self.speed * speed_factor
        # Remove when completely past bottom of screen
        return self.y < rows + self.cord_length
    
    def get_positions(self):
        """Return positions to draw"""
        positions = []
        
        # Main object
        positions.append((int(self.x), int(self.y), self.char, self.color, self.width))
        
        # Cord BELOW the balloon - only draw if there's space
        if self.is_balloon and self.cord_length > 0:
            for i in range(1, self.cord_length + 1):
                cord_y = int(self.y) + i
                cord_x = int(self.x) + self.cord_offset
                positions.append((cord_x, cord_y, self.cord_char, Color.WHITE, 1))
        
        return positions

class BalloonMatrix:
    def __init__(self):
        self.rows, self.cols = get_terminal_size()
        self.objects = []
        self.speed_factor = 1.0
        self.running = True
        
        # Setup signal handler for clean exit
        import signal
        signal.signal(signal.SIGINT, lambda s, f: self.stop())
        
        # Create initial objects
        self.spawn_initial_objects()
    
    def stop(self):
        self.running = False
    
    def spawn_initial_objects(self):
        """Create initial falling objects"""
        for _ in range(15):
            x = random.randint(0, self.cols - 2)
            speed = random.uniform(0.15, 0.35)
            self.objects.append(FallingObject(x, speed, is_balloon=True))
        
        for _ in range(25):
            x = random.randint(0, self.cols - 1)
            speed = random.uniform(0.3, 0.7)
            self.objects.append(FallingObject(x, speed, is_balloon=False))
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def hide_cursor(self):
        """Hide terminal cursor"""
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
    
    def show_cursor(self):
        """Show terminal cursor"""
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
    
    def update(self):
        """Update all objects"""
        # Update existing objects and remove those that are done
        self.objects = [obj for obj in self.objects if obj.update(self.speed_factor, self.rows)]
        
        # Spawn new objects randomly
        if random.random() < 0.03:  # Balloons
            x = random.randint(0, self.cols - 2)
            speed = random.uniform(0.15, 0.35)
            self.objects.append(FallingObject(x, speed, is_balloon=True))
        
        if random.random() < 0.06:  # Confetti
            x = random.randint(0, self.cols - 1)
            speed = random.uniform(0.25, 0.6)
            self.objects.append(FallingObject(x, speed, is_balloon=False))
    
    def draw_frame(self):
        """Draw current frame"""
        # Move cursor to top-left and clear screen
        sys.stdout.write("\033[H\033[J")
        
        # Draw all objects directly
        for obj in self.objects:
            for x, y, char, color, width in obj.get_positions():
                if 0 <= y < self.rows and 0 <= x < self.cols:
                    # Move cursor to position and draw
                    sys.stdout.write(f"\033[{y+1};{x+1}H{color}{char}{Color.RESET}")
        
        sys.stdout.flush()
    
    def handle_input(self):
        """Handle keyboard input"""
        try:
            if os.name == 'nt':
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                    if key == 'q':
                        self.running = False
                    elif key == '+':
                        self.speed_factor = min(2.5, self.speed_factor + 0.1)
                    elif key == '-':
                        self.speed_factor = max(0.2, self.speed_factor - 0.1)
                    elif key == ' ':
                        # Add balloon burst
                        x = random.randint(5, self.cols - 5)
                        for _ in range(3):
                            speed = random.uniform(0.15, 0.35)
                            self.objects.append(FallingObject(x + random.randint(-2, 2), 
                                                             speed, is_balloon=True))
            else:
                # Unix/Linux/Mac
                dr, dw, de = select.select([sys.stdin], [], [], 0)
                if dr:
                    key = sys.stdin.read(1).lower()
                    if key == 'q':
                        self.running = False
                    elif key == '+':
                        self.speed_factor = min(2.5, self.speed_factor + 0.1)
                    elif key == '-':
                        self.speed_factor = max(0.2, self.speed_factor - 0.1)
                    elif key == ' ':
                        x = random.randint(5, self.cols - 5)
                        for _ in range(3):
                            speed = random.uniform(0.15, 0.35)
                            self.objects.append(FallingObject(x + random.randint(-2, 2), 
                                                             speed, is_balloon=True))
        except:
            pass
    
    def run(self):
        """Main animation loop"""
        self.hide_cursor()
        self.clear_screen()
        
        try:
            # Set up non-blocking input for Unix
            if os.name != 'nt':
                old_settings = termios.tcgetattr(sys.stdin)
                tty.setcbreak(sys.stdin.fileno())
            
            # Fixed frame rate
            frame_delay = 1/25  # 25 FPS
            last_time = time.time()
            
            while self.running:
                current_time = time.time()
                
                if current_time - last_time >= frame_delay:
                    self.handle_input()
                    self.update()
                    self.draw_frame()
                    last_time = current_time
                else:
                    time.sleep(0.001)
            
            # Restore terminal settings
            if os.name != 'nt':
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                
        except KeyboardInterrupt:
            pass
        except Exception as e:
            pass  # Silent exit on error
        finally:
            self.show_cursor()
            self.clear_screen()

def main():
    """Main function"""
    if not sys.stdout.isatty():
        print("This program requires a terminal.")
        return
    
    # Create and run animation
    matrix = BalloonMatrix()
    matrix.run()

if __name__ == "__main__":
    main()
