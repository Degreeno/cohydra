"""Nodes are the main components of simulating behaviour."""
import logging

from .base import Node
from .switch import SwitchNode
from .docker import DockerNode
from .lxd import LXDNode
from .external import ExternalNode
from .ssh import SSHNode
