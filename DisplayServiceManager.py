from DisplayService import DisplayService
import display_pb2
import display_pb2_grpc
from grpc_reflection.v1alpha import reflection
import grpc
from concurrent import futures

class DisplayServiceManager():
    
    def __init__(
        self,
        update_display_callback
        ) -> None:
        self.update_display_callback = update_display_callback
    
    def start_display_service(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        display_pb2_grpc.add_DisplayServiceServicer_to_server(
            DisplayService(self.update_display_callback), server)

        # Add reflection
        SERVICE_NAMES = (
            display_pb2.DESCRIPTOR.services_by_name['DisplayService'].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server)

        server.add_insecure_port(f"[::]:50051")
        server.start()
        server.wait_for_termination()