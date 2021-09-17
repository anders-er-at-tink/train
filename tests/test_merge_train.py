from unittest import TestCase

from train.commit import Commit, rebase


class TestRebase(TestCase):
    def test_rebase(self):
        root = Commit(message="root", parents=())
        master = root.commit("ma").commit("mb").commit("mc")
        b1 = master.commit("1a").commit("1b").commit("1c")
        b2 = master.commit("2a").commit("2b")
        new = b2.rebase(b1)
        expected = list(reversed("root ma mb mc 1a 1b 1c 2a 2b".split()))
        actual = []
        it = new
        while True:
            actual.append(it.message)
            if len(it.parents) == 1:
                it = it.parents[0]
            elif len(it.parents) == 0:
                break
            else:
                self.assertFalse("Merges not expected here")

        self.assertEqual(expected, actual)
        self.assertEqual(new._n, 9)

