"""Data schemas and Pydantic validation models for Water Potability & Monitoring."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TrackBWaterSample(BaseModel):
    """Pydantic model for Track B static physicochemical water potability sample."""

    ph: float | None = Field(
        default=None, ge=-2.0, le=16.0, description="pH level including sensor drift bounds"
    )
    Hardness: float = Field(..., ge=0.0, le=2000.0, description="Hardness in mg/L")
    Solids: float = Field(..., ge=0.0, le=200000.0, description="Total dissolved solids in ppm")
    Chloramines: float = Field(..., ge=0.0, le=50.0, description="Chloramines in ppm")
    Sulfate: float | None = Field(default=None, ge=0.0, le=2000.0, description="Sulfate in mg/L")
    Conductivity: float = Field(
        ..., ge=0.0, le=5000.0, description="Electrical conductivity in uS/cm"
    )
    Organic_carbon: float = Field(..., ge=0.0, le=100.0, description="Organic carbon in ppm")
    Trihalomethanes: float | None = Field(
        default=None, ge=0.0, le=500.0, description="Trihalomethanes in ug/L"
    )
    Turbidity: float = Field(..., ge=0.0, le=100.0, description="Turbidity in NTU")
    Potability: int | None = Field(default=None, ge=0, le=1, description="Binary potability label")

    @field_validator("Potability")
    @classmethod
    def validate_potability(cls, v: int | None) -> int | None:
        if v is not None and v not in (0, 1):
            raise ValueError("Potability must be binary {0, 1}")
        return v


class TrackASensorTelemetry(BaseModel):
    """Pydantic model for Track A temporal continuous underwater telemetry reading."""

    timestamp: datetime = Field(..., description="Timestamp in UTC ISO-8601")
    temperature: float = Field(..., ge=-5.0, le=50.0, description="Water temperature in deg C")
    dissolved_oxygen: float | None = Field(
        default=None, ge=0.0, le=25.0, description="Dissolved oxygen in mg/L"
    )
    ph: float | None = Field(default=None, ge=0.0, le=14.0, description="pH measurement")
    conductivity: float = Field(..., ge=10.0, le=2500.0, description="Conductivity in uS/cm")
    turbidity: float = Field(..., ge=0.0, le=150.0, description="Turbidity in NTU")
    pressure: float = Field(..., ge=0.0, le=600.0, description="Pressure in dbar")


# Schema definitions for column types
TRACK_B_COLUMNS = [
    "ph",
    "Hardness",
    "Solids",
    "Chloramines",
    "Sulfate",
    "Conductivity",
    "Organic_carbon",
    "Trihalomethanes",
    "Turbidity",
]

TRACK_A_COLUMNS = [
    "timestamp",
    "temperature",
    "dissolved_oxygen",
    "ph",
    "conductivity",
    "turbidity",
    "pressure",
]
