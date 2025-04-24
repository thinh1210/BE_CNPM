from fastapi import APIRouter,Query, Depends, HTTPException, status
from math import ceil
from sqlmodel import Session
from app.schemas.admin import getUser
from app.schemas.user import User_Short
from app.schemas.metadata import Metadata
from app.schemas.admin import getUser,changeUserStatus
from app.schemas.metadata import Metadata
from app.schemas.room import Branch_In, Buiding_In, TypeRoom_In,Room_with_device_In, RoomIn, RoomDevice, reponse

from app.crud.crud_user import get_all_user,change_user_status
from typing import List
from app.api.dependencies import SessionDep
from app.model import Room, Branch, Building, RoomType
from app.crud.crud_room import create_branch, get_branch, update_branch, delete_branch, get_all_branches
from app.crud.crud_room import create_building, get_building, update_building, delete_building, get_buildings_by_branch
from app.crud.crud_room import create_room_type, get_room_type,get_all_rt, delete_room_type
from app.crud.crud_room import create_room, get_room, update_room, delete_room, delete_room_device,filter_rooms
from app.crud.crud_room import create_room_device, get_room_device, update_room_device, delete_room_device
#from app.crud.crud_room import create_branch, create_building, create_room_type, create_room, 

router = APIRouter()

# router.include_router(
#     router=APIRouter(),
#     dependencies=Depends(isAdmin),
# )

# --- User ---
@router.get("/all_user", response_model=getUser)
def get_all_user_data(
    session: SessionDep,
    page: int = Query(default=1, ge=1, description="Page number (starting from 1)"),  # Thêm query param page
    limit: int = Query(default=10, ge=1, le=100, description="Number of users per page")  # Thêm limit nếu cần
):
    '''
    Get all users (username, MSSV, lastname, firstname, email, isActive) with pagination.

    Args:
        page: Page number to retrieve (default: 1).
        limit: Number of users per page (default: 10, max: 100).
    '''
    # Tạo metadata với page và limit
    metadata = Metadata(page=page, perpage=limit)

    # Gọi hàm CRUD để lấy danh sách user và metadata
    users, metadata = get_all_user(session, metadata)
    if not users:
        raise HTTPException(status_code=404, detail="No user found")

    # Chuyển đổi danh sách user sang User_Short
    users_out: List[User_Short] = [
        User_Short(
            username=user.username,
            MSSV=user.MSSV,
            lastname=user.lastname,
            firstname=user.firstname,
            email=user.email,
            isActive=user.isActive
        )
        for user in users
    ]

    # Trả về response với cấu trúc mong muốn
    return {
        "msg": "Get users successfully",
        "data": users_out,
        "metadata": metadata
    }


@router.put("/change_user_status/{username}", response_model=changeUserStatus)
def admin_change_user_status(username: str, isActive: bool, session: SessionDep):
    '''
    Change user status (isActive)
    
    '''
    user= change_user_status(session, username, isActive)
    if not user:
        raise HTTPException(status_code=404, detail="Have something wrong")
    return{
        "msg": "Change user status successfully",
        "data": user
    }



# --- Branch ---

@router.post("/branch", response_model=reponse)
def create_branch_data(data: Branch_In, session: SessionDep):
    '''
    Create a new branch.

    Args:
        data: Branch data to create.
    '''
    branch = create_branch(session, Branch_name= data.Branch_name)
    if not branch:
        raise HTTPException(status_code=400, detail="Branch already exists")
    return {
        "msg": "Create branch successfully",
        "data": None
    }

@router.get("/all_branch", response_model=reponse)
def get_all_branch_data(session: SessionDep):
    '''
    Get all branches.

    '''
    branches = get_all_branches(session)
    if not branches:
        raise HTTPException(status_code=404, detail="No branch found")
    return {
        "msg": "Get all branches successfully",
        "data": branches
    }

@router.put("/branch/{branch_id}", response_model=reponse)
def update_branch_data(branch_id: int, data: Branch_In, session: SessionDep):
    '''
    Update a branch.

    Args:
        branch_id: ID of the branch to update.
        data: Updated branch data.
    '''
    branch = update_branch(session, branch_id, data.Branch_name)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return {
        "msg": "Update branch successfully",
        "data": branch
    }

@router.delete("/branch/{branch_id}", response_model=reponse)
def delete_branch_data(branch_id: int, session: SessionDep):
    '''
    Delete a branch.

    Args:
        branch_id: ID of the branch to delete.
    '''
    check_del = delete_branch(session, branch_id, None)
    if not check_del:
        raise HTTPException(status_code=404, detail="Branch not found")
    return {
        "msg": "Delete branch successfully",
        "data": None
    }

