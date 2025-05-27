from config import (
    PANEL_TYPES,
    BASE_INSTALLATION_COST,
    COST_PER_PANEL,
    PERMIT_COST,
    INSPECTION_COST,
    ANNUAL_MAINTENANCE,
    CLEANING_COST,
    MONITORING_COST,
    AVERAGE_SUN_HOURS,
    SYSTEM_LOSSES,
    ELECTRICITY_RATE,
    ANNUAL_RATE_INCREASE,
    SYSTEM_LIFESPAN
)

def calculate_system_size(roof_area, panel_type='standard'):
    """
    Calculate the maximum number of panels that can fit on the roof.
    
    Args:
        roof_area: Available roof area in square meters
        panel_type: Type of solar panel to use
        
    Returns:
        int: Maximum number of panels
    """
    panel_area = PANEL_TYPES[panel_type]['dimensions'][0] * PANEL_TYPES[panel_type]['dimensions'][1]
    # Account for spacing and access requirements (80% of area usable)
    usable_area = roof_area * 0.8
    return int(usable_area / panel_area)

def calculate_annual_production(num_panels, panel_type='standard'):
    """
    Calculate annual energy production in kWh.
    
    Args:
        num_panels: Number of solar panels
        panel_type: Type of solar panel used
        
    Returns:
        float: Annual energy production in kWh
    """
    daily_production = (
        num_panels *
        PANEL_TYPES[panel_type]['power_output'] *
        AVERAGE_SUN_HOURS *
        (1 - SYSTEM_LOSSES)
    )
    return daily_production * 365 / 1000  # Convert to kWh

def calculate_installation_cost(num_panels, panel_type='standard'):
    """
    Calculate total installation cost.
    
    Args:
        num_panels: Number of solar panels
        panel_type: Type of solar panel used
        
    Returns:
        float: Total installation cost in USD
    """
    panel_cost = num_panels * PANEL_TYPES[panel_type]['power_output'] * PANEL_TYPES[panel_type]['cost_per_watt']
    labor_cost = BASE_INSTALLATION_COST + (num_panels * COST_PER_PANEL)
    return panel_cost + labor_cost + PERMIT_COST + INSPECTION_COST

def calculate_annual_savings(annual_production):
    """
    Calculate annual electricity cost savings.
    
    Args:
        annual_production: Annual energy production in kWh
        
    Returns:
        float: Annual savings in USD
    """
    return annual_production * ELECTRICITY_RATE

def calculate_roi(installation_cost, annual_savings):
    """
    Calculate return on investment metrics.
    
    Args:
        installation_cost: Total installation cost
        annual_savings: Annual electricity cost savings
        
    Returns:
        dict: ROI metrics including payback period and lifetime savings
    """
    # Calculate lifetime savings with rate increases
    lifetime_savings = 0
    current_savings = annual_savings
    payback_period = None
    
    for year in range(SYSTEM_LIFESPAN):
        lifetime_savings += current_savings
        if payback_period is None and lifetime_savings >= installation_cost:
            payback_period = year + 1
        current_savings *= (1 + ANNUAL_RATE_INCREASE)
    
    return {
        'payback_period': payback_period,
        'lifetime_savings': lifetime_savings,
        'roi_percentage': ((lifetime_savings - installation_cost) / installation_cost) * 100
    }

def calculate_maintenance_costs():
    """
    Calculate annual maintenance costs.
    
    Returns:
        float: Annual maintenance cost in USD
    """
    return ANNUAL_MAINTENANCE + CLEANING_COST + MONITORING_COST

def generate_solar_report(roof_area, panel_type='standard'):
    """
    Generate a comprehensive solar installation report.
    
    Args:
        roof_area: Available roof area in square meters
        panel_type: Type of solar panel to use
        
    Returns:
        dict: Comprehensive solar installation report
    """
    num_panels = calculate_system_size(roof_area, panel_type)
    annual_production = calculate_annual_production(num_panels, panel_type)
    installation_cost = calculate_installation_cost(num_panels, panel_type)
    annual_savings = calculate_annual_savings(annual_production)
    roi_metrics = calculate_roi(installation_cost, annual_savings)
    annual_maintenance = calculate_maintenance_costs()
    
    return {
        'system_size': {
            'panels': num_panels,
            'total_power': num_panels * PANEL_TYPES[panel_type]['power_output'],
            'panel_type': panel_type
        },
        'production': {
            'annual_kwh': annual_production,
            'daily_kwh': annual_production / 365
        },
        'financials': {
            'installation_cost': installation_cost,
            'annual_savings': annual_savings,
            'annual_maintenance': annual_maintenance,
            'payback_period': roi_metrics['payback_period'],
            'lifetime_savings': roi_metrics['lifetime_savings'],
            'roi_percentage': roi_metrics['roi_percentage']
        }
    } 