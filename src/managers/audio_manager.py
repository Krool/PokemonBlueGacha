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
        self.music_volume = 0.25  # Background music at 25%
        self.sfx_volume = 0.50    # Sound effects at 50%
        self.current_music: Optional[str] = None
        self.sounds = {}
        self.sound_paths = {}  # Store paths for web playback
        self.background_tracks: List[str] = []  # List of available background music tracks
        self.sfx_channels = []  # Additional channels for sound effects on web
        self.user_interacted = False  # Track if user has interacted (for web autoplay)
        self.pending_music = None  # Store music to play after user interaction
        
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
            
            # Load as Sound for both desktop and web
            # Pygbag handles loading files properly on web
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.sfx_volume)
            self.sounds[name] = sound
            
            print(f"  [OK] Loaded sound: {name} from {os.path.basename(path)}")
        except Exception as e:
            print(f"  [ERROR] Error loading sound {name} from {path}: {e}")
            import traceback
            traceback.print_exc()
    
    def play_sound(self, name: str):
        """
        Play a sound effect
        
        Args:
            name: Name of sound to play
        """
        if not self.enabled:
            print(f"  [AUDIO] Audio disabled, skipping sound: {name}")
            return
        
        # Check if user has interacted (required for web)
        if IS_WEB and not self.user_interacted:
            print(f"  [AUDIO] ⏸ Sound '{name}' queued (waiting for user interaction)")
            return
            
        if name not in self.sounds:
            print(f"  [AUDIO] Warning: Sound '{name}' not loaded (available: {list(self.sounds.keys())})")
            return
        
        try:
            sound = self.sounds[name]
            
            if IS_WEB:
                # On web, find an available channel and play on it explicitly
                # This is more reliable than sound.play() which can fail silently
                channel_found = False
                for i in range(pygame.mixer.get_num_channels()):
                    channel = pygame.mixer.Channel(i)
                    if not channel.get_busy():
                        channel.set_volume(self.sfx_volume)
                        channel.play(sound)
                        channel_found = True
                        print(f"  [AUDIO] Playing sound: {name} on channel {i}")
                        break
                
                if not channel_found:
                    # Force play on channel 0 if all busy
                    channel = pygame.mixer.Channel(0)
                    channel.set_volume(self.sfx_volume)
                    channel.play(sound)
                    print(f"  [AUDIO] [WARN] Playing sound: {name} on channel 0 (all channels busy)")
            else:
                # Desktop: simpler playback
                sound.play()
                print(f"  [AUDIO] Playing sound: {name}")
        except Exception as e:
            print(f"  [AUDIO] Error playing sound {name}: {e}")
            import traceback
            traceback.print_exc()
    
    def enable_audio_after_interaction(self, allow_music_start: bool = True):
        """
        Call this after first user interaction to enable audio on web.
        Required for browser autoplay policies.
        
        Args:
            allow_music_start: If False, don't auto-play pending music (useful if music is muted)
        """
        if IS_WEB and not self.user_interacted:
            self.user_interacted = True
            print("[OK] User interaction detected - audio enabled")
            
            # If there's pending music, play it now (unless music is muted)
            if self.pending_music and allow_music_start:
                print(f"  Playing pending music: {os.path.basename(self.pending_music)}")
                self.play_music(self.pending_music)
                self.pending_music = None
            elif self.pending_music and not allow_music_start:
                # Clear pending music if muted
                print(f"  Cleared pending music (muted): {os.path.basename(self.pending_music)}")
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
            print(f"Warning: Music file not found: {path}")
            return
        
        # On web, if user hasn't interacted yet, store music to play later
        if IS_WEB and not self.user_interacted:
            self.pending_music = path
            print(f"⏸ Music queued (waiting for user interaction): {os.path.basename(path)}")
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
        
        # Define sound files to load - CHECK FILE EXTENSIONS IN Assets/Sounds FOLDER!
        sound_files = {
            'roll1': 'roll1.mp3',  # Changed to match actual files
            'roll2': 'roll2.mp3',
            'roll3': 'roll3.mp3',
            'legendary': 'legendary.mp3',
            'chaching': 'chaching.mp3',  # Special sound for legendary pulls
            'gotemall': 'gotemall.mp3',  # Sound for completing the collection
            'background': 'background.mp3'  # This will be loaded as music, not sound
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

