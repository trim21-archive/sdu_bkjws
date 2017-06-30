import unittest
import json
import os.path
import sys
import sdu_bkjws

testDir = os.path.split(os.path.realpath(__file__))[0]


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        with open(testDir + '/keys.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
        self.sdu = sdu_bkjws.SduBkjws(obj['student_id'], obj['password'])

    def test_login(self):
        self.sdu.login()

    def test_detail(self):
        self.sdu.get_detail()
        self.assertIsInstance(self.sdu.detail, dict)

    def test_update_contact_info(self):
        self.sdu.update_contact_info()

    def test_lesson(self):
        lesson = self.sdu.lessons
        self.assertIsInstance(self.sdu.lessons, list)
        for key in ["lesson_num_long", "lesson_name", "lesson_num_short",
                    "credit", "school", "teacher", "weeks",
                    "days", "times", "place"]:
            for obj in lesson:
                self.assertIn(key, obj.keys())

    def test_past_score(self):
        raw = self.sdu.get_raw_past_score()
        past_score = self.sdu.get_past_score()
        for key in ['kch', 'kcm', 'kxh', 'xh', 'kssj', 'jsh', 'xnxq', 'xf', 'xs', 'kcsx', 'kscj']:
            for obj in past_score:
                self.assertIn(key, obj.keys())
        self.assertIsInstance(raw, dict)
        self.assertIsInstance(past_score, list)
        self.assertEqual(raw['object']['aaData'], past_score)

    def test_now_score(self):
        self.sdu.get_raw_now_score()
        self.sdu.get_now_score()

    def tearDown(self):
        self.sdu.session.close()


if __name__ == '__main__':
    unittest.main()
