"""
Gacha Outcome State - Shows results with Pokemon/Item tiles
"""
import pygame
from states.base_state import GameState
from config import COLOR_WHITE, COLOR_BLACK, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.button import Button
from ui.pokemon_tile import PokemonTile
from ui.item_tile import ItemTile
from ui.currency_display import CurrencyDisplay
from logic.items_gacha import perform_items_gacha

class GachaOutcomeState(GameState):
    """State for displaying gacha pull results"""
    
    def __init__(self, state_manager, game_data, resource_manager, audio_manager, font_manager=None, gacha_system=None):
        super().__init__(state_manager, game_data, resource_manager, audio_manager, font_manager, gacha_system)
        self.results = []
        self.is_ten_pull = False
        self.is_items_gacha = False
        self.pokemon_tiles = []
        self.item_tiles = []
        self.gacha_button = None
        self.roll_same_button = None
        self.back_button = None
        self.last_machine = "Red"  # Remember which machine was used
        self.currency_rect = None  # Clickable currency area
        self.owned_count_before_pull = 0  # Track count before this pull
        
        # Currency click hold tracking
        self.currency_held = False
        self.currency_hold_timer = 0.0
        self.currency_add_interval = 0.1  # Add gold every 0.1 seconds while held
    
    def enter(self, results=None, is_ten_pull=False, machine=None, owned_before=0, is_items_gacha=False):
        """
        Enter the outcome state
        
        Args:
            results: List of Pokemon/Item objects from gacha roll
            is_ten_pull: Whether this was a 10-pull or single pull
            machine: Which gacha machine was used (Red, Blue, Yellow, Items)
            owned_before: Number of unique Pokemon owned before this pull (0 for items)
            is_items_gacha: Whether this is an items gacha
        """
        print("Entered GachaOutcomeState")
        if results is None:
            results = []
        
        self.results = results
        self.is_ten_pull = is_ten_pull
        self.is_items_gacha = is_items_gacha
        self.last_machine = machine if machine else "Red"
        self.owned_count_before_pull = owned_before
        
        # Create Pokemon/Item tiles
        self._create_pokemon_tiles()
        
        # Check if collection is now complete (151 Pokemon)
        self._check_collection_complete()
        
        # Get machine data for cost display
        machine_data = self.resource_manager.get_gacha_machine(self.last_machine)
        roll_cost = machine_data.cost_10pull if is_ten_pull else machine_data.cost_single
        pull_type = "10-PULL" if is_ten_pull else "PULL"
        
        # Create buttons (taller, similar to gacha buy page)
        button_width = 220
        button_height = 80
        button_y = SCREEN_HEIGHT - 130
        button_spacing = 30
        
        # Calculate total width needed for 3 buttons
        total_button_width = button_width * 3 + button_spacing * 2
        start_x = (SCREEN_WIDTH - total_button_width) // 2
        
        # Left button: Pokédex
        self.back_button = Button(
            start_x,
            button_y,
            button_width,
            button_height,
            "POKÉDEX",
            self.font_manager,
            font_size=22,
            use_title_font=True,
            callback=self._go_to_inventory,
            audio_manager=self.audio_manager
        )
        
        # Middle button: Gacha (return to machine select)
        self.gacha_button = Button(
            start_x + button_width + button_spacing,
            button_y,
            button_width,
            button_height,
            "GACHA",
            self.font_manager,
            font_size=22,
            use_title_font=True,
            bg_color=(0, 100, 200),
            hover_color=(0, 150, 255),
            callback=self._go_to_gacha,
            audio_manager=self.audio_manager
        )
        
        # Right button: Roll Same (with cost inside)
        self.roll_same_button = Button(
            start_x + (button_width + button_spacing) * 2,
            button_y,
            button_width,
            button_height,
            f"{pull_type} AGAIN",
            self.font_manager,
            font_size=20,
            use_title_font=True,
            bg_color=(0, 150, 0),
            hover_color=(0, 200, 0),
            callback=self._roll_same,
            audio_manager=self.audio_manager,
            play_click_sound=False  # Skip click - roll sound plays immediately
        )
        self.roll_same_cost = roll_cost
    
    def exit(self):
        """Clean up when leaving state"""
        print("Exited GachaOutcomeState")
    
    def _create_pokemon_tiles(self):
        """Create Pokemon/Item tile components"""
        self.pokemon_tiles = []
        self.item_tiles = []
        
        if not self.results:
            return
        
        if self.is_items_gacha:
            # Create item tiles
            if self.is_ten_pull:
                # 10-pull: 2 rows of 5
                tile_width = 140
                tile_height = 160
                spacing_x = 20
                spacing_y = 20
                
                total_width = tile_width * 5 + spacing_x * 4
                start_x = (SCREEN_WIDTH - total_width) // 2
                start_y = 100
                
                for i, item in enumerate(self.results):
                    col = i % 5
                    row = i // 5
                    
                    x = start_x + col * (tile_width + spacing_x)
                    y = start_y + row * (tile_height + spacing_y)
                    
                    # Check if new
                    is_new = self._is_new_item(item.number)
                    
                    tile = ItemTile(
                        x, y, tile_width, tile_height,
                        item,
                        self.resource_manager,
                        self.font_manager,
                        show_new_badge=is_new,
                        show_count=False
                    )
                    self.item_tiles.append(tile)
            else:
                # Single pull: large centered tile
                tile_width = 300
                tile_height = 350
                x = (SCREEN_WIDTH - tile_width) // 2
                y = 120
                
                item = self.results[0]
                is_new = self._is_new_item(item.number)
                
                tile = ItemTile(
                    x, y, tile_width, tile_height,
                    item,
                    self.resource_manager,
                    self.font_manager,
                    show_new_badge=is_new,
                    show_count=True,
                    count=self.game_data.items_owned.get(item.number, 0)
                )
                self.item_tiles.append(tile)
        else:
            # Create Pokemon tiles
            if self.is_ten_pull:
                # 10-pull: 2 rows of 5
                tile_width = 140
                tile_height = 160
                spacing_x = 20
                spacing_y = 20
                
                total_width = tile_width * 5 + spacing_x * 4
                start_x = (SCREEN_WIDTH - total_width) // 2
                start_y = 100
                
                for i, pokemon in enumerate(self.results):
                    col = i % 5
                    row = i // 5
                    
                    x = start_x + col * (tile_width + spacing_x)
                    y = start_y + row * (tile_height + spacing_y)
                    
                    # Check if new
                    is_new = self._is_new_pokemon(pokemon.number)
                    
                    tile = PokemonTile(
                        x, y, tile_width, tile_height,
                        pokemon,
                        self.resource_manager,
                        self.font_manager,
                        show_new_badge=is_new,
                        show_count=False
                    )
                    self.pokemon_tiles.append(tile)
            else:
                # Single pull: large centered tile
                tile_width = 300
                tile_height = 350
                x = (SCREEN_WIDTH - tile_width) // 2
                y = 120
                
                pokemon = self.results[0]
                is_new = self._is_new_pokemon(pokemon.number)
                
                tile = PokemonTile(
                    x, y, tile_width, tile_height,
                    pokemon,
                    self.resource_manager,
                    self.font_manager,
                    show_new_badge=is_new,
                    show_count=True,
                    count=self.game_data.pokemon_owned.get(pokemon.number, 0)
                )
                self.pokemon_tiles.append(tile)
    
    def _is_new_pokemon(self, pokemon_number: str) -> bool:
        """Check if this Pokemon was just caught for the first time"""
        # If count is exactly 1, it's new (just added)
        return self.game_data.pokemon_owned.get(pokemon_number, 0) == 1
    
    def _is_new_item(self, item_number: str) -> bool:
        """Check if this Item was just acquired for the first time"""
        # If count is exactly 1, it's new (just added)
        return self.game_data.items_owned.get(item_number, 0) == 1
    
    def _roll_same(self):
        """Roll the same machine and pull type again"""
        machine_data = self.resource_manager.get_gacha_machine(self.last_machine)
        cost = machine_data.cost_10pull if self.is_ten_pull else machine_data.cost_single
        
        # Check if player can afford it
        if self.game_data.gold < cost:
            from ui.popup import Popup
            
            def add_gold():
                self.game_data.gold += 20000
                self.game_data.save()
                print(f"Added 20000 gold! Total: {self.game_data.gold}")
            
            self.error_popup = Popup(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                550, 350,
                "Insufficient Funds",
                f"You need {cost:,} Pokédollars but only have {self.game_data.gold:,}.",
                self.font_manager,
                add_gold_callback=add_gold,
                pokedollar_icon=self.resource_manager.pokedollar_icon,
                audio_manager=self.audio_manager
            )
            return
        
        # Deduct cost
        self.game_data.gold -= cost
        
        # Record pull
        pull_count = 10 if self.is_ten_pull else 1
        self.game_data.record_pull(self.last_machine, count=pull_count)
        
        # Check if this is Items gacha
        if self.is_items_gacha:
            # Perform items gacha
            item_numbers = perform_items_gacha(
                self.resource_manager.items_list,
                self.resource_manager.rarities_dict,
                count=pull_count
            )
            
            # Get item objects
            results = [self.resource_manager.get_item_by_number(num) for num in item_numbers]
            results = [r for r in results if r is not None]  # Filter None
            
            print(f"{pull_count}-pull from Items machine! Gold: {self.game_data.gold}")
            for item in results:
                try:
                    print(f"  - {item.name} ({item.rarity})")
                except UnicodeEncodeError:
                    print(f"  - {item.name.encode('ascii', errors='ignore').decode('ascii')} ({item.rarity})")
                self.game_data.add_item(item.number)
            
            self.game_data.save()
            
            # Go to animation with same machine
            self.state_manager.change_state('gacha_animation', results=results, is_ten_pull=self.is_ten_pull, machine=self.last_machine, owned_before=0, is_items_gacha=True)
        else:
            # Perform Pokemon gacha
            if self.is_ten_pull:
                # Store count before adding Pokemon
                count_before = self.game_data.get_total_owned_count()
                
                results = self.gacha_system.roll_ten(self.last_machine)
                print(f"10-pull from {self.last_machine} machine! Gold: {self.game_data.gold}")
                for result in results:
                    try:
                        print(f"  - {result.name} ({result.rarity})")
                    except UnicodeEncodeError:
                        print(f"  - {result.name.encode('ascii', errors='ignore').decode('ascii')} ({result.rarity})")
                    self.game_data.add_pokemon(result.number)
            else:
                # Store count before adding Pokemon
                count_before = self.game_data.get_total_owned_count()
                
                result = self.gacha_system.roll_single(self.last_machine)
                try:
                    print(f"Single pull from {self.last_machine} machine! Got {result.name} ({result.rarity})! Gold: {self.game_data.gold}")
                except UnicodeEncodeError:
                    print(f"Single pull from {self.last_machine} machine! Got {result.name.encode('ascii', errors='ignore').decode('ascii')} ({result.rarity})! Gold: {self.game_data.gold}")
                results = [result]
                self.game_data.add_pokemon(result.number)
            
            self.game_data.save()
            
            # Go to animation with same machine
            self.state_manager.change_state('gacha_animation', results=results, is_ten_pull=self.is_ten_pull, machine=self.last_machine, owned_before=count_before, is_items_gacha=False)
    
    def _go_to_gacha(self):
        """Return to gacha buy screen with last machine selected"""
        self.state_manager.change_state('gacha_buy', last_machine=self.last_machine)
    
    def _go_to_inventory(self):
        """Go to inventory screen"""
        self.state_manager.change_state('inventory')
    
    def _check_collection_complete(self):
        """Check if collection just became complete (150->151) and play sound"""
        # Simple check: owned before < 151, owned now == 151, and sound hasn't been played yet
        total_pokemon = len(self.resource_manager.pokemon_list)  # Should be 151
        owned_count = self.game_data.get_total_owned_count()
        
        # Check if we just crossed the 151 threshold AND haven't played the sound before
        if (self.owned_count_before_pull < total_pokemon and 
            owned_count == total_pokemon and 
            not self.game_data.collection_complete_sound_played):
            
            try:
                print(f"🎉 COLLECTION COMPLETE! All {total_pokemon} Pokémon caught!")
            except UnicodeEncodeError:
                print(f"COLLECTION COMPLETE! All {total_pokemon} Pokemon caught!")
            self.audio_manager.play_sound("gotemall", priority=True)  # Highest priority!
            
            # Set flag and save immediately
            self.game_data.collection_complete_sound_played = True
            self.game_data.save()
    
    def handle_events(self, events):
        """Handle input events"""
        # Enable audio on any user interaction (for web browser autoplay policy)
        for event in events:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                # Don't auto-start music if muted
                allow_music = not self.game_data.music_muted
                self.audio_manager.enable_audio_after_interaction(allow_music_start=allow_music)
                break
        
        # Handle error popup first if visible
        if hasattr(self, 'error_popup') and self.error_popup.is_showing():
            self.error_popup.update()
            for event in events:
                self.error_popup.handle_event(event)
            return
        
        # Update buttons (they handle hover internally)
        self.roll_same_button.update()
        self.gacha_button.update()
        self.back_button.update()
        
        for event in events:
            # Check for currency click start
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.currency_rect and self.currency_rect.collidepoint(event.pos):
                    self.currency_held = True
                    self.currency_hold_timer = 0.0
                    # Add immediately on first click
                    self.game_data.gold += 10000
                    self.game_data.save()
                    print(f"Added 10000 gold! Total: {self.game_data.gold}")
                    continue
            
            # Check for currency click release
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.currency_held = False
            
            # Pass events to buttons
            self.roll_same_button.handle_event(event)
            self.gacha_button.handle_event(event)
            self.back_button.handle_event(event)
            
            # Handle keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._go_to_inventory()
                elif event.key == pygame.K_SPACE:
                    self._roll_same()
    
    def update(self, dt):
        """Update state"""
        # Handle currency hold - add gold continuously while held
        if self.currency_held:
            self.currency_hold_timer += dt
            if self.currency_hold_timer >= self.currency_add_interval:
                self.currency_hold_timer = 0.0
                self.game_data.gold += 10000
                self.game_data.save()
                print(f"Added 10000 gold (hold)! Total: {self.game_data.gold}")
    
    def render(self):
        """Render the outcome"""
        self.screen.fill(COLOR_BLACK)
        
        # Draw currency (top right, clickable with dark gray background)
        currency_x = SCREEN_WIDTH - 20
        currency_y = 30
        
        # Calculate currency dimensions for background
        icon_size = 28
        if self.font_manager:
            amount_str = f"{self.game_data.gold:,}"
            text_surface = self.font_manager.render_text(amount_str, 28, COLOR_WHITE)
            total_width = icon_size + 5 + text_surface.get_width()
            
            # Store clickable rect for currency (no background)
            self.currency_rect = pygame.Rect(
                currency_x - total_width, currency_y - icon_size // 2,
                total_width, icon_size
            )
        
        CurrencyDisplay.render(
            self.screen,
            currency_x,
            currency_y,
            self.game_data.gold,
            self.resource_manager.pokedollar_icon,
            self.font_manager,
            font_size=28,
            color=COLOR_WHITE,
            icon_size=28,
            align="right"
        )
        
        # Draw title
        if self.font_manager:
            if self.is_ten_pull:
                title = "10-PULL RESULTS!"
            else:
                title = "YOU GOT:"
            
            title_surface = self.font_manager.render_text(title, 42, COLOR_WHITE, is_title=True)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(title_surface, title_rect)
        
        # Draw Pokemon/Item tiles
        for tile in self.pokemon_tiles:
            tile.render(self.screen)
        for tile in self.item_tiles:
            tile.render(self.screen)
        
        # Draw buttons
        self.roll_same_button.render(self.screen)
        self.gacha_button.render(self.screen)
        self.back_button.render(self.screen)
        
        # Draw cost INSIDE "PULL AGAIN" button (below text)
        if self.font_manager and hasattr(self, 'roll_same_cost'):
            CurrencyDisplay.render_centered(
                self.screen,
                self.roll_same_button.rect.centerx,
                self.roll_same_button.rect.centery + 20,
                self.roll_same_cost,
                self.resource_manager.pokedollar_icon,
                self.font_manager,
                font_size=18,
                color=COLOR_WHITE,
                icon_size=18
            )
        
        # Draw error popup if visible
        if hasattr(self, 'error_popup') and self.error_popup.is_showing():
            self.error_popup.render(self.screen)

