import dis
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
    
def start_display_service(update_display_callback):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    display_pb2_grpc.add_DisplayServiceServicer_to_server(
        DisplayService(update_display_callback), server)

    # Add reflection
    SERVICE_NAMES = (
        display_pb2.DESCRIPTOR.services_by_name['DisplayService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port(f"[::]:50051")
    server.start()
    server.wait_for_termination()