"""Wireless channel."""
import ipaddress
import logging
import os

from enum import Enum
from ns import core, internet, network as ns_net, wifi

from .channel import Channel
from ..interface import Interface

logger = logging.getLogger(__name__)

class WiFiChannel(Channel):
    """
    A WiFiChannel is a physical (but of course wireless) connection
    between two or more wireless devices.

    Further information can be found reading the
    `ns-3 source here <https://www.nsnam.org/doxygen/wifi-phy_8cc_source.html>`_.

    Parameters
    ----------
    channel : int
        The WiFi channel to use.
        This will be **ignored** if frequency is set.
    frequency : int
        The frequency of the wireless channel in MHz.
    channel_width : int
        The width of the channel in MHz.
        Valid values are :code:`5`, :code:`10`, :code:`20`, :code:`22`, :code:`40`, :code:`80`, :code:`160`.
    antennas : int
        The number of antennas / spatial streams to use.
    tx_power : float
        The sending power in dBm.
    standard : :class:`.WiFiStandard`
        The WiFi standard to use.
    data_rate : :class:`.WiFiDataRate`
        The WiFi data rate to use. Please make sure to pick a valid data rate for your :code:`standard`.
    """

    class WiFiStandard(Enum):
        """All available WiFi standards.

        See here for further information: https://en.wikipedia.org/wiki/IEEE_802.11.
        """
        #: The first WiFi standard from 1999.
        WIFI_802_11a = wifi.WIFI_PHY_STANDARD_80211a
        #: Standard with maximum raw data rate of 11 Mbit/s.
        WIFI_802_11b = wifi.WIFI_PHY_STANDARD_80211b
        #: Standard with maximum raw bitrate of 54 Mbit/s in 2.4GHz band.
        WIFI_802_11g = wifi.WIFI_PHY_STANDARD_80211g
        #: Standard from 2009 in 2.4GHz band.
        WIFI_802_11n = wifi.WIFI_PHY_STANDARD_80211n_2_4GHZ
        #: Standard from 2009 in 5GHz band.
        WIFI_802_11n_5G = wifi.WIFI_PHY_STANDARD_80211n_5GHZ
        #: Standard from 2013.
        WIFI_802_11ac = wifi.WIFI_PHY_STANDARD_80211ac
        #: "WiFi 6".
        WIFI_802_11ax = wifi.WIFI_PHY_STANDARD_80211ax_2_4GHZ

    class WiFiDataRate(Enum):
        """All available WiFi data rates.

        Choosing the correct and best data rate depends on the standard you are using.
        """
        #: Use with :attr:`.WiFiStandard.WIFI_802_11a`.
        OFDM_RATE_6Mbps = "OfdmRate6Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11a`.
        OFDM_RATE_9Mbps = "OfdmRate9Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11a`.
        OFDM_RATE_12Mbps = "OfdmRate12Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11a`.
        OFDM_RATE_18Mbps = "OfdmRate18Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11a`.
        OFDM_RATE_24Mbps = "OfdmRate24Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11a`.
        OFDM_RATE_36Mbps = "OfdmRate36Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11a`.
        OFDM_RATE_48Mbps = "OfdmRate48Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11a`.
        OFDM_RATE_54Mbps = "OfdmRate54Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11b`, :attr:`.WiFiStandard.WIFI_802_11g`,
        #: :attr:`.WiFiStandard.WIFI_802_11ac` or :attr:`.WiFiStandard.WIFI_802_11ax`.
        DSSS_RATE_1Mbps = "DsssRate1Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11b`, :attr:`.WiFiStandard.WIFI_802_11g`,
        #: :attr:`.WiFiStandard.WIFI_802_11ac` or :attr:`.WiFiStandard.WIFI_802_11ax`.
        DSSS_RATE_2Mbps = "DsssRate2Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11b`, :attr:`.WiFiStandard.WIFI_802_11g`,
        #: :attr:`.WiFiStandard.WIFI_802_11ac` or :attr:`.WiFiStandard.WIFI_802_11ax`.
        DSSS_RATE_5_5Mbps = "DsssRate5_5Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11b`, :attr:`.WiFiStandard.WIFI_802_11g`,
        #: :attr:`.WiFiStandard.WIFI_802_11ac` or :attr:`.WiFiStandard.WIFI_802_11ax`.
        DSSS_RATE_11Mbps = "DsssRate11Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11g`, :attr:`.WiFiStandard.WIFI_802_11ac` or
        #: :attr:`.WiFiStandard.WIFI_802_11ax`.
        ERP_OFDM_RATE_6Mbps = "ErpOfdmRate6Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11g`, :attr:`.WiFiStandard.WIFI_802_11ac` or
        #: :attr:`.WiFiStandard.WIFI_802_11ax`.
        ERP_OFDM_RATE_9Mbps = "ErpOfdmRate9Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11g`, :attr:`.WiFiStandard.WIFI_802_11ac` or
        #: :attr:`.WiFiStandard.WIFI_802_11ax`.
        ERP_OFDM_RATE_12Mbps = "ErpOfdmRate12Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11g`, :attr:`.WiFiStandard.WIFI_802_11ac` or
        #: :attr:`.WiFiStandard.WIFI_802_11ax`.
        ERP_OFDM_RATE_18Mbps = "ErpOfdmRate18Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11g`, :attr:`.WiFiStandard.WIFI_802_11ac` or
        #: :attr:`.WiFiStandard.WIFI_802_11ax`.
        ERP_OFDM_RATE_24Mbps = "ErpOfdmRate24Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11g`, :attr:`.WiFiStandard.WIFI_802_11ac` or
        #: :attr:`.WiFiStandard.WIFI_802_11ax`.
        ERP_OFDM_RATE_36Mbps = "ErpOfdmRate36Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11g`, :attr:`.WiFiStandard.WIFI_802_11ac` or
        #: :attr:`.WiFiStandard.WIFI_802_11ax`.
        ERP_OFDM_RATE_48Mbps = "ErpOfdmRate48Mbps"
        #: Use with :attr:`.WiFiStandard.WIFI_802_11g`, :attr:`.WiFiStandard.WIFI_802_11ac` or
        #: :attr:`.WiFiStandard.WIFI_802_11ax`.
        ERP_OFDM_RATE_54Mbps = "ErpOfdmRate54Mbps"

    def __init__(self, network, nodes, frequency=None, channel=1, channel_width=40, antennas=1, tx_power=20.0,
                 standard: WiFiStandard = WiFiStandard.WIFI_802_11a,
                 data_rate: WiFiDataRate = WiFiDataRate.OFDM_RATE_6Mbps):
        super().__init__(network, nodes)

        #: The channel to use.
        self.channel = channel
        #: The frequency to use.
        #:
        #: This could collide with other WiFi channels.
        self.frequency = frequency
        #: The width of the channel in MHz.
        self.channel_width = channel_width
        #: The number of antennas to use.
        self.antennas = antennas
        #: The sending power in dBm.
        self.tx_power = tx_power
        #: The WiFi standard to use.
        self.standard = standard
        #: The data rate to use.
        self.data_rate = data_rate

        logger.debug("Setting up physical layer of WiFi.")
        self.wifi_phy_helper = wifi.YansWifiPhyHelper.Default()
        self.wifi_phy_helper.Set("ChannelWidth", core.UintegerValue(self.channel_width))
        if self.frequency:
            self.wifi_phy_helper.Set("Frequency", core.UintegerValue(self.frequency))
        else:
            self.wifi_phy_helper.Set("ChannelNumber", core.UintegerValue(self.channel))
        self.wifi_phy_helper.Set("Antennas", core.UintegerValue(self.antennas))
        self.wifi_phy_helper.Set("MaxSupportedTxSpatialStreams", core.UintegerValue(self.antennas))
        self.wifi_phy_helper.Set("MaxSupportedRxSpatialStreams", core.UintegerValue(self.antennas))
        self.wifi_phy_helper.Set("TxPowerStart", core.DoubleValue(self.tx_power))
        self.wifi_phy_helper.Set("TxPowerEnd", core.DoubleValue(self.tx_power))

        # Enable monitoring of radio headers.
        self.wifi_phy_helper.SetPcapDataLinkType(wifi.WifiPhyHelper.DLT_IEEE802_11_RADIO)

        wifi_channel_helper = wifi.YansWifiChannelHelper()
        wifi_channel_helper.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel")
        wifi_channel_helper.AddPropagationLoss("ns3::LogDistancePropagationLossModel")
        # wifi_channel_helper.AddPropagationLoss("ns3::RangePropagationLossModel")

        self.wifi_phy_helper.SetChannel(wifi_channel_helper.Create())

        #: Helper for creating the WiFi channel
        self.wifi = wifi.WifiHelper()
        self.wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager",
                                          "DataMode", core.StringValue(self.data_rate.value),
                                          "ControlMode", core.StringValue(self.data_rate.value))
        self.wifi.SetStandard(self.standard.value)

        wifi_mac_helper = wifi.WifiMacHelper()

        # Adhoc network between multiple nodes (no access point).
        wifi_mac_helper.SetType("ns3::AdhocWifiMac")

        # Install on all connected nodes.
        logger.debug("Installing the WiFi channel to %d nodes. Mode is %s (data) / %s (control).", len(nodes),
                     self.standard, self.data_rate)
        #: All ns-3 devices on this channel.
        self.devices_container = self.wifi.Install(self.wifi_phy_helper, wifi_mac_helper, self.ns3_nodes_container)

        logger.info('Setting IP addresses on nodes.')
        stack_helper = internet.InternetStackHelper()

        for i, node in enumerate(nodes):
            ns3_device = self.devices_container.Get(i)

            address = None
            if node.wants_ip_stack():
                if node.ns3_node.GetObject(internet.Ipv4.GetTypeId()) is None:
                    logger.info('Installing IP stack on %s', node.name)
                    stack_helper.Install(node.ns3_node)
                device_container = ns_net.NetDeviceContainer(ns3_device)
                ip_address = self.network.address_helper.Assign(device_container).GetAddress(0)
                netmask = network.network.prefixlen
                address = ipaddress.ip_interface(f'{ip_address}/{netmask}')

            interface = Interface(node=node, ns3_device=ns3_device, address=address)
            ns3_device.GetMac().SetAddress(ns_net.Mac48Address(interface.mac_address))
            node.add_interface(interface)
            self.interfaces.append(interface)


    def prepare(self, simulation):
        for interface in self.interfaces:
            pcap_log_path = os.path.join(simulation.log_directory, interface.pcap_file_name)
            self.wifi_phy_helper.EnablePcap(pcap_log_path, interface.ns3_device, True, True)
