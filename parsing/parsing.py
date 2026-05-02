from pathlib import Path

from datalab_sdk import DatalabClient

client = DatalabClient(api_key="sdV8TzgMy6ezUhfTagOhXE5-eSoUAXPBSGqXXMRVvyk")

_PDF_NAME = "Suresh-Kumar-Mukhiya-Usman-Ahmed-Hands-On-Exploratory-Data-Analysis-With-Python-Perform-EDA-Techniques-to-Understand-Summarize-And-Investigate.pdf"
_script_dir = Path(__file__).resolve().parent
_path_script = _script_dir / _PDF_NAME
_path_cwd = Path.cwd() / _PDF_NAME
_pdf_for_convert = str(_path_script if _path_script.is_file() else _path_cwd)

result = client.convert(_pdf_for_convert)
print(result.markdown)

_out_md = _script_dir / "parsing.md"
result.save_output(str(_out_md))
