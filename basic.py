"""
Basic Information Module

This module fetches and returns basic company information
based on a stock symbol (ticker).
"""

def get_basic_info(symbol: str) -> dict:
    """
    Fetch basic company information for a given stock symbol.

    Parameters:
    -----------
    symbol : str
        Stock ticker symbol (e.g., 'JPM', 'AAPL', 'GOOGL')

    Returns:
    --------
    dict
        A dictionary containing:
        - company_name: str - Full company name
        - annual_revenue: str - Annual revenue (formatted with currency)
        - annual_profit: str - Annual profit (formatted with currency)
        - symbol: str - Stock ticker symbol

    Example:
    --------
    >>> info = get_basic_info('JPM')
    >>> print(info['company_name'])
    'JP Morgan Chase & Co.'
    """

    # TODO: Implement API call to fetch real company data
    # Potential data sources:
    # - Yahoo Finance API
    # - Alpha Vantage API
    # - Financial Modeling Prep API
    # - IEX Cloud API

    # Placeholder data - will be replaced with actual API calls
    placeholder_data = {
        'JPM': {
            'company_name': 'JP Morgan Chase & Co.',
            'annual_revenue': '$278.9B',
            'annual_profit': '$177.556B',
            'symbol': 'JPM'
        },
        'AAPL': {
            'company_name': 'Apple Inc.',
            'annual_revenue': '$394.3B',
            'annual_profit': '$99.8B',
            'symbol': 'AAPL'
        },
        'GOOGL': {
            'company_name': 'Alphabet Inc.',
            'annual_revenue': '$307.4B',
            'annual_profit': '$73.8B',
            'symbol': 'GOOGL'
        }
    }

    # Convert symbol to uppercase for consistency
    symbol = symbol.upper()

    # Return data if symbol exists, otherwise return default/error structure
    if symbol in placeholder_data:
        return placeholder_data[symbol]
    else:
        return {
            'company_name': f'Company information not found for {symbol}',
            'annual_revenue': 'N/A',
            'annual_profit': 'N/A',
            'symbol': symbol,
            'error': True
        }


def format_currency(amount: float, currency: str = 'USD') -> str:
    """
    Format a numeric amount as currency string.

    Parameters:
    -----------
    amount : float
        The amount to format
    currency : str
        Currency code (default: 'USD')

    Returns:
    --------
    str
        Formatted currency string (e.g., '$123.4B')
    """
    # TODO: Implement proper currency formatting
    # This is a placeholder for future implementation

    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    else:
        return f"${amount:,.2f}"


if __name__ == "__main__":
    # Test the function
    print("Testing get_basic_info()...")
    print("\nJP Morgan Chase:")
    print(get_basic_info('JPM'))

    print("\nApple:")
    print(get_basic_info('AAPL'))

    print("\nUnknown symbol:")
    print(get_basic_info('UNKNOWN'))
