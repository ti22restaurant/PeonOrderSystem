"""This module provides the
FooterContainer class

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from os.path import join
from reportlab.platypus import Paragraph

from peonordersystem.src.Settings import (RECEIPT_FOOTER_TEMPLATE_FILE_NAME,
                                          RECEIPT_FOOTER_CFG_FILE_NAME,
                                          RECEIPT_FOOTER_MSG_FILE_NAME)

from peonordersystem.SystemPath import SYSTEM_TEMPLATE_RECEIPT_FOOT_PATH
from peonordersystem.src.confirmationSystem.printers.formatters.PrinterSettings \
    import DEFAULT_FRONT_PRINTER_WIDTH

from .abc.ReceiptContainer import ReceiptContainer


class FooterContainer(ReceiptContainer):
    """Defines the FooterContainer that
    is used to generate, store and write
    a frame that contains the footer
    messages for a receipt.
    """
    CFG_MSG_KEY = "FOOTER_MSG"
    # Determined experimentally
    DEFAULT_FOOTER_HEIGHT = 185

    RML_FILE_PATH = join(SYSTEM_TEMPLATE_RECEIPT_FOOT_PATH,
                         RECEIPT_FOOTER_TEMPLATE_FILE_NAME)

    CFG_FILE_PATH = join(SYSTEM_TEMPLATE_RECEIPT_FOOT_PATH,
                         RECEIPT_FOOTER_CFG_FILE_NAME)

    MSG_FILE_PATH = join(SYSTEM_TEMPLATE_RECEIPT_FOOT_PATH,
                         RECEIPT_FOOTER_MSG_FILE_NAME)

    def __init__(self):
        """Initializes the FooterContainer"""
        super(FooterContainer, self).__init__()
        self._generate_components()

    def _generate_components(self):
        """

        @return:
        """
        footer = self._get_footer()
        width = DEFAULT_FRONT_PRINTER_WIDTH
        height = self.DEFAULT_FOOTER_HEIGHT

        self.add_flowables([footer], width, height)

    def _get_footer(self):
        """Gets the footer data to
        be stored for writing.

        @return: reportlab.platypus.Paragraph
        class representing the stored text to
        be written.
        """
        ptext = self._get_ptext()
        return Paragraph(ptext, self.DEFAULT_STYLE)

    def _get_ptext(self):
        """Gets the paragraph
        text that will be used to
        display in the footer.

        @return: str representing
        the text for the footer.
        """
        cfg = self._process_cfg()
        rml = self._get_rml_data(self.RML_FILE_PATH)
        return rml.format(**cfg)

    def _process_cfg(self):
        """Process the cfg
        file with the expected
        keys.

        @return: dict representing
        the cfg file that is to be
        used in formatting the rml
        file.
        """
        msg = self._get_rml_data(self.MSG_FILE_PATH)
        cfg = self._get_cfg_data(self.CFG_FILE_PATH)
        cfg[self.CFG_MSG_KEY] = msg
        return cfg