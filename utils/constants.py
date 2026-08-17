"""Constants and static data."""

# Supported countries for phone scanner
SUPPORTED_COUNTRIES = {
    "AT": {"name": "Österreich", "emoji": "🇦🇹", "code": "+43"},
    "DE": {"name": "Deutschland", "emoji": "🇩🇪", "code": "+49"},
    "CH": {"name": "Schweiz", "emoji": "🇨🇭", "code": "+41"},
    "GB": {"name": "Vereinigtes Königreich", "emoji": "🇬🇧", "code": "+44"},
    "US": {"name": "USA", "emoji": "🇺🇸", "code": "+1"},
    "CA": {"name": "Kanada", "emoji": "🇨🇦", "code": "+1"},
    "FR": {"name": "Frankreich", "emoji": "🇫🇷", "code": "+33"},
    "IT": {"name": "Italien", "emoji": "🇮🇹", "code": "+39"},
    "ES": {"name": "Spanien", "emoji": "🇪🇸", "code": "+34"},
    "NL": {"name": "Niederlande", "emoji": "🇳🇱", "code": "+31"},
    "BE": {"name": "Belgien", "emoji": "🇧🇪", "code": "+32"},
    "PL": {"name": "Polen", "emoji": "🇵🇱", "code": "+48"},
    "SE": {"name": "Schweden", "emoji": "🇸🇪", "code": "+46"},
    "NO": {"name": "Norwegen", "emoji": "🇳🇴", "code": "+47"},
    "DK": {"name": "Dänemark", "emoji": "🇩🇰", "code": "+45"},
}

# Time filter options
TIME_FILTERS = {
    "1h": "Letzte Stunde",
    "24h": "Letzte 24 Stunden",
    "7d": "Letzte 7 Tage",
    "30d": "Letzte 30 Tage",
    "90d": "Letzte 90 Tage",
    "all": "Alle Zeiten",
}

# Content type options
CONTENT_TYPES = {
    "video": "Videos",
    "short": "Shorts",
    "both": "Videos & Shorts",
}

# Error messages (German)
ERROR_MESSAGES = {
    "quota_exceeded": "YouTube API Quota wurde heute erreicht. Versuchen Sie es morgen erneut.",
    "no_results": "Keine Ergebnisse gefunden. Es wurde nichts zu Ihrer Suche gefunden.",
    "invalid_query": "Ungültige Suchanfrage. Bitte geben Sie einen gültigen Suchbegriff ein.",
    "api_error": "YouTube API Fehler: {error}",
    "missing_config": "Bot nicht korrekt konfiguriert. Bitte kontaktieren Sie einen Administrator.",
    "country_not_supported": "Land wird nicht unterstützt. Unterstützte Länder: {countries}",
    "timeout": "Anfrage hat zu lange gedauert. Versuchen Sie es später erneut.",
}

# Success messages (German)
SUCCESS_MESSAGES = {
    "search_started": "Suche wird durchgeführt...",
    "search_complete": "Suche abgeschlossen.",
    "results_found": "{count} Treffer gefunden.",
}
