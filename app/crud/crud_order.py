from sqlmodel import Session, select
from app.model import OrderRoom, CancelRoom, UsedRoom, Room, User
from fastapi import HTTPException
from typing import Optional, List
from datetime import date, time, datetime
from app.crud.crud_room import check_library,update_room
# --- OrderRoom ---
def create_order_room(
    session: Session,
    room_id: int,
    user_id: int,
    date: date,
    begin: time,
    end: time
) -> OrderRoom:
    """
    Create a new OrderRoom entry for a user reserving a room.
    
    Args:
        session (Session): The database session.
        room_id (int): The ID of the room being ordered.
        user_id (int): The ID of the user placing the order.
        date (date): The date of the reservation.
        begin (time): The start time of the reservation.
        end (time): The end time of the reservation.
    
    Returns:
        OrderRoom: The newly created OrderRoom object.
    
    Raises:
        HTTPException: If the room or user is not found, or required fields are missing.
    """
    if not room_id or not user_id or not date or not begin or not end:
        raise HTTPException(status_code=400, detail="All fields are required")

    # Kiểm tra Room
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")

    # Kiểm tra User
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    # Tạo OrderRoom
    order_room = OrderRoom(
        room_id=room_id,
        user_id=user_id,
        date=date,
        begin=begin,
        end=end
    )
    session.add(order_room)
    session.commit()
    session.refresh(order_room)
    return order_room

def get_order_room(session: Session, order_id: int) -> OrderRoom:
    """
    Retrieve an OrderRoom by its ID.
    
    Args:
        session (Session): The database session.
        order_id (int): The ID of the OrderRoom to retrieve.
    
    Returns:
        OrderRoom: The requested OrderRoom object.
    
    Raises:
        HTTPException: If the OrderRoom is not found.
    """
    order_room = session.get(OrderRoom, order_id)
    if not order_room:
        raise HTTPException(status_code=404, detail="OrderRoom not found")
    return order_room

def update_order_room(
    session: Session,
    order_id: int,
    room_id: Optional[int] = None,
    user_id: Optional[int] = None,
    date: Optional[date] = None,
    begin: Optional[time] = None,
    end: Optional[time] = None
) -> OrderRoom:
    """
    Update an existing OrderRoom's attributes.
    
    Args:
        session (Session): The database session.
        order_id (int): The ID of the OrderRoom to update.
        room_id (Optional[int]): The new room ID (optional).
        user_id (Optional[int]): The new user ID (optional).
        date (Optional[date]): The new date (optional).
        begin (Optional[time]): The new start time (optional).
        end (Optional[time]): The new end time (optional).
    
    Returns:
        OrderRoom: The updated OrderRoom object.
    
    Raises:
        HTTPException: If the OrderRoom, Room, or User is not found.
    """
    order_room = session.get(OrderRoom, order_id)
    if not order_room:
        raise HTTPException(status_code=404, detail="OrderRoom not found")

    if room_id is not None:
        room = session.get(Room, room_id)
        if not room:
            raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")
        order_room.room_id = room_id

    if user_id is not None:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        order_room.user_id = user_id

    if date is not None:
        order_room.date = date
    if begin is not None:
        order_room.begin = begin
    if end is not None:
        order_room.end = end

    session.add(order_room)
    session.commit()
    session.refresh(order_room)
    return order_room

def delete_order_room(session: Session, order_id: int) -> bool:
    """
    Delete an OrderRoom by its ID.
    
    Args:
        session (Session): The database session.
        order_id (int): The ID of the OrderRoom to delete.
    
    Returns:
        bool: True if deletion is successful.
    
    Raises:
        HTTPException: If the OrderRoom is not found.
    """
    order_room = session.get(OrderRoom, order_id)
    if not order_room:
        raise HTTPException(status_code=404, detail="OrderRoom not found")
    
    session.delete(order_room)
    session.commit()
    return True

