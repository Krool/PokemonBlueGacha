"""
Audio management for music and sound effects
"""
import pygame
import os
import random
from typing import Optional, List


class AudioManager:
    """Manages game audio (music and sound effects)"""
    
    def __init__(self):
        self.enabled = True
        self.music_volume = 0.25  # Background music at 25%
        self.sfx_volume = 0.50    # Sound effects at 50%
        self.current_music: Optional[str] = None
        self.sounds = {}
        self.background_tracks: List[str] = []  # List of available background music tracks
        
        # Try to initialize pygame mixer with web-compatible settings
        try:
            if not pygame.mixer.get_init():
                # Use settings that work better on web
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                print("✓ Audio mixer initialized")
        except Exception as e:
            print(f"Audio initialization failed: {e}")
            self.enabled = False
    
    def load_sound(self, path: str, name: str):
        """
        Load a sound effect
        
        Args:
            path: Path to sound file
            name: Name to reference sound by
        """
        if not self.enabled:
            return
        
        if not os.path.exists(path):
            print(f"Warning: Sound file not found: {path}")
            return
        
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.sfx_volume)
            self.sounds[name] = sound
            print(f"  ✓ Loaded sound: {name} from {os.path.basename(path)}")
        except Exception as e:
            print(f"  ✗ Error loading sound {name} from {path}: {e}")
    
    def play_sound(self, name: str):
        """
        Play a sound effect
        
        Args:
            name: Name of sound to play
        """
        if not self.enabled:
            return
            
        if name not in self.sounds:
            print(f"Warning: Sound '{name}' not loaded")
            return
        
        try:
            self.sounds[name].play()
        except Exception as e:
            print(f"Error playing sound {name}: {e}")
    
    def play_music(self, path: str, loops: int = -1):
        """
        Play background music
        
        Args:
            path: Path to music file
            loops: Number of loops (-1 for infinite)
        """
        if not self.enabled:
            return
        
        if not os.path.exists(path):
            print(f"Warning: Music file not found: {path}")
            return
        
        try:
            # Don't restart if already playing this music
            if self.current_music == path and pygame.mixer.music.get_busy():
                return
            
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)
            self.current_music = path
        except Exception as e:
            print(f"Error playing music {path}: {e}")
    
    def stop_music(self):
        """Stop background music"""
        if not self.enabled:
            return
        
        try:
            pygame.mixer.music.stop()
            self.current_music = None
        except Exception as e:
            print(f"Error stopping music: {e}")
    
    def play_random_background_music(self):
        """Play a random background track from available tracks"""
        if not self.enabled or not self.background_tracks:
            return
        
        # Filter out currently playing track if multiple tracks exist
        available_tracks = self.background_tracks.copy()
        if len(available_tracks) > 1 and self.current_music in available_tracks:
            available_tracks.remove(self.current_music)
        
        # Pick a random track
        track = random.choice(available_tracks)
        self.play_music(track)
        print(f"🎵 Playing random background music: {os.path.basename(track)}")
    
    def load_background_music_tracks(self, sounds_path: str):
        """
        Load all available background music tracks
        
        Args:
            sounds_path: Base path to sounds folder
        """
        self.background_tracks = []
        
        # Look for background1.mp3 through background8.mp3
        for i in range(1, 9):
            for ext in ['.mp3', '.wav', '.ogg']:
                track_path = os.path.join(sounds_path, f'background{i}{ext}')
                if os.path.exists(track_path):
                    self.background_tracks.append(track_path)
                    break
        
        print(f"✓ Found {len(self.background_tracks)} background music tracks")
        
        # Keep all tracks for rotation
        if self.background_tracks:
            random.shuffle(self.background_tracks)
            print(f"  All {len(self.background_tracks)} tracks available for rotation")
    
    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.enabled:
            pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def load_game_sounds(self, sounds_path: str):
        """
        Load all game sound effects
        
        Args:
            sounds_path: Base path to sounds folder
        """
        import os
        
        # Define sound files to load
        sound_files = {
            'roll1': 'roll1.wav',  # or .mp3, .ogg depending on what files exist
            'roll2': 'roll2.wav',
            'roll3': 'roll3.wav',
            'legendary': 'legendary.wav',
            'chaching': 'chaching.wav',  # Special sound for legendary pulls
            'gotemall': 'gotemall.wav',  # Sound for completing the collection
            'background': 'background.wav'  # This will be loaded as music, not sound
        }
        
        print("Loading sound effects...")
        
        for sound_name, filename in sound_files.items():
            # Try different extensions if file doesn't exist
            for ext in ['.wav', '.mp3', '.ogg']:
                full_path = os.path.join(sounds_path, filename.replace('.wav', ext))
                if os.path.exists(full_path):
                    if sound_name != 'background':  # Background is music, not sound effect
                        self.load_sound(full_path, sound_name)
                    break
        
        print(f"✓ Loaded {len(self.sounds)} sound effects")

