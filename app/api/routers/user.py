from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.schemas.user import  UserOut_json 
from app.api.dependencies import SessionDep,get_current_user,CurrentUser,isUser
from app.schemas.user import  UserOut_json
from app.schemas.order import OrderIn, CancelIn, CheckIn, responseorder
from app.model import User
from app.cores.security import create_access_token, verify_key
from datetime import datetime, date, time,timedelta

from app.crud.crud_order import create_order_room,check_room_availability
from app.crud.crud_room import filter_rooms


router = APIRouter()
# router.include_router(
#     router=APIRouter(),
#     dependencies=Depends(isUser),
# )
# ---- infor user ----
@router.get("/me", response_model=UserOut_json)
def read_users_me(current_user:CurrentUser ):
    return{
        "message": "Get user successfully",
        "data": current_user
    }

#---- search room ----
@router.get("/searchroom", response_model=responseorder)
def filter_room(
    session: SessionDep,
    building_id: int = Query(...,ge=0, title="Building ID", description="ID of the building"),
    branch_id: int = Query(..., ge=0, title="Branch ID", description="ID of the branch"),
    type_id: int = Query(...,ge=0, title="Type ID", description="ID of the type"),
    date_order: int = Query(...,ge=1,le=31, title="Date", description="Date of the month"),
    month_order: int = Query(...,ge=1,le=12, title="Month", description="Month of the year"),
    year_order: int = Query(...,ge=2024, title="Year", description="Year"),
    start_time: int = Query(...,ge=7,le=20, title="Start time", description="Start time of the room"),
    end_time: int = Query(...,ge=7,le=20, title="End time", description="End time of the room"),
    limitation: int = Query(10, ge=1, le=20, title="Limit", description="Limit of the number of rooms")
    ):


    # Current datetime
    now = datetime.now()
    # Create a date object for order date
    order_date = date(year_order, month_order, date_order)
    # Create a time object for start time
    start = time(hour=start_time)

    # Combine date and time for start_order
    start_order = datetime(year_order, month_order, date_order, start_time)

    # Create a time object for end time
    end = time(hour=end_time)
    #Validate start and end times
    if start > end:
        raise HTTPException(status_code=400, detail="Start time must be before end time")

    # Check for past bookings
    if start_order < now:
        raise HTTPException(status_code=400, detail=f"{now}, {start_order} Cannot book in the past")

    # Check for bookings too close to now
    if now < start_order < now + timedelta(minutes=50):
        raise HTTPException(status_code=400, detail=f"{now}, {start_order} Your time is not valid")
    

    rooms= filter_rooms(session, branch_id=branch_id, building_id=building_id, type_id=type_id)
    if not rooms:
        raise HTTPException(status_code=404, detail="No rooms found")
    available_rooms = []

    for room in rooms:
        if check_room_availability(session, room.id, order_date, start, end):
            available_rooms.append(room)
            if len(available_rooms) >= limitation:
                break
    if not available_rooms:
        raise HTTPException(status_code=404, detail="No available rooms found")
    return {
        "message": "Search room successfully",
        "data": available_rooms
    }
    
    
#---- order room ----
@router.post("/orderroom", response_model=responseorder)
def order_room(data: OrderIn, current_user: CurrentUser, session: SessionDep):
    user = current_user
    time_start = datetime(data.year, data.month, data.date, data.start_time)
    time_end = datetime(data.year, data.month, data.date, data.end_time)
    if time_start > time_end:
        raise HTTPException(status_code=400, detail="Start time must be before end time")
    
    now = datetime.now()
    if time_start-now < timedelta(minutes=50):
        raise HTTPException(status_code=400, detail="You can only order a room 50 minutes in advance")
        
    
    order_room = create_order_room( session, 
                                   room_id=data.room_id,
                                    user_id=user.id,
                                    date=date(data.year,data.month, data.date),
                                    begin=time(data.start_time),
                                    end=time(data.end_time))
    
    return{
        "message": "Order room successfully",
        "data": order_room
    }