def get_all_order_rooms(session: Session) -> List[OrderRoom]:
    """
    Retrieve all OrderRoom entries.
    
    Args:
        session (Session): The database session.
    
    Returns:
        List[OrderRoom]: A list of all OrderRoom objects.
    
    Raises:
        HTTPException: If no OrderRooms are found.
    """
    order_rooms = session.exec(select(OrderRoom)).all()
    if not order_rooms:
        raise HTTPException(status_code=404, detail="No OrderRooms found")
    return order_rooms

def filter_order_rooms(
    session: Session,
    room_id: Optional[int] = None,
    date: Optional[date] = None,
    begin: Optional[time] = None,
    end: Optional[time] = None,
    page: int = 1,
    limit: int = 0
) -> List[OrderRoom]:
    """
    Filter OrderRoom entries based on room_id and time range, with pagination support.
    If limit is 0, return all matching orders.
    
    Args:
        session (Session): The database session.
        room_id (Optional[int]): Filter by room ID.
        date (Optional[date]): Filter by reservation date.
        begin (Optional[time]): Filter by start time (inclusive).
        end (Optional[time]): Filter by end time (inclusive).
        page (int): Page number for pagination (default: 1).
        limit (int): Number of items per page (default: 0, meaning no limit).
    
    Returns:
        List[OrderRoom]: A list of OrderRoom objects matching the filters.
    
    Raises:
        HTTPException: If no OrderRooms match the filters or the room is not found.
    """
    query = select(OrderRoom)

    # Filter by room_id
    if room_id is not None:
        room = session.get(Room, room_id)
        if not room:
            raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")
        query = query.where(OrderRoom.room_id == room_id)

    # Filter by date
    if date is not None:
        query = query.where(OrderRoom.date == date)

    # Filter by time range (begin and end)
    if begin is not None:
        query = query.where(OrderRoom.begin >= begin)
    if end is not None:
        query = query.where(OrderRoom.end <= end)

    # Pagination
    if limit == 0:
        order_rooms = session.exec(query).all()
    else:
        offset = (page - 1) * limit
        order_rooms = session.exec(query.offset(offset).limit(limit)).all()

    if not order_rooms:
        raise HTTPException(status_code=404, detail="No OrderRooms found with the given filters")

    return order_rooms

