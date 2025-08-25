from app.utils import create_excel_from_models

MODEL_PATH = "app.models.excel_models.dhcp_info_model"
DEST_FILE = "app/src/barebone/dhcp_info_models.xlsx"


def run():
    create_excel_from_models(MODEL_PATH, DEST_FILE)
