#!/usr/bin/env python
# coding: utf-8

import os
import copy
import unittest
import tempfile

from amulog import config
from amulog import log_db
from amulog import lt_common

from . import testlog


class TestLTGen(unittest.TestCase):

    _path_testlog = None

    @classmethod
    def setUpClass(cls):
        fd_testlog, cls._path_testlog = tempfile.mkstemp()
        os.close(fd_testlog)
        tlg = testlog.TestLogGenerator(testlog.DEFAULT_CONFIG, seed=3)
        tlg.dump_log(cls._path_testlog)

        cls._conf = config.open_config()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls._path_testlog)

    def _try_method(self, conf, online=True):
        table = lt_common.TemplateTable()
        ltgen = lt_common.init_ltgen_methods(conf, table)

        iterobj = log_db.iter_plines(conf, [self._path_testlog])
        if online:
            for pline in iterobj:
                ltgen.process_line(pline)
        else:
            plines = [pline for pline in iterobj]
            ltgen.process_offline(plines)
        return table

    def test_import(self):
        conf = copy.deepcopy(self._conf)
        conf['log_template']['lt_methods'] = "import"
        tpl_path = "/".join((os.path.dirname(os.path.abspath(__file__)),
                             "./testlog_tpl.txt"))
        conf['log_template_import']['def_path'] = tpl_path
        table = self._try_method(conf)

        n_tpl = len(table)
        self.assertTrue(n_tpl == 6)

    def test_drain(self):
        conf = copy.deepcopy(self._conf)
        conf['log_template']['lt_methods'] = "drain"
        table = self._try_method(conf)

        n_tpl = len(table)
        self.assertTrue(3 < n_tpl < 20)

    def test_lenma(self):
        conf = copy.deepcopy(self._conf)
        conf['log_template']['lt_methods'] = "lenma"
        table = self._try_method(conf)

        n_tpl = len(table)
        self.assertTrue(3 < n_tpl < 20)

    def test_dlog(self):
        conf = copy.deepcopy(self._conf)
        conf['log_template']['lt_methods'] = "dlog"
        table = self._try_method(conf, online=False)

        n_tpl = len(table)
        self.assertTrue(3 < n_tpl < 300)

    def test_fttree(self):
        conf = copy.deepcopy(self._conf)
        conf['log_template']['lt_methods'] = "fttree"
        table = self._try_method(conf)

        n_tpl = len(table)
        self.assertTrue(3 < n_tpl < 50)

    def test_va(self):
        conf = copy.deepcopy(self._conf)
        conf['log_template']['lt_methods'] = "va"
        table = self._try_method(conf)

        n_tpl = len(table)
        self.assertTrue(3 < n_tpl < 20)

    def test_shiso_first(self):
        conf = copy.deepcopy(self._conf)
        conf['log_template']['lt_methods'] = "shiso"
        table = self._try_method(conf)

        n_tpl = len(table)
        self.assertTrue(3 < n_tpl < 20)


if __name__ == "__main__":
    unittest.main()


