#!/usr/bin/env python3
"""
Standalone GPT Creator 
"""

import asyncio
import json
import re
import time
import os
import platform
import warnings
import random
from typing import Optional, Dict, Any
import logging

from playwright.async_api import async_playwright, Page, Browser

# Python 3.12 compatibility fixes
import sys
if sys.version_info >= (3, 12):
    # Suppress new warnings in Python 3.12
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="playwright")
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

# Suppress harmless Windows asyncio cleanup warnings
if platform.system() == "Windows":
    warnings.filterwarnings("ignore", category=ResourceWarning, message=".*unclosed transport.*")
    warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*Event loop is closed.*")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrowserCrashedException(Exception):
    """Custom exception for when browser crashes or becomes unresponsive"""
    pass

class GPTManager:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.context = None
        self.cookies_file = "chatgpt_cookies.json"
        
    def load_config_from_json(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    
    def load_openapi_schema(self, openapi_file: str) -> Dict[str, Any]:
        """Load and update OpenAPI schema"""
        with open(openapi_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
            
        return schema

    async def save_cookies(self):
        """Save browser cookies to file"""
        try:
            if self.context:
                cookies = await self.context.cookies()
                with open(self.cookies_file, 'w') as f:
                    json.dump(cookies, f)
                logger.info("Cookies saved successfully")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    async def load_cookies(self):
        """Load browser cookies from file"""
        try:
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                await self.context.add_cookies(cookies)
                logger.info("Cookies loaded successfully")
                return True
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
        return False
        
    async def initialize_browser(self):
        """Initialize Playwright browser with simple settings for older version"""
        playwright = await async_playwright().start()
        
        # Use simple browser settings that worked with older Playwright versions
        self.browser = await playwright.chromium.launch(
            headless=False,  # Keep visible for user to see login process
            args=[
                '--disable-blink-features=AutomationControlled',  # Hide automation
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        # Create context with simple settings
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York'
        )
        
        self.page = await self.context.new_page()

        # Add script to remove webdriver property
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        # Load existing cookies if available
        await self.load_cookies()
        
    async def close_browser(self):
        """Close the browser and clean up resources properly"""
        try:
            # Save cookies before closing
            await self.save_cookies()
        except Exception as e:
            logger.debug(f"Error saving cookies during cleanup: {e}")
            
        try:
            # Close page first and wait for it to fully close
            if self.page and not self.page.is_closed():
                await self.page.close()
                await asyncio.sleep(0.5)  # Give time for page cleanup
                self.page = None
                
            # Close context and wait for cleanup
            if self.context:
                await self.context.close()
                await asyncio.sleep(0.5)  # Give time for context cleanup
                self.context = None
                
            # Close browser and wait for all processes to terminate
            if self.browser:
                await self.browser.close()
                await asyncio.sleep(1)  # Give time for browser processes to terminate
                self.browser = None
                
            # Additional wait for Windows to clean up pipes/transports
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.debug(f"Error during browser cleanup: {e}")
            # Force close if normal cleanup fails
            try:
                if self.browser:
                    await self.browser.close()
                    await asyncio.sleep(1)
                    self.browser = None
            except Exception as force_error:
                logger.debug(f"Error during force close: {force_error}")
                
        # Reset all references
        self.page = None
        self.context = None
        self.browser = None
        
    async def is_browser_alive(self) -> bool:
        """Check if browser and page are still alive"""
        try:
            if not self.browser or not self.page or not self.context:
                return False
            if self.page.is_closed():
                return False
            # Try a simple operation to test if browser is responsive
            await self.page.evaluate("() => true")
            return True
        except Exception as e:
            logger.debug(f"Browser health check failed: {e}")
            return False
            
    async def ensure_browser_alive(self):
        """Ensure browser is alive, raise exception if not"""
        if not await self.is_browser_alive():
            logger.error("Browser has crashed or become unresponsive")
            raise BrowserCrashedException("Browser is not responsive")
            
    async def login_to_openai(self) -> bool:
        """Navigate to OpenAI and wait for user to login"""
        try:
            logger.info("Navigating to OpenAI ChatGPT...")
            await self.page.goto("https://chatgpt.com/")
            
            # Add human-like delay
            await asyncio.sleep(2)
            
            # Wait for page to fully load
            await self.page.wait_for_load_state('networkidle')
            
            # Check if browser is still alive after navigation
            await self.ensure_browser_alive()

            # Wait for either login button or already logged in state
            try:
                # Check if login button is present (user not logged in)
                login_button = await self.page.wait_for_selector('button[data-testid="login-button"]', timeout=3000)
                logger.info("Login button found, clicking to start login process...")   
            except:
                # Login button not found, user is already logged in
                logger.info("Already logged in to OpenAI")
                return True
            
            # Wait for login to complete and page to reload with profile
            try:        
                await login_button.click()
                
                logger.info("Please complete the login process in the browser window...")
                logger.info("If you see a CAPTCHA, please complete it manually - the script will continue automatically")
                logger.info("Waiting for login to complete...")
                
                # Wait for the page to display profile button (indicating successful login)
                await asyncio.sleep(3)
                await self.page.wait_for_selector('[data-testid="profile-button"]', timeout=180000)  # 3 minutes
                
                # Check if browser is still alive after login
                await self.ensure_browser_alive()
                
                logger.info("Login successful!")
                return True
            except Exception as e:
                logger.info("Did not login within time limit...exiting")
                raise Exception(f"Login failed: {e}")       
        except BrowserCrashedException:
            # Re-raise browser crashes to trigger restart
            raise
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    async def navigate_to_gpt_builder(self) -> bool:
        """Navigate to the GPT builder page"""
        try:
            logger.info("Navigating to GPT builder...")
            await self.page.goto("https://chatgpt.com/gpts/editor")
            
            # Wait for the page to load
            await self.page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
            
            # Check if browser is still alive after navigation
            await self.ensure_browser_alive()
            
            # Debug: Check what page we're actually on
            current_url = self.page.url
            page_title = await self.page.title()
            logger.info(f"Current URL: {current_url}")
            logger.info(f"Page title: {page_title}")
            
            logger.info("GPT builder loaded successfully!")
            return True
        except BrowserCrashedException:
            # Re-raise browser crashes to trigger restart
            raise
        except Exception as e:
            logger.error(f"Failed to navigate to GPT builder: {e}")
            return False
    
    async def check_existing_gpt(self, gpt_name: str) -> Optional[str]:
        """Check if a GPT with the given name already exists"""
        try:
            await self.ensure_browser_alive()
            
            logger.info(f"Checking for existing GPT: {gpt_name}")
            
            # Go to "My GPTs" page first
            await self.page.goto("https://chatgpt.com/gpts/mine")
            await self.page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)
            
            # Check if page crashed after navigation
            await self.ensure_browser_alive()
            
            # Look for GPT containers - they typically have the GPT name
            gpt_containers = await self.page.query_selector_all('div[tabindex="0"]')
            
            for container in gpt_containers:
                try:
                    # Get text content of the container
                    container_text = await container.text_content()
                    logger.info(f"Container text: {container_text}")
                    
                    if container_text and gpt_name.lower() in container_text.lower():
                        logger.info(f"Found GPT container with matching name")
                        
                        # Look for the edit button within this container
                        edit_button = await container.query_selector('button[class*="text-token-text-primary"]')
                        
                        if edit_button:
                            logger.info(f"Found edit button: {edit_button}")
                            await edit_button.click()
                            await asyncio.sleep(3)
                            logger.info("Clicked edit button for existing GPT")
                            # Return a special indicator that we clicked the edit button
                            return "EDIT_BUTTON_CLICKED"
                        else:
                            # Fallback: try to find any button in the container
                            fallback_button = await container.query_selector('button')
                            if fallback_button:
                                logger.info("Using fallback button")
                                await fallback_button.click()
                                await asyncio.sleep(3)
                                return "EDIT_BUTTON_CLICKED"
                            else:
                                logger.warning("No edit button found in container")
                except Exception as e:
                    logger.error(f"Error checking container: {e}")
                    continue
                    
            logger.info("No existing GPT found")
            return None
            
        except BrowserCrashedException:
            # Re-raise browser crashes to trigger restart
            raise
        except Exception as e:
            logger.warning(f"Error checking for existing GPT: {e}")
            return None

    async def create_new_gpt(self, config: Dict[str, Any], existing_gpt_url: Optional[str] = None) -> bool:
        """Create or update GPT with the given configuration"""
        try:
            await self.ensure_browser_alive()
            
            if existing_gpt_url and existing_gpt_url != "EDIT_BUTTON_CLICKED":
                logger.info("Updating existing GPT...")
                await self.page.goto(existing_gpt_url)
                await self.page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)
                await self.ensure_browser_alive()
            elif existing_gpt_url == "EDIT_BUTTON_CLICKED":
                logger.info("Edit button was already clicked, continuing with current page")
                # Wait for the page to load after clicking edit button
                await self.page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)
                await self.ensure_browser_alive()
            else:
                logger.info("Creating new GPT...")
                if not await self.navigate_to_gpt_builder():
                    return False
                await asyncio.sleep(2)
                await self.ensure_browser_alive()
            
            await asyncio.sleep(1)
            
            # Click on Configure tab
            await self.click_configure_tab()
            
            # Fill in GPT name
            logger.info("Setting GPT name...")
            try:
                # Debug: Check what input fields are available
                all_inputs = await self.page.query_selector_all('input, textarea')
                logger.info(f"Found {len(all_inputs)} input fields on page")
                
                for i, input_elem in enumerate(all_inputs[:5]):  # Check first 5 inputs
                    try:
                        placeholder = await input_elem.get_attribute('placeholder')
                        input_type = await input_elem.get_attribute('type')
                        logger.info(f"Input {i+1}: type='{input_type}', placeholder='{placeholder}'")
                    except:
                        pass
                
                name_input = await self.page.wait_for_selector('input[placeholder*="Name"], input[placeholder*="name"], textarea[placeholder*="Name"]', timeout=5000)
                await name_input.click()
                await self.page.keyboard.press('Control+a')
                await name_input.fill(config['name'])
                logger.info("GPT name filled successfully")
                await self.ensure_browser_alive()
            except Exception as e:
                logger.error(f"Failed to fill GPT name: {e}")
                # Don't return False - continue with other fields
                logger.info("Continuing despite name field error...")
            
            # Fill in description using the specific data-testid selector
            logger.info("Setting GPT description...")
            try:
                desc_input = await self.page.wait_for_selector('input[data-testid="gizmo-description-input"]', timeout=5000)
                await desc_input.click()
                await self.page.keyboard.press('Control+a')
                await desc_input.fill(config['description'])
                logger.info("GPT description filled successfully")
                await self.ensure_browser_alive()
            except Exception as e:
                logger.warning(f"Failed to fill description with specific selector: {e}")
                # Fallback to generic selectors
                desc_selectors = [
                    'textarea[placeholder*="Description"]',
                    'input[placeholder*="Description"]',
                    'textarea[placeholder*="description"]'
                ]
                
                for selector in desc_selectors:
                    try:
                        desc_input = await self.page.wait_for_selector(selector, timeout=3000)
                        await desc_input.click()
                        await self.page.keyboard.press('Control+a')
                        await desc_input.fill(config['description'])
                        logger.info("Set GPT description with fallback")
                        break
                    except:
                        continue
            
            # Fill in instructions using the specific data-testid selector
            logger.info("Setting GPT instructions...")
            try:
                instructions_input = await self.page.wait_for_selector('textarea[data-testid="gizmo-instructions-input"]', timeout=5000)
                await instructions_input.click()
                await self.page.keyboard.press('Control+a')
                await instructions_input.fill(config['instructions'])
                logger.info("GPT instructions filled successfully")
                await self.ensure_browser_alive()
            except Exception as e:
                logger.warning(f"Failed to configure instructions with specific selector: {e}")
                # Fallback to generic selectors
                instructions_selectors = [
                    'textarea[placeholder*="Instructions"]',
                    'textarea[placeholder*="instructions"]',
                    'div[contenteditable="true"]'
                ]
                
                for selector in instructions_selectors:
                    try:
                        instructions_input = await self.page.wait_for_selector(selector, timeout=3000)
                        await instructions_input.click()
                        await self.page.keyboard.press('Control+a')
                        await instructions_input.fill(config['instructions'])
                        logger.info("Set GPT instructions with fallback")
                        break
                    except:
                        continue
            
            # Add conversation starters
            await self.add_conversation_starters(config.get('conversation_starters', []))
            
            # Configure actions if OpenAPI spec is provided
            if config.get('openapi_spec_file'):
                openapi_spec = self.load_openapi_schema(config['openapi_spec_file'])
                await self.configure_actions(openapi_spec)
            
            # Save GPT
            await self.save_gpt()
            
            logger.info("GPT created/updated successfully!")
            return True
            
        except BrowserCrashedException:
            # Re-raise browser crashes to trigger restart
            raise
        except Exception as e:
            logger.error(f"Error creating GPT: {e}")
            return False

    async def click_configure_tab(self):
        """Click on the Configure tab in GPT editor"""
        try:
            logger.info("Looking for Configure tab...")
            
            # Try the specific data-testid selector first (most reliable)
            try:
                configure_tab = await self.page.wait_for_selector('button[data-testid="gizmo-editor-configure-button"]', timeout=5000)
                await configure_tab.click()
                await asyncio.sleep(2)
                logger.info("Clicked Configure tab using data-testid")
                return True
            except Exception as e:
                logger.debug(f"Configure data-testid selector not found: {e}")
            
            # Fallback to other selectors
            configure_selectors = [
                'button:has-text("Configure")',
                'div:has-text("Configure")',
                'tab:has-text("Configure")',
                '[role="tab"]:has-text("Configure")',
                'button[aria-selected="false"]:has-text("Configure")',
                'a:has-text("Configure")'
            ]
            
            for selector in configure_selectors:
                try:
                    configure_tab = await self.page.wait_for_selector(selector, timeout=3000)
                    await configure_tab.click()
                    await asyncio.sleep(2)
                    logger.info("Clicked Configure tab")
                    return True
                except Exception as e:
                    logger.debug(f"Configure selector '{selector}' not found: {e}")
                    continue
            
            # If no Configure tab found, we might already be in the right place
            logger.info("No Configure tab found - assuming already in configure mode")
            return True
            
        except Exception as e:
            logger.warning(f"Error clicking Configure tab: {e}")
            return True  # Continue anyway

    async def add_conversation_starters(self, starters: list):
        """Add conversation starters using the better section-based approach"""
        try:
            logger.info("Adding conversation starters...")
            
            # Look for the conversation starters section with parent div mb-6
            try:
                # Find the div with class mb-6 that contains "Conversation starters"
                conversation_section = await self.page.wait_for_selector('div.mb-6:has-text("Conversation starters")', timeout=5000)
                if conversation_section:
                    logger.info("Found conversation starters section")
                    
                    # Add conversation starters to empty fields
                    added_count = 0
                    for i, starter in enumerate(starters[:4]):  # Max 4 starters
                        # Find all text input fields within this section
                        text_inputs = await conversation_section.query_selector_all('input[type="text"]')
                        logger.info(f"Found {len(text_inputs)} text input fields in conversation starters section")
                        
                        if i < len(text_inputs):
                            try:
                                input_field = text_inputs[i]
                                current_value = await input_field.input_value()
                                
                                await input_field.fill(starter)
                                logger.info(f"Added conversation starter {i+1}: {starter}")
                                added_count += 1    
                            except Exception as e:
                                logger.debug(f"Failed to add conversation starter {i+1}: {e}")
                                continue
                    
                    logger.info(f"Successfully added {added_count} conversation starters")
                else:
                    logger.warning("Could not find conversation starters section")
                    # Fallback to old method
                    await self.add_conversation_starters_fallback(starters)
                    
            except Exception as e:
                logger.warning(f"Failed to find conversation starters section: {e}")
                # Fallback to old method
                await self.add_conversation_starters_fallback(starters)
                    
        except Exception as e:
            logger.error(f"Failed to add conversation starters: {e}")

    async def add_conversation_starters_fallback(self, starters: list):
        """Fallback method for adding conversation starters"""
        try:
            # Clear existing conversation starters first
            await self.clear_conversation_starters()
            
            for i, starter in enumerate(starters[:4]):  # Max 4 starters
                try:
                    # Look for conversation starter input or add button
                    starter_selectors = [
                        'input[placeholder*="conversation"]',
                        'textarea[placeholder*="conversation"]',
                        'button:has-text("Add")',
                        'button[aria-label*="Add conversation starter"]'
                    ]
                    
                    starter_input = None
                    for selector in starter_selectors:
                        try:
                            starter_input = await self.page.wait_for_selector(selector, timeout=3000)
                            break
                        except:
                            continue
                    
                    if starter_input:
                        # If it's a button, click it first to create input
                        tag_name = await starter_input.evaluate('el => el.tagName.toLowerCase()')
                        if tag_name == 'button':
                            await starter_input.click()
                            await asyncio.sleep(1)
                            # Now look for the input that appeared
                            starter_input = await self.page.wait_for_selector('input[placeholder*="conversation"], textarea[placeholder*="conversation"]', timeout=5000)
                        
                        await starter_input.fill(starter)
                        await self.page.keyboard.press('Enter')
                        await asyncio.sleep(1)
                        logger.info(f"Added conversation starter {i+1}: {starter[:50]}...")
                    else:
                        logger.warning(f"Could not find input for conversation starter {i+1}")
                        
                except Exception as e:
                    logger.warning(f"Could not add conversation starter {i+1}: {e}")
        except Exception as e:
            logger.warning(f"Failed to add conversation starters with fallback: {e}")

    async def clear_conversation_starters(self):
        """Clear existing conversation starters"""
        try:
            # Look for existing conversation starter inputs and clear them
            starter_inputs = await self.page.query_selector_all('input[placeholder*="conversation"], textarea[placeholder*="conversation"]')
            
            for input_elem in starter_inputs:
                try:
                    await input_elem.click()
                    await self.page.keyboard.press('Control+a')
                    await self.page.keyboard.press('Delete')
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.debug(f"Error clearing conversation starter: {e}")
                    
            # Also look for delete buttons for conversation starters
            delete_buttons = await self.page.query_selector_all('button[aria-label*="delete"], button[title*="delete"], button:has-text("×")')
            
            for button in delete_buttons:
                try:
                    await button.click()
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.debug(f"Error clicking delete button: {e}")
                    
        except Exception as e:
            logger.debug(f"Error clearing conversation starters: {e}")

    async def configure_actions(self, openapi_spec: Dict[str, Any]):
        """Configure GPT actions with OpenAPI spec using the better section-based approach"""
        try:
            await self.ensure_browser_alive()
            
            logger.info("Configuring GPT actions...")
            
            # Look for the Actions section with parent div mb-6
            try:
                # Find the div with class mb-6 that contains "Actions"
                actions_section = await self.page.wait_for_selector('div.mb-6:has-text("Actions")', timeout=5000)
                if actions_section:
                    logger.info(f"Found Actions section: {actions_section}")
                    
                    # Look for existing populated actions within this section
                    # Look for buttons other than "Create new action" - those are existing actions
                    all_buttons = await actions_section.query_selector_all('button')
                    existing_actions = []
                    
                    logger.info(f"Found {len(all_buttons)} total buttons in actions section")
                    
                    for i, button in enumerate(all_buttons):
                        try:
                            button_text = await button.text_content()
                            button_classes = await button.get_attribute('class')
                            logger.info(f"Button {i+1}: text='{button_text}', classes='{button_classes}'")
                            
                            # Check if this is NOT the "Create new action" button
                            if not button_text or "create new action" not in button_text.lower():
                                existing_actions.append(button)
                                logger.info(f"Added button {i+1} as existing action")
                            else:
                                logger.info(f"Skipped button {i+1} - it's the create button")
                                
                        except Exception as e:
                            logger.debug(f"Error checking button {i+1}: {e}")
                            # If we can't get text, assume it's an action button (like icon buttons)
                            existing_actions.append(button)
                            logger.info(f"Added button {i+1} as existing action (no text)")
                    
                    logger.info(f"Total existing action buttons found: {len(existing_actions)}")
                    
                    if existing_actions and len(existing_actions) > 0:
                        logger.info(f"Found {len(existing_actions)} existing action(s)")
                        
                        await existing_actions[0].click()
                        await asyncio.sleep(2)
                        logger.info("Clicked on existing action")
                    else:
                        logger.info("No existing actions found, creating new action")
                        
                        # Look for "Create new action" button within the actions section
                        try:
                            create_action_btn = await actions_section.wait_for_selector('button:has-text("Create new action")', timeout=5000)
                            await create_action_btn.click()
                            await asyncio.sleep(2)
                            logger.info("Clicked Create new action button")
                        except Exception as e:
                            logger.warning(f"Could not find 'Create new action' button in actions section: {e}")
                else:
                    logger.warning("Could not find Actions section")
                    # Fallback to old method
                    await self.configure_actions_fallback(openapi_spec)
                    return
                    
            except Exception as e:
                logger.warning(f"Failed to find Actions section: {e}")
                # Fallback to old method
                await self.configure_actions_fallback(openapi_spec)
                return
                
            # Fill in OpenAPI schema using the specific selector
            try:
                # First try to find the schema textarea by looking for the specific placeholder
                schema_textarea = await self.page.wait_for_selector('textarea[placeholder*="Enter your OpenAPI schema here"]', timeout=5000)
                if schema_textarea:
                    await schema_textarea.click()
                    await self.page.keyboard.press('Control+a')  # Select all existing content
                    await schema_textarea.fill(json.dumps(openapi_spec, indent=2))
                    logger.info("OpenAPI schema configured successfully using specific selector")
                else:
                    raise Exception("Schema textarea not found with specific selector")
                    
            except Exception as e:
                logger.warning(f"Failed to find schema textarea with specific selector: {e}")
                # Fallback to generic selectors
                schema_selectors = [
                    'textarea[placeholder*="schema"]',
                    'textarea[placeholder*="OpenAPI"]',
                    'textarea[placeholder*="Schema"]',
                    'div[contenteditable="true"]'
                ]
                
                for selector in schema_selectors:
                    try:
                        schema_input = await self.page.wait_for_selector(selector, timeout=3000)
                        await schema_input.click()
                        await self.page.keyboard.press('Control+a')  # Select all existing content
                        await schema_input.fill(json.dumps(openapi_spec, indent=2))
                        logger.info("Added/Updated OpenAPI schema with fallback")
                        break
                    except:
                        continue
            
            # Look for and click any "Create" or "Save" button for the action
            action_save_selectors = [
                'button:has-text("Create")',
                'button:has-text("Save")',
                'button:has-text("Update")'
            ]
            
            for selector in action_save_selectors:
                try:
                    save_btn = await self.page.wait_for_selector(selector, timeout=3000)
                    await save_btn.click()
                    await asyncio.sleep(1)
                    logger.info(f"Clicked action save button: {selector}")
                    break
                except:
                    continue
            
        except BrowserCrashedException:
            # Re-raise browser crashes to trigger restart
            raise
        except Exception as e:
            logger.warning(f"Failed to configure actions: {e}")

    async def configure_actions_fallback(self, openapi_spec: Dict[str, Any]):
        """Fallback method for configuring actions"""
        try:
            logger.info("Using fallback method for configuring actions...")
            
            # First check if there are existing actions to update
            existing_actions = await self.page.query_selector_all('button:has-text("Edit"), a[href*="action"]')
            
            if existing_actions:
                logger.info("Found existing actions - updating first action")
                try:
                    await existing_actions[0].click()
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.warning(f"Could not click existing action: {e}")
            else:
                # Look for Actions section or button to create new action
                actions_selectors = [
                    'button:has-text("Create new action")',
                    'button:has-text("Add action")',
                    'button:has-text("Actions")',
                    '[data-testid="action-button"]'
                ]
                
                for selector in actions_selectors:
                    try:
                        actions_btn = await self.page.wait_for_selector(selector, timeout=5000)
                        await actions_btn.click()
                        await asyncio.sleep(2)
                        logger.info("Clicked actions button")
                        break
                    except:
                        continue
            
            # Fill in OpenAPI schema
            schema_selectors = [
                'textarea[placeholder*="schema"]',
                'textarea[placeholder*="OpenAPI"]',
                'textarea[placeholder*="Schema"]',
                'div[contenteditable="true"]'
            ]
            
            for selector in schema_selectors:
                try:
                    schema_input = await self.page.wait_for_selector(selector, timeout=5000)
                    await schema_input.click()
                    await self.page.keyboard.press('Control+a')  # Select all existing content
                    await schema_input.fill(json.dumps(openapi_spec, indent=2))
                    logger.info("Added/Updated OpenAPI schema")
                    break
                except:
                    continue
            
        except Exception as e:
            logger.warning(f"Failed to configure actions with fallback: {e}")
            
    async def save_gpt(self):
        """Save the GPT configuration and handle the sharing dialog"""
        try:
            await self.ensure_browser_alive()
            
            # Look for save/create/update button
            save_selectors = [
                'button:has(div:has-text("Create"))',
                'button:has(div:has-text("Update"))',
                'button:has(span:has-text("Create"))',
                'button:has(span:has-text("Update"))',
                'button div:has-text("Create")',
                'button div:has-text("Update")'
            ]
            
            for selector in save_selectors:
                try:
                    save_btn = await self.page.wait_for_selector(selector, timeout=10000)
                    await save_btn.click()
                    await asyncio.sleep(2)
                    logger.info(f"Clicked save button: {selector}")
                    break
                except Exception as e:
                    logger.debug(f"Could not find button with selector '{selector}': {e}")
                    continue
            else:
                logger.warning("Could not find save button with any selector")
                return None
            
            # Wait for either "Share GPT" dialog (new GPT) or "GPT Updated" dialog (existing GPT)
            try:
                # Check which dialog appears
                dialog_appeared = await self.page.wait_for_selector('div:has-text("Share GPT"), div:has-text("GPT Updated")', timeout=10000)
                dialog_text = await dialog_appeared.text_content()
                
                if "Share GPT" in dialog_text:
                    logger.info("Share GPT dialog appeared (new GPT)")
                    return await self.handle_share_gpt_dialog()
                elif "GPT Updated" in dialog_text:
                    logger.info("GPT Updated dialog appeared (existing GPT)")
                    return await self.handle_final_dialog()
                else:
                    logger.warning("Unknown dialog appeared")
                    return None
                    
            except Exception as e:
                logger.warning(f"No dialog appeared: {e}")
                return None
            
        except BrowserCrashedException:
            # Re-raise browser crashes to trigger restart
            raise
        except Exception as e:
            logger.error(f"Failed to save GPT: {e}")
            return None
    
    async def handle_share_gpt_dialog(self):
        """Handle the Share GPT dialog for new GPTs"""
        try:
            # Click "Only me" option
            try:
                only_me_button = await self.page.wait_for_selector('button:has-text("Only me")', timeout=5000)
                await only_me_button.click()
                await asyncio.sleep(1)
                logger.info("Selected 'Only me' privacy option")
            except Exception as e:
                logger.warning(f"Could not find 'Only me' button: {e}")
            
            # Click Save button in the dialog
            try:
                dialog_save_btn = await self.page.wait_for_selector('button:has-text("Save")', timeout=5000)
                await dialog_save_btn.click()
                await asyncio.sleep(3)
                logger.info("Clicked Save button in dialog")
            except Exception as e:
                logger.warning(f"Could not find Save button in dialog: {e}")
                return None
            
            # Wait for "Settings Saved" dialog and handle copy/view
            return await self.handle_final_dialog()
            
        except BrowserCrashedException:
            # Re-raise browser crashes to trigger restart
            raise
        except Exception as e:
            logger.error(f"Failed to handle Share GPT dialog: {e}")
            return None
    
    async def handle_final_dialog(self):
        """Handle the final dialog with copy link and view GPT buttons"""
        try:
            # Wait a bit for the dialog to fully load
            await asyncio.sleep(2)
            
            # Click "View GPT" button
            try:
                view_gpt_btn = await self.page.wait_for_selector(':has-text("View GPT")', timeout=5000)
                await view_gpt_btn.click()
                await asyncio.sleep(2)
                logger.info("Clicked View GPT element")
            except Exception as e:
                logger.warning(f"Could not find View GPT element: {e}")
            return None
                
        except BrowserCrashedException:
            # Re-raise browser crashes to trigger restart
            raise
        except Exception as e:
            logger.error(f"Failed to handle final dialog: {e}")
            return None

