from pathlib import Path

from datalab_sdk import DatalabClient

client = DatalabClient(api_key="sdV8TzgMy6ezUhfTagOhXE5-eSoUAXPBSGqXXMRVvyk")

_PDF_NAME = "pima_indians_diabetes_lab03.pdf"
_script_dir = Path(__file__).resolve().parent
_path_script = _script_dir / _PDF_NAME
_path_cwd = Path.cwd() / _PDF_NAME
_pdf_for_convert = str(_path_script if _path_script.is_file() else _path_cwd)

result = client.convert(_pdf_for_convert)
print(result.markdown)

_out_dir = _script_dir / "nhom01"
_out_dir.mkdir(parents=True, exist_ok=True)
result.save_output(str(_out_dir / "parsing"))
