import os
import pathlib
import tempfile

import pydupe.dupetable as dupetable
import pytest
from pydupe.db import PydupeDB
from pydupe.hasher import Hasher

cwd = str(pathlib.Path.cwd())
tdata = cwd + "/pydupe/pydupe/"
home = str(pathlib.Path.home())

class Test_check:
    def test_check_file_on_disk_before_clear(self) -> None:
        with tempfile.TemporaryDirectory() as newpath:
            old_cwd = os.getcwd()
            os.chdir(newpath)
            cwd = pathlib.Path(newpath)
            dbname = pathlib.Path(newpath) / ".pydupe.sqlite"
            file_exists = cwd / "file_exists"
            file_is_dupe = cwd / "somedir" / "file_is_dupe"
            dupe2_in_dir = cwd / "somedir" / "somedir2" / "dupe2_in_dir"
            dupe_in_dir = cwd / "somedir" / "somedir2" / "dupe_in_dir"

            dupe2_in_dir.parent.mkdir(parents=True)
            dupe2_in_dir.write_text("some dummy text")
            file_exists.write_text("some dummy text")
            file_is_dupe.write_text("some dummy text")
            dupe_in_dir.write_text("some dummy text")

            hsh = Hasher(dbname)
            hsh.hashdir(cwd)
            with PydupeDB(dbname) as db:
                db.update_hash(str(file_is_dupe), None)
                db.commit()

            hsh = Hasher(dbname)
            file_is_dupe.unlink()
            hsh.clean() # here file_is_dupe should be deleted from db

            with PydupeDB(dbname) as db:
                flist = db.get_list_of_files_in_dir(str(cwd))

            assert set(flist) == {str(file_exists),str(dupe2_in_dir),str(dupe_in_dir)}

            os.chdir(old_cwd)