"""Receipts Router - AI-powered receipt scanning"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import base64
import json
import re
import logging

from database import get_supabase, Database
from auth import get_current_user, CurrentUser, require_permission
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


# Cost categories
COST_CATEGORIES = {
    "insurance": "Insurance",
    "labor": "Labor",
    "stamps": "Stamps/Taxes",
    "material": "Material",
    "subs_bond": "Subs/Bond",
    "equipment": "Equipment",
}


class ReceiptScanResult(BaseModel):
    vendor_name: str = ""
    vendor_address: str = ""
    receipt_date: str = ""
    receipt_number: str = ""
    subtotal: float = 0
    tax: float = 0
    total: float = 0
    payment_method: str = ""
    line_items: List[Dict[str, Any]] = []
    suggested_category: str = "material"
    confidence_score: float = 0
    notes: str = ""


class ReceiptScanRequest(BaseModel):
    image_base64: str
    job_context: Optional[str] = None


def get_anthropic_client():
    """Get Anthropic client"""
    if not settings.anthropic_api_key:
        return None
    try:
        import anthropic
        return anthropic.Anthropic(api_key=settings.anthropic_api_key)
    except Exception as e:
        logger.error(f"Failed to create Anthropic client: {e}")
        return None


@router.post("/scan", response_model=ReceiptScanResult)
async def scan_receipt(
    request: ReceiptScanRequest,
    current_user: CurrentUser = Depends(require_permission("manage_costs"))
):
    """
    Scan a receipt image and extract data using AI.
    Send image as base64 encoded string.
    """
    client = get_anthropic_client()
    if not client:
        raise HTTPException(
            status_code=503,
            detail="Receipt scanning not available - API key not configured"
        )
    
    category_list = "\n".join([f"- {k}: {v}" for k, v in COST_CATEGORIES.items()])
    
    prompt = f"""Analyze this receipt/invoice image and extract all relevant information.

COST CATEGORIES:
{category_list}

JOB CONTEXT: {request.job_context or "General construction job"}

CATEGORIZATION RULES:
- material: Building materials, supplies, hardware, lumber, drywall, paint, tile
- equipment: Tool rentals, equipment purchases, machinery
- labor: Labor charges, hourly work, time-based billing
- subs_bond: Subcontractor work (excavation, landscaping, electrical subs), bonding
- insurance: Insurance premiums, certificates
- stamps: Permits, taxes, government fees

Return a JSON object:
{{
    "vendor_name": "Store/vendor name",
    "vendor_address": "Address if visible",
    "receipt_date": "YYYY-MM-DD",
    "receipt_number": "Receipt number if visible",
    "subtotal": 0.00,
    "tax": 0.00,
    "total": 0.00,
    "payment_method": "cash/credit/debit/check/invoice/other",
    "line_items": [
        {{
            "description": "Item description",
            "category": "material|subs_bond|labor|equipment|insurance|stamps",
            "quantity": 1,
            "unit_price": 0.00,
            "total": 0.00,
            "date": "YYYY-MM-DD if visible",
            "vendor_name": "Vendor for this line if different"
        }}
    ],
    "suggested_category": "Most common category",
    "confidence_score": 0.95,
    "notes": "Brief description"
}}

Return ONLY JSON. If not a receipt, return {{"error": "Not a valid receipt"}}
"""

    try:
        # Determine media type from base64 header or default to jpeg
        image_data = request.image_base64
        media_type = "image/jpeg"
        
        if image_data.startswith("data:"):
            # Extract media type and data
            match = re.match(r'data:([^;]+);base64,(.+)', image_data)
            if match:
                media_type = match.group(1)
                image_data = match.group(2)
        
        # Call Claude API
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {"type": "text", "text": prompt}
                ]
            }]
        )
        
        response_text = message.content[0].text.strip()
        
        # Extract JSON
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group()
        
        data = json.loads(response_text)
        
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return ReceiptScanResult(**data)
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse AI response")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Receipt scan error: {e}")
        raise HTTPException(status_code=500, detail="Failed to scan receipt")


@router.post("/scan/upload")
async def scan_receipt_upload(
    file: UploadFile = File(...),
    job_context: Optional[str] = None,
    current_user: CurrentUser = Depends(require_permission("manage_costs"))
):
    """
    Scan a receipt by uploading a file.
    Supports: JPG, PNG, GIF, WebP, PDF
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
    
    # Read and encode
    content = await file.read()
    image_base64 = base64.b64encode(content).decode("utf-8")
    
    # Add data URI prefix
    data_uri = f"data:{file.content_type};base64,{image_base64}"
    
    # Call the scan endpoint
    request = ReceiptScanRequest(image_base64=data_uri, job_context=job_context)
    return await scan_receipt(request, current_user)


@router.get("/categories")
async def get_cost_categories(current_user: CurrentUser = Depends(get_current_user)):
    """Get available cost categories"""
    return COST_CATEGORIES


@router.get("/status")
async def get_receipt_scanning_status(current_user: CurrentUser = Depends(get_current_user)):
    """Check if receipt scanning is available"""
    client = get_anthropic_client()
    return {
        "available": client is not None,
        "message": "Receipt scanning is available" if client else "API key not configured"
    }
