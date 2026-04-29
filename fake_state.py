"""Modèle de game_state par défaut utilisé pour tester le bon fonctionnement des différents modèles.

Fait par Lucas"""

fake_state = {
    "discard": "Green-1",
    "direction": 1,
    "current_player": "Lucas",
    "players": [
        {
            "name": "Robert",
            "cards": [
                "Red-3", "Blue-5", "Yellow-2", "Green-7",
                "Wild", "Red-Skip", "Blue-1", "Yellow-9"
            ]
        },
        {
            "name": "Joris",
            "cards": [
                "Green-4", "Red-Draw2"
            ]
        },
        {
            "name": "Jean-Louis",
            "cards": [
                "Blue-0", "Blue-2", "Blue-7", "Green-5", "Green-9",
                "Yellow-1", "Yellow-4", "Yellow-6", "Yellow-Reverse",
                "Red-1", "Red-5", "Red-8", "Wild+4", "Green-Skip", "Blue-Reverse"
            ]
        },
        {
            "name": "Chien",
            "cards": [
                "Green-2", "Green-3", "Blue-9",
                "Yellow-7", "Red-6", "Wild", "Blue-Skip"
            ]
        },
        {
            "name": "Kevin",
            "cards": [
                "Red-0", "Red-2", "Red-4", "Blue-3", "Blue-8",
                "Green-6", "Yellow-5", "Yellow-8", "Wild+4", "Green-Reverse"
            ]
        },
        {
            "name": "Alexis",
            "cards": []
        },
        {
            "name": "Lucas",
            "cards": [
                "Green-1",
                "Green-1",
                "Green-1",
                "Green-1"
            ]
        },
        {
            "name": "JSP",
            "cards": [
                "Red-9"
            ]
        },
    ],
    "draw_stack": 0,
    "winner": None
}
