from pathlib import Path
import re

from django.test import TestCase


class ArcadePlatformTests(TestCase):
    def test_homepage_shows_classic_game_platform(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "THE ARCADE")
        self.assertContains(response, "game-grid")
        self.assertContains(response, "genre-filter")
        self.assertContains(response, "year-filter")
        self.assertContains(response, "style-filter")
        self.assertContains(response, "arcade-games.js")
        self.assertNotContains(response, "rom-file")
        self.assertNotContains(response, "EmulatorJS")

    def test_catalog_has_ten_original_games_and_no_external_emulator(self):
        script = Path(__file__).parent / "static" / "main" / "js" / "arcade-platform.js"
        source = script.read_text(encoding="utf-8")

        self.assertEqual(len(re.findall(r'\{ id: "[a-z-]+", title:', source)), 10)
        self.assertNotIn("emulatorjs.org", source.lower())
        self.assertIn('window.ArcadeGames.start(game.id', source)

    def test_previous_minigame_routes_are_removed(self):
        for path in ("/arcade", "/kitty", "/sumo", "/last-stand"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)
