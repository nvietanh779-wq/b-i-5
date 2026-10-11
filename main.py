from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


class DeviceStatus(Enum):
  ACTIVE = "Active"
  UNDER_MAINTENANCE = "UnderMaintenance"
  RETIRED = "Retired"


class INetworkable(ABC):

  @property
  @abstractmethod
  def ip_address(self) -> str:
    pass

  @property
  @abstractmethod
  def is_connected(self) -> bool:
    pass

  @abstractmethod
  def connect(self, ip_address: str):
    pass

  @abstractmethod
  def disconnect(self):
    pass


class Device(ABC):

  def __init__(
      self,
      id: str,
      name: str,
      year_in_use: int,
      purchase_price: float,
      status: DeviceStatus,
  ):
    self.id = id
    self.name = name
    self.year_in_use = year_in_use
    self.purchase_price = purchase_price
    self.status = status

  @property
  def id(self) -> str:
    return self._id

  @id.setter
  def id(self, value: str):
    if not value or not value.strip():
      raise ValueError("Mã thiết bị không được rỗng.")
    self._id = value

  @property
  def name(self) -> str:
    return self._name

  @name.setter
  def name(self, value: str):
    if not value or not value.strip():
      raise ValueError("Tên thiết bị không được rỗng.")
    self._name = value

  @property
  def year_in_use(self) -> int:
    return self._year_in_use

  @year_in_use.setter
  def year_in_use(self, value: int):
    current_year = datetime.now().year
    if value > current_year:
      raise ValueError(
          f"Năm đưa vào sử dụng không được lớn hơn năm hiện tại ({current_year})."
      )
    self._year_in_use = value

  @property
  def purchase_price(self) -> float:
    return self._purchase_price

  @purchase_price.setter
  def purchase_price(self, value: float):
    if value <= 0:
      raise ValueError("Giá mua phải lớn hơn 0.")
    self._purchase_price = value

  @abstractmethod
  def calculate_annual_maintenance_cost(self) -> float:
    pass

  def is_older_than_5_years(self) -> bool:
    return (datetime.now().year - self.year_in_use) > 5

  def __str__(self):
    return (
        f"[ID: {self.id}] {self.name} | Năm SD: {self.year_in_use} | Giá:"
        f" {self.purchase_price:,.0f} VNĐ | Trạng thái: {self.status.value}"
    )


class Computer(Device, INetworkable):

  def __init__(
      self,
      id: str,
      name: str,
      year_in_use: int,
      purchase_price: float,
      status: DeviceStatus,
      ram_size: int,
      processor_type: str,
      has_discrete_gpu: bool,
  ):
    super().__init__(id, name, year_in_use, purchase_price, status)
    self.ram_size = ram_size
    self.processor_type = processor_type
    self.has_discrete_gpu = has_discrete_gpu
    self._ip_address = ""
    self._is_connected = False

  @property
  def ip_address(self) -> str:
    return self._ip_address

  @property
  def is_connected(self) -> bool:
    return self._is_connected

  def calculate_annual_maintenance_cost(self) -> float:
    cost = self.purchase_price * 0.05
    if self.has_discrete_gpu:
      cost += self.purchase_price * 0.02
    if self.is_older_than_5_years():
      cost += self.purchase_price * 0.01
    return cost

  def connect(self, ip_address: str):
    if not ip_address or not ip_address.strip():
      raise ValueError("Địa chỉ IP không được rỗng.")
    if self._is_connected:
      raise RuntimeError("Thiết bị đang kết nối.")
    self._ip_address = ip_address
    self._is_connected = True

  def disconnect(self):
    self._is_connected = False
    self._ip_address = ""

  def __str__(self):
    net_info = f" | IP: {self.ip_address}" if self._is_connected else ""
    return (
        super().__str__()
        + f" | RAM: {self.ram_size}GB, CPU: {self.processor_type}, GPU rời:"
        f" {self.has_discrete_gpu}{net_info}"
    )


class Printer(Device):

  def __init__(
      self,
      id: str,
      name: str,
      year_in_use: int,
      purchase_price: float,
      status: DeviceStatus,
      printer_type: str,
      pages_printed: int,
      is_color: bool,
  ):
    super().__init__(id, name, year_in_use, purchase_price, status)
    self.printer_type = printer_type
    self.pages_printed = pages_printed
    self.is_color = is_color

  def calculate_annual_maintenance_cost(self) -> float:
    cost = self.purchase_price * 0.04
    if self.pages_printed > 100000:
      cost += 500000.0
    if self.is_color:
      cost += 300000.0
    return cost

  def __str__(self):
    return (
        super().__str__()
        + f" | Loại: {self.printer_type}, Số trang:"
        f" {self.pages_printed:,}, Màu: {self.is_color}"
    )


class NetworkPrinter(Printer, INetworkable):

  def __init__(
      self,
      id: str,
      name: str,
      year_in_use: int,
      purchase_price: float,
      status: DeviceStatus,
      printer_type: str,
      pages_printed: int,
      is_color: bool,
  ):
    super().__init__(
        id,
        name,
        year_in_use,
        purchase_price,
        status,
        printer_type,
        pages_printed,
        is_color,
    )
    self._ip_address = ""
    self._is_connected = False

  @property
  def ip_address(self) -> str:
    return self._ip_address

  @property
  def is_connected(self) -> bool:
    return self._is_connected

  def connect(self, ip_address: str):
    if not ip_address or not ip_address.strip():
      raise ValueError("Địa chỉ IP không được rỗng.")
    if self._is_connected:
      raise RuntimeError("Thiết bị đang kết nối.")
    self._ip_address = ip_address
    self._is_connected = True

  def disconnect(self):
    self._is_connected = False
    self._ip_address = ""

  def __str__(self):
    net_info = f" | IP: {self.ip_address}" if self._is_connected else ""
    return super().__str__() + net_info