def get_order_room_by_user_id(session: Session, user_id: int) -> List[OrderRoom]:
    """
    Retrieve all OrderRoom entries for a specific user.
    
    Args:
        session (Session): The database session.
        user_id (int): The ID of the user.
    
    Returns:
        List[OrderRoom]: A list of OrderRoom objects associated with the user.
    
    Raises:
        HTTPException: If no OrderRooms are found for the user.
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    order_rooms = session.exec(select(OrderRoom).where(OrderRoom.user_id == user_id)).all()
    if not order_rooms:
        raise HTTPException(status_code=404, detail="No OrderRooms found for this user")
    return order_rooms

def get_order_room_by_room_id(session: Session, room_id: int) -> List[OrderRoom]:
    """
    Retrieve all OrderRoom entries for a specific room.
    
    Args:
        session (Session): The database session.
        room_id (int): The ID of the room.
    
    Returns:
        List[OrderRoom]: A list of OrderRoom objects associated with the room.
    
    Raises:
        HTTPException: If no OrderRooms are found for the room.
    """
    if not room_id:
        raise HTTPException(status_code=400, detail="Room ID is required")
    order_rooms = session.exec(select(OrderRoom).where(OrderRoom.room_id == room_id)).all()
    if not order_rooms:
        raise HTTPException(status_code=404, detail="No OrderRooms found for this room")
    return order_rooms

# --- Check Room Availability ---
def check_room_availability(
    session: Session,
    room_id: int,
    date: date,
    start_time: time,
    end_time: time
) -> bool:
    """
    Check if a room is available for a given time range on a specific date.
    Returns True if no OrderRoom exists that overlaps with the provided time range.
    
    Args:
        session (Session): The database session.
        room_id (int): The ID of the room to check.
        date (date): The date to check availability for.
        start_time (time): The start time of the time range.
        end_time (time): The end time of the time range.
    
    Returns:
        bool: True if the room is available, False otherwise.
    
    Raises:
        HTTPException: If the room is not found or required fields are missing.
    """
    if not room_id or not date or not start_time or not end_time:
        raise HTTPException(status_code=400, detail="Room ID, date, start time, and end time are required")

    # Kiểm tra Room
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")

    # Tìm các OrderRoom có thời gian trùng lặp
    query = (
        select(OrderRoom)
        .where(OrderRoom.room_id == room_id)
        .where(OrderRoom.date == date)
        .where(
            # Kiểm tra xem khoảng thời gian yêu cầu có giao với khoảng thời gian của OrderRoom không
            (OrderRoom.begin < end_time) & (OrderRoom.end > start_time)
        )
    )
    conflicting_order = session.exec(query).first()

    # Nếu không có OrderRoom nào trùng, phòng trống
    return not conflicting_order

# ---checkin checkout library ---

def checkin_library(session: Session, room_id:int) -> bool:
    if not room_id:
        raise HTTPException(status_code=400, detail="Room ID is required")
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")
    
    if not check_library(room):
        raise HTTPException(status_code=400, detail="Room is not a library room")
    
    if room.quantity > room.max_quantity:
        raise HTTPException(status_code=400, detail="Library is not available now")
    
    update_room(session, room_id, quantity=room.quantity+1)
    return True
def checkout_library(session: Session, room_id:int) -> bool:
    if not room_id:
        raise HTTPException(status_code=400, detail="Room ID is required")
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")
    
    if not check_library(room):
        raise HTTPException(status_code=400, detail="Room is not a library room")
    
    if room.quantity <= 0:
        raise HTTPException(status_code=400, detail="Library is not available now")
    
    update_room(session, room_id, quantity=room.quantity-1)
    return True
# --- CancelRoom ---

def create_cancel_room(
    session: Session,
    order_id: int,
    user_id: int,
    date_cancel: datetime
) -> CancelRoom:
    """
    Create a new CancelRoom entry for a canceled order.
    
    Args:
        session (Session): The database session.
        order_id (int): The ID of the OrderRoom being canceled.
        user_id (int): The ID of the user canceling the order.
        date_cancel (datetime): The date and time of cancellation.
    
    Returns:
        CancelRoom: The newly created CancelRoom object.
    
    Raises:
        HTTPException: If the OrderRoom or User is not found, or required fields are missing.
    """
    if not order_id or not user_id or not date_cancel:
        raise HTTPException(status_code=400, detail="All fields are required")

    # Kiểm tra OrderRoom
    order_room = session.get(OrderRoom, order_id)
    if not order_room:
        raise HTTPException(status_code=404, detail=f"OrderRoom with ID {order_id} not found")

    # Kiểm tra User
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    # Tạo CancelRoom
    cancel_room = CancelRoom(
        order_id=order_id,
        user_id=user_id,
        date_cancel=date_cancel
    )
    session.add(cancel_room)
    session.commit()
    session.refresh(cancel_room)
    return cancel_room

def get_cancel_room(session: Session, cancel_id: int) -> CancelRoom:
    """
    Retrieve a CancelRoom by its ID.
    
    Args:
        session (Session): The database session.
        cancel_id (int): The ID of the CancelRoom to retrieve.
    
    Returns:
        CancelRoom: The requested CancelRoom object.
    
    Raises:
        HTTPException: If the CancelRoom is not found.
    """
    cancel_room = session.get(CancelRoom, cancel_id)
    if not cancel_room:
        raise HTTPException(status_code=404, detail="CancelRoom not found")
    return cancel_room

def update_cancel_room(
    session: Session,
    cancel_id: int,
    order_id: Optional[int] = None,
    user_id: Optional[int] = None,
    date_cancel: Optional[datetime] = None
) -> CancelRoom:
    """
    Update an existing CancelRoom's attributes.
    
    Args:
        session (Session): The database session.
        cancel_id (int): The ID of the CancelRoom to update.
        order_id (Optional[int]): The new OrderRoom ID (optional).
        user_id (Optional[int]): The new user ID (optional).
        date_cancel (Optional[datetime]): The new cancellation date (optional).
    
    Returns:
        CancelRoom: The updated CancelRoom object.
    
    Raises:
        HTTPException: If the CancelRoom, OrderRoom, or User is not found.
    """
    cancel_room = session.get(CancelRoom, cancel_id)
    if not cancel_room:
        raise HTTPException(status_code=404, detail="CancelRoom not found")

    if order_id is not None:
        order_room = session.get(OrderRoom, order_id)
        if not order_room:
            raise HTTPException(status_code=404, detail=f"OrderRoom with ID {order_id} not found")
        cancel_room.order_id = order_id

    if user_id is not None:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        cancel_room.user_id = user_id

    if date_cancel is not None:
        cancel_room.date_cancel = date_cancel

    session.add(cancel_room)
    session.commit()
    session.refresh(cancel_room)
    return cancel_room

def delete_cancel_room(session: Session, cancel_id: int) -> bool:
    """
    Delete a CancelRoom by its ID.
    
    Args:
        session (Session): The database session.
        cancel_id (int): The ID of the CancelRoom to delete.
    
    Returns:
        bool: True if deletion is successful.
    
    Raises:
        HTTPException: If the CancelRoom is not found.
    """
    cancel_room = session.get(CancelRoom, cancel_id)
    if not cancel_room:
        raise HTTPException(status_code=404, detail="CancelRoom not found")
    
    session.delete(cancel_room)
    session.commit()
    return True

def get_all_cancel_rooms(session: Session) -> List[CancelRoom]:
    """
    Retrieve all CancelRoom entries.
    
    Args:
        session (Session): The database session.
    
    Returns:
        List[CancelRoom]: A list of all CancelRoom objects.
    
    Raises:
        HTTPException: If no CancelRooms are found.
    """
    cancel_rooms = session.exec(select(CancelRoom)).all()
    if not cancel_rooms:
        raise HTTPException(status_code=404, detail="No CancelRooms found")
    return cancel_rooms

def get_cancel_room_by_order_id(session: Session, order_id: int) -> CancelRoom:
    """
    Retrieve a CancelRoom by its associated OrderRoom ID.
    
    Args:
        session (Session): The database session.
        order_id (int): The ID of the associated OrderRoom.
    
    Returns:
        CancelRoom: The requested CancelRoom object.
    
    Raises:
        HTTPException: If the CancelRoom is not found.
    """
    if not order_id:
        raise HTTPException(status_code=400, detail="Order ID is required")
    cancel_room = session.exec(select(CancelRoom).where(CancelRoom.order_id == order_id)).first()
    if not cancel_room:
        raise HTTPException(status_code=404, detail="CancelRoom not found")
    return cancel_room

def check_order_cancel(session: Session, order_id: int) -> bool:
    """
    Check if an OrderRoom has been canceled.
    
    Args:
        session (Session): The database session.
        order_id (int): The ID of the OrderRoom to check.
    
    Returns:
        bool: True if the OrderRoom has been canceled, False otherwise.
    
    Raises:
        HTTPException: If the OrderRoom is not found.
    """
    order_room = session.get(OrderRoom, order_id)
    if not order_room:
        raise HTTPException(status_code=404, detail="OrderRoom not found")
    
    return order_room.cancel is not None
# --- UsedRoom ---
def create_used_room(
    session: Session,
    order_id: int,
    user_id: int,
    room_id: int,
    date: date,
    checkin: time,
    checkout: time =time(23, 59, 59)
) -> UsedRoom:
    """
    Create a new UsedRoom entry for a room usage record.
    
    Args:
        session (Session): The database session.
        order_id (int): The ID of the associated OrderRoom.
        user_id (int): The ID of the user who used the room.
        room_id (int): The ID of the room used.
        date (date): The date of usage.
        checkin (time): The check-in time.
        checkout (time): The check-out time.
    
    Returns:
        UsedRoom: The newly created UsedRoom object.
    
    Raises:
        HTTPException: If the OrderRoom, User, or Room is not found, or required fields are missing.
    """
    if not order_id or not user_id or not room_id or not date or not checkin or not checkout:
        raise HTTPException(status_code=400, detail="All fields are required")

    # Kiểm tra OrderRoom
    order_room = session.get(OrderRoom, order_id)
    if not order_room:
        raise HTTPException(status_code=404, detail=f"OrderRoom with ID {order_id} not found")

    # Kiểm tra User
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    # Kiểm tra Room
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")

    # Tạo UsedRoom
    used_room = UsedRoom(
        order_id=order_id,
        user_id=user_id,
        room_id=room_id,
        date=date,
        checkin=checkin,
        checkout=checkout
    )
    session.add(used_room)
    session.commit()
    session.refresh(used_room)
    return used_room

def get_used_room(session: Session, used_room_id: int) -> UsedRoom:
    """
    Retrieve a UsedRoom by its ID.
    
    Args:
        session (Session): The database session.
        used_room_id (int): The ID of the UsedRoom to retrieve.
    
    Returns:
        UsedRoom: The requested UsedRoom object.
    
    Raises:
        HTTPException: If the UsedRoom is not found.
    """
    used_room = session.get(UsedRoom, used_room_id)
    if not used_room:
        raise HTTPException(status_code=404, detail="UsedRoom not found")
    return used_room

def update_used_room(
    session: Session,
    used_room_id: int,
    order_id: Optional[int] = None,
    user_id: Optional[int] = None,
    room_id: Optional[int] = None,
    date: Optional[date] = None,
    checkin: Optional[time] = None,
    checkout: Optional[time] = None
) -> UsedRoom:
    """
    Update an existing UsedRoom's attributes.
    
    Args:
        session (Session): The database session.
        used_room_id (int): The ID of the UsedRoom to update.
        order_id (Optional[int]): The new OrderRoom ID (optional).
        user_id (Optional[int]): The new user ID (optional).
        room_id (Optional[int]): The new room ID (optional).
        date (Optional[date]): The new date (optional).
        checkin (Optional[time]): The new check-in time (optional).
        checkout (Optional[time]): The new check-out time (optional).
    
    Returns:
        UsedRoom: The updated UsedRoom object.
    
    Raises:
        HTTPException: If the UsedRoom, OrderRoom, User, or Room is not found.
    """
    used_room = session.get(UsedRoom, used_room_id)
    if not used_room:
        raise HTTPException(status_code=404, detail="UsedRoom not found")

    if order_id is not None:
        order_room = session.get(OrderRoom, order_id)
        if not order_room:
            raise HTTPException(status_code=404, detail=f"OrderRoom with ID {order_id} not found")
        used_room.order_id = order_id

    if user_id is not None:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        used_room.user_id = user_id

    if room_id is not None:
        room = session.get(Room, room_id)
        if not room:
            raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")
        used_room.room_id = room_id

    if date is not None:
        used_room.date = date
    if checkin is not None:
        used_room.checkin = checkin
    if checkout is not None:# Default checkout time
        used_room.checkout = checkout
    if checkin >= checkout:
        raise HTTPException(status_code=400, detail="Check-in time must be before check-out time")
    
    session.add(used_room)
    session.commit()
    session.refresh(used_room)
    return used_room

def delete_used_room(session: Session, used_room_id: int) -> bool:
    """
    Delete a UsedRoom by its ID.
    
    Args:
        session (Session): The database session.
        used_room_id (int): The ID of the UsedRoom to delete.
    
    Returns:
        bool: True if deletion is successful.
    
    Raises:
        HTTPException: If the UsedRoom is not found.
    """
    used_room = session.get(UsedRoom, used_room_id)
    if not used_room:
        raise HTTPException(status_code=404, detail="UsedRoom not found")
    
    session.delete(used_room)
    session.commit()
    return True

def get_cancel_room_by_order_id(session: Session, order_id: int) -> CancelRoom:
    """
    Retrieve a CancelRoom by its associated OrderRoom ID.
    
    Args:
        session (Session): The database session.
        order_id (int): The ID of the associated OrderRoom.
    
    Returns:
        CancelRoom: The requested CancelRoom object.
    
    Raises:
        HTTPException: If the CancelRoom is not found.
    """
    if not order_id:
        raise HTTPException(status_code=400, detail="Order ID is required")
    cancel_room = session.exec(select(CancelRoom).where(CancelRoom.order_id == order_id)).first()
    if not cancel_room:
        raise HTTPException(status_code=404, detail="CancelRoom not found")
    return cancel_room

def get_cancel_room_by_user_id(session: Session, user_id: int) -> List[CancelRoom]:
    """
    Retrieve all CancelRoom entries for a specific user.
    
    Args:
        session (Session): The database session.
        user_id (int): The ID of the user.
    
    Returns:
        List[CancelRoom]: A list of CancelRoom objects associated with the user.
    
    Raises:
        HTTPException: If no CancelRooms are found for the user.
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    cancel_rooms = session.exec(select(CancelRoom).where(CancelRoom.user_id == user_id)).all()
    if not cancel_rooms:
        raise HTTPException(status_code=404, detail="No CancelRooms found for this user")
    return cancel_rooms

