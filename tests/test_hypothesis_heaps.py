from __future__ import print_function
import os
import subprocess
import glob
from unittest import TestCase


class TestHypothesisHeap(TestCase):
    def setUp(self):
        os.chdir("examples/hypothesis_heaps")

    def tearDown(self):
        os.chdir("../..")

    def test_hypothesis_heap(self):
        dnull = open(os.devnull, 'w')

        r = subprocess.call(["tstl", "heaps.tstl"], stdout=dnull)
        self.assertEqual(r, 0)

        r = subprocess.call(
            ["tstl_rt", "--noCover", "--output", ".heaptest"], stdout=dnull)
        self.assertEqual(r, 255)

        r = subprocess.call(["tstl_replay", ".heaptest"], stdout=dnull)
        self.assertEqual(r, 255)

        r = subprocess.call(["tstl_reduce", ".heaptest",
                             ".heaptest.norm"], stdout=dnull)
        self.assertEqual(r, 0)

        r = subprocess.call(
            ["tstl_replay", ".heaptest.norm", "--verbose"], stdout=dnull)
        self.assertEqual(r, 255)

        r = subprocess.call(
            ["tstl_generalize", ".heaptest.norm"], stdout=dnull)
        self.assertEqual(r, 0)

        r = subprocess.call(
            ["tstl_standalone", ".heaptest.norm", ".heaptest.norm.py"], stdout=dnull)
        self.assertEqual(r, 0)

        r = subprocess.call(["python", ".heaptest.norm.py"],
                            stdout=dnull, stderr=dnull)
        self.assertEqual(r, 1)

        for f in glob.glob(".heaptest*"):
            os.remove(f)

        os.remove("coverage.out")