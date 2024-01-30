from entities.characters import Character
from gui.message_box import MessageBox


class Animal(Character):
    def __init__(self, animal) -> None:
        data = self.get_animal_data(animal)
        super().__init__(data)
        self.animal = animal

    def get_animal_data(self, animal):
        return {
            "race" : "bunny",
            "sprite" : "base",
            "location" : {
                "position" : {
                    "x" : 128,
                    "y" : 32 * 10
                }
            },
            "inventory" : {
                "equipped" : {},
                "bag" : []
            }
        }
    
    def interact(self, game_state):
        box = MessageBox(
            [
                f"Oh look a {self.animal}!",
                f"Here's its save dict: {vars(self)}"
            ]
        )
        game_state.manager.change_state("message_box", [box])
        box2 = MessageBox(
            [
                "I wonder if I can use it's hair as a core..."
            ]
        )
        game_state.manager.change_state("message_box", [box2])