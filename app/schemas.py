from pydantic import BaseModel, Field


class PhoneAddressCreate(BaseModel):
    phone: str = Field(..., description="Phone number")
    address: str = Field(..., description="Address")


class PhoneAddressUpdate(BaseModel):
    address: str = Field(..., description="New address")


class PhoneAddressResponse(BaseModel):
    phone: str
    address: str

