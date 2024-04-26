import display_pb2
import display_pb2_grpc
import google.protobuf.empty_pb2
from grpc_reflection.v1alpha import reflection
import grpc
from concurrent import futures

class DisplayService(display_pb2_grpc.DisplayServiceServicer):
    
    def __init__(
        self,
        update_display_callback
        ) -> None:
        super().__init__()
        self.update_display_callback = update_display_callback
    
    def DisplayText(self, request: display_pb2.DisplayTextRequest, context):
        self.update_display_callback(request.text)
        return google.protobuf.empty_pb2.Empty()