from datetime import timezone as dt_timezone
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

def get_utc_timestamp() -> str:
    """Returns current UTC timestamp in ISO-8601 format."""
    return datetime.now(dt_timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(default='healthy', description='Service health status')
    timestamp: str = Field(default_factory=get_utc_timestamp, description='UTC ISO-8601 timestamp')

class ToolItem(BaseModel):
    """Individual tool description schema."""
    name: str = Field(default='', description='Tool identifier name')
    description: str = Field(default='', description='Tool capability description')
    input_schema: Dict[str, Any] = Field(default_factory=dict, description='JSON schema for inputs')
    output_schema: Dict[str, Any] = Field(default_factory=dict, description='JSON schema for outputs')

class ToolsResponse(BaseModel):
    """Response containing list of available tools."""
    tools: List[Dict[str, Any]] = Field(default_factory=list, description='List of registered agent tools')

class VerifyMcpCapabilityEscrowRequest(BaseModel):
    """Request schema for verify_mcp_capability_escrow with zero-failure defaults."""
    target_identifier: str = Field(default='filesystem-server', description='MCP server unique identifier or endpoint')
    query_parameter: str = Field(default='capability_verification', description='Verification scope or profile name')
    lat: float = Field(default=0.0, ge=-90.0, le=90.0, description='Latitude coordinate clamped to [-90, 90]')
    lon: float = Field(default=0.0, ge=-180.0, le=180.0, description='Longitude coordinate clamped to [-180, 180]')
    window_steps: int = Field(default=10, ge=1, le=100, description='Observation execution windows')
    verification_depth: int = Field(default=5, ge=1, le=20, description='Verification depth level [1, 20]')

class ExplainabilityDetail(BaseModel):
    """Explainability breakdown for metric scoring."""
    primary_driver: str = Field(default='capability_assurance', description='Primary driving factor for score')
    weights: Dict[str, float] = Field(default_factory=lambda: {'capability_assurance': 0.35, 'escrow_trust': 0.25, 'operational_safety': 0.2, 'stability': 0.2}, description='Weight distribution used in scoring')

class VerifyMcpCapabilityEscrowResponse(BaseModel):
    """Canonical response schema matching project specifications."""
    timestamp: str = Field(default_factory=get_utc_timestamp, description='UTC ISO-8601 timestamp')
    status: str = Field(default='healthy', description='Operational status')
    primary_metric: float = Field(default=91.4, description='Primary trust score (0-100)')
    secondary_score: float = Field(default=0.96, description='Secondary normalized metric index')
    state_index: float = Field(default=87.9, description='State classification index')
    classification: str = Field(default='ESCROW_VERIFIED', description='Trust classification state')
    explainability: ExplainabilityDetail = Field(default_factory=ExplainabilityDetail, description='Explainability attribution')

class GetSpatialH3TensorRequest(BaseModel):
    """Request schema for spatial H3 tensor analysis with strict defaults."""
    lat: float = Field(default=2.0442, ge=-90.0, le=90.0, description='Latitude coordinate')
    lon: float = Field(default=102.5689, ge=-180.0, le=180.0, description='Longitude coordinate')
    resolution: int = Field(default=8, ge=0, le=15, description='Uber H3 resolution level')

class GetSpatialH3TensorResponse(BaseModel):
    """Spatial H3 tensor response schema."""
    h3_index: str = Field(default='886520d81dfffff', description='Uber H3 cell index')
    spatial_cell: str = Field(default='886520d81dfffff', description='Spatial grid cell reference')
    density_score: float = Field(default=64.2, description='Trust density score')
    terrain_state_index: float = Field(default=75.1, description='Terrain state index')
    status: str = Field(default='ACTIVE', description='Cell infrastructure status')

class InspectMcpManifestRequest(BaseModel):
    mcp_id: str = Field(default='filesystem-server', description='MCP Identifier')
    manifest_uri: str = Field(default='', description='Optional manifest URI')

class InspectMcpManifestResponse(BaseModel):
    mcp_id: str = Field(default='filesystem-server')
    declared_capabilities: List[str] = Field(default_factory=lambda: ['filesystem', 'network'])
    status: str = Field(default='PARSED')

class VerifyDeclaredCapabilitiesRequest(BaseModel):
    mcp_id: str = Field(default='filesystem-server')
    strict_mode: bool = Field(default=True)

class VerifyDeclaredCapabilitiesResponse(BaseModel):
    ocr: float = Field(default=1.0, description='Observed Capability Ratio')
    verified: bool = Field(default=True)

class DiscoverUndeclaredCapabilitiesRequest(BaseModel):
    mcp_id: str = Field(default='filesystem-server')
    observation_depth: int = Field(default=5)

class DiscoverUndeclaredCapabilitiesResponse(BaseModel):
    undeclared_capabilities: List[str] = Field(default_factory=list)
    drift_score: float = Field(default=0.0)

class ComputeBlastRadiusScoreRequest(BaseModel):
    mcp_id: str = Field(default='filesystem-server')
    privileged_capabilities: List[str] = Field(default_factory=lambda: ['shell', 'code_execution'])

class ComputeBlastRadiusScoreResponse(BaseModel):
    blast_radius: float = Field(default=0.25, description='Blast Radius score (0-1)')

class ComputePrivilegeRiskIndexRequest(BaseModel):
    mcp_id: str = Field(default='filesystem-server')

class ComputePrivilegeRiskIndexResponse(BaseModel):
    pri: float = Field(default=0.15, description='Privilege Risk Index')

class ComputeOperationalSafetyRequest(BaseModel):
    mcp_id: str = Field(default='filesystem-server')

class ComputeOperationalSafetyResponse(BaseModel):
    osi: float = Field(default=0.85, description='Operational Safety Index')

class ComputeExecutionDeterminismRequest(BaseModel):
    mcp_id: str = Field(default='filesystem-server')
    total_executions: int = Field(default=100)

class ComputeExecutionDeterminismResponse(BaseModel):
    determinism: float = Field(default=0.99, description='Execution Determinism ratio')

class ComputeTrustScoreRequest(BaseModel):
    mcp_id: str = Field(default='filesystem-server')

class ComputeTrustScoreResponse(BaseModel):
    trust_score: float = Field(default=91.4, description='Normalized Trust Score 0-100')
    classification: str = Field(default='ESCROW_VERIFIED')

class GenerateCapabilityAttestationRequest(BaseModel):
    mcp_id: str = Field(default='filesystem-server')
    signer_id: str = Field(default='validator-node-1')

class GenerateCapabilityAttestationResponse(BaseModel):
    attestation_id: str = Field(default='attest-sha256-abc123xyz')
    signature: str = Field(default='sig-mock-crypto-proof')
    timestamp: str = Field(default_factory=get_utc_timestamp)

class PublishCapabilityAttestationRequest(BaseModel):
    attestation_id: str = Field(default='attest-sha256-abc123xyz')

class PublishCapabilityAttestationResponse(BaseModel):
    published: bool = Field(default=True)
    registry_uri: str = Field(default='https://escrow.mcp.network/attestations')

class VerifyCapabilityAttestationRequest(BaseModel):
    attestation_id: str = Field(default='attest-sha256-abc123xyz')

class VerifyCapabilityAttestationResponse(BaseModel):
    valid: bool = Field(default=True)
    consensus_ratio: float = Field(default=1.0)

class CompareMcpVersionsRequest(BaseModel):
    mcp_id: str = Field(default='filesystem-server')
    version_a: str = Field(default='1.0.0')
    version_b: str = Field(default='1.1.0')

class CompareMcpVersionsResponse(BaseModel):
    drift_detected: bool = Field(default=False)
    capability_delta: List[str] = Field(default_factory=list)

class BuildTrustGraphRequest(BaseModel):
    network_scope: str = Field(default='global')

class BuildTrustGraphResponse(BaseModel):
    nodes_count: int = Field(default=42)
    edges_count: int = Field(default=128)
    status: str = Field(default='BUILT')