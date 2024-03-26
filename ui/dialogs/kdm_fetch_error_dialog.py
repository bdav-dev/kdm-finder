from models.misc_models import KdmFetchResponse
from ui.dialogs.error_dialog import ErrorDialog
from util.string_util import enum


class KdmFetchErrorDialog(ErrorDialog):

    def __init__(self, kdm_fetch_response: KdmFetchResponse):
        super().__init__(self._title(kdm_fetch_response), self._description(kdm_fetch_response))

    def _title(self, kdm_fetch_response: KdmFetchResponse):
        if kdm_fetch_response.is_erroneous():
            return "Fetch error"
        else:
            return "Fetch warning"

    def _description(self, kdm_fetch_response: KdmFetchResponse):
        message: str

        if kdm_fetch_response.is_erroneous():
            message = "An error occured during KDM fetch.\n\n"
        else:
            message = "Warnings occured during KDM fetch.\n\n"

        if kdm_fetch_response.is_erroneous():
            message = message + "Following error occured:\n" + kdm_fetch_response.error_message + "\n\n"

        if kdm_fetch_response.has_skipped_emails():
            message = message + "Some emails were skipped during fetch:\n" + enum(kdm_fetch_response.skipped_emails)

        return message
        