@router.get("/branch/{branch_id}", response_model=reponse)
def get_branch_data(branch_id: int, session: SessionDep):
    '''
    Get a branch by ID.

    Args:
        branch_id: ID of the branch to retrieve.
    '''
    branch = get_branch(session, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return {
        "msg": "Get branch successfully",
        "data": branch
    }
# --- Building ---

@router.post("/building", response_model=reponse)
def create_building_data(data: Buiding_In, session: SessionDep):
    '''
    Create a new building.

    Args:
        data: Building data to create.
    '''
    building = create_building(session, name_building=data.name_building, id_branch=data.id_branch)
    if not building:
        raise HTTPException(status_code=400, detail="Building already exists")
    return {
        "msg": "Create building successfully",
        "data": None
    }

@router.get("/all_building1", response_model=reponse)
def get_all_building_data(session: SessionDep, branch_id: int):
    '''
    Get all buildings by branch ID.

    Args:
        branch_id: ID of the branch to filter buildings.
    '''
    buildings = get_buildings_by_branch(session, branch_id, None)
    if not buildings:
        raise HTTPException(status_code=404, detail="No building found")
    return {
        "msg": "Get all buildings successfully",
        "data": buildings
    }

# @router.get("/all_building2", response_model=reponse)
# def get_all_building_data_by_branch_name(session: SessionDep, branch_name: str):
#     '''
#     Get all buildings by branch name.

#     Args:
#         branch_name: Name of the branch to filter buildings.
#     '''
#     buildings = get_buildings_by_branch(session, None, branch_name)
#     if not buildings:
#         raise HTTPException(status_code=404, detail="No building found")
#     return {
#         "msg": "Get all buildings successfully",
#         "data": buildings
#     }


@router.put("/building/{building_id}", response_model=reponse)
def update_building(building_id: int, data: Buiding_In, session: SessionDep):
    '''
    Update a building.

    Args:
        building_id: ID of the building to update.
        data: Updated building data.
    '''
    building = update_building(session, building_id, data.name_building, data.id_branch)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return {
        "msg": "Update building successfully",
        "data": building
    }

@router.delete("/building/{building_id}", response_model=reponse)
def delete_building(building_id: int, session: SessionDep):
    '''
    Delete a building.

    Args:
        building_id: ID of the building to delete.
    '''
    check_del = delete_building(session, building_id, None)
    if not check_del:
        raise HTTPException(status_code=404, detail="Building not found")
    return {
        "msg": "Delete building successfully",
        "data": None
    }

# --- RoomType ---
@router.post("/room_type", response_model=reponse)
def creat_room_type(data: TypeRoom_In, session: SessionDep):
    '''
    Create a new room type.

    Args:
        data: Room type data to create.
    '''
    room_type = create_room_type(session, name_type_room=data.name_type_room)
    if not room_type:
        raise HTTPException(status_code=400, detail="Cannot create room type")
    return {
        "msg": "Create room type successfully",
        "data": None
    }

@router.get("/all_room_type", response_model=reponse)
def get_all_room_type(session: SessionDep):
    '''
    Get all room types.

    '''
    room_types = get_all_rt(session)
    if not room_types:
        raise HTTPException(status_code=404, detail="No room type found")
    return {
        "msg": "Get all room types successfully",
        "data": room_types
    }

@router.put("/room_type/{room_type_id}", response_model=reponse)
def update_room_type(room_type_id: int, data: TypeRoom_In, session: SessionDep):
    '''
    Update a room type.

    Args:
        room_type_id: ID of the room type to update.
        data: Updated room type data.
    '''
    room_type = update_room_type(session, room_type_id, data.name_type_room)
    if not room_type:
        raise HTTPException(status_code=404, detail="Room type not found")
    return {
        "msg": "Update room type successfully",
        "data": room_type
    }

@router.delete("/room_type/{room_type_id}", response_model=reponse)
def delete_room_type(room_type_id: int, session: SessionDep):
    '''
    Delete a room type.

    Args:
        room_type_id: ID of the room type to delete.
    '''
    check_del = delete_room_type(session, room_type_id)
    if not check_del:
        raise HTTPException(status_code=404, detail="Room type not found")
    return {
        "msg": "Delete room type successfully",
        "data": None
    }

# --- Room ---

@router.post("/room_and_device", response_model=reponse)
def create_room_and_device(data: Room_with_device_In, session: SessionDep):
    '''
    Create a new room and its devices.

    Args:
        data: Room data to create.
    '''
    room = create_room(session,
                    data.name_room, 
                    branch_id=data.id_branch, 
                    building_id=data.id_building, 
                    type_id=data.id_type_room, 
                    capacity=data.max_quantity)
    if not room:
        raise HTTPException(status_code=400, detail="Cannot create room")
    
    device = create_room_device(session, room.id, data.led, data.projector, data.air_conditioner, data.socket, data.interactive_display, data.online_meeting_devices)
    if not device:
        raise HTTPException(status_code=400, detail="Cannot create room device")
    
    # Create room device
    # room_device = create_room_device(session, room.id, data.led, data.projector, data.air_conditioner, data.socket, data.interactive_display, data.online_meeting_devices)
    
    return {
        "msg": "Create room successfully",
        "data": None
    }

@router.get("/all_room", response_model=reponse)
def get_all_room_data(session: SessionDep,
                     branch_id: int = Query(default=None),
                     building_id: int = Query(default=None), 
                     room_type_id: int = Query(default=None),
                     page: int = Query(default=1, ge=1, description="Page number (starting from 1)"),  # Thêm query param page
                     limit: int = Query(default=10, ge=0, le=100, description="Number of users per page")  # Thêm limit nếu cần
                     ):
    '''
    Get all rooms with optional filters.
    If want to get all rooms, limit =0
    Args:
        branch_id: ID of the branch to filter rooms (optional).
        building_id: ID of the building to filter rooms (optional).
        room_type_id: ID of the room type to filter rooms (optional).
    '''
    # print("branch_id", branch_id)
    # print("building_id", building_id)
    
    rooms =filter_rooms(session, 
                        branch_id=  branch_id,
                        building_id= building_id,
                        type_id= room_type_id,
                        page=page,
                        limit=limit
                        )
    # rooms = get_room(session, branch_id, building_id, room_type_id)


    
    return {
        "msg": "Get all rooms successfully",
        "data": rooms,
        "metadata": {
            "page": page,
            "perpage": limit,
            "total": len(rooms),
            "total_page": ceil(len(rooms) / limit) if limit > 0 else 1
        }
    }

@router.get("/room1/{room_id}", response_model=reponse)
def get_room_data(room_id: int, session: SessionDep):
    '''
    Get a room by ID.

    Args:
        room_id: ID of the room to retrieve.
    '''
    room = get_room(session, room_id, None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "msg": "Get room successfully",
        "data": room
    }

# @router.get("/room2/{room_name}", response_model=reponse)
# def get_room_data_by_name(room_name: str, session: SessionDep):
#     '''
#     Get a room by name.

#     Args:
#         room_name: Name of the room to retrieve.
#     '''
#     room = get_room(session, None, room_name)
#     if not room:
#         raise HTTPException(status_code=404, detail="Room not found")
#     return {
#         "msg": "Get room successfully",
#         "data": room
#     }

@router.put("/room/{room_id}", response_model=reponse)
def update_room_data(room_id: int, data: RoomIn, session: SessionDep):
    '''
    Update a room.

    Args:
        room_id: ID of the room to update.
        data: Updated room data.
    '''
    room = update_room(session, room_id, data.name_room, data.id_branch, data.id_building, data.id_type_room, data.max_quantity, data.quantity)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "msg": "Update room successfully",
        "data": room
    }

@router.put("/room_device/{room_id}", response_model=reponse)
def update_room_device_data(room_id: int, data: RoomDevice, session: SessionDep):
    '''
    Update a room device.

    Args:
        room_id: ID of the room to update.
        data: Updated room device data.
    '''
    device = update_room_device(session, room_id, data.led, data.projector, data.air_conditioner, data.socket, data.interactive_display, data.online_meeting_devices)
    if not device:
        raise HTTPException(status_code=404, detail="Room device not found")
    return {
        "msg": "Update room device successfully",
        "data": device
    }

@router.delete("/room/{room_id}", response_model=reponse)
def delete_room_data(room_id: int, session: SessionDep):
    '''
    Delete a room.

    Args:
        room_id: ID of the room to delete.
    '''
    check_del_device= delete_room_device(session, room_id)
    check_del = delete_room(session, room_id, None)
    if not check_del_device:
        raise HTTPException(status_code=404, detail="Cannot delete room device")
    if not check_del:
        raise HTTPException(status_code=404, detail="Cannot delete room")
    return {
        "msg": "Delete room successfully",
        "data": None
    }

