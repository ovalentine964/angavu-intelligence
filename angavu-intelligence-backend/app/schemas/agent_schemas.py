"""
PydanticAI Type-Safe Validation for Angavu Intelligence Financial Transactions.

WHY: Financial transactions need strict validation. PydanticAI ensures agent
inputs/outputs are type-safe, preventing malformed data from reaching M-Pesa
integrations or corrupting worker records.

HOW: Pydantic v2 models with strict validation, custom validators for
African financial contexts (M-Pesa, mobile money, informal market pricing),
and JSON Schema generation for API documentation.

WHERE: angavu-intelligence-backend/app/schemas/agent_schemas.py

Pattern borrowed from: PydanticAI (open-source, Pydantic team)
Alignment: NIST AI RMF Layer 1 — Transaction Safety
"""

from __future__ import annotations

import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ── Enums ────────────────────────────────────────────────────


class Currency(str, Enum):
    """Currencies supported in East African informal markets."""
    KES = "KES"  # Kenyan Shilling
    UGX = "UGX"  # Ugandan Shilling
    TZS = "TZS"  # Tanzanian Shilling
    ETB = "ETB"  # Ethiopian Birr
    NGN = "NGN"  # Nigerian Naira
    GHS = "GHS"  # Ghanaian Cedi
    USD = "USD"  # US Dollar (for cross-border)


class TransactionType(str, Enum):
    """Types of financial transactions in informal markets."""
    PAYMENT = "payment"              # M-Pesa / mobile money payment
    TRANSFER = "transfer"            # P2P transfer
    CREDIT_DISBURSEMENT = "credit_disbursement"  # Loan disbursement
    CREDIT_REPAYMENT = "credit_repayment"        # Loan repayment
    PURCHASE = "purchase"            # Goods/services purchase
    SALE = "sale"                    # Revenue from sale
    SUPPLIER_PAYMENT = "supplier_payment"  # Inventory restocking
    SUBSCRIPTION = "subscription"    # Angavu service fee


class TransactionStatus(str, Enum):
    """Transaction lifecycle states."""
    PENDING = "pending"
    VALIDATED = "validated"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REVERSED = "reversed"


class CreditStatus(str, Enum):
    """Credit assessment outcomes."""
    APPROVED = "approved"
    CONDITIONALLY_APPROVED = "conditionally_approved"
    DENIED = "denied"
    PENDING_REVIEW = "pending_review"
    INSUFFICIENT_HISTORY = "insufficient_history"


class WorkerType(str, Enum):
    """Informal worker categories — from Swarm G research."""
    BODA_BODA = "boda_boda"          # Motorcycle taxi
    MAMA_MBOGA = "mama_mboga"        # Vegetable vendor
    FUNDI = "fundi"                   # Tradesperson/mechanic
    HAWKER = "hawker"                 # Street vendor
    MITI_OPERATOR = "miti_operator"   # Mobile money agent
    MKOPO_AGENT = "mkopo_agent"      # Micro-lender
    MJENGA = "mjenga"                # Construction worker
    SALONIST = "salonist"            # Hair salon owner
    FOOD_VENDOR = "food_vendor"      # Food seller
    GENERAL = "general"              # Unclassified


class MarketCondition(str, Enum):
    """Market conditions affecting pricing."""
    BULL = "bull"        # Prices rising
    BEAR = "bear"        # Prices falling
    STABLE = "stable"    # Prices steady
    VOLATILE = "volatile"  # High price swings
    SEASONAL = "seasonal"  # Seasonal patterns


# ── Transaction Schemas ──────────────────────────────────────


class TransactionInput(BaseModel):
    """
    Input schema for financial transaction processing.

    Every field is validated. No malformed data passes through.
    Designed for M-Pesa, Airtel Money, and cash transactions
    in East African informal markets.
    """
    model_config = {"strict": True, "json_schema_extra": {
        "description": "Validated transaction input for Angavu financial agent"
    }}

    worker_id: str = Field(
        ...,
        min_length=8,
        max_length=64,
        description="Unique worker identifier (hashed phone number)"
    )
    transaction_type: TransactionType = Field(
        ...,
        description="Type of financial transaction"
    )
    amount: Decimal = Field(
        ...,
        gt=Decimal("0"),
        le=Decimal("10000000"),  # 10M KES max
        description="Transaction amount in specified currency"
    )
    currency: Currency = Field(
        default=Currency.KES,
        description="Transaction currency"
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Human-readable transaction description"
    )
    counterparty_id: Optional[str] = Field(
        None,
        max_length=64,
        description="Other party's worker ID (if P2P)"
    )
    mpesa_receipt: Optional[str] = Field(
        None,
        pattern=r"^[A-Z0-9]{10}$",
        description="M-Pesa transaction receipt code (10 alphanumeric)"
    )
    category: Optional[str] = Field(
        None,
        max_length=100,
        description="Transaction category (e.g., 'tomatoes', 'transport', 'rent')"
    )
    market_id: Optional[str] = Field(
        None,
        max_length=64,
        description="Market where transaction occurred"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional transaction metadata"
    )

    @field_validator("amount")
    @classmethod
    def validate_amount_precision(cls, v: Decimal) -> Decimal:
        """Ensure amount has at most 2 decimal places."""
        if v.as_tuple().exponent < -2:
            raise ValueError("Amount must have at most 2 decimal places")
        return v

    @field_validator("worker_id")
    @classmethod
    def validate_worker_id_format(cls, v: str) -> str:
        """Worker ID must be alphanumeric with optional hyphens/underscores."""
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Worker ID must be alphanumeric (hyphens/underscores allowed)")
        return v


