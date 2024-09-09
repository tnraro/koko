import unittest
import utils

class TestUtils(unittest.TestCase):
  def test_scoreIndicator(self):
    self.assertEqual(utils.scoreIndicator(-1.0), "🟥🟥🟥🟥🟥")
    self.assertEqual(utils.scoreIndicator(-0.9), "🟥🟥🟥🟥🟧")
    self.assertEqual(utils.scoreIndicator(-0.8), "🟥🟥🟥🟥")
    self.assertEqual(utils.scoreIndicator(-0.7), "🟥🟥🟥🟧")
    self.assertEqual(utils.scoreIndicator(-0.6), "🟥🟥🟥")
    self.assertEqual(utils.scoreIndicator(-0.5), "🟥🟥🟧")
    self.assertEqual(utils.scoreIndicator(-0.4), "🟥🟥")
    self.assertEqual(utils.scoreIndicator(-0.3), "🟥🟧")
    self.assertEqual(utils.scoreIndicator(-0.2), "🟥")
    self.assertEqual(utils.scoreIndicator(-0.1), "🟧")
    self.assertEqual(utils.scoreIndicator(0.0), "")
    self.assertEqual(utils.scoreIndicator(0.1), "🟨")
    self.assertEqual(utils.scoreIndicator(0.2), "🟩")
    self.assertEqual(utils.scoreIndicator(0.3), "🟩🟨")
    self.assertEqual(utils.scoreIndicator(0.4), "🟩🟩")
    self.assertEqual(utils.scoreIndicator(0.5), "🟩🟩🟨")
    self.assertEqual(utils.scoreIndicator(0.6), "🟩🟩🟩")
    self.assertEqual(utils.scoreIndicator(0.7), "🟩🟩🟩🟨")
    self.assertEqual(utils.scoreIndicator(0.8), "🟩🟩🟩🟩")
    self.assertEqual(utils.scoreIndicator(0.9), "🟩🟩🟩🟩🟨")
    self.assertEqual(utils.scoreIndicator(1.0), "🟩🟩🟩🟩🟩")

if __name__ == "__main__":
  unittest.main()