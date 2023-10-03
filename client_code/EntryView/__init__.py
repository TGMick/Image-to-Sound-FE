from ._anvil_designer import EntryViewTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..EntryEdit import EntryEdit
from PIL import Image
from gtts import gTTS
from pytesseract import image_to_string

class EntryView(EntryViewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def edit_entry_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Create a copy of the existing entry from the Data Table 
    entry_copy = dict(self.item)
    # Open an alert displaying the 'EntryEdit' Form
    # set the `self.item` property of the EntryEdit Form to a copy of the entry to be updated
    save_clicked = alert(
      content=EntryEdit(item=entry_copy),
      title="Update Entry",
      large=True,
      buttons=[("Save", True), ("Cancel", False)]
    )
    # Update the entry if the user clicks save
    if save_clicked:
      anvil.server.call('update_entry', self.item, entry_copy)
  
      # Now refresh the page
      self.refresh_data_bindings()

  def delete_entry_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Get the user to confirm if they wish to delete the entry
    # If yes, raise the 'x-delete-entry' event on the parent 
    # (which is the entries_panel on Homepage)
    if confirm(f"Are you sure you want to delete {self.item['title']}?"):
      self.parent.raise_event('x-delete-entry', entry=self.item)

  def image_to_sound(self, image_path):
    try:
      loaded_image = Image.open(image_path)
      decoded_text = image_to_string(loaded_image)
      cleaned_text = " ".join(decoded_text.split("\n"))
      print(cleaned_text)
      sound = gTTS(cleaned_text, lang="en")
      sound.save("test.mp3")
      return True
    except:
      alert("Error has occured")
      return

  if __name__== "__main__":
    image_to_sound("image.png")
    input()

  def image_1_mouse_enter(self, x, y, **event_args):
    """This method is called when the mouse cursor enters this component"""
    self.image_to_sound()



