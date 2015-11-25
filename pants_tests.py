import unittest
from pants import PantsState, PantsPath

class PantsStateTest(unittest.TestCase):

    def test_valid_move_left(self):
        actual_state = PantsState(pointer=2, state=[1, 2, 3]).move_pointer_left()
        expected_state = PantsState(pointer=0, state=[1, 2, 3])

        self.assertEqual(expected_state, actual_state)

    def test_invalid_move_left_when_one_away(self):
        actual_state = PantsState(pointer=1, state=[1, 2, 3]).move_pointer_left()

        self.assertIsNone(actual_state)

    def test_invalid_move_left_when_on_edge(self):
        actual_state = PantsState(pointer=0, state=[1, 2, 3, 4, 5]).move_pointer_left()

        self.assertIsNone(actual_state)

    def test_valid_move_right(self):
        actual_state = PantsState(pointer=1, state=[1, 2, 3, 4]).move_pointer_right()
        expected_state = PantsState(pointer=3, state=[1, 2, 3, 4])

        self.assertEqual(expected_state, actual_state)

    def test_invalid_move_right_when_one_away(self):
        actual_state = PantsState(pointer=2, state=[1, 2, 3, 4]).move_pointer_right()

        self.assertIsNone(actual_state)

    def test_invalid_move_right_when_on_edge(self):
        actual_state = PantsState(pointer=3, state=[1, 2, 3, 4]).move_pointer_right()

        self.assertIsNone(actual_state)

    def test_valid_swap_left(self):
        actual_state = PantsState(pointer=1, state=[1, 2, 3, 4]).swap_left()
        expected_state = PantsState(pointer=0, state=[2, 1, 3, 4])

        self.assertEqual(expected_state, actual_state)

    def test_invalid_swap_left(self):
        actual_state = PantsState(pointer=0, state=[1, 2, 3, 4]).swap_left()

        self.assertIsNone(actual_state)

    def test_valid_swap_right(self):
        actual_state = PantsState(pointer=1, state=[1, 2, 3, 4]).swap_right()
        expected_state = PantsState(pointer=2, state=[1, 3, 2, 4])

        self.assertEqual(expected_state, actual_state)

    def test_invalid_swap_right(self):
        actual_state = PantsState(pointer=3, state=[1, 2, 3, 4]).swap_right()

        self.assertIsNone(actual_state)

    def test_initial_string_representation(self):
        expected_string = '[*1 2 3 4 5]'
        actual_string = str(PantsState(0, [1, 2, 3, 4, 5]))

        self.assertEqual(expected_string, actual_string)

    def test_intermediate_string_representation(self):
        expected_string = '[3 5 *2 1 4]'
        actual_string = str(PantsState(2, [3, 5, 2, 1, 4]))

        self.assertEqual(expected_string, actual_string)


class PantsPathTest(unittest.TestCase):

    def test_all_children_generated(self):
        initial_state = PantsState(2, [1, 2, 3, 4, 5])
        initial_path = PantsPath([initial_state])

        actual_child_paths = list(initial_path.children)

        expected_paths = [
            PantsPath([initial_state, PantsState(0, [1, 2, 3, 4, 5])]),
            PantsPath([initial_state, PantsState(4, [1, 2, 3, 4, 5])]),
            PantsPath([initial_state, PantsState(1, [1, 3, 2, 4, 5])]),
            PantsPath([initial_state, PantsState(3, [1, 2, 4, 3, 5])])
        ]

        self.assertEqual(expected_paths, actual_child_paths)

    def test_only_right_children_generated(self):
        initial_state = PantsState(0, [1, 2, 3, 4, 5])
        initial_path = PantsPath([initial_state])

        actual_child_paths = list(initial_path.children)

        expected_paths = [
            PantsPath([initial_state, PantsState(2, [1, 2, 3, 4, 5])]),
            PantsPath([initial_state, PantsState(1, [2, 1, 3, 4, 5])])
        ]

        self.assertEqual(expected_paths, actual_child_paths)

    def test_only_left_children_generated(self):
        initial_state = PantsState(4, [1, 2, 3, 4, 5])
        initial_path = PantsPath([initial_state])

        actual_child_paths = list(initial_path.children)

        expected_paths = [
            PantsPath([initial_state, PantsState(2, [1, 2, 3, 4, 5])]),
            PantsPath([initial_state, PantsState(3, [1, 2, 3, 5, 4])])
        ]

        self.assertEqual(expected_paths, actual_child_paths)

    def test_skip_children_if_already_in_path(self):
        initial_states = [
            PantsState(0, [1, 2, 3, 4, 5]),
            PantsState(1, [2, 1, 3, 4, 5]),
        ]
        initial_path = PantsPath(initial_states)

        actual_child_paths = list(initial_path.children)

        expected_paths = [
            PantsPath(initial_states + [PantsState(3, [2, 1, 3, 4, 5])]),
            PantsPath(initial_states + [PantsState(2, [2, 3, 1, 4, 5])])
        ]

        self.assertEqual(expected_paths, actual_child_paths)


if __name__ == '__main__':
    unittest.main()
