"""
WhatsApp handler for the WhatsApp Image Sender application.
"""
import streamlit as st
from typing import List, Dict, Any
import urllib.parse

class WhatsAppHandler:
    """Handler for WhatsApp operations."""
    
    @staticmethod
    def generate_whatsapp_link(phone: str, message: str = "") -> str:
        """
        Generate a WhatsApp share link.
        
        Args:
            phone: Phone number to send to
            message: Optional message to include
            
        Returns:
            WhatsApp share URL
        """
        # Remove any non-digit characters from phone
        phone = ''.join(filter(str.isdigit, phone))
        
        # Encode message
        encoded_message = urllib.parse.quote(message)
        
        # Generate WhatsApp link
        return f"https://wa.me/{phone}?text={encoded_message}"

    @staticmethod
    def prepare_image_message(image_name: str, drive_link: str) -> str:
        """
        Prepare a message for sending an image via WhatsApp.
        
        Args:
            image_name: Name of the image
            drive_link: Google Drive sharing link for the image
            
        Returns:
            Formatted message with image details
        """
        return f"Image: {image_name}\nDownload link: {drive_link}"

    @staticmethod
    def send_to_whatsapp(contacts: List[Dict[str, str]], image_name: str, drive_link: str) -> List[str]:
        """
        Generate WhatsApp links for sending images to contacts.
        
        Args:
            contacts: List of contact dictionaries
            image_name: Name of the image to send
            drive_link: Google Drive sharing link for the image
            
        Returns:
            List of WhatsApp links for each contact
        """
        try:
            # Generate message with image details
            message = WhatsAppHandler.prepare_image_message(image_name, drive_link)
            
            # Generate WhatsApp links for each contact
            whatsapp_links = []
            for contact in contacts:
                whatsapp_link = WhatsAppHandler.generate_whatsapp_link(
                    contact["phone"],
                    message
                )
                whatsapp_links.append({
                    "name": contact["name"],
                    "link": whatsapp_link
                })
            
            return whatsapp_links
            
        except Exception as e:
            st.error(f"Error generating WhatsApp links: {str(e)}")
            return []

    @staticmethod
    def send_bulk_messages(contacts: List[Dict[str, str]], message: str) -> List[str]:
        """
        Generate WhatsApp links for sending bulk messages.
        
        Args:
            contacts: List of contact dictionaries
            message: Message to send
            
        Returns:
            List of WhatsApp links for each contact
        """
        try:
            whatsapp_links = []
            for contact in contacts:
                whatsapp_link = WhatsAppHandler.generate_whatsapp_link(
                    contact["phone"],
                    message
                )
                whatsapp_links.append({
                    "name": contact["name"],
                    "link": whatsapp_link
                })
            return whatsapp_links
        except Exception as e:
            st.error(f"Error generating bulk message links: {str(e)}")
            return [] 