async def setup_gpt(config_file: str) -> Optional[str]:
    """Main function to setup or update GPT"""
    max_retries = 3
    
    for attempt in range(max_retries):
        gpt_manager = GPTManager()  # Create fresh instance each attempt
        
        try:
            logger.info(f"GPT setup attempt {attempt + 1}/{max_retries}")
            
            # Load configuration
            config = gpt_manager.load_config_from_json(config_file)
            
            # Initialize browser
            await gpt_manager.initialize_browser()
            
            # Login to OpenAI
            if not await gpt_manager.login_to_openai():
                logger.error("Failed to login to OpenAI")
                if attempt < max_retries - 1:
                    logger.info("Retrying with fresh browser...")
                    continue
                return None
                
            # Check for existing GPT
            existing_gpt = await gpt_manager.check_existing_gpt(config['name'])
            
            # Use create_new_gpt for both creating and updating
            await gpt_manager.create_new_gpt(config, existing_gpt)
            
            logger.info("GPT setup completed successfully!")
            return "SUCCESS"
            
        except BrowserCrashedException as e:
            logger.error(f"Browser crashed during attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                logger.info("Restarting entire process with fresh browser...")
                await asyncio.sleep(3)  # Wait before retry
            else:
                logger.error("Max retries reached due to browser crashes")
                
        except Exception as e:
            logger.error(f"Error in GPT setup attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                logger.info("Retrying with fresh browser...")
                await asyncio.sleep(3)  # Wait before retry
            else:
                logger.error("Max retries reached, giving up")
                
        finally:
            # Always cleanup the current attempt's browser
            try:
                await gpt_manager.close_browser()
                await asyncio.sleep(2)  # Give extra time for Windows cleanup
            except Exception as cleanup_error:
                logger.debug(f"Cleanup error (non-critical): {cleanup_error}")
                
    # Final cleanup - ensure all pending tasks are completed
    await final_cleanup()
    return None

async def final_cleanup():
    """Final cleanup to ensure all asyncio resources are properly closed"""
    try:
        # Wait for any remaining tasks to complete
        pending_tasks = [task for task in asyncio.all_tasks() if not task.done()]
        if pending_tasks:
            logger.debug(f"Waiting for {len(pending_tasks)} pending tasks to complete...")
            await asyncio.sleep(2)
            
        # Give extra time for Windows to clean up pipes and transports
        await asyncio.sleep(1)
        
    except Exception as e:
        logger.debug(f"Final cleanup error (non-critical): {e}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python gpt_creator_standalone.py <config_file>")
        return
    
    config_file = sys.argv[1]
    
    print(f"🚀 Creating GPT from config: {config_file}")
    
    result = asyncio.run(setup_gpt(config_file))
    
    if result:
        print("✅ GPT created successfully!")
    else:
        print("❌ GPT creation failed!")

if __name__ == "__main__":
    import sys
    main() 