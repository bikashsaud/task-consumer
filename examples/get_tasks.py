import uuid

import grpc
from taskconsumerservice.taskpb.task import task_rpc_pb2_grpc
from taskconsumerservice.taskpb.task.task_pb2 import FetchTaskBaseRequest, Debug


def run():
    debug = Debug(
        debug_id=uuid.uuid4().hex,
    )
    with grpc.insecure_channel('localhost:9010') as channel:
        stub = task_rpc_pb2_grpc.TaskRpcStub(channel)
        request = FetchTaskBaseRequest(debug=debug)
        response = stub.fetchTask(request)
        print(f"task_list: {response}")

if __name__ == '__main__':
    run()
