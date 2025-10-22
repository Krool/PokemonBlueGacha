"""
GachaBuy state - Select and purchase gacha rolls
"""
import pygame
import random
from .base_state import GameState
from config import COLOR_WHITE, COLOR_BLACK, COLOR_GRAY, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.button import Button
from ui.currency_display import CurrencyDisplay
from ui.gacha_info_popup import GachaInfoPopup
from ui.items_info_popup import ItemsInfoPopup
from utils.gacha_stats import GachaStats
from logic.items_gacha import perform_items_gacha, calculate_new_item_chance


class GachaBuyState(GameState):
    """Gacha purchase screen with three machine options"""
    
    def enter(self, **kwargs):
        """Initialize gacha buy state"""
        # Restore last selected machine if provided
        if 'last_machine' in kwargs:
            self.selected_machine = kwargs['last_machine']
        else:
            self.selected_machine = "Red"  # Default selection
        
        # Get gacha machine data
        self.machines = {
            "Red": self.resource_manager.get_gacha_machine("Red"),
            "Blue": self.resource_manager.get_gacha_machine("Blue"),
            "Yellow": self.resource_manager.get_gacha_machine("Yellow"),
            "Items": self.resource_manager.get_gacha_machine("Items")
        }
        
        # Calculate recommended machine (needs most pulls)
        # Don't show recommendation if collection is complete
        total_pokemon = len(self.resource_manager.pokemon_list)
        owned_count = self.game_data.get_total_owned_count()
        
        if owned_count >= total_pokemon:
            self.recommended_machine = None  # No recommendation when complete
        else:
            self.recommended_machine, _ = GachaStats.find_recommended_version(
                self.resource_manager.pokemon_list,
                self.resource_manager.rarities_dict,
                self.game_data.pokemon_owned
            )
        
        # Currency click hold tracking
        self.currency_held = False
        self.currency_hold_timer = 0.0
        self.currency_add_interval = 0.1  # Add gold every 0.1 seconds while held
        
        # Info popup
        self.info_popup = None
        
        # Select 3 random Pokemon to highlight for each machine
        self._select_featured_pokemon()
        
        # Create UI elements
        self._create_ui_elements()
        
        print(f"Entered GachaBuyState (Recommended: {self.recommended_machine})")
    
    def _create_ui_elements(self):
        """Create all UI buttons and elements"""
        # Machine selection buttons (tabs at top) - now 4 machines
        button_width = 180
        button_height = 50
        button_y = 50
        spacing = 15
        total_width = (button_width * 4) + (spacing * 3)
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        # Store button positions for rendering RECOMMENDED badge
        self.button_positions = {
            "Red": (start_x, button_y),
            "Blue": (start_x + button_width + spacing, button_y),
            "Yellow": (start_x + (button_width + spacing) * 2, button_y),
            "Items": (start_x + (button_width + spacing) * 3, button_y)
        }
        
        self.machine_buttons = {
            "Red": Button(
                start_x, button_y, button_width, button_height,
                "RED MACHINE",
                self.font_manager,
                font_size=20,
                bg_color=(180, 50, 50),
                hover_color=(220, 70, 70),
                use_title_font=True,
                callback=lambda: self._select_machine("Red")
            ),
            "Blue": Button(
                start_x + button_width + spacing, button_y, button_width, button_height,
                "BLUE MACHINE",
                self.font_manager,
                font_size=20,
                bg_color=(50, 50, 180),
                hover_color=(70, 70, 220),
                use_title_font=True,
                callback=lambda: self._select_machine("Blue")
            ),
            "Yellow": Button(
                start_x + (button_width + spacing) * 2, button_y, button_width, button_height,
                "YELLOW MACHINE",
                self.font_manager,
                font_size=20,
                bg_color=(180, 180, 50),
                hover_color=(220, 220, 70),
                use_title_font=True,
                callback=lambda: self._select_machine("Yellow")
            ),
            "Items": Button(
                start_x + (button_width + spacing) * 3, button_y, button_width, button_height,
                "ITEMS MACHINE",
                self.font_manager,
                font_size=20,
                bg_color=(100, 150, 100),
                hover_color=(130, 180, 130),
                use_title_font=True,
                callback=lambda: self._select_machine("Items")
            )
        }
        
        # Pull buttons (bottom section) - larger with cost inside
        pull_button_width = 250
        pull_button_height = 80
        pull_button_y = SCREEN_HEIGHT - 130
        pull_button_spacing = 40
        
        self.single_pull_button = Button(
            SCREEN_WIDTH // 2 - pull_button_width - pull_button_spacing // 2,
            pull_button_y,
            pull_button_width,
            pull_button_height,
            "1-PULL",
            self.font_manager,
            font_size=24,
            bg_color=(50, 150, 50),
            hover_color=(70, 200, 70),
            use_title_font=True,
            callback=self._single_pull
        )
        
        self.ten_pull_button = Button(
            SCREEN_WIDTH // 2 + pull_button_spacing // 2,
            pull_button_y,
            pull_button_width,
            pull_button_height,
            "10-PULL",
            self.font_manager,
            font_size=24,
            bg_color=(50, 100, 200),
            hover_color=(70, 150, 255),
            use_title_font=True,
            callback=self._ten_pull
        )
        
        # Back button
        self.back_button = Button(
            50, SCREEN_HEIGHT - 70, 150, 50,
            "BACK",
            self.font_manager,
            font_size=20,
            bg_color=(100, 100, 100),
            hover_color=(150, 150, 150),
            callback=self._go_back
        )
        
        # Info button (to the left of 1-pull button)
        info_button_width = 100
        info_button_height = 50
        info_button_x = SCREEN_WIDTH // 2 - pull_button_width - pull_button_spacing // 2 - info_button_width - 20
        self.info_button = Button(
            info_button_x,
            pull_button_y + (pull_button_height - info_button_height) // 2,  # Vertically centered with pull buttons
            info_button_width,
            info_button_height,
            "INFO",
            self.font_manager,
            font_size=20,
            bg_color=(50, 100, 150),
            hover_color=(70, 130, 180),
            callback=self._show_info
        )
        
        # Add gold button (cheat)
    
    def _select_machine(self, machine_name: str):
        """Select a gacha machine"""
        self.selected_machine = machine_name
        print(f"Selected {machine_name} machine")
    
    def _select_featured_pokemon(self):
        """Select 3 Pokemon/Items to feature for each gacha machine"""
        self.featured_pokemon = {}
        self.featured_items = {}
        
        # RED: Show version exclusives (Pokemon with Blue_Weight=0 and Red_Weight>0)
        red_exclusives = [p for p in self.resource_manager.pokemon_list 
                         if p.red_weight > 0 and p.blue_weight == 0]
        if len(red_exclusives) >= 3:
            self.featured_pokemon["Red"] = random.sample(red_exclusives, 3)
        else:
            # Fallback: just show random Pokemon from Red
            red_available = [p for p in self.resource_manager.pokemon_list 
                           if p.red_weight > 0]
            self.featured_pokemon["Red"] = random.sample(red_available, min(3, len(red_available)))
        
        # BLUE: Show version exclusives (Pokemon with Red_Weight=0 and Blue_Weight>0)
        blue_exclusives = [p for p in self.resource_manager.pokemon_list 
                          if p.blue_weight > 0 and p.red_weight == 0]
        if len(blue_exclusives) >= 3:
            self.featured_pokemon["Blue"] = random.sample(blue_exclusives, 3)
        else:
            # Fallback: just show random Pokemon from Blue
            blue_available = [p for p in self.resource_manager.pokemon_list 
                            if p.blue_weight > 0]
            self.featured_pokemon["Blue"] = random.sample(blue_available, min(3, len(blue_available)))
        
        # YELLOW: Show Legendary Pokemon
        legendaries = [p for p in self.resource_manager.pokemon_list 
                      if p.rarity == "Legendary" and p.yellow_weight > 0]
        if len(legendaries) >= 3:
            self.featured_pokemon["Yellow"] = random.sample(legendaries, 3)
        else:
            # If less than 3 legendaries, show all legendaries + some epics
            epics = [p for p in self.resource_manager.pokemon_list 
                    if p.rarity == "Epic" and p.yellow_weight > 0]
            all_featured = legendaries + random.sample(epics, min(3 - len(legendaries), len(epics)))
            self.featured_pokemon["Yellow"] = all_featured[:3]
        
        # ITEMS: Show high-value items (Legendary and Epic)
        high_value_items = [i for i in self.resource_manager.items_list 
                           if i.rarity in ["Legendary", "Epic"]]
        if len(high_value_items) >= 3:
            self.featured_items["Items"] = random.sample(high_value_items, 3)
        else:
            # Show all high-value + some rare
            rare_items = [i for i in self.resource_manager.items_list if i.rarity == "Rare"]
            all_featured = high_value_items + random.sample(rare_items, min(3 - len(high_value_items), len(rare_items)))
            self.featured_items["Items"] = all_featured[:3]
    
    def _calculate_new_pokemon_chance(self, version: str) -> float:
        """Calculate % chance of getting a new (unowned) Pokemon"""
        # Get available Pokemon for this version
        available = [p for p in self.resource_manager.pokemon_list 
                    if p.get_weight_for_version(version) > 0]
        
        if not available:
            return 0.0
        
        # Count unowned Pokemon
        unowned_count = sum(1 for p in available if not self.game_data.has_pokemon(p.number))
        
        # Simple calculation: unowned / total available
        return (unowned_count / len(available)) * 100.0
    
    def _single_pull(self):
        """Perform single pull"""
        machine = self.machines[self.selected_machine]
        
        if self.game_data.gold >= machine.cost_single:
            self.game_data.gold -= machine.cost_single
            self.game_data.record_pull(self.selected_machine, count=1)
            self.game_data.save()
            
            # Check if this is Items gacha
            if self.selected_machine == "Items":
                # Perform items gacha
                item_numbers = perform_items_gacha(
                    self.resource_manager.items_list,
                    self.resource_manager.rarities_dict,
                    count=1
                )
                
                # Get item objects
                results = [self.resource_manager.get_item_by_number(num) for num in item_numbers]
                results = [r for r in results if r is not None]  # Filter None
                
                print(f"Single pull from Items machine! Got {results[0].name} ({results[0].rarity})! Gold: {self.game_data.gold}")
                
                # Add to inventory
                for item in results:
                    self.game_data.add_item(item.number)
                self.game_data.save()
                
                # Transition to animation
                self.state_manager.change_state('gacha_animation', results=results, is_ten_pull=False, machine=self.selected_machine, owned_before=0, is_items_gacha=True)
            else:
                # Store count before adding Pokemon
                count_before = self.game_data.get_total_owned_count()
                
                # Perform gacha roll
                result = self.gacha_system.roll_single(self.selected_machine)
                print(f"Single pull from {self.selected_machine} machine! Got {result.name} ({result.rarity})! Gold: {self.game_data.gold}")
                
                # Add to inventory
                self.game_data.add_pokemon(result.number)
                self.game_data.save()
                
                # Transition to animation
                self.state_manager.change_state('gacha_animation', results=[result], is_ten_pull=False, machine=self.selected_machine, owned_before=count_before, is_items_gacha=False)
        else:
            from ui.popup import Popup
            machine = self.machines[self.selected_machine]
            
            def add_gold():
                self.game_data.gold += 20000
                self.game_data.save()
                print(f"Added 20000 gold! Total: {self.game_data.gold}")
            
            self.error_popup = Popup(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                550, 350,
                "Insufficient Funds",
                f"You need {machine.cost_single:,} Pokédollars but only have {self.game_data.gold:,}.",
                self.font_manager,
                add_gold_callback=add_gold,
                pokedollar_icon=self.resource_manager.pokedollar_icon
            )
    
    def _ten_pull(self):
        """Perform 10-pull"""
        machine = self.machines[self.selected_machine]
        
        if self.game_data.gold >= machine.cost_10pull:
            self.game_data.gold -= machine.cost_10pull
            self.game_data.record_pull(self.selected_machine, count=10)
            self.game_data.save()
            
            # Check if this is Items gacha
            if self.selected_machine == "Items":
                # Perform items gacha
                item_numbers = perform_items_gacha(
                    self.resource_manager.items_list,
                    self.resource_manager.rarities_dict,
                    count=10
                )
                
                # Get item objects
                results = [self.resource_manager.get_item_by_number(num) for num in item_numbers]
                results = [r for r in results if r is not None]  # Filter None
                
                print(f"10-pull from Items machine! Gold: {self.game_data.gold}")
                for item in results:
                    print(f"  - {item.name} ({item.rarity})")
                    self.game_data.add_item(item.number)
                self.game_data.save()
                
                # Transition to animation
                self.state_manager.change_state('gacha_animation', results=results, is_ten_pull=True, machine=self.selected_machine, owned_before=0, is_items_gacha=True)
            else:
                # Store count before adding Pokemon
                count_before = self.game_data.get_total_owned_count()
                
                # Perform gacha rolls
                results = self.gacha_system.roll_ten(self.selected_machine)
                print(f"10-pull from {self.selected_machine} machine! Gold: {self.game_data.gold}")
                for result in results:
                    print(f"  - {result.name} ({result.rarity})")
                    self.game_data.add_pokemon(result.number)
                self.game_data.save()
                
                # Transition to animation
                self.state_manager.change_state('gacha_animation', results=results, is_ten_pull=True, machine=self.selected_machine, owned_before=count_before, is_items_gacha=False)
        else:
            from ui.popup import Popup
            machine = self.machines[self.selected_machine]
            
            def add_gold():
                self.game_data.gold += 20000
                self.game_data.save()
                print(f"Added 20000 gold! Total: {self.game_data.gold}")
            
            self.error_popup = Popup(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                550, 350,
                "Insufficient Funds",
                f"You need {machine.cost_10pull:,} Pokédollars but only have {self.game_data.gold:,}.",
                self.font_manager,
                add_gold_callback=add_gold,
                pokedollar_icon=self.resource_manager.pokedollar_icon
            )
    
    def _go_back(self):
        """Return to inventory"""
        self.state_manager.change_state('inventory')
    
    def _show_info(self):
        """Show drop rates popup for selected machine"""
        if self.selected_machine == "Items":
            # Show items info popup
            self.info_popup = ItemsInfoPopup(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                700,
                600,
                self.resource_manager.items_list,
                self.resource_manager.rarities_dict,
                self.font_manager,
                callback=None
            )
        else:
            # Show Pokemon info popup
            self.info_popup = GachaInfoPopup(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                700,
                600,
                self.selected_machine,
                self.resource_manager.pokemon_list,
                self.resource_manager.rarities_dict,
                self.font_manager,
                callback=None
            )
    
    def exit(self):
        """Clean up gacha buy state"""
        print("Exited GachaBuyState")
    
    def handle_events(self, events):
        """Handle input events"""
        # Enable audio on any user interaction (for web browser autoplay policy)
        for event in events:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.audio_manager.enable_audio_after_interaction()
                break
        
        # Handle info popup first if visible
        if self.info_popup is not None and self.info_popup.is_showing():
            self.info_popup.update()
            for event in events:
                self.info_popup.handle_event(event)
            # Check if popup was closed
            if not self.info_popup.is_showing():
                self.info_popup = None
            return
        
        # Handle error popup if visible
        if hasattr(self, 'error_popup') and self.error_popup.is_showing():
            self.error_popup.update()
            for event in events:
                self.error_popup.handle_event(event)
            return
        
        for event in events:
            # Check for currency click start (note: currency_rect is set in render())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hasattr(self, 'currency_rect') and self.currency_rect and self.currency_rect.collidepoint(event.pos):
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
            
            # Handle all buttons
            for button in self.machine_buttons.values():
                button.handle_event(event)
            
            self.single_pull_button.handle_event(event)
            self.ten_pull_button.handle_event(event)
            self.back_button.handle_event(event)
            self.info_button.handle_event(event)
    
    def update(self, dt):
        """Update state"""
        # Update button hover states
        for button in self.machine_buttons.values():
            button.update()
        
        # Handle currency hold - add gold continuously while held
        if self.currency_held:
            self.currency_hold_timer += dt
            if self.currency_hold_timer >= self.currency_add_interval:
                self.currency_hold_timer = 0.0
                self.game_data.gold += 10000
                self.game_data.save()
                print(f"Added 10000 gold (hold)! Total: {self.game_data.gold}")
        
        self.single_pull_button.update()
        self.ten_pull_button.update()
        self.back_button.update()
        self.info_button.update()
    
    def render(self):
        """Render the gacha buy screen"""
        self.screen.fill(COLOR_BLACK)
        
        # Draw gacha machine image based on selection
        machine_image = None
        if self.selected_machine == "Red":
            machine_image = self.resource_manager.gacha_red
        elif self.selected_machine == "Blue":
            machine_image = self.resource_manager.gacha_blue
        elif self.selected_machine == "Yellow":
            machine_image = self.resource_manager.gacha_yellow
        elif self.selected_machine == "Items":
            machine_image = self.resource_manager.gacha_item
        
        if machine_image:
            # Scale machine image to fit screen (max 400x400)
            max_size = 400
            original_size = machine_image.get_size()
            scale_factor = min(max_size / original_size[0], max_size / original_size[1])
            
            # Only scale down if image is too large
            if scale_factor < 1.0:
                new_width = int(original_size[0] * scale_factor)
                new_height = int(original_size[1] * scale_factor)
                scaled_image = pygame.transform.smoothscale(machine_image, (new_width, new_height))
            else:
                scaled_image = machine_image
            
            # Center the gacha machine image
            img_rect = scaled_image.get_rect(center=(SCREEN_WIDTH // 2, 300))
            self.screen.blit(scaled_image, img_rect)
        
        # Draw machine selection buttons
        for machine_name, button in self.machine_buttons.items():
            # Highlight selected machine
            if machine_name == self.selected_machine:
                # Draw a thicker border for selected
                pygame.draw.rect(self.screen, (255, 255, 0), button.rect, 4)
            button.render(self.screen)
            
            # Draw RECOMMENDED badge on top of button if this is the recommended machine
            if machine_name == self.recommended_machine:
                badge_width = 160
                badge_height = 25
                badge_x = button.rect.centerx - badge_width // 2
                badge_y = button.rect.top - 30  # Position above button
                badge_rect = pygame.Rect(badge_x, badge_y, badge_width, badge_height)
                
                # Draw bright yellow background
                pygame.draw.rect(self.screen, (255, 255, 0), badge_rect)
                pygame.draw.rect(self.screen, (200, 200, 0), badge_rect, 2)  # Border
                
                # Draw RECOMMENDED text in black
                rec_text = self.font_manager.render_text("RECOMMENDED", 14, (0, 0, 0), is_title=True)
                rec_rect = rec_text.get_rect(center=badge_rect.center)
                self.screen.blit(rec_text, rec_rect)
        
        # Draw featured Pokemon sprites (3 random for this machine)
        # Don't show featured items for Items machine
        if self.selected_machine != "Items" and hasattr(self, 'featured_pokemon') and self.selected_machine in self.featured_pokemon:
            # Draw featured Pokemon
            featured = self.featured_pokemon[self.selected_machine]
            sprite_size = 80
            sprite_spacing = 20
            total_width = (sprite_size * 3) + (sprite_spacing * 2)
            start_x = (SCREEN_WIDTH - total_width) // 2
            sprite_y = 400
            
            for i, pokemon in enumerate(featured):
                x = start_x + i * (sprite_size + sprite_spacing)
                
                # Get rarity color
                rarity_obj = self.resource_manager.rarities_dict.get(pokemon.rarity)
                rarity_color = rarity_obj.get_color_rgb() if rarity_obj else COLOR_WHITE
                
                # Draw background box with rarity color border
                box_rect = pygame.Rect(x, sprite_y, sprite_size, sprite_size)
                pygame.draw.rect(self.screen, COLOR_BLACK, box_rect)
                pygame.draw.rect(self.screen, rarity_color, box_rect, 3)
                
                # Draw Pokemon sprite
                image = self.resource_manager.images.get(pokemon.image_path)
                if image:
                    scaled_image = pygame.transform.scale(image, (sprite_size - 10, sprite_size - 10))
                    img_rect = scaled_image.get_rect(center=box_rect.center)
                    self.screen.blit(scaled_image, img_rect)
        
        # Draw % chance for new Pokemon/Items
        if self.selected_machine == "Items":
            new_chance = calculate_new_item_chance(
                self.resource_manager.items_list,
                self.resource_manager.rarities_dict,
                self.game_data.items_owned
            )
            chance_text = f"New Item Chance: {new_chance:.1f}%"
        else:
            new_chance = self._calculate_new_pokemon_chance(self.selected_machine)
            chance_text = f"New Pokémon Chance: {new_chance:.1f}%"
        chance_surface = self.font_manager.render_text(chance_text, 22, COLOR_WHITE, is_title=True)
        chance_rect = chance_surface.get_rect(center=(SCREEN_WIDTH // 2, 495))
        self.screen.blit(chance_surface, chance_rect)
        
        # Draw machine description (with more spacing from buttons)
        machine = self.machines[self.selected_machine]
        desc_y = 525
        desc_lines = self._wrap_text(machine.description, 700, 18)
        for i, line in enumerate(desc_lines):
            desc_surface = self.font_manager.render_text(line, 18, COLOR_WHITE)
            desc_rect = desc_surface.get_rect(center=(SCREEN_WIDTH // 2, desc_y + i * 25))
            self.screen.blit(desc_surface, desc_rect)
        
        # Add spacing line between description and buttons (visual separator)
        separator_y = desc_y + len(desc_lines) * 25 + 15
        # (buttons start at SCREEN_HEIGHT - 130, so this creates good spacing)
        
        # Draw player's currency balance (top right with dark gray background)
        currency_x = SCREEN_WIDTH - 20
        currency_y = 35
        icon_size = 28
        
        if self.font_manager:
            amount_str = f"{self.game_data.gold:,}"
            text_surface = self.font_manager.render_text(amount_str, 28, COLOR_WHITE)
            total_width = icon_size + 5 + text_surface.get_width()
            
            # Draw dark gray background container
            padding = 10
            bg_rect = pygame.Rect(
                currency_x - total_width - padding,
                currency_y - icon_size // 2 - padding,
                total_width + padding * 2,
                icon_size + padding * 2
            )
            pygame.draw.rect(self.screen, (50, 50, 50), bg_rect)
            pygame.draw.rect(self.screen, (100, 100, 100), bg_rect, 2)  # Border
            
            # Store clickable rect (same as background)
            self.currency_rect = bg_rect
        
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
        
        # Draw pull buttons
        self.single_pull_button.render(self.screen)
        self.ten_pull_button.render(self.screen)
        
        # Draw currency costs INSIDE pull buttons
        machine = self.machines[self.selected_machine]
        
        # Single pull cost (inside button, below text)
        CurrencyDisplay.render_centered(
            self.screen,
            self.single_pull_button.rect.centerx,
            self.single_pull_button.rect.centery + 20,
            machine.cost_single,
            self.resource_manager.pokedollar_icon,
            self.font_manager,
            font_size=18,
            color=COLOR_WHITE,
            icon_size=18
        )
        
        # 10-pull cost (inside button, below text)
        CurrencyDisplay.render_centered(
            self.screen,
            self.ten_pull_button.rect.centerx,
            self.ten_pull_button.rect.centery + 20,
            machine.cost_10pull,
            self.resource_manager.pokedollar_icon,
            self.font_manager,
            font_size=18,
            color=COLOR_WHITE,
            icon_size=18
        )
        
        # Draw back button
        self.back_button.render(self.screen)
        
        # Draw info button
        self.info_button.render(self.screen)
        
        # Draw info popup if visible
        if self.info_popup is not None and self.info_popup.is_showing():
            self.info_popup.render(self.screen)
        
        # Draw error popup if visible
        if hasattr(self, 'error_popup') and self.error_popup.is_showing():
            self.error_popup.render(self.screen)
    
    def _wrap_text(self, text: str, max_width: int, font_size: int) -> list:
        """
        Wrap text to fit within max_width
        
        Args:
            text: Text to wrap
            max_width: Maximum width in pixels
            font_size: Font size
            
        Returns:
            List of text lines
        """
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            width, _ = self.font_manager.get_text_size(test_line, font_size)
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