class TransactionOutput(BaseModel):
    """
    Output schema for processed financial transactions.

    Every field is validated before returning to the worker.
    Includes audit trail fields for NIST AI RMF compliance.
    """
    model_config = {"strict": True}

    transaction_id: str = Field(
        ...,
        description="Unique transaction identifier (UUID)"
    )
    status: TransactionStatus = Field(
        ...,
        description="Transaction processing status"
    )
    amount: Decimal = Field(
        ...,
        description="Confirmed transaction amount"
    )
    currency: Currency = Field(
        ...,
        description="Transaction currency"
    )
    fee: Decimal = Field(
        default=Decimal("0"),
        ge=Decimal("0"),
        description="Transaction fee charged"
    )
    new_balance: Optional[Decimal] = Field(
        None,
        description="Worker's balance after transaction"
    )
    mpesa_receipt: Optional[str] = Field(
        None,
        description="M-Pesa receipt code (populated on completion)"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Transaction completion timestamp (UTC)"
    )
    agent_id: str = Field(
        ...,
        description="ID of the agent that processed this transaction"
    )
    verification_hash: Optional[str] = Field(
        None,
        description="PQC signature hash for transaction integrity (ML-DSA)"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error details if status is FAILED"
    )
    audit_trail: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Ordered list of processing steps for auditability"
    )


# ── Credit Assessment Schemas ────────────────────────────────


class TransactionHistory(BaseModel):
    """Worker's transaction history summary for credit assessment."""
    total_transactions: int = Field(ge=0)
    total_volume: Decimal = Field(ge=Decimal("0"))
    average_transaction: Decimal = Field(ge=Decimal("0"))
    months_active: int = Field(ge=0, le=120)
    default_count: int = Field(default=0, ge=0)
    on_time_repayment_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    largest_transaction: Decimal = Field(ge=Decimal("0"))


class CreditAssessmentInput(BaseModel):
    """
    Input schema for creditworthiness assessment.

    Used by the CreditAgent to evaluate loan applications
    from informal workers. Considers transaction history,
    business patterns, and market conditions.
    """
    model_config = {"strict": True}

    worker_id: str = Field(..., min_length=8, max_length=64)
    worker_type: WorkerType = Field(...)
    requested_amount: Decimal = Field(
        ...,
        gt=Decimal("0"),
        le=Decimal("5000000"),  # 5M KES max credit
        description="Requested loan amount"
    )
    currency: Currency = Field(default=Currency.KES)
    purpose: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="What the credit will be used for"
    )
    transaction_history: TransactionHistory = Field(
        ...,
        description="Summary of worker's transaction history"
    )
    business_age_months: int = Field(
        ...,
        ge=0,
        le=600,
        description="How long the worker has been in business"
    )
    has_existing_loan: bool = Field(
        default=False,
        description="Whether worker has an outstanding loan"
    )
    existing_loan_balance: Decimal = Field(
        default=Decimal("0"),
        ge=Decimal("0"),
        description="Outstanding loan balance"
    )
    market_id: Optional[str] = Field(None, max_length=64)
    collateral_description: Optional[str] = Field(None, max_length=500)
    references: list[str] = Field(
        default_factory=list,
        max_length=5,
        description="Worker IDs of references (max 5)"
    )

    @model_validator(mode="after")
    def validate_loan_logic(self) -> "CreditAssessmentInput":
        """If has existing loan, balance must be > 0."""
        if self.has_existing_loan and self.existing_loan_balance <= 0:
            raise ValueError("Existing loan balance must be positive when has_existing_loan is true")
        return self


class CreditAssessmentOutput(BaseModel):
    """
    Output schema for credit assessment results.

    Every credit decision must be auditable and explainable.
    Workers deserve to know WHY they were approved or denied.
    """
    model_config = {"strict": True}

    assessment_id: str = Field(..., description="Unique assessment ID")
    worker_id: str = Field(...)
    status: CreditStatus = Field(...)
    approved_amount: Optional[Decimal] = Field(
        None,
        ge=Decimal("0"),
        description="Approved loan amount (may differ from requested)"
    )
    interest_rate_annual: Optional[float] = Field(
        None,
        ge=0.0,
        le=0.50,  # Max 50% annual — regulatory cap
        description="Annual interest rate (e.g., 0.18 = 18%)"
    )
    repayment_period_days: Optional[int] = Field(
        None,
        ge=7,
        le=365,
        description="Repayment period in days"
    )
    credit_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Internal credit score (0-1)"
    )
    risk_level: str = Field(
        ...,
        pattern=r"^(low|medium|high|very_high)$",
        description="Risk classification"
    )
    reasons: list[str] = Field(
        ...,
        min_length=1,
        description="Human-readable reasons for the decision"
    )
    conditions: list[str] = Field(
        default_factory=list,
        description="Conditions for conditional approval"
    )
    agent_id: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(
        None,
        description="When this assessment expires"
    )


