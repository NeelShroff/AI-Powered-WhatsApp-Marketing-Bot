"""
Contact manager for the WhatsApp Image Sender application.
"""
import streamlit as st
from typing import List, Dict, Any

# Mock contact data
MOCK_CONTACTS = [
    {"name": "John Doe", "phone": "+1234567890"},
    {"name": "Jane Smith", "phone": "+1987654321"},
    {"name": "Alice Johnson", "phone": "+1122334455"},
    {"name": "Bob Wilson", "phone": "+1555666777"},
    {"name": "Carol Brown", "phone": "+1888999000"}
]

class ContactManager:
    """Manager for contact operations."""
    
    @staticmethod
    def get_contacts() -> List[Dict[str, str]]:
        """
        Get list of available contacts.
        
        Returns:
            List of contact dictionaries
        """
        return MOCK_CONTACTS

    @staticmethod
    def get_selected_contacts() -> List[Dict[str, str]]:
        """
        Get list of currently selected contacts.
        
        Returns:
            List of selected contact dictionaries
        """
        return st.session_state.get("selected_contacts", [])

    @staticmethod
    def set_selected_contacts(contacts: List[Dict[str, str]]) -> None:
        """
        Set the list of selected contacts.
        
        Args:
            contacts: List of contact dictionaries to select
        """
        st.session_state.selected_contacts = contacts

    @staticmethod
    def format_contact_display(contact: Dict[str, str]) -> str:
        """
        Format contact for display in selection widgets.
        
        Args:
            contact: Contact dictionary
            
        Returns:
            Formatted contact string
        """
        return f"{contact['name']} ({contact['phone']})"

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format.
        
        Args:
            phone: Phone number to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Simple validation: starts with + and has 10-15 digits
        return phone.startswith("+") and phone[1:].isdigit() and 10 <= len(phone[1:]) <= 15

    @staticmethod
    def add_contact(name: str, phone: str) -> bool:
        """
        Add a new contact.
        
        Args:
            name: Contact name
            phone: Contact phone number
            
        Returns:
            True if successful, False otherwise
        """
        if not name or not phone:
            return False
        
        if not ContactManager.validate_phone(phone):
            return False
        
        # Check if contact already exists
        if any(c["phone"] == phone for c in MOCK_CONTACTS):
            return False
        
        # Add new contact
        MOCK_CONTACTS.append({"name": name, "phone": phone})
        return True 