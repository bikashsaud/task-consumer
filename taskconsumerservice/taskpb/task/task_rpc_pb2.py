# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: task/task_rpc.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'task/task_rpc.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from taskconsumerservice.taskpb.task import task_pb2 as task_dot_task__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13task/task_rpc.proto\x12\x1etaskprocessservice.taskpb.task\x1a\x0ftask/task.proto2\x87\x02\n\x07TaskRpc\x12x\n\tfetchTask\x12\x34.taskprocessservice.taskpb.task.FetchTaskBaseRequest\x1a\x35.taskprocessservice.taskpb.task.FetchTaskBaseResponse\x12\x81\x01\n\x10updateTaskStatus\x12\x35.taskprocessservice.taskpb.task.UpdateTaskBaseRequest\x1a\x36.taskprocessservice.taskpb.task.UpdateTaskBaseResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'task.task_rpc_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TASKRPC']._serialized_start=73
  _globals['_TASKRPC']._serialized_end=336
# @@protoc_insertion_point(module_scope)