def check_using_room_by_used_room_id(session: Session, used_room_id: int) -> bool:
    """
    Check if a UsedRoom entry is being used by used_room_id.
    
    Args:
        session (Session): The database session.
        used_room_id (int): The ID of the UsedRoom to check.
    
    Returns:
        bool: True if the UsedRoom has been used, False otherwise.
    
    Raises:
        HTTPException: If the UsedRoom is not found.
    """
    used_room = session.get(UsedRoom, used_room_id)
    if not used_room:
        raise HTTPException(status_code=404, detail="UsedRoom not found")
    
    if used_room.checkout is time(23, 59, 59):
        return True
    
    return False

def get_rooms_being_used(session: Session) -> List[Room]:
    """
    Retrieve all UsedRoom entries that are currently being used.
    
    Args:
        session (Session): The database session.
    
    Returns:
        List[UsedRoom]: A list of UsedRoom objects that are currently being used.
    
    Raises:
        HTTPException: If no UsedRooms are found.
    """
    used_rooms = session.exec(select(UsedRoom).where(UsedRoom.checkout == time(23, 59, 59))).all()
    if not used_rooms:
        raise HTTPException(status_code=404, detail="No UsedRooms found")
    order_id = [used_room.order_id for used_room in used_rooms]
    if not order_id:
        raise HTTPException(status_code=404, detail="No OrderRooms found")
    order_rooms = [session.get(OrderRoom, order_id) for order_id in order_id]
    if not order_rooms:
        raise HTTPException(status_code=404, detail="No OrderRooms found")
    rooms=[session.get(Room, order_room.room_id) for order_room in order_rooms]
    return rooms

def get_all_used_rooms(session: Session) -> List[UsedRoom]:
    """
    Retrieve all UsedRoom entries.
    
    Args:
        session (Session): The database session.
    
    Returns:
        List[UsedRoom]: A list of all UsedRoom objects.
    
    Raises:
        HTTPException: If no UsedRooms are found.
    """
    used_rooms = session.exec(select(UsedRoom)).all()
    if not used_rooms:
        raise HTTPException(status_code=404, detail="No UsedRooms found")
    return used_rooms