# ── Price Query Schemas ──────────────────────────────────────


class PriceQueryInput(BaseModel):
    """
    Input schema for market price queries.

    Informal workers ask "How much are tomatoes at Gikomba?"
    This schema validates that query before hitting the market agent.
    """
    model_config = {"strict": True}

    worker_id: str = Field(..., min_length=8, max_length=64)
    item_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Item being queried (e.g., 'tomatoes', 'sukuma wiki')"
    )
    unit: Optional[str] = Field(
        None,
        max_length=50,
        description="Unit of measurement (e.g., 'kg', 'bunch', 'crate')"
    )
    quantity: Optional[Decimal] = Field(
        None,
        gt=Decimal("0"),
        description="Desired quantity"
    )
    market_id: Optional[str] = Field(
        None,
        max_length=64,
        description="Specific market to query (None = nearest)"
    )
    location_lat: Optional[float] = Field(
        None,
        ge=-90.0,
        le=90.0,
        description="Worker's latitude for proximity pricing"
    )
    location_lon: Optional[float] = Field(
        None,
        ge=-180.0,
        le=180.0,
        description="Worker's longitude for proximity pricing"
    )
    language: str = Field(
        default="sw",
        pattern=r"^(sw|en|yo|ha|am|lg|rw)$",
        description="Response language code"
    )


class PriceQueryOutput(BaseModel):
    """
    Output schema for market price responses.

    Includes current price, trend, and actionable advice.
    Workers get the full picture, not just a number.
    """
    model_config = {"strict": True}

    query_id: str = Field(...)
    item_name: str = Field(...)
    current_price: Decimal = Field(
        ...,
        ge=Decimal("0"),
        description="Current market price per unit"
    )
    currency: Currency = Field(default=Currency.KES)
    unit: str = Field(..., description="Unit of measurement")
    market_id: str = Field(..., description="Market where price was found")
    market_name: str = Field(..., description="Human-readable market name")
    condition: MarketCondition = Field(
        ...,
        description="Current market condition"
    )
    price_trend_7d: Optional[float] = Field(
        None,
        description="7-day price change percentage (e.g., 0.15 = +15%)"
    )
    price_trend_30d: Optional[float] = Field(
        None,
        description="30-day price change percentage"
    )
    lowest_price_nearby: Optional[Decimal] = Field(
        None,
        description="Lowest price in nearby markets"
    )
    lowest_market_name: Optional[str] = Field(
        None,
        description="Market with lowest price"
    )
    advice: Optional[str] = Field(
        None,
        max_length=500,
        description="Actionable advice for the worker"
    )
    agent_id: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    freshness_minutes: int = Field(
        ...,
        ge=0,
        description="How old the price data is in minutes"
    )


# ── Worker Profile Schema ────────────────────────────────────


class WorkerProfile(BaseModel):
    """
    Comprehensive worker profile for agent context.

    The worker's identity across all Angavu interactions.
    Updated by the Closed Learning Loop (Hermes pattern)
    as the system learns worker preferences over time.
    """
    model_config = {"strict": True}

    worker_id: str = Field(..., min_length=8, max_length=64)
    name: str = Field(..., min_length=1, max_length=200)
    phone_hash: str = Field(
        ...,
        description="Hashed phone number (never store raw)"
    )
    worker_type: WorkerType = Field(...)
    primary_language: str = Field(
        default="sw",
        pattern=r"^(sw|en|yo|ha|am|lg|rw)$"
    )
    market_id: Optional[str] = Field(None, max_length=64)
    location_lat: Optional[float] = Field(None, ge=-90.0, le=90.0)
    location_lon: Optional[float] = Field(None, ge=-180.0, le=180.0)
    currency: Currency = Field(default=Currency.KES)
    daily_revenue_estimate: Optional[Decimal] = Field(
        None,
        ge=Decimal("0"),
        description="Estimated daily revenue in local currency"
    )
    risk_tolerance: str = Field(
        default="medium",
        pattern=r"^(conservative|moderate|aggressive)$",
        description="Worker's financial risk tolerance"
    )
    preferred_communication: str = Field(
        default="voice",
        pattern=r"^(voice|text|ussd)$"
    )
    business_categories: list[str] = Field(
        default_factory=list,
        max_length=20,
        description="What the worker sells/services"
    )
    active_loans: int = Field(default=0, ge=0)
    credit_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    onboarding_date: datetime = Field(...)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("worker_id")
    @classmethod
    def validate_worker_id(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Worker ID must be alphanumeric")
        return v
