class Pet:
    """A very small Pet Management System built with OOP principles."""

    def __init__(self, name: str, pet_type: str, age: int):
        """Constructor – initialises a pet with the given data."""
        self.name = name
        self.pet_type = pet_type
        self.age = age

    def display_info(self):
        """Prints a nicely formatted summary of the pet’s details."""
        print(f"Name: {self.name}, Type: {self.pet_type}, Age: {self.age} year(s)")

    def update_age(self, new_age: int):
        """Updates the pet’s age to the new value."""
        self.age = new_age


# ── Demonstration / Test-drive ---------------------------------------------
if __name__ == "__main__":
    # 1. Instantiate at least two pets
    pet1 = Pet("Buddy", "Dog", 3)
    pet2 = Pet("Whiskers", "Cat", 2)

    # 2. Display initial details
    print("Initial details:")
    pet1.display_info()
    pet2.display_info()

    # 3. Update one pet’s age
    pet1.update_age(4)

    # 4. Display again to confirm the change
    print("\nAfter updating Buddy's age:")
    pet1.display_info()
    pet2.display_info()
