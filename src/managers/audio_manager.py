"""
Audio management for music and sound effects
"""
import pygame
import os
import random
from typing import Optional, List
from config import IS_WEB


class AudioManager:
    """Manages game audio (music and sound effects)"""
    
    def __init__(self):
        self.enabled = True
        self.music_volume = 0.046875  # Background music at ~4.7% (reduced by 81% total)
        self.sfx_volume = 0.125       # Sound effects at 12.5% (reduced by 75% total)
        self.current_music: Optional[str] = None
        self.sounds = {}
        self.sound_paths = {}  # Store paths for web playback
        self.background_tracks: List[str] = []  # List of available background music tracks
        self.sfx_channels = []  # Additional channels for sound effects on web
        self.user_interacted = False  # Track if user has interacted (for web autoplay)
        self.pending_music = None  # Store music to play after user interaction
        self.audio_errors_logged = set()  # Track logged errors to avoid spam
        
        # Try to initialize pygame mixer with web-compatible settings
        try:
            if not pygame.mixer.get_init():
                # Use settings that work better on web
                pygame.mixer.init(frequency=22050, size=-16, channels=8, buffer=512)
                print("[OK] Audio mixer initialized")
                
                # Set up multiple channels for sound effects (web workaround)
                if IS_WEB:
                    pygame.mixer.set_num_channels(16)  # More channels for better mixing
                    # Reserve channel 0 for music effects, channels 1-15 for sound effects
                    print("  Set up 16 audio channels for web compatibility")
                    print("  Note: Audio may require user interaction to start (browser policy)")
                else:
                    pygame.mixer.set_num_channels(8)
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
            # Store path for reference
            self.sound_paths[name] = path
            
            if IS_WEB:
                # On web, pygame.mixer.Sound() doesn't work
                # Store the path and use pygame.mixer.music to play it later
                self.sounds[name] = path  # Store path instead of Sound object
                print(f"  [OK] Registered sound for web: {name}")
            else:
                # Desktop: use pygame.mixer.Sound (works perfectly, allows multiple sounds)
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sfx_volume)
                self.sounds[name] = sound
                print(f"  [OK] Loaded sound: {name}")
        except Exception as e:
            print(f"  [ERROR] Error loading sound {name}: {e}")
    
    def play_sound(self, name: str):
        """
        Play a sound effect
        
        Args:
            name: Name of sound to play
        
        Note: On web, sound effects can only play when music channel is idle
        """
        if not self.enabled:
            return
        
        # Check if user has interacted (required for web)
        if IS_WEB and not self.user_interacted:
            return
            
        if name not in self.sounds:
            return
        
        try:
            sound = self.sounds[name]
            
            if IS_WEB:
                # On web, check if pygame.mixer.music is busy
                # If it is, skip sound to avoid "interrupted" errors
                try:
                    is_busy = pygame.mixer.music.get_busy()
                    if is_busy:
                        # Music is currently playing/loading - skip sound effect
                        return
                except:
                    # If get_busy fails, assume it's safe to play
                    pass
                
                # On web, pygame.mixer.Sound() doesn't work, so self.sounds[name] is a file path
                sound_path = sound  # It's actually a path, not a Sound object
                
                try:
                    pygame.mixer.music.load(sound_path)
                    pygame.mixer.music.set_volume(self.sfx_volume)
                    pygame.mixer.music.play()
                except:
                    pass  # Silently ignore all errors
            else:
                # Desktop: use pygame.mixer.Sound (works perfectly, allows multiple sounds)
                sound.play()
        except Exception:
            # Catch any other errors silently
            pass
    
    def enable_audio_after_interaction(self, allow_music_start: bool = True):
        """
        Call this after first user interaction to enable audio on web.
        Required for browser autoplay policies.
        
        Args:
            allow_music_start: If False, don't auto-play pending music (useful if music is muted)
        """
        if IS_WEB and not self.user_interacted:
            self.user_interacted = True
            
            # If there's pending music, play it now (unless music is muted)
            if self.pending_music and allow_music_start:
                self.play_music(self.pending_music)
                self.pending_music = None
            elif self.pending_music:
                # Clear pending music if muted
                self.pending_music = None
    
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
            return
        
        # On web, if user hasn't interacted yet, store music to play later
        if IS_WEB and not self.user_interacted:
            self.pending_music = path
            return
        
        try:
            # Don't restart if already playing this music
            try:
                if self.current_music == path and pygame.mixer.music.get_busy():
                    return
            except:
                pass  # Silently ignore get_busy errors
            
            # Wrap each call individually to suppress pythons.js errors
            try:
                pygame.mixer.music.load(path)
            except:
                pass  # Silently ignore load errors
            
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except:
                pass  # Silently ignore volume errors
            
            try:
                pygame.mixer.music.play(loops)
            except:
                pass  # Silently ignore play errors
            
            self.current_music = path
        except Exception:
            # Silently handle all web audio errors
            pass
    
    def stop_music(self):
        """Stop background music"""
        if not self.enabled:
            return
        
        try:
            pygame.mixer.music.stop()
            self.current_music = None
        except Exception as e:
            # Silently handle errors
            pass
    
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
        
        # Only print playing message if not queued (already printed in play_music)
        if not IS_WEB or self.user_interacted:
            print(f"[MUSIC] Playing random background music: {os.path.basename(track)}")
    
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
        
        print(f"[OK] Found {len(self.background_tracks)} background music tracks")
        
        # Keep all tracks for rotation
        if self.background_tracks:
            random.shuffle(self.background_tracks)
            print(f"  All {len(self.background_tracks)} tracks available for rotation")
    
    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.enabled:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except:
                pass  # Silently ignore all errors
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        try:
            for sound in self.sounds.values():
                try:
                    if not IS_WEB:  # Only set volume on desktop (web stores paths, not Sound objects)
                        sound.set_volume(self.sfx_volume)
                except:
                    pass  # Silently ignore errors
        except:
            pass  # Silently ignore all errors
    
    def play_random_click_sound(self):
        """
        Play a random UI click sound (click1, click2, or click3)
        """
        if not self.enabled:
            return
        
        # Check if user has interacted (required for web)
        if IS_WEB and not self.user_interacted:
            return
        
        # Choose a random click sound
        click_sounds = ['click1', 'click2', 'click3']
        available_clicks = [s for s in click_sounds if s in self.sounds]
        
        if available_clicks:
            click_name = random.choice(available_clicks)
            self.play_sound(click_name)
    
    def load_game_sounds(self, sounds_path: str):
        """
        Load all game sound effects
        
        Args:
            sounds_path: Base path to sounds folder
        """
        import os
        
        # Define sound files to load
        sound_files = {
            'roll1': 'roll1.mp3',
            'roll2': 'roll2.mp3',
            'roll3': 'roll3.mp3',
            'legendary': 'legendary.mp3',
            'chaching': 'chaching.mp3',
            'gotemall': 'gotemall.mp3',
            'background': 'background.mp3',  # This will be loaded as music, not sound
            'click1': 'click1.mp3',
            'click2': 'click2.mp3',
            'click3': 'click3.mp3'
        }
        
        print("Loading sound effects...")
        
        for sound_name, filename in sound_files.items():
            full_path = os.path.join(sounds_path, filename)
            
            if os.path.exists(full_path):
                if sound_name != 'background':  # Background is music, not sound effect
                    self.load_sound(full_path, sound_name)
            else:
                # Try alternative extensions if primary doesn't exist
                for ext in ['.wav', '.ogg']:
                    alt_path = os.path.join(sounds_path, filename.replace('.mp3', ext))
                    if os.path.exists(alt_path):
                        if sound_name != 'background':
                            self.load_sound(alt_path, sound_name)
                        break
        
        print(f"[OK] Loaded {len(self.sounds)} sound effects")

