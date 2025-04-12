# app/api/crud/crud_branch_room.py
from sqlmodel import Session, select
from app.model import Branch, Building, RoomType, Room, RoomDevice
from fastapi import HTTPException
from typing import Optional, List

# --- Branch ---
def create_branch(session: Session, Branch_name: str) -> Branch:
    """
    Create a new Branch with the given name.
    
    Args:
        session (Session): The database session.
        Branch_name (str): The name of the branch to create.
    
    Returns:
        Branch: The newly created Branch object.
    
    Raises:
        HTTPException: If a branch with the same name already exists (logic currently reversed).
    """
    branch = session.exec(select(Branch).where(Branch.branch_name == Branch_name)).first()
    if branch :  # Note: Logic is reversed; should raise error if branch exists
        raise HTTPException(status_code=400, detail="Branch already exists")
   
    branch = Branch(branch_name=Branch_name)
    session.add(branch)
    session.commit()
    session.refresh(branch)

    return branch

def get_branch(session: Session, branch_id: int|None, branch_name: str|None) -> Branch:
    """
    Retrieve a Branch by its ID or name.
    
    Args:
        session (Session): The database session.
        branch_id (int | None): The ID of the branch to retrieve.
        branch_name (str | None): The name of the branch to retrieve.
    
    Returns:
        Branch: The requested Branch object.
    
    Raises:
        HTTPException: If neither ID nor name is provided, or if the branch is not found.
    """
    if branch_id is None and branch_name is None:
        raise HTTPException(status_code=400, detail="Branch ID or name must be provided")
    if branch_id:
        branch = session.get(Branch, branch_id)
        if not branch:
            raise HTTPException(status_code=404, detail="Branch not found")
        return branch
    if branch_name:
        branch = session.exec(select(Branch).where(Branch.branch_name == branch_name)).first()
        if not branch:
            raise HTTPException(status_code=404, detail="Branch not found")
        return branch

def update_branch(session: Session, branch_id: int, branch_name_new: str) -> Branch:
    """
    Update the name of an existing Branch.
    
    Args:
        session (Session): The database session.
        branch_id (int): The ID of the branch to update.
        branch_name_new (str): The new name for the branch.
    
    Returns:
        Branch: The updated Branch object.
    
    Raises:
        HTTPException: If the branch with the given ID is not found.
    """
    branch = session.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    branch.branch_name = branch_name_new
    session.add(branch)
    session.commit()
    session.refresh(branch)
    return branch

def delete_branch(session: Session, branch_id: int, branch_name: str|None) -> bool:
    """
    Delete a Branch by its ID.
    
    Args:
        session (Session): The database session.
        branch_id (int): The ID of the branch to delete.
        branch_name (str | None): Optional branch name (not used in this implementation).
    
    Returns:
        bool: True if deletion is successful.
    
    Raises:
        HTTPException: If the branch with the given ID is not found.
    """
    branch = session.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    session.delete(branch)
    session.commit()
    return True

def get_all_branches(session: Session) -> List[Branch]:
    """
    Retrieve all Branches from the database.
    
    Args:
        session (Session): The database session.
    
    Returns:
        List[Branch]: A list of all Branch objects.
    
    Raises:
        HTTPException: If no branches are found.
    """
    branches = session.exec(select(Branch)).all()
    if not branches:
        raise HTTPException(status_code=404, detail="No branches found")
    return branches

# --- Building ---
def create_building(session: Session, building_name: str, branch_id: int|None, branch_name:str|None) -> Building:
    """
    Create a new Building associated with a Branch.
    
    Args:
        session (Session): The database session.
        building_name (str): The name of the building.
        branch_id (int | None): The ID of the associated branch.
        branch_name (str | None): The name of the associated branch.
    
    Returns:
        Building: The newly created Building object.
    
    Raises:
        HTTPException: If neither branch ID nor name is provided, or if the branch is not found.
    """
    if branch_id is None and branch_name is None:
        raise HTTPException(status_code=400, detail="Branch ID or name must be provided")
    if branch_id:
        branch = session.get(Branch, branch_id)
    if branch_name:
        branch = session.exec(select(Branch).where(Branch.branch_name == branch_name)).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    building = Building(building_name=building_name, branch_id=branch.id)
    session.add(building)
    session.commit()
    session.refresh(building)
    return building

