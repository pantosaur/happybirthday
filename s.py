#!/usr/bin/env python3

import pyfiglet
import time
import random
import sys
import math

# Extended ANSI color codes with more party colors
COLORS = {
    # Bright neon colors
    'neon_pink': '\033[38;5;200m',
    'neon_blue': '\033[38;5;45m',
    'neon_green': '\033[38;5;46m',
    'neon_yellow': '\033[38;5;226m',
    'neon_orange': '\033[38;5;208m',
    'neon_purple': '\033[38;5;129m',
    'neon_cyan': '\033[38;5;51m',
    'neon_red': '\033[38;5;196m',
    
    # Pastel colors
    'pastel_pink': '\033[38;5;218m',
    'pastel_blue': '\033[38;5;153m',
    'pastel_green': '\033[38;5;158m',
    'pastel_yellow': '\033[38;5;229m',
    'pastel_orange': '\033[38;5;223m',
    'pastel_purple': '\033[38;5;183m',
    'pastel_cyan': '\033[38;5;159m',
    'pastel_red': '\033[38;5;210m',
    
    # Standard bright colors
    'bright_red': '\033[1;91m',
    'bright_green': '\033[1;92m',
    'bright_yellow': '\033[1;93m',
    'bright_blue': '\033[1;94m',
    'bright_magenta': '\033[1;95m',
    'bright_cyan': '\033[1;96m',
    
    'reset': '\033[0m',
    'bold': '\033[1m',
    'blink': '\033[5m',
    'fast_blink': '\033[6m',
}

# Mixed color palettes - each with a different theme
COLOR_PALETTES = [
    # Neon rave
    ['neon_pink', 'neon_blue', 'neon_green', 'neon_yellow', 'neon_orange', 'neon_purple'],
    
    # Cyberpunk
    ['neon_cyan', 'neon_pink', 'neon_purple', 'bright_cyan', 'neon_blue', 'bright_magenta'],
    
    # Tropical sunset
    ['neon_orange', 'pastel_pink', 'neon_red', 'pastel_orange', 'neon_yellow', 'pastel_yellow'],
    
    # Ocean waves
    ['neon_blue', 'pastel_blue', 'bright_cyan', 'neon_cyan', 'pastel_green', 'bright_blue'],
    
    # Candy shop
    ['pastel_pink', 'pastel_yellow', 'pastel_blue', 'pastel_green', 'pastel_purple', 'pastel_orange'],
    
    # Electric neon
    ['neon_green', 'neon_pink', 'neon_cyan', 'neon_yellow', 'neon_purple', 'neon_blue'],
    
    # Rainbow explosion
    ['neon_red', 'neon_orange', 'neon_yellow', 'neon_green', 'neon_blue', 'neon_purple'],
    
    # Mystical fantasy
    ['pastel_purple', 'neon_cyan', 'pastel_pink', 'neon_purple', 'pastel_blue', 'neon_pink'],
]

# Balloon characters for decoration
BALLOONS = ['🎉', '🎂', '🎈', '🎁']

def get_random_palette():
    """Get a random palette and shuffle it for more variety"""
    palette = random.choice(COLOR_PALETTES)
    random.shuffle(palette)
    return palette

def safe_get_color(color_name):
    """Safely get a color code, with fallback to white if not found"""
    return COLORS.get(color_name, COLORS['neon_purple'])

def clear_area(start_line, start_col, width, height):
    """Clear a rectangular area on the screen"""
    for i in range(height):
        sys.stdout.write(f'\033[{start_line + i};{start_col}H')
        sys.stdout.write(' ' * width)

def get_word_width(word):
    """Calculate the ASCII art width of a word"""
    if len(word) > 1:
        word_without_first = word[1:]
        word_art = pyfiglet.figlet_format(word_without_first, font="standard")
        word_lines = word_art.split('\n')
        if word_lines:
            return max(len(line) for line in word_lines)
    return 0

