import os
from pathlib import Path

import papermill as pm

test_dir = Path(__file__).absolute().parents[0]
code_dir = Path(__file__).absolute().parents[1]

out_dir = code_dir / 'out_notebooks'
out_dir.mkdir(exist_ok=True)

os.chdir(code_dir)


def test_verify_requirements_nb():
    planet_id = '20210903_150800_60_2458'
    pm.execute_notebook(code_dir / '0-Verify_Requirements.ipynb',
                        output_path=(out_dir / '__test_0-Verify_Requirements.ipynb'),
                        parameters={'PLANET_ID': planet_id}
                        )


def test_read_nb():
    pm.execute_notebook(code_dir / '1-Read_Verification.ipynb',
                        output_path=(out_dir / '__test_1-Read_Verification.ipynb'),
                        )
