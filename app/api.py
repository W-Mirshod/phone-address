from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis
from app.schemas import PhoneAddressCreate, PhoneAddressUpdate, PhoneAddressResponse
from app.deps import get_redis

router = APIRouter(prefix="/phones", tags=["phones"])


@router.get(
    "/{phone}",
    response_model=PhoneAddressResponse,
    status_code=status.HTTP_200_OK,
    summary="Get address by phone",
    description="Fetch the address associated with the given phone number.",
    responses={
        404: {"description": "The phone number is not present in storage."},
    },
)
async def get_address(phone: str, redis: Redis = Depends(get_redis)):
    address = await redis.get(phone)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone number not found"
        )
    return PhoneAddressResponse(phone=phone, address=address)


@router.post(
    "",
    response_model=PhoneAddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create phone-address pair",
    description="Persist a new phone number with its address. Fails if the phone already exists.",
    responses={
        201: {"description": "Phone number and address created."},
        409: {"description": "Phone number already exists."},
    },
)
async def create_phone_address(
    data: PhoneAddressCreate,
    redis: Redis = Depends(get_redis)
):
    exists = await redis.exists(data.phone)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already exists"
        )
    
    await redis.set(data.phone, data.address)
    return PhoneAddressResponse(phone=data.phone, address=data.address)


@router.put(
    "/{phone}",
    response_model=PhoneAddressResponse,
    status_code=status.HTTP_200_OK,
    summary="Update address by phone",
    description="Replace the stored address for an existing phone number.",
    responses={
        200: {"description": "Address updated."},
        404: {"description": "Phone number not found."},
    },
)
async def update_address(
    phone: str,
    data: PhoneAddressUpdate,
    redis: Redis = Depends(get_redis)
):
    exists = await redis.exists(phone)
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone number not found"
        )
    
    await redis.set(phone, data.address)
    return PhoneAddressResponse(phone=phone, address=data.address)


@router.delete(
    "/{phone}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete phone-address pair",
    description="Remove the phone number and its address from storage.",
    responses={
        204: {"description": "Phone number deleted."},
        404: {"description": "Phone number not found."},
    },
)
async def delete_phone_address(phone: str, redis: Redis = Depends(get_redis)):
    deleted = await redis.delete(phone)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone number not found"
        )

