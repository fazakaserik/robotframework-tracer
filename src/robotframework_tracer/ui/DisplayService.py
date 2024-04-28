from concurrent import futures

import google.protobuf.empty_pb2
import grpc
from grpc_reflection.v1alpha import reflection

from robotframework_tracer.ui.generated.display_pb2 import DisplayTextRequest
from robotframework_tracer.ui.generated.display_pb2_grpc import (
    DisplayServiceServicer,
)


class DisplayService(DisplayServiceServicer):

    def __init__(self, update_display_callback) -> None:
        super().__init__()
        self.update_display_callback = update_display_callback

    def DisplayText(self, request: DisplayTextRequest, context):
        self.update_display_callback(request.text)
        return google.protobuf.empty_pb2.Empty()