def get_building(session: Session, building_id: int|None, buiding_name:str|None) -> Building:
    """
    Retrieve a Building by its ID or name.
    
    Args:
        session (Session): The database session.
        building_id (int | None): The ID of the building to retrieve.
        buiding_name (str | None): The name of the building to retrieve (typo: should be building_name).
    
    Returns:
        Building: The requested Building object.
    
    Raises:
        HTTPException: If neither ID nor name is provided, or if the building is not found.
    """
    if building_id is None and buiding_name is None:
        raise HTTPException(status_code=400, detail="Building ID or name must be provided")
    if building_id:
        building = session.get(Building, building_id)
        if not building:
            raise HTTPException(status_code=404, detail="Building not found")
        return building
    if buiding_name:
        building = session.exec(select(Building).where(Building.building_name == buiding_name)).first()
        if not building:
            raise HTTPException(status_code=404, detail="Building not found")
    return building

def get_buildings_by_branch(session: Session, branch_id: int = None, branch_name: str = None) -> List[Building]:
    """
    Retrieve all Buildings associated with a specific Branch.
    
    Args:
        session (Session): The database session.
        branch_id (int, optional): The ID of the branch to filter by.
        branch_name (str, optional): The name of the branch to filter by.
    
    Returns:
        List[Building]: A list of Building objects associated with the branch.
    
    Raises:
        HTTPException: If the branch is not found or no buildings are found for the branch.
    """
    query = select(Building)
    if branch_id:
        query = query.where(Building.branch_id == branch_id)
    if branch_name:
        branch = session.exec(select(Branch).where(Branch.branch_name == branch_name)).first()
        if not branch:
            raise HTTPException(status_code=404, detail="Branch not found")
        query = query.where(Building.branch_id == branch.id)
    buildings = session.exec(query).all()
    if not buildings:
        raise HTTPException(status_code=404, detail="No buildings found for this branch")
    return buildings

