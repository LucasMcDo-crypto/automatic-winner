"""Modèle de game_state par défaut utilisé pour tester le bon fonctionnement des différents modèles.

Fait par Lucas"""

fake_state = {
    "discard": "v1",

    "direction": 1,

    "current_player": "Lucas",

    "etat_main": [
        "normal", "normal", "disabled", "normal"
    ],

    "players": [
        {
            "name": "Robert",
            "cards": [
                "r3", "b5", "j2", "v7", "r0", "b1", "j9"
            ]
        },

        {
            "name": "Joris",
            "cards": [
                "v4", "r2"
            ]
        },

        {
            "name": "Jean-Louis",
            "cards": [
                "b0", "b2", "b7", "v5", "v9",
                "j1", "j4", "j6"
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
                "r0", "r2", "r4"
            ]
        },

        {
            "name": "Alexis",
            "cards": [
                "j3"
            ]
        },

        {
            "name": "Lucas",
            "cards": [
                "j1", "v1", "v1", "v1"
            ]
        },

        {
            "name": "JSP",
            "cards": [
                "r9"
            ]
        }
    ],

    "draw_stack": 0,

    "winner": None
}
