import utils
import unittest


class TestUtils(unittest.TestCase):
    def test_flattenDict(self):
        a = {
            "type": "realestate",
            "ad_id": 249540733,
            "main_search_key": "SEARCH_ID_REALESTATE_HOMES",
            "heading": "Fyllingsdalen | Lys og romslig topp- og endeleilighet med 3 soverom, samt nydelige sol- og utsiktsforhold.",
            "location": "Hesjaholtveien 22, Fyllingsdalen",
            "image": {
                "url": "https://images.finncdn.no/dynamic/default/2022/2/vertical-2/25/3/249/540/733_964844205.jpg",
                "path": "2022/2/vertical-2/25/3/249/540/733_964844205.jpg",
                "height": 1067,
                "width": 1600,
                "aspect_ratio": 1.499531396438613,
            },
            "test": {"best": {"lol": 123}},
        }
        self.assertDictEqual(
            utils.flattenDict(a),
            {
                "ad_id": 249540733,
                "heading": "Fyllingsdalen | Lys og romslig topp- og endeleilighet med 3 "
                "soverom, samt nydelige sol- og utsiktsforhold.",
                "image_aspect_ratio": 1.499531396438613,
                "image_height": 1067,
                "image_path": "2022/2/vertical-2/25/3/249/540/733_964844205.jpg",
                "image_url": "https://images.finncdn.no/dynamic/default/2022/2/vertical-2/25/3/249/540/733_964844205.jpg",
                "image_width": 1600,
                "location": "Hesjaholtveien 22, Fyllingsdalen",
                "main_search_key": "SEARCH_ID_REALESTATE_HOMES",
                "test_best_lol": 123,
                "type": "realestate",
            },
        )
