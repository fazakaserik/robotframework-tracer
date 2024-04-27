from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from robotframework_tracer.display_pb2 import DESCRIPTOR
from robotframework_tracer.display_pb2_grpc import (
    add_DisplayServiceServicer_to_server,
)
from robotframework_tracer.DisplayService import DisplayService


class DisplayServiceManager:

    def __init__(self, update_display_callback) -> None:
        self.update_display_callback = update_display_callback

    def start_display_service(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_DisplayServiceServicer_to_server(
            DisplayService(self.update_display_callback), server
        )

        # Add reflection
        SERVICE_NAMES = (
            DESCRIPTOR.services_by_name["DisplayService"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server)

        server.add_insecure_port(f"[::]:50051")
        server.start()
        server.wait_for_termination()
