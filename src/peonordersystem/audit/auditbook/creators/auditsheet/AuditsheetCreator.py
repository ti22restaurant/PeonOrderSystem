"""This module defines the creator used to
create the Auditsheet areas of the Auditbook.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from src.peonordersystem.audit.auditbook.creators.abc.Creator import Creator

from .areaContainers.AuditAreaContainer import AuditAreaContainer
from .areaContainers.ChartsAuditAreaContainer import ChartsAuditAreaContainer
from .areaContainers.StatsChartAuditAreaContainer import StatsChartsAuditAreaContainer


class AuditsheetCreator(Creator):
    """AuditsheetCreator controls
    the areas that are part of the
    main overviews area for the
    auditbook.
    """

    def __init__(self, workbook, start_date, end_date, **flags):
        """Initializes the Creator.

        @param workbook: Workbook that the subsequent worksheets
        and data should be added to.

        @param start_date: datetime.datetime that represents the
        starting datetime for the audit.

        @param end_date: datetime.datetime that represents the
        ending datetime for the audit.

        @keyword flags: keyword arguments that allow slight
        customization of which features are activated by this
        creator. Accepted terms are:

            'auditsheet'    :   bool representing if the main
                                auditsheet should be created.

            'audit_charts'  :   bool representing if the main
                                auditwide charts should be created.

            'stats_charts'  :   bool representing if the stats
                                charts for overall audit should
                                be generated.
        """
        self.workbook = workbook
        self._flags = flags
        self.datasheet = workbook.datasheet
        self.date_keys = self.datasheet.create_date_keys(start_date, end_date)

        self._containers = []
        self._create_containers()

    def _create_containers(self):
        """Creates the containers
        associated with the Auditsheets.

        @return: None
        """
        self._create_container_audit_area()
        self._create_container_audit_charts()
        self._create_container_stats_charts()

    def _create_container_audit_area(self):
        """Creates the general auditsheet
        container.

        @return: None
        """
        if self._flags['auditsheet']:
            container = AuditAreaContainer(self.workbook, **self._flags)
            self._containers.append(container)

    def _create_container_audit_charts(self):
        """Creates the general audit charts
        container.

        @return: None
        """
        if self._flags['audit_charts']:
            container = ChartsAuditAreaContainer(self.workbook)
            self._containers.append(container)

    def _create_container_stats_charts(self):
        """Creates the audit stats charts
        container.

        @return: None
        """
        print self._flags
        if self._flags['stats_charts']:
            container = StatsChartsAuditAreaContainer(self.workbook)
            self._containers.append(container)

    def update(self, data):
        """Updates the Creator
        with the given data.

        @param data: data to
        update audit areas.

        @return:None
        """
        for container in self._containers:
            container.update(data)

    def finalize(self):
        """Finalizes the creator.

        @return: None
        """
        for container in self._containers:
            container.finalize()
