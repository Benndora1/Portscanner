from threading import Thread
from time import time


class DictCleaner(Thread):
    # Define a class that extends the Thread class

    def __init__(self, first_contacts, lock, max_age_seconds=300):
        # Define the constructor for the class
        super().__init__()
        # Call the constructor of the superclass

        self.first_contacts = first_contacts
        # Store the first_contacts dictionary

        self.lock = lock
        # Store the lock object

        self.max_age_seconds = max_age_seconds
        # Store the maximum age of an entry

        self.is_running = True
        # Initialize the is_running attribute to True

    def run(self):
        # Define the run method that will be executed when the thread starts

        while self.is_running:
            # While the thread is running...

            current_time = time()
            # Get the current time

            keys_to_remove = []
            # Create an empty list to store the keys to remove

            with self.lock:
                # Use the lock to synchronize access to the dictionary

                for key in self.first_contacts.keys():
                    # Iterate over the keys in the dictionary

                    if current_time - self.first_contacts[key] > self.max_age_seconds:
                        # If the age of the entry is greater than the maximum age...

                        keys_to_remove.append(key)
                        # Add the key to the list of keys to remove

                for key in keys_to_remove:
                    # Iterate over the list of keys to remove

                    del self.first_contacts[key]
                    # Remove the key from the dictionary

   