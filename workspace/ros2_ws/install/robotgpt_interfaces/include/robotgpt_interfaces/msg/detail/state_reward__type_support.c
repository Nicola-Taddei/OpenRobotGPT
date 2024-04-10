// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from robotgpt_interfaces:msg/StateReward.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "robotgpt_interfaces/msg/detail/state_reward__rosidl_typesupport_introspection_c.h"
#include "robotgpt_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "robotgpt_interfaces/msg/detail/state_reward__functions.h"
#include "robotgpt_interfaces/msg/detail/state_reward__struct.h"


// Include directives for member types
// Member `state`
// Member `info`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `info_keys`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void StateReward__rosidl_typesupport_introspection_c__StateReward_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  robotgpt_interfaces__msg__StateReward__init(message_memory);
}

void StateReward__rosidl_typesupport_introspection_c__StateReward_fini_function(void * message_memory)
{
  robotgpt_interfaces__msg__StateReward__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember StateReward__rosidl_typesupport_introspection_c__StateReward_message_member_array[5] = {
  {
    "state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotgpt_interfaces__msg__StateReward, state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "info_keys",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotgpt_interfaces__msg__StateReward, info_keys),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotgpt_interfaces__msg__StateReward, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reward",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotgpt_interfaces__msg__StateReward, reward),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "terminal",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotgpt_interfaces__msg__StateReward, terminal),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers StateReward__rosidl_typesupport_introspection_c__StateReward_message_members = {
  "robotgpt_interfaces__msg",  // message namespace
  "StateReward",  // message name
  5,  // number of fields
  sizeof(robotgpt_interfaces__msg__StateReward),
  StateReward__rosidl_typesupport_introspection_c__StateReward_message_member_array,  // message members
  StateReward__rosidl_typesupport_introspection_c__StateReward_init_function,  // function to initialize message memory (memory has to be allocated)
  StateReward__rosidl_typesupport_introspection_c__StateReward_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t StateReward__rosidl_typesupport_introspection_c__StateReward_message_type_support_handle = {
  0,
  &StateReward__rosidl_typesupport_introspection_c__StateReward_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_robotgpt_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, robotgpt_interfaces, msg, StateReward)() {
  if (!StateReward__rosidl_typesupport_introspection_c__StateReward_message_type_support_handle.typesupport_identifier) {
    StateReward__rosidl_typesupport_introspection_c__StateReward_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &StateReward__rosidl_typesupport_introspection_c__StateReward_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
