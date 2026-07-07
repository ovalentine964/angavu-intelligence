"""
CrewAI-Inspired Role-Based Agent Teams for Angavu Intelligence.

WHY: CrewAI's role-based pattern maps perfectly to informal market roles.
Each agent has a clear role, goal, backstory, and set of tools — just like
real market participants (buyer, seller, analyst, lender).

HOW: Define agent roles with goals, backstories, tools, and delegation rules.
Each role is a data class that configures how an agent behaves, what tools
it can access, and how it collaborates with other agents.

WHERE: angavu-intelligence-backend/app/agents/roles/market_roles.py

Pattern borrowed from: CrewAI (open-source, CrewAI Inc.)
Alignment: Hermes Closed Learning Loop — roles evolve based on outcomes
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from app.schemas.agent_schemas import (
    Currency,
    MarketCondition,
    TransactionType,
    WorkerType,
)


# ── Role Enums ───────────────────────────────────────────────


class AgentTier(str, Enum):
    """
    Agent complexity tier — maps to model routing (Swarm G recommendation).
    Cheaper models for routine tasks, better models for complex decisions.
    """
    TIER_1_SIMPLE = "tier_1_simple"      # Balance checks, stock counts → tiny model
    TIER_2_STANDARD = "tier_2_standard"  # Price queries, trade matching → small model
    TIER_3_COMPLEX = "tier_3_complex"    # Credit assessment, planning → medium model


class DelegationPolicy(str, Enum):
    """When an agent can delegate to another agent."""
    NEVER = "never"            # Handle everything internally
    WHEN_STUCK = "when_stuck"  # Delegate only when unable to resolve
    ALWAYS = "always"          # Delegate sub-tasks freely
    NEVER_DELEGATE = "never_delegate"  # This agent is a terminal node


# ── Tool Definitions ─────────────────────────────────────────


@dataclass(frozen=True)
class AgentTool:
    """A tool available to an agent role."""
    name: str
    description: str
    requires_confirmation: bool = False  # Financial actions need worker confirmation


# Predefined tools available to market agents
MARKET_TOOLS = {
    "price_lookup": AgentTool(
        name="price_lookup",
        description="Query current market prices for commodities",
    ),
    "price_history": AgentTool(
        name="price_history",
        description="Retrieve historical price data for trend analysis",
    ),
    "market_search": AgentTool(
        name="market_search",
        description="Search for markets by location, commodity, or condition",
    ),
    "transaction_record": AgentTool(
        name="transaction_record",
        description="Record a financial transaction",
        requires_confirmation=True,
    ),
    "balance_check": AgentTool(
        name="balance_check",
        description="Check worker's current balance",
    ),
    "mpesa_send": AgentTool(
        name="mpesa_send",
        description="Initiate M-Pesa payment",
        requires_confirmation=True,
    ),
    "mpesa_receive": AgentTool(
        name="mpesa_receive",
        description="Generate M-Pesa payment request (STK push)",
        requires_confirmation=True,
    ),
    "credit_assess": AgentTool(
        name="credit_assess",
        description="Run creditworthiness assessment for a worker",
    ),
    "loan_offer": AgentTool(
        name="loan_offer",
        description="Generate a loan offer for an approved worker",
        requires_confirmation=True,
    ),
    "loan_repay": AgentTool(
        name="loan_repay",
        description="Process loan repayment",
        requires_confirmation=True,
    ),
    "inventory_track": AgentTool(
        name="inventory_track",
        description="Track stock levels for a worker's business",
    ),
    "inventory_restock": AgentTool(
        name="inventory_restock",
        description="Suggest restocking based on sales patterns",
    ),
    "demand_forecast": AgentTool(
        name="demand_forecast",
        description="Predict demand for commodities in a market",
    ),
    "supplier_match": AgentTool(
        name="supplier_match",
        description="Match buyer with suppliers for best prices",
    ),
    "buyer_match": AgentTool(
        name="buyer_match",
        description="Match seller with potential buyers",
    ),
    "route_optimize": AgentTool(
        name="route_optimize",
        description="Optimize delivery/transport routes between markets",
    ),
    "weather_check": AgentTool(
        name="weather_check",
        description="Check weather forecast for market planning",
    ),
    "alert_set": AgentTool(
        name="alert_set",
        description="Set price or event alerts for a worker",
    ),
}


# ── Role Definitions ─────────────────────────────────────────


@dataclass
class AgentRole:
    """
    Base agent role configuration.

    Inspired by CrewAI's role-based pattern: each agent has a role name,
    goal, backstory (for LLM context), allowed tools, and delegation rules.

    The backstory is critical — it tells the LLM *who* this agent is,
    which shapes its reasoning and communication style.
    """
    role_name: str
    goal: str
    backstory: str
    tier: AgentTier
    tools: list[str]  # Tool names from MARKET_TOOLS
    delegation_policy: DelegationPolicy = DelegationPolicy.WHEN_STUCK
    allowed_worker_types: list[WorkerType] = field(default_factory=list)
    max_delegation_depth: int = 2
    verbose: bool = True
    memory_enabled: bool = True  # L2 episodic memory (Hermes pattern)

    def get_tools(self) -> list[AgentTool]:
        """Resolve tool names to AgentTool objects."""
        return [MARKET_TOOLS[name] for name in self.tools if name in MARKET_TOOLS]

    def requires_confirmation(self, tool_name: str) -> bool:
        """Check if a tool requires worker confirmation before execution."""
        tool = MARKET_TOOLS.get(tool_name)
        return tool.requires_confirmation if tool else False


# ── Buyer Agent ──────────────────────────────────────────────


@dataclass
class BuyerAgent(AgentRole):
    """
    Buyer Agent — finds the best prices for informal workers.

    GOAL: Help workers find the cheapest suppliers and best deals.
    This agent acts like a savvy market shopper who knows every stall,
    every price, and every negotiation trick.

    In CrewAI terms: this is the "researcher" role — gathering
    information and presenting options to the worker.
    """
    role_name: str = "Buyer Agent"
    goal: str = (
        "Find the best prices and quality for the worker's needs. "
        "Compare across markets, negotiate where possible, and ensure "
        "the worker gets maximum value for every shilling spent."
    )
    backstory: str = (
        "You are a seasoned market intelligence agent who has spent years "
        "navigating East Africa's informal markets. You know that Gikomba "
        "has the best wholesale prices on Tuesday mornings, that Wakulima "
        "Market is cheaper for vegetables after 2pm, and that Mama Njeri's "
        "stall in Korogocho always has the freshest sukuma wiki. You speak "
        "in simple, clear language — many of your workers are semi-literate "
        "and rely on voice instructions. You never recommend a purchase "
        "without confirming the price and the worker's budget."
    )
    tier: AgentTier = AgentTier.TIER_2_STANDARD
    tools: list[str] = field(default_factory=lambda: [
        "price_lookup",
        "price_history",
        "market_search",
        "supplier_match",
        "route_optimize",
        "balance_check",
        "alert_set",
    ])
    delegation_policy: DelegationPolicy = DelegationPolicy.ALWAYS
    allowed_worker_types: list[WorkerType] = field(default_factory=lambda: [
        WorkerType.MAMA_MBOGA,
        WorkerType.HAWKER,
        WorkerType.FOOD_VENDOR,
        WorkerType.FUNDI,
        WorkerType.SALONIST,
        WorkerType.GENERAL,
    ])


# ── Seller Agent ─────────────────────────────────────────────


@dataclass
class SellerAgent(AgentRole):
    """
    Seller Agent — maximizes sales revenue for informal workers.

    GOAL: Help workers price their goods/services competitively,
    find buyers, and optimize their sales strategy.

    This agent is the "optimizer" — it analyzes market conditions,
    competition, and demand to recommend the best selling strategy.
    """
    role_name: str = "Seller Agent"
    goal: str = (
        "Maximize the worker's sales revenue by recommending optimal pricing, "
        "identifying high-demand markets, and connecting with buyers. "
        "Every recommendation must increase the worker's income."
    )
    backstory: str = (
        "You are a market strategist agent who understands the rhythms of "
        "African informal markets. You know that tomatoes sell for 30% more "
        "in Nairobi's CBD than in Gikomba wholesale market. You know that "
        "boda boda riders earn more during rush hours and that Friday evenings "
        "are peak time for food vendors near matatu stages. You help workers "
        "decide WHAT to sell, WHERE to sell it, and WHEN to sell it for "
        "maximum profit. You always factor in transport costs and time."
    )
    tier: AgentTier = AgentTier.TIER_2_STANDARD
    tools: list[str] = field(default_factory=lambda: [
        "price_lookup",
        "price_history",
        "market_search",
        "buyer_match",
        "demand_forecast",
        "route_optimize",
        "transaction_record",
        "alert_set",
    ])
    delegation_policy: DelegationPolicy = DelegationPolicy.ALWAYS
    allowed_worker_types: list[WorkerType] = field(default_factory=lambda: [
        WorkerType.MAMA_MBOGA,
        WorkerType.HAWKER,
        WorkerType.FOOD_VENDOR,
        WorkerType.FUNDI,
        WorkerType.SALONIST,
        WorkerType.MJENGA,
        WorkerType.GENERAL,
    ])


# ── Market Analyst Agent ─────────────────────────────────────


@dataclass
class MarketAnalystAgent(AgentRole):
    """
    Market Analyst Agent — identifies trends and market intelligence.

    GOAL: Analyze market data to identify price trends, seasonal patterns,
    and emerging opportunities. This is the "brain" of the market crew.

    Uses the Stigmergy pattern — reads traces left by other agents
    to build a collective market intelligence picture.
    """
    role_name: str = "Market Analyst Agent"
    goal: str = (
        "Identify market trends, price patterns, and emerging opportunities "
        "across informal markets. Provide actionable intelligence that helps "
        "workers and other agents make better decisions."
    )
    backstory: str = (
        "You are a data-driven market intelligence analyst who processes "
        "thousands of transactions across East Africa's informal markets "
        "every day. You spot patterns that humans miss: that maize prices "
        "in Eldoret drop 20% every harvest season, that fish prices in "
        "Mombasa spike when the monsoon keeps boats in port, that Nairobi "
        "construction material demand peaks in Q1. You read the traces "
        "left by other agents — price queries, transaction volumes, "
        "inventory levels — and synthesize them into market intelligence. "
        "Your reports are concise, actionable, and always in the worker's "
        "preferred language."
    )
    tier: AgentTier = AgentTier.TIER_3_COMPLEX
    tools: list[str] = field(default_factory=lambda: [
        "price_lookup",
        "price_history",
        "market_search",
        "demand_forecast",
        "weather_check",
    ])
    delegation_policy: DelegationPolicy = DelegationPolicy.WHEN_STUCK
    allowed_worker_types: list[WorkerType] = field(default_factory=lambda: list(WorkerType))
    max_delegation_depth: int = 1  # Analysts don't delegate much


# ── Credit Agent ─────────────────────────────────────────────


@dataclass
class CreditAgent(AgentRole):
    """
    Credit Agent — assesses creditworthiness and manages loans.

    GOAL: Evaluate loan applications fairly, considering the worker's
    transaction history, business patterns, and market conditions.
    Every decision must be explainable (NIST AI RMF Layer 1).

    This is the most sensitive agent — it handles money.
    All outputs require worker confirmation.
    """
    role_name: str = "Credit Agent"
    goal: str = (
        "Assess creditworthiness fairly and transparently. Approve loans "
        "that workers can repay, deny loans that would harm them. Every "
        "decision must be explainable in the worker's language."
    )
    backstory: str = (
        "You are a careful, fair-minded credit assessment agent who "
        "understands that informal workers have irregular income patterns. "
        "A mama mboga might earn 5,000 KES on Monday and 500 KES on "
        "Wednesday — that's normal, not a red flag. You look at 30-day "
        "and 90-day averages, not single-day income. You know that a "
        "boda boda rider's best collateral is their consistent daily "
        "trips, not a property deed they don't have. You NEVER approve "
        "a loan that would burden the worker with more than 30% of their "
        "average monthly income in repayments. When you deny a loan, you "
        "explain WHY and suggest what they can do to qualify in the future."
    )
    tier: AgentTier = AgentTier.TIER_3_COMPLEX
    tools: list[str] = field(default_factory=lambda: [
        "credit_assess",
        "loan_offer",
        "loan_repay",
        "balance_check",
        "transaction_record",
    ])
    delegation_policy: DelegationPolicy = DelegationPolicy.NEVER
    allowed_worker_types: list[WorkerType] = field(default_factory=lambda: list(WorkerType))
    max_delegation_depth: int = 0  # Credit decisions are final within this agent


# ── Logistics Agent ──────────────────────────────────────────


@dataclass
class LogisticsAgent(AgentRole):
    """
    Logistics Agent — handles transport and delivery coordination.

    GOAL: Optimize delivery routes, coordinate transport between markets,
    and reduce logistics costs for informal workers.

    In the informal economy, transport is often the biggest cost center.
    A mama mboga paying 200 KES to transport 500 KES worth of vegetables
    is losing 40% to logistics. This agent fights for that margin.
    """
    role_name: str = "Logistics Agent"
    goal: str = (
        "Minimize transport costs and delivery times for informal workers. "
        "Find the cheapest, fastest routes between markets. Coordinate "
        "shared transport when possible."
    )
    backstory: str = (
        "You are a logistics optimization agent who knows every matatu "
        "route, every boda boda shortcut, and every truck that runs between "
        "major markets. You know that sharing a truck from Gikomba to "
        "Korogocho with 3 other traders costs 100 KES each instead of "
        "300 KES for a solo trip. You track delivery reliability — some "
        "boda riders are fast but careless with produce; others are slow "
        "but everything arrives intact. You always factor in time-of-day: "
        "Nairobi traffic adds 45 minutes between 7-9am and 4-7pm."
    )
    tier: AgentTier = AgentTier.TIER_2_STANDARD
    tools: list[str] = field(default_factory=lambda: [
        "route_optimize",
        "market_search",
        "weather_check",
        "alert_set",
    ])
    delegation_policy: DelegationPolicy = DelegationPolicy.ALWAYS
    allowed_worker_types: list[WorkerType] = field(default_factory=lambda: [
        WorkerType.MAMA_MBOGA,
        WorkerType.HAWKER,
        WorkerType.FOOD_VENDOR,
        WorkerType.BODA_BODA,
        WorkerType.GENERAL,
    ])


# ── Crew Composition ─────────────────────────────────────────


@dataclass
class MarketCrew:
    """
    A crew of agents that work together to serve a market.

    Maps to CrewAI's "crew" concept — a team of specialized agents
    that collaborate to accomplish complex tasks.

    Example: "Gikomba Tuesday Crew" = BuyerAgent + SellerAgent +
    MarketAnalystAgent + LogisticsAgent, all focused on Gikomba
    market operations on Tuesdays.
    """
    crew_name: str
    market_id: str
    agents: list[AgentRole] = field(default_factory=list)
    process_mode: str = "hierarchical"  # "sequential" or "hierarchical"

    def add_agent(self, agent: AgentRole) -> None:
        """Add an agent to the crew."""
        self.agents.append(agent)

    def get_agent_for_task(self, task_type: str) -> Optional[AgentRole]:
        """Route a task to the most appropriate agent in the crew."""
        task_agent_map = {
            "buy": "Buyer Agent",
            "purchase": "Buyer Agent",
            "find_supplier": "Buyer Agent",
            "sell": "Seller Agent",
            "price": "Seller Agent",
            "revenue": "Seller Agent",
            "analyze": "Market Analyst Agent",
            "trend": "Market Analyst Agent",
            "forecast": "Market Analyst Agent",
            "credit": "Credit Agent",
            "loan": "Credit Agent",
            "repay": "Credit Agent",
            "deliver": "Logistics Agent",
            "transport": "Logistics Agent",
            "route": "Logistics Agent",
        }
        target_role = task_agent_map.get(task_type)
        if target_role:
            for agent in self.agents:
                if agent.role_name == target_role:
                    return agent
        return None  # No matching agent — escalate to orchestrator


# ── Crew Factory ─────────────────────────────────────────────


def create_default_market_crew(market_id: str) -> MarketCrew:
    """
    Create a standard market crew with all five agent roles.

    This is the default crew composition for any market.
    Markets can customize by adding/removing agents.
    """
    crew = MarketCrew(
        crew_name=f"Market Crew — {market_id}",
        market_id=market_id,
        process_mode="hierarchical",
    )
    crew.add_agent(BuyerAgent())
    crew.add_agent(SellerAgent())
    crew.add_agent(MarketAnalystAgent())
    crew.add_agent(CreditAgent())
    crew.add_agent(LogisticsAgent())
    return crew