class Projector(Device):

  def __init__(
      self,
      id: str,
      name: str,
      year_in_use: int,
      purchase_price: float,
      status: DeviceStatus,
      brightness_lumens: int,
      bulb_hours_used: int,
  ):
    super().__init__(id, name, year_in_use, purchase_price, status)
    self.brightness_lumens = brightness_lumens
    self.bulb_hours_used = bulb_hours_used

  def calculate_annual_maintenance_cost(self) -> float:
    cost = self.purchase_price * 0.03
    if self.bulb_hours_used > 3000:
      cost += 1500000.0
    return cost

  def __str__(self):
    return (
        super().__str__()
        + f" | Độ sáng: {self.brightness_lumens} lumens, Giờ bóng đèn:"
        f" {self.bulb_hours_used}h"
    )
class LabRoom:

  def __init__(self, room_id: str, room_name: str, capacity: int):
    self.room_id = room_id
    self.room_name = room_name
    self.capacity = capacity
    self._devices = []

  @property
  def devices(self):
    return list(self._devices)

  def add_device(self, device: Device):
    if device is None:
      raise ValueError("Không chấp nhận đối tượng thiết bị null.")
    if self.find_device(device.id) is not None:
      raise ValueError(
          f"Thiết bị có mã '{device.id}' đã tồn tại trong phòng."
      )
    self._devices.append(device)

  def remove_device(self, device_id: str) -> bool:
    device = self.find_device(device_id)
    if device:
      self._devices.remove(device)
      return True
    return False

  def find_device(self, device_id: str):
    for d in self._devices:
      if d.id.lower() == device_id.lower():
        return d
    return None

  def calculate_annual_maintenance_cost(self) -> float:
    total_cost = 0.0
    for device in self._devices:
      total_cost += device.calculate_annual_maintenance_cost()  # Đa hình
    return total_cost

  def get_devices_requiring_maintenance(self):
    return [
        d
        for d in self._devices
        if d.status == DeviceStatus.UNDER_MAINTENANCE
        or d.is_older_than_5_years()
    ]
if __name__ == "__main__":
  print("=== CHƯƠNG TRÌNH QUẢN LÝ THIẾT BỊ VÀ BẢO TRÌ (PYTHON) ===")
  try:
    pc1 = Computer(
        "PC01",
        "Dell OptiPlex",
        2024,
        15000000.0,
        DeviceStatus.ACTIVE,
        16,
        "Intel Core i5",
        False,
    )
    pc2 = Computer(
        "PC02",
        "ASUS ROG Strix",
        2019,
        28000000.0,
        DeviceStatus.UNDER_MAINTENANCE,
        32,
        "Intel Core i7",
        True,
    )
    printer1 = Printer(
        "PR01",
        "HP LaserJet Pro",
        2022,
        5000000.0,
        DeviceStatus.ACTIVE,
        "Laser",
        120000,
        False,
    )
    printer2 = NetworkPrinter(
        "PR02",
        "Canon Pixma Network",
        2023,
        7000000.0,
        DeviceStatus.ACTIVE,
        "Phun",
        45000,
        True,
    )
    projector1 = Projector(
        "PJ01",
        "Epson EB-S41",
        2020,
        12000000.0,
        DeviceStatus.ACTIVE,
        3300,
        3500,
    )

    room_a = LabRoom("ROOM_A", "Phòng Thực hành Tin học 1", 30)
    room_b = LabRoom("ROOM_B", "Phòng Thực hành Phần cứng", 25)

    room_a.add_device(pc1)
    room_a.add_device(printer1)
    room_a.add_device(projector1)

    room_b.add_device(pc2)
    room_b.add_device(printer2)

    try:
      pc_dup = Computer(
          "PC01",
          "Clone PC",
          2025,
          10000000.0,
          DeviceStatus.ACTIVE,
          8,
          "Intel Core i3",
          False,
      )
      room_a.add_device(pc_dup)
    except Exception as ex:
      print(f"\n[Bắt lỗi trùng mã]: {ex}")

    print(f"\n--- DANH SÁCH THIẾT BỊ TRONG {room_a.room_name.upper()} ---")
    for d in room_a.devices:
      print(d)

    print(f"\n--- DANH SÁCH THIẾT BỊ TRONG {room_b.room_name.upper()} ---")
    for d in room_b.devices:
      print(d)

    print("\n--- CHI PHÍ BẢO TRÌ DỰ KIẾN ---")
    print(f"- {room_a.room_name}: {room_a.calculate_annual_maintenance_cost():,.0f} VNĐ")
    print(f"- {room_b.room_name}: {room_b.calculate_annual_maintenance_cost():,.0f} VNĐ")

    print("\n--- KIỂM TRA TÍNH NĂNG KẾT NỐI MẠNG (INetworkable) ---")
    network_devices = [pc1, pc2, printer2]
    for idx, net_dev in enumerate(network_devices, start=1):
      net_dev.connect(f"192.168.1.{10 + idx}")
      print(
          f"Thiết bị mạng #{idx} | IP: {net_dev.ip_address} | IsConnected:"
          f" {net_dev.is_connected}"
      )

  except Exception as ex:
    print(f"Lỗi chương trình: {ex}")