def update_building(session: Session, building_id: int, building_name: Optional[str] = None, branch_id: Optional[int] = None) -> Building:
    """
    Update an existing Building's name or branch association.
    
    Args:
        session (Session): The database session.
        building_id (int): The ID of the building to update.
        building_name (str, optional): The new name for the building.
        branch_id (int, optional): The new branch ID for the building.
    
    Returns:
        Building: The updated Building object.
    
    Raises:
        HTTPException: If the building with the given ID is not found.
    """
    building = session.get(Building, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    if building_name:
        building.building_name = building_name
    if branch_id:
        building.branch_id = branch_id
    session.commit()
    session.refresh(building)
    return building

def delete_building(session: Session, building_id: int):
    """
    Delete a Building by its ID.
    
    Args:
        session (Session): The database session.
        building_id (int): The ID of the building to delete.
    
    Raises:
        HTTPException: If the building with the given ID is not found.
    """
    building = session.get(Building, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    session.delete(building)
    session.commit()

# --- RoomType ---
def create_room_type(session: Session, room_type: str, max_capacity: int|None) -> RoomType:
    """
    Create a new RoomType with a name and optional maximum capacity.
    
    Args:
        session (Session): The database session.
        room_type (str): The name of the room type.
        max_capacity (int | None): The maximum capacity of this room type.
    
    Returns:
        RoomType: The newly created RoomType object.
    
    Raises:
        HTTPException: If a RoomType with the same name already exists.
    """
    existing_room_type = session.exec(select(RoomType).where(RoomType.type_name == room_type)).first()
    if existing_room_type:
        raise HTTPException(status_code=400, detail="RoomType already exists")
    room_type = RoomType(type_name=room_type, max_capacity=max_capacity)
    session.add(room_type)
    session.commit()
    session.refresh(room_type)
    return room_type

def get_room_type(session: Session, type_id: int|None, room_type: str|None) -> RoomType:
    """
    Retrieve a RoomType by its ID or name.
    
    Args:
        session (Session): The database session.
        type_id (int | None): The ID of the room type to retrieve.
        room_type (str | None): The name of the room type to retrieve.
    
    Returns:
        RoomType: The requested RoomType object.
    
    Raises:
        HTTPException: If neither ID nor name is provided, or if the RoomType is not found.
    """
    if type_id is None and room_type is None:
        raise HTTPException(status_code=400, detail="RoomType ID or name must be provided")
    if type_id:
        room_type = session.get(RoomType, type_id)
        if not room_type:
            raise HTTPException(status_code=404, detail="RoomType not found")
        return room_type
    if room_type:
        room_type = session.exec(select(RoomType).where(RoomType.type_name == room_type)).first()
        if not room_type:
            raise HTTPException(status_code=404, detail="RoomType not found")
    return room_type

def delete_room_type(session: Session, type_id: int|None, room_type: str|None):
    """
    Delete a RoomType by its ID or name.
    
    Args:
        session (Session): The database session.
        type_id (int | None): The ID of the room type to delete.
        room_type (str | None): The name of the room type to delete.
    
    Raises:
        HTTPException: If neither ID nor name is provided, or if the RoomType is not found.
    """
    if type_id is None and room_type is None:
        raise HTTPException(status_code=400, detail="RoomType ID or name must be provided")
    if type_id:
        room_type = session.get(RoomType, type_id)
    else:
        room_type = session.exec(select(RoomType).where(RoomType.type_name == room_type)).first()
    if not room_type:
        raise HTTPException(status_code=404, detail="RoomType not found")
    session.delete(room_type)
    session.commit()

# --- RoomDevice ---
def create_room_device(session: Session,
                       room_id: int,
                       led: bool,
                       projector: bool,
                       air_conditioner: bool,
                       socket: int,
                       interactive_display: bool,
                       online_meeting_devicese: bool) -> RoomDevice:
    """
    Create a new RoomDevice with the specified equipment for a Room.
    
    Args:
        session (Session): The database session.
        room_id (int): The ID of the room to associate with the devices.
        led (bool): Whether the room has LED lighting.
        projector (bool): Whether the room has a projector.
        air_conditioner (bool): Whether the room has an air conditioner.
        socket (int): Number of power sockets in the room.
        interactive_display (bool): Whether the room has an interactive display.
        online_meeting_devicese (bool): Whether the room has online meeting devices (typo: should be online_meeting_devices).
    
    Returns:
        RoomDevice: The newly created RoomDevice object.
    
    Raises:
        HTTPException: If the room with the given ID is not found.
    """
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room_device = RoomDevice(
        room_id=room_id,
        led=led,
        projector=projector,
        air_conditioner=air_conditioner,
        socket=socket,
        interactive_display=interactive_display,
        online_meeting_devices=online_meeting_devicese
    )
    session.add(room_device)
    session.commit()
    session.refresh(room_device)
    return room_device

def get_room_device(session: Session, room_id: int|None, room_name: str|None) -> RoomDevice:
    """
    Retrieve a RoomDevice by its associated room's ID or name.
    
    Args:
        session (Session): The database session.
        room_id (int | None): The ID of the room to retrieve devices for.
        room_name (str | None): The name of the room to retrieve devices for.
    
    Returns:
        RoomDevice: The requested RoomDevice object.
    
    Raises:
        HTTPException: If neither room ID nor name is provided, or if the RoomDevice or Room is not found.
    """
    if room_id is None and room_name is None:
        raise HTTPException(status_code=400, detail="Room ID or name must be provided")
    if room_id:
        room_device = session.get(RoomDevice, room_id)
        if not room_device:
            raise HTTPException(status_code=404, detail="RoomDevice not found")
        return room_device
    if room_name:
        room = session.exec(select(Room).where(Room.room_name == room_name)).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        room_id = room.id
        room_device = session.exec(select(RoomDevice).where(RoomDevice.room_id == room_id)).first()
        if not room_device:
            raise HTTPException(status_code=404, detail="RoomDevice not found")
        return room_device

def update_room_device(
    session: Session,
    room_id: int | None = None,
    room_name: str | None = None,
    led: Optional[bool] = None,
    projector: Optional[bool] = None,
    air_conditioner: Optional[bool] = None,
    socket: Optional[int] = None,
    interactive_display: Optional[bool] = None,
    online_meeting_devices: Optional[bool] = None
) -> RoomDevice:
    """
    Update an existing RoomDevice based on room_id or room_name.
    Only provided fields will be updated.
    
    Args:
        session (Session): The database session.
        room_id (int | None): The ID of the room to update devices for.
        room_name (str | None): The name of the room to update devices for.
        led (Optional[bool]): New value for LED lighting (optional).
        projector (Optional[bool]): New value for projector (optional).
        air_conditioner (Optional[bool]): New value for air conditioner (optional).
        socket (Optional[int]): New number of sockets (optional).
        interactive_display (Optional[bool]): New value for interactive display (optional).
        online_meeting_devices (Optional[bool]): New value for online meeting devices (optional).
    
    Returns:
        RoomDevice: The updated RoomDevice object.
    
    Raises:
        HTTPException: If neither room ID nor name is provided, or if the RoomDevice or Room is not found.
    """
    if room_id is None and room_name is None:
        raise HTTPException(status_code=400, detail="Room ID or name must be provided")
    if room_id:
        room_device = session.exec(select(RoomDevice).where(RoomDevice.room_id == room_id)).first()
        if not room_device:
            raise HTTPException(status_code=404, detail="RoomDevice not found")
    if room_name:
        room = session.exec(select(Room).where(Room.no_room == room_name)).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        room_device = session.exec(select(RoomDevice).where(RoomDevice.room_id == room.id)).first()
        if not room_device:
            raise HTTPException(status_code=404, detail="RoomDevice not found")
    if led is not None:
        room_device.led = led
    if projector is not None:
        room_device.projector = projector
    if air_conditioner is not None:
        room_device.air_conditioner = air_conditioner
    if socket is not None:
        room_device.socket = socket
    if interactive_display is not None:
        room_device.interactive_display = interactive_display
    if online_meeting_devices is not None:
        room_device.online_meeting_devices = online_meeting_devices
    session.add(room_device)
    session.commit()
    session.refresh(room_device)
    return room_device

def delete_room_device(session: Session, room_id: int | None = None, room_name: str | None = None) -> bool:
    """
    Delete a RoomDevice based on its associated room's ID or name.
    
    Args:
        session (Session): The database session.
        room_id (int | None): The ID of the room whose devices will be deleted.
        room_name (str | None): The name of the room whose devices will be deleted.
    
    Returns:
        bool: True if deletion is successful.
    
    Raises:
        HTTPException: If neither room ID nor name is provided, or if the RoomDevice or Room is not found.
    """
    if room_id is None and room_name is None:
        raise HTTPException(status_code=400, detail="Room ID or name must be provided")

    # Lấy room_device dựa trên room_id hoặc room_name
    if room_id:
        room_device = session.exec(select(RoomDevice).where(RoomDevice.room_id == room_id)).first()
        if not room_device:
            raise HTTPException(status_code=404, detail="RoomDevice not found")
    if room_name:
        room = session.exec(select(Room).where(Room.no_room == room_name)).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        room_device = session.exec(select(RoomDevice).where(RoomDevice.room_id == room.id)).first()
        if not room_device:
            raise HTTPException(status_code=404, detail="RoomDevice not found")

    # Xóa RoomDevice
    session.delete(room_device)
    session.commit()
    return True
# --- Room ---
def check_library(session: Session, room_id: int) -> bool:
    if not room_id:
        raise HTTPException(status_code=400, detail="Room ID is required")
    room = session.get(Room, room_id)
    type_id = room.type_id
    type= session.get(RoomType, type_id)
    return type.type_name =="Library"

def create_room(
    session: Session,
    room_name: str,
    branch_id: int,
    building_id: int,
    type_id: int,
    capacity: int|None,
) -> Room:
    """
    Create a new Room with the specified attributes.
    
    Args:
        session (Session): The database session.
        room_name (str): The name of the room.
        branch_id (int): The ID of the associated branch.
        building_id (int): The ID of the associated building.
        type_id (int): The ID of the associated room type.
        capacity (int): The maximum capacity of the room.
    
    Returns:
        Room: The newly created Room object.
    
    Raises:
        HTTPException: If required fields are missing, the room already exists, or related entities are not found.
    """
    if not room_name or not branch_id or not building_id or not type_id:
        raise HTTPException(status_code=400, detail="Room name, Branch ID, Building ID, and Type ID are required")
    exist_room = session.exec(select(Room).where(Room.room_name == room_name)).first()
    if exist_room:
        raise HTTPException(status_code=400, detail="Room already exists")
    if not session.get(Branch, branch_id):
        raise HTTPException(status_code=404, detail=f"Branch with ID {branch_id} not found")
    if not session.get(Building, building_id):
        raise HTTPException(status_code=404, detail=f"Building with ID {building_id} not found")
    if not session.get(RoomType, type_id):
        raise HTTPException(status_code=404, detail=f"RoomType with ID {type_id} not found")
    
    check_lib= session.get(RoomType,type_id)
    if check_lib.type_name == "Library" and capacity == 0 :
        raise HTTPException(status_code=400, detail="Library room must have a capacity greater than 0")
    

    room = Room(
        no_room=room_name,
        branch_id=branch_id,
        building_id=building_id,
        type_id=type_id,
        max_quantity=capacity if capacity else 0,
        quantity=0,
    )
    session.add(room)
    session.commit()
    session.refresh(room)
    return room

def get_room(session: Session, room_id: int|None, no_room: str|None) -> Room:
    """
    Retrieve a Room by its ID.
    
    Args:
        session (Session): The database session.
        room_id (int): The ID of the room to retrieve.
    
    Returns:
        Room: The requested Room object.
    
    Raises:
        HTTPException: If the room with the given ID is not found.
    """
    if room_id is None and no_room is None:
        raise HTTPException(status_code=400, detail="Room ID or name must be provided")
    if room_id:
        room = session.get(Room, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return room
    if no_room:
        room = session.exec(select(Room).where(Room.room_name == no_room)).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return room

def update_room(
    session: Session,
    room_id: int,
    room_name: Optional[str] = None,
    branch_id: Optional[int] = None,
    building_id: Optional[int] = None,
    type_id: Optional[int] = None,
    capacity: Optional[int] = None,
) -> Room:
    """
    Update an existing Room's attributes.
    
    Args:
        session (Session): The database session.
        room_id (int): The ID of the room to update.
        room_name (Optional[str]): The new name for the room (optional).
        branch_id (Optional[int]): The new branch ID for the room (optional).
        building_id (Optional[int]): The new building ID for the room (optional).
        type_id (Optional[int]): The new type ID for the room (optional).
        capacity (Optional[int]): The new capacity for the room (optional).
    
    Returns:
        Room: The updated Room object.
    
    Raises:
        HTTPException: If the room ID is not provided or the room is not found.
    """
    if not room_id:
        raise HTTPException(status_code=400, detail="Room ID is required")
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room_name:
        room.room_name = room_name
    if branch_id:
        room.branch_id = branch_id
    if building_id:
        room.building_id = building_id
    if type_id:
        room.type_id = type_id
    if capacity is not None:
        room.capacity = capacity
    session.commit()
    session.refresh(room)
    return room

def delete_room(session: Session, room_id: int) -> bool:
    """
    Delete a Room by its ID.
    
    Args:
        session (Session): The database session.
        room_id (int): The ID of the room to delete.
    
    Returns:
        bool: True if deletion is successful.
    
    Raises:
        HTTPException: If the room with the given ID is not found.
    """
    room = session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Xóa Room
    session.delete(room)
    session.commit()
    return True

def filter_rooms(
    session: Session,
    branch_id: Optional[int] = None,
    branch_name: Optional[str] = None,
    building_id: Optional[int] = None,
    building_name: Optional[str] = None,
    type_id: Optional[int] = None,
    type_name: Optional[str] = None,
    page: int = 1,
    limit: int = 0
) -> List[Room]:
    """
    Filter Rooms based on branch, building, or room type, with pagination support.
    If limit is 0, return all matching rooms.
    
    Args:
        session (Session): The database session.
        branch_id (Optional[int]): Filter by branch ID.
        branch_name (Optional[str]): Filter by branch name.
        building_id (Optional[int]): Filter by building ID.
        building_name (Optional[str]): Filter by building name.
        type_id (Optional[int]): Filter by room type ID.
        type_name (Optional[str]): Filter by room type name.
        page (int): Page number for pagination (default: 1).
        limit (int): Number of items per page (default: 0, meaning no limit).
    
    Returns:
        List[Room]: A list of Room objects matching the filters.
    
    Raises:
        HTTPException: If no rooms match the filters or related entities are not found.
    """
    query = select(Room)
    if branch_id:
        query = query.where(Room.branch_id == branch_id)
    if branch_name:
        branch = session.exec(select(Branch).where(Branch.branch_name == branch_name)).first()
        if not branch:
            raise HTTPException(status_code=404, detail="Branch not found")
        query = query.where(Room.branch_id == branch.id)
    if building_id:
        query = query.where(Room.building_id == building_id)
    if building_name:
        building = session.exec(select(Building).where(Building.building_name == building_name)).first()
        if not building:
            raise HTTPException(status_code=404, detail="Building not found")
        query = query.where(Room.building_id == building.id)
    if type_id:
        query = query.where(Room.type_id == type_id)
    if type_name:
        room_type = session.exec(select(RoomType).where(RoomType.type_name == type_name)).first()
        if not room_type:
            raise HTTPException(status_code=404, detail="RoomType not found")
        query = query.where(Room.type_id == room_type.id)
    if limit == 0:
        rooms = session.exec(query).all()
    else:
        offset = (page - 1) * limit
        rooms = session.exec(query.offset(offset).limit(limit)).all()
    if not rooms:
        raise HTTPException(status_code=404, detail="No rooms found with the given filters")
    return rooms