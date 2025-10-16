from pinocchio.visualize import MeshcatVisualizer
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_
import numpy as np
import pinocchio as pin
import sys
import time

robot = pin.RobotWrapper.BuildFromURDF(
    'G1/G1.urdf',
    'G1',
    root_joint=pin.JointModelFreeFlyer()
)
robot.setVisualizer(MeshcatVisualizer())
robot.initViewer(open=True)
robot.loadViewerModel("G1")

Q = pin.neutral(robot.model)

last_display_time = 0
display_interval = 1.0 / 60.0  # 60 Hz


def LowStateHandler(msg: LowState_):
    global robot, Q, last_display_time

    now = time.time()
    if now - last_display_time < display_interval:
        return  # skip too frequent updates

    last_display_time = now

    q_wxyz = np.array(msg.imu_state.quaternion)
    Q[3:7] = q_wxyz[[1, 2, 3, 0]]
    offset = 7
    for i in range(29):
        Q[i+offset] = msg.motor_state[i].q

    # 可视化
    robot.display(Q)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0, "lo")

    sub = ChannelSubscriber("rt/lowstate", LowState_)
    sub.Init(LowStateHandler, 1)

    while True:
        time.sleep(10.0)
