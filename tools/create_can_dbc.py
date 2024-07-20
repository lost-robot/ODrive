import cantools
from cantools.database.can import Signal, Node, Message
from odrive.enums import AxisError, AxisState, MotorError, EncoderError, SensorlessEstimatorError, ControlMode, InputMode, ControllerError

msgList = []
nodes = [Node('Master', 'Master node comment')]

for axisID in range(0, 8):
    newNode = Node(f"ODrive_Axis{axisID}", f"Axis node {axisID} comment")
    nodes.append(newNode)

    # 0x001 - Heartbeat
    axisError = Signal("Axis_Error", 0, 32, receivers=['Master'], choices={error.value: error.name for error in AxisError})
    axisState = Signal("Axis_State", 32, 8, receivers=['Master'], choices={state.value: state.name for state in AxisState})
    motorErrorFlag = Signal("Motor_Error_Flag", 40, 1, receivers=['Master'])
    encoderErrorFlag = Signal("Encoder_Error_Flag", 48, 1, receivers=['Master'])
    controllerErrorFlag = Signal("Controller_Error_Flag", 56, 1, receivers=['Master'])
    trajectoryDoneFlag = Signal("Trajectory_Done_Flag", 63, 1, receivers=['Master'])

    heartbeatMsg = Message(
        frame_id=0x001,
        name="Heartbeat",
        length=8,
        signals=[
            axisError,
            axisState,
            motorErrorFlag,
            encoderErrorFlag,
            controllerErrorFlag,
            trajectoryDoneFlag
        ],
        senders=[newNode.name]
    )

    # 0x002 - E-Stop Message
    estopMsg = Message(
        frame_id=0x002,
        name="Estop",
        length=0,
        signals=[],
        senders=['Master']
    )

    # 0x003 - Motor Error
    motorError = Signal("Motor_Error", 0, 32, receivers=['Master'], choices={error.value: error.name for error in MotorError})
    motorErrorMsg = Message(
        frame_id=0x003,
        name="Get_Motor_Error",
        length=8,
        signals=[motorError],
        senders=[newNode.name]
    )

    # 0x004 - Encoder Error
    encoderError = Signal("Encoder_Error", 0, 32, receivers=['Master'], choices={error.value: error.name for error in EncoderError})
    encoderErrorMsg = Message(
        frame_id=0x004,
        name="Get_Encoder_Error",
        length=8,
        signals=[encoderError],
        senders=[newNode.name]
    )

    # 0x005 - Sensorless Error
    sensorlessError = Signal("Sensorless_Error", 0, 32, receivers=['Master'], choices={error.value: error.name for error in SensorlessEstimatorError})
    sensorlessErrorMsg = Message(
        frame_id=0x005,
        name="Get_Sensorless_Error",
        length=8,
        signals=[sensorlessError],
        senders=[newNode.name]
    )

    # Add all other messages similarly...

    axisMsgs = [
        heartbeatMsg,
        motorErrorMsg,
        encoderErrorMsg,
        sensorlessErrorMsg,
        # Add other messages here
    ]

    # Prepend Axis ID to each message name
    for msg in axisMsgs:
        msg.name = f"Axis{axisID}_{msg.name}"
        msg.frame_id |= (axisID << 5)

    msgList.extend(axisMsgs)

# Create the CAN database
db = cantools.db.Database()
for node in nodes:
    db.nodes.append(node)
for msg in msgList:
    db.messages.append(msg)

# Export the database to a DBC file
with open("odrive-cansimple.dbc", 'w') as f:
    f.write(db.as_dbc_string())

# Load the database from the DBC file (if needed)
db = cantools.database.load_file("odrive-cansimple.dbc")