def display_happy_birthday_party(name, word_dict, delay=2):
    """
    Happy Birthday party with name "MARTIN" in big letters below
    """
    sys.stdout.write('\033[2J\033[H\033[?25l')
    sys.stdout.flush()
    
    # Text to display in big ASCII letters
    text = name.upper()  # "MARTIN"
    
    # Generate ASCII art for each letter of the name
    letters = {}
    
    # Get a random palette and shuffle it
    palette = get_random_palette()
    
    # Assign shuffled colors to letters
    letter_colors = {}
    for idx, char in enumerate(text):
        art = pyfiglet.figlet_format(char, font="standard")
        lines = art.split('\n')
        letters[char] = lines
        # Cycle through palette, but start at random position
        start_idx = random.randint(0, len(palette) - 1)
        color_idx = (start_idx + idx) % len(palette)
        letter_colors[char] = palette[color_idx]
    
    # Calculate positions ONCE
    line_num = 8  # Start lower to accommodate "HAPPY BIRTHDAY"
    positions = {}
    
    # First, find the maximum word width to allocate enough space
    max_word_width = 0
    for char in text.upper():
        if char in word_dict:
            for word in word_dict[char]:
                word_width = get_word_width(word)
                max_word_width = max(max_word_width, word_width)
    
    # Add generous padding for longer words
    extra_word_padding = 40  # Increased for very long words
    
    for idx, char in enumerate(text):
        lines = letters[char]
        if lines:
            letter_width = max(len(line) for line in lines)
        else:
            letter_width = 0
            
        positions[char] = {
            'start': line_num,
            'width': letter_width,
            'height': len(lines)
        }
        line_num += len(lines) + 1
    
    # Find where the last letter ends (for confetti placement)
    last_letter_end = 0
    for char in text:
        pos = positions[char]
        last_letter_end = max(last_letter_end, pos['start'] + pos['height'])
    
    # Get max width for positioning
    max_letter_width = max(pos['width'] for pos in positions.values()) if positions else 0
    
    # Calculate total screen width needed for words
    total_word_area_width = max_letter_width + max_word_width + extra_word_padding
    
    # Animation variables
    frame = 0
    color_shift = 0
    palette_change_counter = 0
    current_palette = palette
    
    # Track current word
    current_word = None
    current_char = None
    current_word_width = 0
    
    # Define safe color choices
    safe_neon_colors = ['neon_cyan', 'neon_pink', 'neon_green', 'neon_yellow', 'neon_blue', 'neon_purple', 'neon_orange', 'neon_red']
    safe_pastel_colors = ['pastel_pink', 'pastel_blue', 'pastel_green', 'pastel_yellow', 'pastel_orange', 'pastel_purple', 'pastel_cyan', 'pastel_red']
    
    # Store word arts for faster access
    word_arts_cache = {}
    for char in text.upper():
        if char in word_dict:
            for word in word_dict[char]:
                if len(word) > 1:
                    word_without_first = word[1:]
                    word_art = pyfiglet.figlet_format(word_without_first, font="standard")
                    word_arts_cache[(char, word)] = word_art
    
    # Calculate safe zones for decorations (don't interfere with words)
    # Words appear from column 0 to total_word_area_width
    word_area_start_x = 0
    word_area_end_x = total_word_area_width
    
    # Balloons will appear only on the right side, away from word area
    balloon_positions = []
    available_colors = list(COLORS.keys())
    # Remove non-color keys
    for non_color in ['reset', 'bold', 'blink', 'fast_blink']:
        if non_color in available_colors:
            available_colors.remove(non_color)
    
    try:
        while True:
            time.sleep(0.05)
            frame += 1
            
            sys.stdout.write('\033[H')
            
            # Change palette occasionally
            palette_change_counter += 1
            if palette_change_counter > 150:
                current_palette = get_random_palette()
                palette_change_counter = 0
                for idx, char in enumerate(text):
                    color_idx = (color_shift + idx) % len(current_palette)
                    letter_colors[char] = current_palette[color_idx]
            
            # Update color shift
            if frame % 4 == 0:
                color_shift = (color_shift + 1) % len(current_palette)
            
            # Animated balloons - ONLY on right side
            for balloon in balloon_positions:
                color_code = safe_get_color(balloon['color'])
                float_offset = math.sin(frame * balloon['speed'] + balloon['phase']) * 1.5
                if frame % 40 == 0:
                    balloon['type'] = random.choice(BALLOONS)
                sys.stdout.write(f'\033[{int(balloon['y'] + float_offset)};{balloon['x']}H')
                sys.stdout.write(f"{color_code}{balloon['type']}{COLORS['reset']}")
            
            # Display "HAPPY BIRTHDAY" at the top - centered in word area
            sys.stdout.write('\033[1;0H')
            
            happy_birthday = "🎉🎂 Bonne Fête! 🎂🎉"
            padding = 23#max(0, (total_word_area_width - len(happy_birthday)) // 2)
            sys.stdout.write(' ' * padding)
            
            hb_colors = ['neon_yellow', 'neon_pink', 'neon_cyan', 'neon_green', 'neon_blue']
            hb_color = hb_colors[(frame // 10) % len(hb_colors)]
            
            if frame % 15 < 8:
                sys.stdout.write(f"{COLORS['blink']}{safe_get_color(hb_color)}{happy_birthday}{COLORS['reset']}")
            else:
                sys.stdout.write(f"{COLORS['bold']}{safe_get_color(hb_color)}{happy_birthday}{COLORS['reset']}")
            
            sys.stdout.write('\n\n\n')
            
            # Character row - aligned with letters
            sys.stdout.write('\033[5;0H')
            
            if frame % 50 < 25:
                left_emoji = random.choice(['🎂 ', '🍰 ', '🎁 ', '🥳 '])
                right_emoji = random.choice([' 🎂', ' 🍰', ' 🎁', ' 🥳'])
            else:
                left_emoji = right_emoji = "   "
            
            sys.stdout.write(f"                 {safe_get_color('neon_yellow')}{left_emoji}{COLORS['reset']}   ")
            
            for idx, char in enumerate(text):
                color_idx = (color_shift + idx) % len(current_palette)
                base_color = current_palette[color_idx]
                color_code = safe_get_color(base_color)
                
                blink_pattern = frame % 24
                if blink_pattern < 6:
                    effect = COLORS['blink']
                    color_code = safe_get_color('neon_yellow')
                elif blink_pattern < 12:
                    effect = COLORS['fast_blink']
                    comp_idx = (color_idx + len(current_palette)//2) % len(current_palette)
                    color_code = safe_get_color(current_palette[comp_idx])
                elif blink_pattern < 18:
                    effect = COLORS['bold']
                    if 'pastel' in base_color:
                        alt_color = base_color.replace('pastel', 'neon')
                        color_code = safe_get_color(alt_color)
                else:
                    effect = ''
                
                sys.stdout.write(f"{effect}{color_code}{char}{COLORS['reset']}   ")
            
            sys.stdout.write(f"{safe_get_color('neon_pink')}{right_emoji}{COLORS['reset']}")
            sys.stdout.write('\n\n')
            
            # Display name letters
            for idx, char in enumerate(text):
                lines = letters[char]
                pos = positions[char]
                
                color_strategy = (frame // 10 + idx) % 4
                
                if color_strategy == 0:
                    color_code = safe_get_color(letter_colors[char])
                elif color_strategy == 1:
                    color_idx = (idx + len(current_palette)//2) % len(current_palette)
                    color_code = safe_get_color(current_palette[color_idx])
                elif color_strategy == 2:
                    color_code = safe_get_color(random.choice(safe_neon_colors))
                else:
                    cycle_idx = (color_shift + idx * 2) % len(current_palette)
                    color_code = safe_get_color(current_palette[cycle_idx])
                
                for i, line in enumerate(lines):
                    sys.stdout.write(f'\033[{pos['start'] + i};0H')
                    
                    pulse = (frame + i + idx) % 30
                    
                    if pulse < 10:
                        display_line = f"{COLORS['bold']}{color_code}{line}"
                    elif pulse < 20:
                        alt_color = safe_get_color(current_palette[(color_shift + i) % len(current_palette)])
                        display_line = f"{alt_color}{line}"
                    else:
                        display_line = f"{color_code}{line}"
                    
                    if (frame + i) % 45 == 0:
                        display_line = f"{COLORS['blink']}{display_line}"
                    
                    sys.stdout.write(f"{display_line}{COLORS['reset']}")
            
            # Word display logic
            if frame % (int(delay * 20)) == 0:
                char = random.choice(text)
                word = random.choice(word_dict[char])
                word_without_first = word[1:] if len(word) > 1 else ""
                
                # Clear previous word - Clear entire word area
                if current_word and current_char in positions:
                    prev_pos = positions[current_char]
                    # Clear from letter end to end of screen
                    clear_area(prev_pos['start'], prev_pos['width'] + 1, 
                              total_word_area_width - prev_pos['width'], 
                              prev_pos['height'] + 2)
                
                # Display new word
                if word_without_first:
                    # Get word art from cache or generate it
                    cache_key = (char, word)
                    if cache_key in word_arts_cache:
                        word_art = word_arts_cache[cache_key]
                    else:
                        word_art = pyfiglet.figlet_format(word_without_first, font="standard")
                    
                    word_lines = word_art.split('\n')
                    pos = positions[char]
                    
                    # Calculate word width
                    if word_lines:
                        current_word_width = max(len(line) for line in word_lines)
                    else:
                        current_word_width = 0
                    
                    # Random word color strategy
                    color_strat = random.randint(0, 3)
                    if color_strat == 0:
                        letter_idx = text.index(char)
                        word_color_idx = (letter_idx + len(current_palette)//2) % len(current_palette)
                        word_color = current_palette[word_color_idx]
                    elif color_strat == 1:
                        word_color = random.choice(safe_neon_colors)
                    elif color_strat == 2:
                        base_color = letter_colors[char]
                        if 'neon' in base_color:
                            potential_pastel = base_color.replace('neon', 'pastel')
                            if potential_pastel in COLORS:
                                word_color = potential_pastel
                            else:
                                word_color = random.choice(safe_pastel_colors)
                        else:
                            word_color = random.choice(safe_pastel_colors)
                    else:
                        word_color = current_palette[(color_shift + 3) % len(current_palette)]
                    
                    color_code = safe_get_color(word_color)
                    
                    # Display each line of the word
                    for i, line in enumerate(word_lines):
                        sys.stdout.write(f'\033[{pos["start"] + i};{pos["width"] + 1}H')
                        
                        # Simple blink effect only
                        if frame % 12 < 6:
                            sys.stdout.write(f"{COLORS['blink']}{color_code}{line}{COLORS['reset']}")
                        else:
                            sys.stdout.write(f"{color_code}{line}{COLORS['reset']}")
                    
                    sys.stdout.flush()
                    
                    current_word = word_art
                    current_char = char
                else:
                    current_word = None
                    current_char = None
                    current_word_width = 0
            
            # Confetti bursts - ONLY appear on right side, away from words
            if frame % 40 == 0:
                for _ in range(random.randint(2, 3)):  # Fewer confetti
                    # Place confetti only on right side, away from word area
                    x = random.randint(0, 40)
                    y = random.randint(15, 50)  # Below the word area
                    confetti_char = random.choice(['⭐', '🎈', '🎉'])
                    confetti_color = random.choice(['neon_yellow', 'neon_pink', 'neon_cyan', 'neon_green'])
                    sys.stdout.write(f'\033[{y};{x}H')
                    sys.stdout.write(f"{safe_get_color(confetti_color)}{confetti_char}{COLORS['reset']}")
            
            sys.stdout.flush()
            
    except KeyboardInterrupt:
        sys.stdout.write('\033[?25h\033[0m\033[2J\033[H')
        sys.stdout.flush()
        final_message = "🎉🎂 HAPPY BIRTHDAY MARTIN! 🎂🎉"
        print("\n" * 3)
        for i in range(len(final_message)):
            color = ['neon_pink', 'neon_blue', 'neon_green', 'neon_yellow', 'neon_orange'][i % 5]
            print(f"{safe_get_color(color)}{final_message[i]}{COLORS['reset']}", end='', flush=True)
            time.sleep(0.05)
        print("\n")
        print(f"{safe_get_color('neon_cyan')}{'🎊' * 25}{COLORS['reset']}")
        print(f"{safe_get_color('neon_pink')}{'🥳' * 25}{COLORS['reset']}")
        print(f"{safe_get_color('neon_yellow')}{'✨' * 25}{COLORS['reset']}\n")
    except Exception as e:
        sys.stdout.write('\033[?25h\033[0m')
        sys.stdout.flush()
        print(f"\nError occurred: {e}")
        print("The script will now exit.")

if __name__ == "__main__":
    name = "MARTIN"
    
    word_dict = {
        'M': ["MERVEILLEUX", "MAJESTIC", "MODESTE", "METHODIQUE", "MAJESTUEUX", "MAGNIFIQUE", "MAGNANIME", "MAGIQUE", "MARQUANT", "MIRACULEUX", "MELODIEUX"],
        'A': ["AWESOME", "ARTISTIQUE", "ATTENTIF", "ALTRUISTE", "AUDACIEUX", "AUTHENTIQUE", "AMBITIEUX", "ADMIRABLE", "AIMABLE", "AGREABLE"],
        'R': ["RADIANT", "REMARQUABLE", "RESPONSABLE", "RESILIENT", "RAYONNANT", "RAFFINE", "RIGOUREUX", "RESPECTABLE", "RESPECTUEUX", "RENVERSANT", "RASSURANT"],
        'T': ["TRESOR", "TRAVAILLANT", "TENACE", "TALENTUEUX", "TROP COOL", "TRANQUILLE", "TROP NICE", "TRIOMPHANT"],
        'I': ["INCROYABLE", "INTEGRE", "INSPIRANT", "IMAGINATIF", "ILLUSTRE", "INTELLIGENT", "INTEGRE", "IRREMPLACABLE", "INCOMPARABLE", "INNOVANT", "IDEAL"],
        'N': ["NOBLE", "NOTOIRE", "NOVATEUR", "NATUREL"]
    }
    
    display_happy_birthday_party(name, word_dict, delay=2)
