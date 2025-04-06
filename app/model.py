from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date, time
from uuid import uuid4

# ======================= 1️⃣ User =======================
class User(SQLModel, table=True, extend_existing=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str
    MSSV: int | None
    lastname: str
    firstname: str
    isUser: bool = True
    isAdmin: bool = False
    isActive: Optional[bool] = True

    # Quan hệ với OrderRoom, UsedRoom, CancelRoom, và Report
    orders: List["OrderRoom"] = Relationship(back_populates="user")
    used_rooms: List["UsedRoom"] = Relationship(back_populates="user")
    cancellations: List["CancelRoom"] = Relationship(back_populates="user")
    reports: List["Report"] = Relationship(back_populates="user")


# ======================= 2️⃣ Branch =======================
class Branch(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    branch_name: str
    buildings: List["Building"] = Relationship(back_populates="branch")


# ======================= 3️⃣ Building =======================
class Building(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    branch_id: int = Field(foreign_key="branch.id")
    building_name: str

    branch: Optional[Branch] = Relationship(back_populates="buildings")
    rooms: List["Room"] = Relationship(back_populates="building")


# ======================= 4️⃣ RoomType =======================
class RoomType(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    type_name: str
    max_capacity: int

    rooms: List["Room"] = Relationship(back_populates="room_type")


# ======================= 5️⃣ Room =======================
class Room(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    branch_id: int = Field(foreign_key="branch.id")
    building_id: int = Field(foreign_key="building.id")
    type_id: int = Field(foreign_key="roomtype.id")

    floor: int
    no_room: str
    max_quantity: int
    quantity: Optional[int] = None
    led: bool = False
    air_conditioner: bool = False
    socket: int
    projector: bool = False
    interactive_display: bool = False
    online_meeting_devices: bool = False
    active: bool = True

    branch: Optional[Branch] = Relationship()  # Xóa back_populates="rooms"
    building: Optional[Building] = Relationship(back_populates="rooms")
    room_type: Optional[RoomType] = Relationship(back_populates="rooms")
    orders: List["OrderRoom"] = Relationship(back_populates="room")
    used_rooms: List["UsedRoom"] = Relationship(back_populates="room")


# ======================= 6️⃣ OrderRoom (Đặt phòng) =======================
class OrderRoom(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    room_id: int = Field(foreign_key="room.id")
    user_id: int = Field(foreign_key="user.id")

    date: date
    begin: time
    end: time

    room: Optional[Room] = Relationship(back_populates="orders")
    user: Optional[User] = Relationship(back_populates="orders")
    used_rooms: List["UsedRoom"] = Relationship(back_populates="order")
    cancel: Optional["CancelRoom"] = Relationship(back_populates="order")


# ======================= 7️⃣ CancelRoom (Hủy đặt phòng) =======================
class CancelRoom(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orderroom.id")
    user_id: int = Field(foreign_key="user.id")

    date_cancel: date

    order: Optional[OrderRoom] = Relationship(back_populates="cancel")
    user: Optional[User] = Relationship(back_populates="cancellations")


# ======================= 8️⃣ UsedRoom (Phòng đã sử dụng) =======================
class UsedRoom(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orderroom.id")
    user_id: int = Field(foreign_key="user.id")
    room_id: int = Field(foreign_key="room.id")

    date: date
    checkin: time
    checkout: time

    order: Optional[OrderRoom] = Relationship(back_populates="used_rooms")
    user: Optional[User] = Relationship(back_populates="used_rooms")
    room: Optional[Room] = Relationship(back_populates="used_rooms")
    report: Optional["Report"] = Relationship(back_populates="used_room")


# ======================= 9️⃣ Report (Báo cáo sự cố) =======================
class Report(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    used_room_id: int = Field(foreign_key="usedroom.id")
    user_id: int = Field(foreign_key="user.id")

    led: bool = False
    air_conditioner: bool = False
    socket: bool = False
    projector: bool = False
    interactive_display: bool = False
    online_meeting_devices: bool = False
    description: Optional[str] = None

    used_room: Optional[UsedRoom] = Relationship(back_populates="report")
    user: Optional[User] = Relationship(back_populates="reports")
