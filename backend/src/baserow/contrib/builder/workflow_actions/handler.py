from typing import Dict, Iterable, List, Optional
from zipfile import ZipFile

from django.core.files.storage import Storage
from django.db.models import QuerySet

from baserow.contrib.builder.elements.handler import ElementHandler
from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.pages.models import Page
from baserow.contrib.builder.workflow_actions.exceptions import (
    WorkflowActionNotInElement,
)
from baserow.contrib.builder.workflow_actions.models import BuilderWorkflowAction
from baserow.contrib.builder.workflow_actions.registries import (
    builder_workflow_action_type_registry,
)
from baserow.core.exceptions import IdDoesNotExist
from baserow.core.workflow_actions.handler import WorkflowActionHandler
from baserow.core.workflow_actions.models import WorkflowAction
from baserow.core.workflow_actions.registries import WorkflowActionType


class BuilderWorkflowActionHandler(WorkflowActionHandler):
    model = BuilderWorkflowAction
    registry = builder_workflow_action_type_registry

    def get_workflow_actions(
        self, page: Page, base_queryset: Optional[QuerySet] = None
    ) -> Iterable[WorkflowAction]:
        """
        Get all the workflow actions of an page

        :param page: The page associated with the workflow actions
        :param base_queryset: Optional base queryset to filter the results
        :return: A list of workflow actions
        """

        if base_queryset is None:
            base_queryset = self.model.objects

        base_queryset = base_queryset.filter(page=page)

        return super().get_all_workflow_actions(base_queryset)

    def update_workflow_action(
        self, workflow_action: BuilderWorkflowAction, **kwargs
    ) -> WorkflowAction:
        # When we are switching types we want to preserve the event and element and
        # page ids
        if "type" in kwargs and kwargs["type"] != workflow_action.get_type().type:
            kwargs["page_id"] = workflow_action.page_id
            kwargs["element_id"] = workflow_action.element_id
            kwargs["event"] = workflow_action.event
            kwargs["order"] = workflow_action.order

        return super().update_workflow_action(workflow_action, **kwargs)

    def import_workflow_action(
        self,
        page: Page,
        serialized_workflow_action: Dict,
        id_mapping: Dict[str, Dict[int, int]],
        files_zip: Optional[ZipFile] = None,
        storage: Optional[Storage] = None,
    ):
        """
        Creates an instance using the serialized version previously exported with
        `.export_workflow_action'.

        :param page: The page instance the new  action should belong to.
        :param serialized_workflow_action: The serialized version of the action.
        :param id_mapping: A map of old->new id per data type
            when we have foreign keys that need to be migrated.
        :param files_zip: Contains files to import if any.
        :param storage: Storage to get the files from.
        :return: the new action instance.
        """

        workflow_action_type = builder_workflow_action_type_registry.get(
            serialized_workflow_action["type"]
        )
        return workflow_action_type.import_serialized(
            page, serialized_workflow_action, id_mapping
        )

    def order_workflow_actions(
        self, page: Page, order: List[int], base_qs=None, element: Element = None
    ):
        """
        Assigns a new order to the domains in a builder application.
        You can provide a base_qs for pre-filter the domains affected by this change.

        :param page: The page the workflow actions belong to
        :param order: The new order of the workflow actions
        :param base_qs: A QS that can have filters already applied
        :param element: The element the workflow action belongs to
        :raises WorkflowActionNotInElement: If the workflow action is not part of the
            provided element
        :return: The new order of the domains
        """

        if base_qs is None:
            base_qs = BuilderWorkflowAction.objects.filter(page=page, element=element)

        try:
            full_order = BuilderWorkflowAction.order_objects(base_qs, order)
        except IdDoesNotExist as error:
            raise WorkflowActionNotInElement(error.not_existing_id)

        return full_order

    def create_workflow_action(
        self, workflow_action_type: WorkflowActionType, **kwargs
    ) -> BuilderWorkflowAction:
        if "order" not in kwargs:
            if "element_id" in kwargs:
                element = ElementHandler().get_element(element_id=kwargs["element_id"])
                kwargs["order"] = BuilderWorkflowAction.get_last_order_element_scope(
                    element
                )
            else:
                kwargs["order"] = BuilderWorkflowAction.get_last_order_page_scope(
                    kwargs["page"]
                )

        return super().create_workflow_action(workflow_action_type, **kwargs).specific
