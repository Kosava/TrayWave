"""
TrayWave SVG Icon System — Premium Edition
==========================================
Svaka kategorija ima jedinstvenu, prepoznatljivu ikonu sa gradijentima,
karakterom i vizuelnim identitetom koji odgovara žanru muzike.
"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QByteArray
import re as _re
import logging

logger = logging.getLogger(__name__)

_SVG = {

    # ═══════════════════════════════════════════════════════════════════════
    # UI AKCIJE
    # ═══════════════════════════════════════════════════════════════════════

    "stop": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="sg" cx="40%" cy="35%" r="65%">
        <stop offset="0%" stop-color="#f87171"/>
        <stop offset="100%" stop-color="#b91c1c"/>
      </radialGradient></defs>
      <rect x="4" y="4" width="16" height="16" rx="3" fill="url(#sg)"/>
      <rect x="8" y="8" width="8" height="8" rx="1" fill="white" opacity="0.9"/>
    </svg>""",

    "power": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="pg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#9ca3af"/>
        <stop offset="100%" stop-color="#4b5563"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="9" fill="url(#pg)"/>
      <path d="M12 6v6" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M8.5 8A5.5 5.5 0 1 0 15.5 8" stroke="white" stroke-width="2"
            stroke-linecap="round" fill="none"/>
    </svg>""",

    "settings": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="setg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#60a5fa"/>
        <stop offset="100%" stop-color="#2563eb"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#setg)"/>
      <circle cx="12" cy="12" r="3" fill="white"/>
      <circle cx="12" cy="12" r="3" fill="none" stroke="white" stroke-width="1"/>
      <g stroke="white" stroke-width="2" stroke-linecap="round">
        <line x1="12" y1="4.5" x2="12" y2="6.5"/>
        <line x1="12" y1="17.5" x2="12" y2="19.5"/>
        <line x1="4.5" y1="12" x2="6.5" y2="12"/>
        <line x1="17.5" y1="12" x2="19.5" y2="12"/>
        <line x1="6.7" y1="6.7" x2="8.1" y2="8.1"/>
        <line x1="15.9" y1="15.9" x2="17.3" y2="17.3"/>
        <line x1="17.3" y1="6.7" x2="15.9" y2="8.1"/>
        <line x1="8.1" y1="15.9" x2="6.7" y2="17.3"/>
      </g>
    </svg>""",

    "edit": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="eg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#34d399"/>
        <stop offset="100%" stop-color="#059669"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#eg)"/>
      <path d="M8 16l1.5-4L15 6.5l2.5 2.5L12 14.5z" fill="white" opacity="0.95"/>
      <path d="M8 16l1.5-1.5 1.5 1.5-1.5 1.5z" fill="white" opacity="0.7"/>
      <line x1="13.5" y1="8" x2="16" y2="10.5" stroke="white" stroke-width="1.5"/>
    </svg>""",

    "add": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="ag" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#22d3ee"/>
        <stop offset="100%" stop-color="#0891b2"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#ag)"/>
      <line x1="12" y1="7" x2="12" y2="17" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="7" y1="12" x2="17" y2="12" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
    </svg>""",

    "delete": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="dg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#f87171"/>
        <stop offset="100%" stop-color="#dc2626"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#dg)"/>
      <path d="M8 8l8 8M16 8l-8 8" stroke="white" stroke-width="2.2"
            stroke-linecap="round"/>
    </svg>""",

    "save": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="savg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#a78bfa"/>
        <stop offset="100%" stop-color="#7c3aed"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#savg)"/>
      <rect x="8" y="7" width="8" height="6" rx="1" fill="white" opacity="0.9"/>
      <rect x="10" y="7" width="2" height="3" fill="#7c3aed"/>
      <path d="M7 13v4h10v-4" fill="white" opacity="0.9"/>
    </svg>""",

    "cancel": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="cag" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#f87171"/>
        <stop offset="100%" stop-color="#b91c1c"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#cag)"/>
      <path d="M8 8l8 8M16 8l-8 8" stroke="white" stroke-width="2.2"
            stroke-linecap="round"/>
    </svg>""",

    "checkmark": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="chg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#34d399"/>
        <stop offset="100%" stop-color="#059669"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#chg)"/>
      <polyline points="7,12 10,16 17,8" stroke="white" stroke-width="2.5"
                stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    </svg>""",

    "mute": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="mg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#fb923c"/>
        <stop offset="100%" stop-color="#ea580c"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#mg)"/>
      <path d="M7 10H5v4h2l4 3V7L7 10z" fill="white"/>
      <line x1="15" y1="9" x2="19" y2="15" stroke="white" stroke-width="2"
            stroke-linecap="round"/>
      <line x1="19" y1="9" x2="15" y2="15" stroke="white" stroke-width="2"
            stroke-linecap="round"/>
    </svg>""",

    "volume": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="vg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#34d399"/>
        <stop offset="100%" stop-color="#059669"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#vg)"/>
      <path d="M6 10H4v4h2l3.5 2.5v-9L6 10z" fill="white"/>
      <path d="M14 9a4 4 0 0 1 0 6" stroke="white" stroke-width="1.8"
            stroke-linecap="round" fill="none"/>
      <path d="M16 7a7 7 0 0 1 0 10" stroke="white" stroke-width="1.5"
            stroke-linecap="round" fill="none" opacity="0.7"/>
    </svg>""",

    "sleep": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="slg" cx="40%" cy="35%" r="65%">
        <stop offset="0%" stop-color="#a78bfa"/>
        <stop offset="100%" stop-color="#4c1d95"/>
      </radialGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#slg)"/>
      <circle cx="12" cy="12" r="6" fill="none" stroke="white" stroke-width="1.5"
              opacity="0.6"/>
      <polyline points="12,7 12,12 15,15" stroke="white" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <circle cx="18" cy="6" r="1.2" fill="#fde68a"/>
      <circle cx="20" cy="10" r="0.8" fill="#fde68a" opacity="0.7"/>
      <circle cx="16" cy="4" r="0.7" fill="#fde68a" opacity="0.5"/>
    </svg>""",

    "folder": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="fog" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#fcd34d"/>
        <stop offset="100%" stop-color="#d97706"/>
      </linearGradient></defs>
      <path d="M3 8a2 2 0 0 1 2-2h3.5l2 2H19a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8z"
            fill="url(#fog)"/>
      <path d="M3 8h18v2H3z" fill="#f59e0b" opacity="0.4"/>
    </svg>""",

    "url": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="ug" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#38bdf8"/>
        <stop offset="100%" stop-color="#0284c7"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#ug)"/>
      <line x1="3" y1="12" x2="21" y2="12" stroke="white" stroke-width="1.2" opacity="0.6"/>
      <path d="M12 3C9.5 6.5 9.5 17.5 12 21M12 3C14.5 6.5 14.5 17.5 12 21"
            stroke="white" stroke-width="1.2" fill="none" opacity="0.8"/>
      <ellipse cx="12" cy="12" rx="9" ry="9" fill="none" stroke="white"
               stroke-width="1.5" opacity="0.5"/>
    </svg>""",

    "palette": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="palg" cx="45%" cy="40%" r="60%">
        <stop offset="0%" stop-color="#f0f4ff"/>
        <stop offset="100%" stop-color="#c7d2fe"/>
      </radialGradient></defs>
      <path d="M12 3C7 3 3 7 3 12s4 9 9 9c.6 0 1-.4 1-1 0-.3-.1-.5-.2-.7-.4-.5-.6-1.1-.6-1.8 0-1.5 1.3-2.8 2.8-2.8H17c2.8 0 5-2.2 5-5 0-4.4-4-8-10-8z"
            fill="url(#palg)" stroke="#818cf8" stroke-width="0.8"/>
      <circle cx="7.5" cy="9.5" r="1.8" fill="#f87171"/>
      <circle cx="11.5" cy="6.5" r="1.8" fill="#34d399"/>
      <circle cx="16" cy="8.5" r="1.8" fill="#60a5fa"/>
      <circle cx="17.5" cy="13" r="1.8" fill="#fbbf24"/>
    </svg>""",

    "radio": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="rg2" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#22d3ee"/>
        <stop offset="100%" stop-color="#0e7490"/>
      </linearGradient></defs>
      <rect x="2" y="8" width="20" height="13" rx="2.5" fill="url(#rg2)"/>
      <circle cx="8" cy="14.5" r="3" fill="none" stroke="white" stroke-width="1.5"/>
      <circle cx="8" cy="14.5" r="1.2" fill="white" opacity="0.7"/>
      <line x1="13" y1="11" x2="19" y2="11" stroke="white" stroke-width="1.5"
            stroke-linecap="round" opacity="0.8"/>
      <line x1="13" y1="14" x2="19" y2="14" stroke="white" stroke-width="1.5"
            stroke-linecap="round" opacity="0.8"/>
      <line x1="13" y1="17" x2="17" y2="17" stroke="white" stroke-width="1.5"
            stroke-linecap="round" opacity="0.5"/>
      <path d="M8 8L15 4" stroke="white" stroke-width="1.5" stroke-linecap="round"
            opacity="0.6"/>
    </svg>""",

    "about": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="abg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#a78bfa"/>
        <stop offset="100%" stop-color="#6d28d9"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#abg)"/>
      <circle cx="12" cy="7.5" r="1.5" fill="white"/>
      <line x1="12" y1="11" x2="12" y2="17.5" stroke="white" stroke-width="2.2"
            stroke-linecap="round"/>
    </svg>""",

    "stations": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="stg" cx="40%" cy="35%" r="65%">
        <stop offset="0%" stop-color="#22d3ee"/>
        <stop offset="100%" stop-color="#0e7490"/>
      </radialGradient></defs>
      <circle cx="12" cy="12" r="10" fill="url(#stg)"/>
      <circle cx="12" cy="12" r="6" fill="none" stroke="white"
              stroke-width="1.2" opacity="0.5"/>
      <circle cx="12" cy="12" r="2.5" fill="white" opacity="0.9"/>
      <line x1="12" y1="2.2" x2="12" y2="5.5" stroke="white"
            stroke-width="1.5" stroke-linecap="round"/>
      <line x1="12" y1="18.5" x2="12" y2="21.8" stroke="white"
            stroke-width="1.5" stroke-linecap="round"/>
      <line x1="2.2" y1="12" x2="5.5" y2="12" stroke="white"
            stroke-width="1.5" stroke-linecap="round"/>
      <line x1="18.5" y1="12" x2="21.8" y2="12" stroke="white"
            stroke-width="1.5" stroke-linecap="round"/>
    </svg>""",

    # ═══════════════════════════════════════════════════════════════════════
    # MUZIČKE KATEGORIJE — svaka je jedinstvena vizuelna priča
    # ═══════════════════════════════════════════════════════════════════════

    # 🎸 ROCK — električna gitara, agresivna crvena iskra
    "category_rock": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="rkg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1c1c1c"/>
          <stop offset="100%" stop-color="#3b0a0a"/>
        </linearGradient>
        <linearGradient id="rkg2" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ef4444"/>
          <stop offset="100%" stop-color="#f97316"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#rkg)"/>
      <!-- Gitarsko tijelo -->
      <ellipse cx="9" cy="15" rx="5" ry="4" fill="url(#rkg2)" opacity="0.9"/>
      <ellipse cx="9" cy="15" rx="3" ry="2.5" fill="#7f1d1d" opacity="0.5"/>
      <!-- Vrat gitare -->
      <rect x="12.5" y="5" width="2" height="11" rx="1" fill="#f97316" opacity="0.8"/>
      <rect x="13" y="5" width="1" height="11" rx="0.5" fill="#fbbf24" opacity="0.4"/>
      <!-- Žice -->
      <line x1="13" y1="5" x2="13" y2="14" stroke="#fde68a" stroke-width="0.4" opacity="0.8"/>
      <line x1="14" y1="5" x2="14" y2="14" stroke="#fde68a" stroke-width="0.4" opacity="0.8"/>
      <!-- Munja efekt -->
      <path d="M17 4 L15 10 L17 10 L14 17" stroke="#facc15" stroke-width="1.5"
            stroke-linecap="round" fill="none" opacity="0.9"/>
    </svg>""",

    # 🎵 POP — mikrofon, bubblegum pink
    "category_pop": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="popg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#be185d"/>
          <stop offset="100%" stop-color="#6d28d9"/>
        </linearGradient>
        <radialGradient id="popg2" cx="50%" cy="40%" r="55%">
          <stop offset="0%" stop-color="#f9a8d4"/>
          <stop offset="100%" stop-color="#ec4899"/>
        </radialGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#popg)"/>
      <!-- Mikrofon glava -->
      <ellipse cx="12" cy="9" rx="4" ry="5" fill="url(#popg2)"/>
      <ellipse cx="12" cy="9" rx="4" ry="5" fill="none" stroke="#fbcfe8"
               stroke-width="0.8" opacity="0.6"/>
      <!-- Horizontalne mrežice -->
      <line x1="8" y1="7" x2="16" y2="7" stroke="white" stroke-width="0.6" opacity="0.5"/>
      <line x1="8" y1="9" x2="16" y2="9" stroke="white" stroke-width="0.6" opacity="0.5"/>
      <line x1="8" y1="11" x2="16" y2="11" stroke="white" stroke-width="0.6" opacity="0.5"/>
      <!-- Držač -->
      <line x1="12" y1="14" x2="12" y2="19" stroke="#f9a8d4" stroke-width="1.8"
            stroke-linecap="round"/>
      <line x1="9" y1="19" x2="15" y2="19" stroke="#f9a8d4" stroke-width="1.8"
            stroke-linecap="round"/>
      <!-- Zvjezdice -->
      <circle cx="5" cy="6" r="1" fill="#fde68a" opacity="0.8"/>
      <circle cx="19" cy="8" r="0.8" fill="#fde68a" opacity="0.7"/>
      <circle cx="18" cy="4" r="0.6" fill="#fde68a" opacity="0.5"/>
    </svg>""",

    # 🎤 HIP HOP — EQ valovi, zlatna grila
    "category_hiphop": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="hhg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#18181b"/>
          <stop offset="100%" stop-color="#3f3f46"/>
        </linearGradient>
        <linearGradient id="hhg2" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#fbbf24"/>
          <stop offset="100%" stop-color="#d97706"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#hhg)"/>
      <!-- EQ stupci -->
      <rect x="3" y="16" width="3" height="6" rx="1.5" fill="url(#hhg2)"/>
      <rect x="7.5" y="10" width="3" height="12" rx="1.5" fill="url(#hhg2)" opacity="0.9"/>
      <rect x="12" y="6" width="3" height="16" rx="1.5" fill="url(#hhg2)"/>
      <rect x="16.5" y="13" width="3" height="9" rx="1.5" fill="url(#hhg2)" opacity="0.8"/>
      <!-- Zlatna horizontala -->
      <line x1="2" y1="22.5" x2="22" y2="22.5" stroke="#f59e0b" stroke-width="0.8"
            opacity="0.4"/>
      <!-- Zvučni val na vrhu -->
      <path d="M3 4 Q6 2 9 4 Q12 6 15 4 Q18 2 21 4" stroke="#fbbf24" stroke-width="1.2"
            fill="none" opacity="0.6" stroke-linecap="round"/>
    </svg>""",

    # 🎹 JAZZ — klavijature, noćna atmosfera
    "category_jazz": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="jzg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1c1917"/>
          <stop offset="100%" stop-color="#292524"/>
        </linearGradient>
        <linearGradient id="jzg2" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#fef3c7"/>
          <stop offset="100%" stop-color="#fde68a"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#jzg)"/>
      <!-- Klavijature — bijele tipke -->
      <rect x="2" y="9" width="3" height="12" rx="1" fill="url(#jzg2)"/>
      <rect x="6" y="9" width="3" height="12" rx="1" fill="url(#jzg2)"/>
      <rect x="10" y="9" width="3" height="12" rx="1" fill="url(#jzg2)"/>
      <rect x="14" y="9" width="3" height="12" rx="1" fill="url(#jzg2)"/>
      <rect x="18" y="9" width="3" height="12" rx="1" fill="url(#jzg2)"/>
      <!-- Crne tipke -->
      <rect x="4" y="9" width="2.5" height="7.5" rx="0.8" fill="#1c1917"/>
      <rect x="8" y="9" width="2.5" height="7.5" rx="0.8" fill="#1c1917"/>
      <rect x="16" y="9" width="2.5" height="7.5" rx="0.8" fill="#1c1917"/>
      <rect x="20" y="9" width="2.5" height="7.5" rx="0.8" fill="#1c1917"/>
      <!-- Nota i bljesak -->
      <path d="M14 3 Q16 1 18 3 L17 7 Q15 8 14 6Z" fill="#fbbf24" opacity="0.9"/>
      <path d="M17 7 L17 3" stroke="#fbbf24" stroke-width="1" opacity="0.7"/>
      <!-- Zvjezdice -->
      <circle cx="5" cy="5" r="0.8" fill="#fde68a" opacity="0.6"/>
      <circle cx="10" cy="3" r="0.6" fill="#fde68a" opacity="0.4"/>
    </svg>""",

    # 🎻 CLASSICAL — violina / notni zapisi, elegancija
    "category_classical": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="clg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1e1b4b"/>
          <stop offset="100%" stop-color="#312e81"/>
        </linearGradient>
        <linearGradient id="clg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#c7d2fe"/>
          <stop offset="100%" stop-color="#818cf8"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#clg)"/>
      <!-- Notne linije -->
      <line x1="2" y1="8" x2="22" y2="8" stroke="#6366f1" stroke-width="0.6" opacity="0.5"/>
      <line x1="2" y1="11" x2="22" y2="11" stroke="#6366f1" stroke-width="0.6" opacity="0.5"/>
      <line x1="2" y1="14" x2="22" y2="14" stroke="#6366f1" stroke-width="0.6" opacity="0.5"/>
      <line x1="2" y1="17" x2="22" y2="17" stroke="#6366f1" stroke-width="0.6" opacity="0.5"/>
      <!-- Violinski ključ (G clef) stilizovan -->
      <path d="M8 18 Q6 16 7 13 Q8 10 10 9 Q12 8 11 11 Q10 14 12 15 Q14 16 13 19 Q12 21 10 20 Q8 19 8 18Z"
            fill="url(#clg2)" opacity="0.9"/>
      <line x1="10" y1="7" x2="10" y2="21" stroke="#a5b4fc" stroke-width="1.2"
            stroke-linecap="round" opacity="0.7"/>
      <!-- Nota -->
      <ellipse cx="17" cy="13.5" rx="2" ry="1.4" fill="#c7d2fe" transform="rotate(-15 17 13.5)"/>
      <line x1="18.8" y1="12" x2="18.8" y2="7" stroke="#c7d2fe" stroke-width="1.2"
            stroke-linecap="round"/>
    </svg>""",

    # 💃 DANCE — disco kugla, neonski odsjaji
    "category_dance": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <radialGradient id="dng" cx="50%" cy="50%" r="70%">
          <stop offset="0%" stop-color="#701a75"/>
          <stop offset="100%" stop-color="#1a0033"/>
        </radialGradient>
        <radialGradient id="dng2" cx="40%" cy="35%" r="60%">
          <stop offset="0%" stop-color="#f0abfc"/>
          <stop offset="100%" stop-color="#a855f7"/>
        </radialGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#dng)"/>
      <!-- Disco kugla -->
      <circle cx="12" cy="9" r="5.5" fill="url(#dng2)"/>
      <!-- Refleksija na kugli — mozaik kvadratića -->
      <rect x="9.5" y="6.5" width="1.5" height="1.5" rx="0.2" fill="white" opacity="0.8"/>
      <rect x="11.5" y="6.5" width="1.5" height="1.5" rx="0.2" fill="white" opacity="0.6"/>
      <rect x="9.5" y="8.5" width="1.5" height="1.5" rx="0.2" fill="white" opacity="0.7"/>
      <rect x="11.5" y="8.5" width="1.5" height="1.5" rx="0.2" fill="#f0abfc" opacity="0.9"/>
      <rect x="13.5" y="8.5" width="1.5" height="1.5" rx="0.2" fill="white" opacity="0.5"/>
      <rect x="9.5" y="10.5" width="1.5" height="1.5" rx="0.2" fill="white" opacity="0.5"/>
      <rect x="11.5" y="10.5" width="1.5" height="1.5" rx="0.2" fill="white" opacity="0.8"/>
      <!-- Nit koja drži kuglu -->
      <line x1="12" y1="3.5" x2="12" y2="1" stroke="#e9d5ff" stroke-width="1"
            stroke-linecap="round"/>
      <!-- Odsjaji svetlosti -->
      <line x1="3" y1="13" x2="6" y2="12" stroke="#f0abfc" stroke-width="1.5"
            stroke-linecap="round" opacity="0.7"/>
      <line x1="2" y1="9" x2="5.5" y2="9.5" stroke="#f0abfc" stroke-width="1.2"
            stroke-linecap="round" opacity="0.5"/>
      <line x1="21" y1="13" x2="18" y2="12" stroke="#f0abfc" stroke-width="1.5"
            stroke-linecap="round" opacity="0.7"/>
      <line x1="22" y1="9" x2="18.5" y2="9.5" stroke="#f0abfc" stroke-width="1.2"
            stroke-linecap="round" opacity="0.5"/>
      <!-- Plesnička figura -->
      <circle cx="8" cy="18" r="1.2" fill="#e9d5ff" opacity="0.8"/>
      <path d="M8 19.2 L7 22 M8 19.2 L9.5 21.5" stroke="#e9d5ff" stroke-width="1"
            stroke-linecap="round"/>
      <path d="M8 19.2 L6.5 20.5 M8 19.2 L9.5 20.5" stroke="#e9d5ff" stroke-width="1"
            stroke-linecap="round"/>
    </svg>""",

    # 🌀 TRANCE — spiralni portal, električno plava
    "category_trance": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <radialGradient id="trg" cx="50%" cy="50%" r="75%">
          <stop offset="0%" stop-color="#0c4a6e"/>
          <stop offset="100%" stop-color="#082f49"/>
        </radialGradient>
        <linearGradient id="trg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#38bdf8"/>
          <stop offset="100%" stop-color="#0284c7"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#trg)"/>
      <!-- Koncentrični krugovi koji pulsiraju -->
      <circle cx="12" cy="12" r="9" fill="none" stroke="#0ea5e9" stroke-width="0.8" opacity="0.3"/>
      <circle cx="12" cy="12" r="7" fill="none" stroke="#38bdf8" stroke-width="0.9" opacity="0.5"/>
      <circle cx="12" cy="12" r="5" fill="none" stroke="#7dd3fc" stroke-width="1.1" opacity="0.7"/>
      <circle cx="12" cy="12" r="3" fill="none" stroke="#bae6fd" stroke-width="1.3" opacity="0.85"/>
      <!-- Centralno jezgro -->
      <circle cx="12" cy="12" r="1.8" fill="url(#trg2)"/>
      <circle cx="12" cy="12" r="1" fill="white" opacity="0.9"/>
      <!-- Električni luk gore-dole -->
      <path d="M12 2 Q14 5 12 7 Q10 9 12 11" stroke="#38bdf8" stroke-width="1.2"
            fill="none" stroke-linecap="round" opacity="0.7"/>
      <path d="M12 13 Q14 15 12 17 Q10 19 12 22" stroke="#38bdf8" stroke-width="1.2"
            fill="none" stroke-linecap="round" opacity="0.7"/>
      <!-- Horizontalni električni luk -->
      <path d="M2 12 Q5 10 7 12 Q9 14 11 12" stroke="#7dd3fc" stroke-width="1.2"
            fill="none" stroke-linecap="round" opacity="0.6"/>
      <path d="M13 12 Q15 10 17 12 Q19 14 22 12" stroke="#7dd3fc" stroke-width="1.2"
            fill="none" stroke-linecap="round" opacity="0.6"/>
    </svg>""",

    # 🛸 ELECTRONIC — sintetizerski val + LED glow
    "category_electronic": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="elg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#064e3b"/>
          <stop offset="100%" stop-color="#052e16"/>
        </linearGradient>
        <linearGradient id="elg2" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#10b981"/>
          <stop offset="50%" stop-color="#34d399"/>
          <stop offset="100%" stop-color="#6ee7b7"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#elg)"/>
      <!-- Osciloskop — zvučni val -->
      <path d="M1.5 12 L4 12 L5.5 7 L7 17 L8.5 7 L10 17 L11.5 9 L13 15 L14.5 10 L16 14 L17.5 12 L22.5 12"
            stroke="url(#elg2)" stroke-width="1.8" fill="none" stroke-linecap="round"
            stroke-linejoin="round"/>
      <!-- LED tačkice ispod vala -->
      <circle cx="5.5" cy="18" r="0.8" fill="#10b981" opacity="0.9"/>
      <circle cx="8" cy="18" r="0.8" fill="#34d399" opacity="0.7"/>
      <circle cx="10.5" cy="18" r="0.8" fill="#10b981" opacity="0.9"/>
      <circle cx="13" cy="18" r="0.8" fill="#34d399" opacity="0.7"/>
      <circle cx="15.5" cy="18" r="0.8" fill="#10b981" opacity="0.9"/>
      <circle cx="18" cy="18" r="0.8" fill="#34d399" opacity="0.5"/>
      <!-- Spektralni glow na vrhu -->
      <path d="M4 6 Q7 4 12 5 Q17 6 20 4" stroke="#6ee7b7" stroke-width="0.8"
            fill="none" opacity="0.4" stroke-linecap="round"/>
    </svg>""",

    # ❄️ CHILLOUT — led kristali, hladan plavi
    "category_chillout": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="chg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#0c4a6e"/>
          <stop offset="100%" stop-color="#0e7490"/>
        </linearGradient>
        <linearGradient id="chg3" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#e0f2fe"/>
          <stop offset="100%" stop-color="#7dd3fc"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#chg2)"/>
      <!-- Snježna pahuljica - 6 krakova -->
      <line x1="12" y1="3" x2="12" y2="21" stroke="url(#chg3)" stroke-width="1.5"
            stroke-linecap="round"/>
      <line x1="3" y1="7.5" x2="21" y2="16.5" stroke="url(#chg3)" stroke-width="1.5"
            stroke-linecap="round"/>
      <line x1="3" y1="16.5" x2="21" y2="7.5" stroke="url(#chg3)" stroke-width="1.5"
            stroke-linecap="round"/>
      <!-- Mali krakovi na svakom kraju -->
      <line x1="12" y1="3" x2="10" y2="5.5" stroke="#bae6fd" stroke-width="1"
            stroke-linecap="round"/>
      <line x1="12" y1="3" x2="14" y2="5.5" stroke="#bae6fd" stroke-width="1"
            stroke-linecap="round"/>
      <line x1="12" y1="21" x2="10" y2="18.5" stroke="#bae6fd" stroke-width="1"
            stroke-linecap="round"/>
      <line x1="12" y1="21" x2="14" y2="18.5" stroke="#bae6fd" stroke-width="1"
            stroke-linecap="round"/>
      <line x1="3" y1="7.5" x2="5" y2="9.5" stroke="#bae6fd" stroke-width="1"
            stroke-linecap="round"/>
      <line x1="21" y1="16.5" x2="19" y2="14.5" stroke="#bae6fd" stroke-width="1"
            stroke-linecap="round"/>
      <line x1="3" y1="16.5" x2="5" y2="14.5" stroke="#bae6fd" stroke-width="1"
            stroke-linecap="round"/>
      <line x1="21" y1="7.5" x2="19" y2="9.5" stroke="#bae6fd" stroke-width="1"
            stroke-linecap="round"/>
      <!-- Centralni dijamant -->
      <circle cx="12" cy="12" r="2.5" fill="#7dd3fc" opacity="0.8"/>
      <circle cx="12" cy="12" r="1.2" fill="white" opacity="0.9"/>
    </svg>""",

    # 🌍 WORLD — globus s meridijanima
    "category_world": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <radialGradient id="wlg" cx="40%" cy="35%" r="65%">
          <stop offset="0%" stop-color="#166534"/>
          <stop offset="100%" stop-color="#052e16"/>
        </radialGradient>
        <linearGradient id="wlg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#4ade80"/>
          <stop offset="100%" stop-color="#16a34a"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#wlg)"/>
      <!-- Globus — okean -->
      <circle cx="12" cy="12" r="9" fill="#1d4ed8" opacity="0.7"/>
      <!-- Kontinenti (stilizovani) -->
      <path d="M5 8 Q7 6 10 7 Q12 8 11 11 Q9 13 7 12 Q5 11 5 8Z"
            fill="url(#wlg2)" opacity="0.9"/>
      <path d="M13 6 Q16 5 17 8 Q18 11 16 12 Q14 13 13 10 Q12 8 13 6Z"
            fill="url(#wlg2)" opacity="0.8"/>
      <path d="M8 14 Q10 13 12 15 Q13 17 11 18 Q9 19 8 17 Q7 16 8 14Z"
            fill="url(#wlg2)" opacity="0.85"/>
      <path d="M14 15 Q16 14 17 16 Q17.5 18 16 18.5 Q14.5 19 14 17 Q13.5 16 14 15Z"
            fill="url(#wlg2)" opacity="0.7"/>
      <!-- Meridijani -->
      <circle cx="12" cy="12" r="9" fill="none" stroke="#86efac"
              stroke-width="0.6" opacity="0.4"/>
      <ellipse cx="12" cy="12" rx="5" ry="9" fill="none" stroke="#86efac"
               stroke-width="0.6" opacity="0.35"/>
      <line x1="3" y1="12" x2="21" y2="12" stroke="#86efac" stroke-width="0.6"
            opacity="0.35"/>
    </svg>""",

    # 🤠 COUNTRY — kaubojski šešir, smeđa zemlja
    "category_country": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="cng" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#292524"/>
          <stop offset="100%" stop-color="#1c1917"/>
        </linearGradient>
        <linearGradient id="cng2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#d4a96a"/>
          <stop offset="100%" stop-color="#92400e"/>
        </linearGradient>
        <linearGradient id="cng3" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#b45309"/>
          <stop offset="100%" stop-color="#d97706"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#cng)"/>
      <!-- Kaubojski šešir — obod -->
      <ellipse cx="12" cy="16" rx="10" ry="3" fill="url(#cng2)"/>
      <ellipse cx="12" cy="16" rx="10" ry="3" fill="none" stroke="#78350f"
               stroke-width="0.8" opacity="0.6"/>
      <!-- Tjeme šešira -->
      <path d="M5 16 Q5 9 12 9 Q19 9 19 16" fill="url(#cng3)"/>
      <path d="M5 16 Q5 9 12 9 Q19 9 19 16" fill="none" stroke="#78350f"
            stroke-width="0.8" opacity="0.5"/>
      <!-- Vrpca -->
      <line x1="5" y1="14" x2="19" y2="14" stroke="#78350f" stroke-width="1.5" opacity="0.7"/>
      <!-- Zvjezda šerifa -->
      <path d="M12 10.5 L12.5 12 L14 12 L12.8 12.9 L13.2 14.4 L12 13.5 L10.8 14.4 L11.2 12.9 L10 12 L11.5 12Z"
            fill="#fbbf24" opacity="0.9"/>
      <!-- Sunce u pozadini -->
      <circle cx="19" cy="6" r="2.5" fill="#fbbf24" opacity="0.6"/>
      <line x1="19" y1="2.5" x2="19" y2="3.8" stroke="#fbbf24" stroke-width="1"
            stroke-linecap="round" opacity="0.5"/>
      <line x1="22.5" y1="6" x2="21.2" y2="6" stroke="#fbbf24" stroke-width="1"
            stroke-linecap="round" opacity="0.5"/>
      <line x1="21.3" y1="3.7" x2="20.4" y2="4.6" stroke="#fbbf24" stroke-width="1"
            stroke-linecap="round" opacity="0.5"/>
    </svg>""",

    # 🎷 BLUES — saksofon, noćni klub, plava melanholija
    "category_blues": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="blg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1e3a5f"/>
          <stop offset="100%" stop-color="#0f172a"/>
        </linearGradient>
        <linearGradient id="blg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#93c5fd"/>
          <stop offset="50%" stop-color="#60a5fa"/>
          <stop offset="100%" stop-color="#3b82f6"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#blg)"/>
      <!-- Saksofon tijelo -->
      <path d="M14 3 Q17 3 18 5 Q19 7 18 9 Q17 11 15 12 Q13 13 11 15 Q9 17 9 19 Q9 21 7 21 Q5 21 5 19 Q5 17 7 17 Q8 17 9 17"
            stroke="url(#blg2)" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <!-- Usnik -->
      <rect x="12" y="2" width="3" height="3" rx="1" fill="#93c5fd" opacity="0.8"/>
      <!-- Dugmad saksofona -->
      <circle cx="15.5" cy="8" r="1" fill="#93c5fd" opacity="0.9"/>
      <circle cx="13.5" cy="10.5" r="1" fill="#93c5fd" opacity="0.8"/>
      <circle cx="11.5" cy="13" r="1" fill="#93c5fd" opacity="0.7"/>
      <circle cx="9.5" cy="15.5" r="1" fill="#93c5fd" opacity="0.6"/>
      <!-- Zvučni valovi -->
      <path d="M19 10 Q21 12 20 14" stroke="#60a5fa" stroke-width="1.2"
            fill="none" stroke-linecap="round" opacity="0.6"/>
      <path d="M20 8 Q23 11 22 15" stroke="#93c5fd" stroke-width="0.9"
            fill="none" stroke-linecap="round" opacity="0.4"/>
      <!-- Notna zvjezda -->
      <circle cx="4" cy="7" r="1.5" fill="#60a5fa" opacity="0.5"/>
      <line x1="5.5" y1="7" x2="5.5" y2="3.5" stroke="#60a5fa" stroke-width="1"
            stroke-linecap="round" opacity="0.5"/>
    </svg>""",

    # 🤘 METAL — munja / lubanja, teška atmosfera
    "category_metal": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="mtg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#0c0c0c"/>
          <stop offset="100%" stop-color="#1f0000"/>
        </linearGradient>
        <linearGradient id="mtg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fca5a5"/>
          <stop offset="100%" stop-color="#dc2626"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#mtg)"/>
      <!-- Munja - glavna -->
      <path d="M14 2 L8 12 L12 12 L9 22 L18 10 L13.5 10 Z"
            fill="url(#mtg2)" opacity="0.95"/>
      <!-- Sjena munje -->
      <path d="M14 2 L8 12 L12 12 L9 22 L18 10 L13.5 10 Z"
            fill="none" stroke="#7f1d1d" stroke-width="0.5" opacity="0.4"/>
      <!-- Iskre oko munje -->
      <circle cx="5" cy="5" r="0.8" fill="#f87171" opacity="0.7"/>
      <circle cx="20" cy="7" r="0.6" fill="#f87171" opacity="0.5"/>
      <circle cx="4" cy="15" r="0.7" fill="#f87171" opacity="0.6"/>
      <circle cx="21" cy="18" r="0.5" fill="#f87171" opacity="0.4"/>
      <!-- Tekstura metala -->
      <line x1="2" y1="20" x2="22" y2="20" stroke="#3f3f46" stroke-width="0.5" opacity="0.5"/>
      <line x1="2" y1="22" x2="22" y2="22" stroke="#3f3f46" stroke-width="0.5" opacity="0.3"/>
    </svg>""",

    # 🎺 REGGAE — jamajčanska zastava + muzički ritam
    "category_reggae": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="reg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#14532d"/>
          <stop offset="100%" stop-color="#052e16"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#reg)"/>
      <!-- Jamajčanske boje — 3 trake -->
      <rect x="2" y="4" width="20" height="5" rx="1.5" fill="#dc2626" opacity="0.9"/>
      <rect x="2" y="10" width="20" height="4" rx="0" fill="#f5f5f5" opacity="0.1"/>
      <!-- X dijagonale (Jamajčanska zastava) -->
      <line x1="2" y1="4" x2="22" y2="21" stroke="#1a1a1a" stroke-width="2.5" opacity="0.7"/>
      <line x1="22" y1="4" x2="2" y2="21" stroke="#1a1a1a" stroke-width="2.5" opacity="0.7"/>
      <!-- Zeleni trougli -->
      <path d="M2 4 L12 12.5 L2 21Z" fill="#16a34a" opacity="0.9"/>
      <path d="M22 4 L12 12.5 L22 21Z" fill="#16a34a" opacity="0.9"/>
      <!-- Žuta -->
      <path d="M2 4 L22 4 L12 12.5Z" fill="#eab308" opacity="0.9"/>
      <path d="M2 21 L22 21 L12 12.5Z" fill="#eab308" opacity="0.9"/>
      <!-- Centralni krug -->
      <circle cx="12" cy="12.5" r="2.5" fill="#1a1a1a" opacity="0.8"/>
      <circle cx="12" cy="12.5" r="1.5" fill="#fbbf24" opacity="0.9"/>
    </svg>""",

    # 📰 NEWS — mikrofon + val + Breaking
    "category_news": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="nwg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1e293b"/>
          <stop offset="100%" stop-color="#0f172a"/>
        </linearGradient>
        <linearGradient id="nwg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#f8fafc"/>
          <stop offset="100%" stop-color="#cbd5e1"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#nwg)"/>
      <!-- Mikrofon za vijesti -->
      <rect x="9" y="4" width="6" height="9" rx="3" fill="url(#nwg2)"/>
      <!-- Mrežica mikrofona -->
      <line x1="9.5" y1="7" x2="14.5" y2="7" stroke="#64748b" stroke-width="0.7" opacity="0.6"/>
      <line x1="9.5" y1="9" x2="14.5" y2="9" stroke="#64748b" stroke-width="0.7" opacity="0.6"/>
      <line x1="9.5" y1="11" x2="14.5" y2="11" stroke="#64748b" stroke-width="0.7" opacity="0.6"/>
      <!-- Stativ -->
      <path d="M7 14 Q12 16 17 14" stroke="#94a3b8" stroke-width="1.5"
            stroke-linecap="round" fill="none"/>
      <line x1="12" y1="15.5" x2="12" y2="19" stroke="#94a3b8" stroke-width="1.5"
            stroke-linecap="round"/>
      <line x1="9" y1="20" x2="15" y2="20" stroke="#94a3b8" stroke-width="1.5"
            stroke-linecap="round"/>
      <!-- Radio valovi -->
      <path d="M5.5 9 Q4 12 5.5 15" stroke="#ef4444" stroke-width="1.3"
            fill="none" stroke-linecap="round" opacity="0.8"/>
      <path d="M3.5 7.5 Q1.5 12 3.5 16.5" stroke="#ef4444" stroke-width="1"
            fill="none" stroke-linecap="round" opacity="0.5"/>
      <path d="M18.5 9 Q20 12 18.5 15" stroke="#ef4444" stroke-width="1.3"
            fill="none" stroke-linecap="round" opacity="0.8"/>
      <path d="M20.5 7.5 Q22.5 12 20.5 16.5" stroke="#ef4444" stroke-width="1"
            fill="none" stroke-linecap="round" opacity="0.5"/>
      <!-- Crvena tačka - ON AIR -->
      <circle cx="12" cy="4" r="1.5" fill="#ef4444"/>
      <circle cx="12" cy="4" r="2.5" fill="none" stroke="#ef4444"
              stroke-width="0.8" opacity="0.4"/>
    </svg>""",

    # 🎬 SOUNDTRACKS — klapa za film, zlatna boja
    "category_soundtracks": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="stg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1c1917"/>
          <stop offset="100%" stop-color="#292524"/>
        </linearGradient>
        <linearGradient id="stg3" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fbbf24"/>
          <stop offset="100%" stop-color="#d97706"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#stg2)"/>
      <!-- Klapa za film — tijelo -->
      <rect x="3" y="9" width="18" height="12" rx="1.5" fill="#292524"/>
      <rect x="3" y="9" width="18" height="3" rx="1.5" fill="url(#stg3)"/>
      <!-- Pruge na klapi -->
      <line x1="6.5" y1="9" x2="4.5" y2="5" stroke="url(#stg3)" stroke-width="2.5"
            stroke-linecap="round"/>
      <line x1="10.5" y1="9" x2="8.5" y2="5" stroke="#1c1917" stroke-width="2.5"
            stroke-linecap="round"/>
      <line x1="14.5" y1="9" x2="12.5" y2="5" stroke="url(#stg3)" stroke-width="2.5"
            stroke-linecap="round"/>
      <line x1="18.5" y1="9" x2="16.5" y2="5" stroke="#1c1917" stroke-width="2.5"
            stroke-linecap="round"/>
      <line x1="21.5" y1="9" x2="20" y2="6" stroke="url(#stg3)" stroke-width="2"
            stroke-linecap="round"/>
      <!-- Film traka unutar -->
      <circle cx="12" cy="15.5" r="3" fill="none" stroke="#fbbf24"
              stroke-width="1" opacity="0.6"/>
      <circle cx="12" cy="15.5" r="1.2" fill="#fbbf24" opacity="0.5"/>
      <!-- Notne linije -->
      <line x1="5" y1="14" x2="8" y2="14" stroke="#6b7280" stroke-width="0.7"/>
      <line x1="5" y1="16" x2="8" y2="16" stroke="#6b7280" stroke-width="0.7"/>
      <line x1="5" y1="18" x2="8" y2="18" stroke="#6b7280" stroke-width="0.7"/>
      <line x1="16" y1="14" x2="19" y2="14" stroke="#6b7280" stroke-width="0.7"/>
      <line x1="16" y1="16" x2="19" y2="16" stroke="#6b7280" stroke-width="0.7"/>
      <line x1="16" y1="18" x2="19" y2="18" stroke="#6b7280" stroke-width="0.7"/>
    </svg>""",

    # 🕺 HOUSE — kuća + bass speaker, narandžasta
    "category_house": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="hsg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#7c2d12"/>
          <stop offset="100%" stop-color="#431407"/>
        </linearGradient>
        <linearGradient id="hsg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fb923c"/>
          <stop offset="100%" stop-color="#ea580c"/>
        </linearGradient>
        <radialGradient id="hsg3" cx="50%" cy="50%" r="60%">
          <stop offset="0%" stop-color="#fed7aa"/>
          <stop offset="100%" stop-color="#f97316"/>
        </radialGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#hsg)"/>
      <!-- Krov kuće -->
      <path d="M2 12 L12 3 L22 12" fill="url(#hsg2)" opacity="0.9"/>
      <path d="M2 12 L12 3 L22 12" fill="none" stroke="#c2410c"
            stroke-width="0.6" opacity="0.5"/>
      <!-- Zidovi -->
      <rect x="4.5" y="12" width="15" height="9" rx="0.5" fill="#9a3412" opacity="0.9"/>
      <!-- Vrata -->
      <rect x="10" y="16" width="4" height="5" rx="0.5" fill="#431407"/>
      <circle cx="13.5" cy="18.8" r="0.5" fill="#fbbf24"/>
      <!-- Prozor (zvučnik - speaker grill) -->
      <circle cx="7.5" cy="15" r="2.5" fill="url(#hsg3)" opacity="0.8"/>
      <circle cx="7.5" cy="15" r="1.5" fill="#7c2d12" opacity="0.7"/>
      <circle cx="7.5" cy="15" r="0.7" fill="#fed7aa" opacity="0.8"/>
      <!-- Bass valovi -->
      <path d="M16 14 Q18 15 16 16" stroke="#fb923c" stroke-width="1.2"
            fill="none" stroke-linecap="round" opacity="0.7"/>
      <path d="M17.5" y1="13 Q20.5 15 17.5 17" stroke="#fb923c" stroke-width="0.9"
            fill="none" stroke-linecap="round" opacity="0.5"/>
    </svg>""",

    # 🌿 AMBIENT — šumski zvukovi, zelena tišina
    "category_ambient": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <radialGradient id="amg" cx="50%" cy="60%" r="70%">
          <stop offset="0%" stop-color="#14532d"/>
          <stop offset="100%" stop-color="#052e16"/>
        </radialGradient>
        <linearGradient id="amg2" x1="0%" y1="100%" x2="50%" y2="0%">
          <stop offset="0%" stop-color="#4ade80"/>
          <stop offset="100%" stop-color="#86efac"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#amg)"/>
      <!-- Drvo — deblo -->
      <rect x="11" y="15" width="2" height="7" rx="1" fill="#713f12"/>
      <!-- Krošnja — tri nivoa listova -->
      <ellipse cx="12" cy="14" rx="7" ry="5" fill="url(#amg2)" opacity="0.9"/>
      <ellipse cx="12" cy="10.5" rx="5.5" ry="4" fill="#22c55e" opacity="0.9"/>
      <ellipse cx="12" cy="7.5" rx="4" ry="3.5" fill="#4ade80" opacity="0.95"/>
      <!-- Zvučni val / aura -->
      <circle cx="12" cy="11" r="9.5" fill="none" stroke="#86efac"
              stroke-width="0.8" opacity="0.15"/>
      <!-- Zvjezdice/glitch u lisju -->
      <circle cx="9" cy="8" r="0.7" fill="#bbf7d0" opacity="0.7"/>
      <circle cx="15" cy="9" r="0.6" fill="#bbf7d0" opacity="0.6"/>
      <circle cx="10" cy="12" r="0.5" fill="#bbf7d0" opacity="0.5"/>
      <!-- Maglina u bazi -->
      <ellipse cx="12" cy="22.5" rx="8" ry="2" fill="#16a34a" opacity="0.2"/>
    </svg>""",

    # 🎙️ PODCASTS — studio mikrofon, vijolična
    "category_podcasts": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="pcg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#2e1065"/>
          <stop offset="100%" stop-color="#1e1b4b"/>
        </linearGradient>
        <linearGradient id="pcg2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#c4b5fd"/>
          <stop offset="100%" stop-color="#7c3aed"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#pcg)"/>
      <!-- Mikrofon kapsula — lisnato tijelo -->
      <path d="M8 5 Q8 2 12 2 Q16 2 16 5 L16 13 Q16 16 12 16 Q8 16 8 13 Z"
            fill="url(#pcg2)"/>
      <!-- Mrežica mikrofona -->
      <line x1="8.5" y1="7" x2="15.5" y2="7" stroke="white" stroke-width="0.8" opacity="0.4"/>
      <line x1="8.5" y1="9" x2="15.5" y2="9" stroke="white" stroke-width="0.8" opacity="0.4"/>
      <line x1="8.5" y1="11" x2="15.5" y2="11" stroke="white" stroke-width="0.8" opacity="0.4"/>
      <line x1="8.5" y1="13" x2="15.5" y2="13" stroke="white" stroke-width="0.8" opacity="0.4"/>
      <!-- Krak stativa -->
      <path d="M5.5 12 Q5.5 18 12 18" stroke="#a78bfa" stroke-width="1.5"
            fill="none" stroke-linecap="round"/>
      <path d="M18.5 12 Q18.5 18 12 18" stroke="#a78bfa" stroke-width="1.5"
            fill="none" stroke-linecap="round"/>
      <line x1="12" y1="16" x2="12" y2="22" stroke="#a78bfa" stroke-width="1.5"
            stroke-linecap="round"/>
      <!-- Radio val / podcast signal -->
      <circle cx="12" cy="9" r="7" fill="none" stroke="#c4b5fd"
              stroke-width="0.7" stroke-dasharray="2 3" opacity="0.4"/>
      <!-- Live tačka -->
      <circle cx="12" cy="3.5" r="1.2" fill="#f43f5e"/>
    </svg>""",

    # 🏆 TOP 40 — zvjezda / trofej
    "category_top40": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <radialGradient id="t40g" cx="45%" cy="35%" r="65%">
          <stop offset="0%" stop-color="#713f12"/>
          <stop offset="100%" stop-color="#3f1e07"/>
        </radialGradient>
        <linearGradient id="t40g2" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fef08a"/>
          <stop offset="40%" stop-color="#fbbf24"/>
          <stop offset="100%" stop-color="#d97706"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#t40g)"/>
      <!-- Velika zvjezda -->
      <path d="M12 2 L14.5 8.5 L21.5 9 L16.5 13.5 L18.2 20.5 L12 17 L5.8 20.5 L7.5 13.5 L2.5 9 L9.5 8.5 Z"
            fill="url(#t40g2)"/>
      <!-- Unutrašnja zvjezda sjena -->
      <path d="M12 5 L13.5 9.5 L18.5 9.8 L14.8 12.8 L16 17 L12 14.5 L8 17 L9.2 12.8 L5.5 9.8 L10.5 9.5 Z"
            fill="#fef08a" opacity="0.3"/>
      <!-- Sjaj -->
      <circle cx="9.5" cy="7.5" r="1" fill="white" opacity="0.4"/>
    </svg>""",

    # 🇷🇸 EX-YU — stilizovana Balkanska zastava / muzika
    "category_exyu": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs>
        <linearGradient id="eyg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1e3a5f"/>
          <stop offset="100%" stop-color="#0f2744"/>
        </linearGradient>
      </defs>
      <rect width="24" height="24" rx="5" fill="url(#eyg)"/>
      <!-- Zastava unutar zaobljenog pravougaonika -->
      <rect x="3" y="6" width="18" height="5" rx="0.5" fill="#003DA5" opacity="0.9"/>
      <rect x="3" y="11" width="18" height="5" rx="0" fill="#f5f5f5" opacity="0.9"/>
      <rect x="3" y="16" width="18" height="4" rx="0.5" fill="#C8102E" opacity="0.9"/>
      <!-- Zvjezda petokraka u plavom -->
      <path d="M12 6.5 L12.8 8.7 L15.2 8.7 L13.3 10 L14 12.2 L12 11 L10 12.2 L10.7 10 L8.8 8.7 L11.2 8.7 Z"
            fill="#fbbf24" opacity="0.95"/>
      <!-- Noty / muzika -->
      <path d="M5 19 Q5 17.5 6.5 17.5 Q8 17.5 8 19 Q8 20.5 6.5 20.5 Q5 20.5 5 19Z"
            fill="none" stroke="white" stroke-width="1" opacity="0.7"/>
      <line x1="8" y1="15" x2="8" y2="19" stroke="white" stroke-width="1"
            stroke-linecap="round" opacity="0.7"/>
      <line x1="8" y1="15" x2="10" y2="14.5" stroke="white" stroke-width="1"
            stroke-linecap="round" opacity="0.7"/>
    </svg>""",

    # ═══════════════════════════════════════════════════════════════════════
    # TEME — mini preview koji odražava paletu teme
    # ═══════════════════════════════════════════════════════════════════════

    "theme_teal": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="ttg" cx="40%" cy="35%" r="70%">
        <stop offset="0%" stop-color="#2dd4bf"/>
        <stop offset="100%" stop-color="#0f766e"/>
      </radialGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#ttg)"/>
      <path d="M6 12 Q9 6 12 12 Q15 18 18 12" fill="none" stroke="white"
            stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    "theme_midnight": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="mng" cx="50%" cy="50%" r="70%">
        <stop offset="0%" stop-color="#312e81"/>
        <stop offset="100%" stop-color="#0f0a1e"/>
      </radialGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#mng)"/>
      <path d="M15 6a7 7 0 1 1-9 9A8 8 0 0 0 15 6z" fill="#c7d2fe" opacity="0.9"/>
      <circle cx="7" cy="5" r="0.8" fill="white" opacity="0.9"/>
      <circle cx="18" cy="8" r="0.6" fill="white" opacity="0.7"/>
      <circle cx="16" cy="4" r="0.5" fill="white" opacity="0.5"/>
      <circle cx="5" cy="10" r="0.4" fill="white" opacity="0.4"/>
    </svg>""",

    "theme_ocean": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="ocg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0369a1"/>
        <stop offset="100%" stop-color="#0c4a6e"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#ocg)"/>
      <path d="M3 14 Q7 10 11 14 Q15 18 19 14 Q21 12 21 13" fill="none"
            stroke="#7dd3fc" stroke-width="2" stroke-linecap="round"/>
      <path d="M3 17 Q7 13 11 17 Q15 21 19 17" fill="none"
            stroke="#bae6fd" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
    </svg>""",

    "theme_forest": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="frg" cx="50%" cy="60%" r="70%">
        <stop offset="0%" stop-color="#166534"/>
        <stop offset="100%" stop-color="#052e16"/>
      </radialGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#frg)"/>
      <path d="M12 4 L17 12 L14 12 L18 19 L6 19 L10 12 L7 12 Z"
            fill="#4ade80" opacity="0.9"/>
      <rect x="11" y="19" width="2" height="3" rx="0.5" fill="#713f12"/>
    </svg>""",

    "theme_dracula": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="drg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#282a36"/>
        <stop offset="100%" stop-color="#191a24"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#drg)"/>
      <path d="M12 4 L10 8 L12 6.5 L14 8 Z" fill="#ff79c6"/>
      <ellipse cx="12" cy="14" rx="5.5" ry="4.5" fill="#44475a"/>
      <circle cx="9" cy="12" r="1.5" fill="#ff5555" opacity="0.8"/>
      <circle cx="15" cy="12" r="1.5" fill="#ff5555" opacity="0.8"/>
      <path d="M9 16 Q12 19 15 16" fill="#ff79c6" opacity="0.6"/>
    </svg>""",

    "theme_nord": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="ndg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#2e3440"/>
        <stop offset="100%" stop-color="#1e2330"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#ndg)"/>
      <!-- Aurora borealis -->
      <path d="M2 14 Q6 8 10 12 Q14 16 18 10 Q20 8 22 10" fill="none"
            stroke="#88c0d0" stroke-width="1.8" stroke-linecap="round" opacity="0.8"/>
      <path d="M2 17 Q6 11 10 15 Q14 19 18 13 Q20 11 22 13" fill="none"
            stroke="#5e81ac" stroke-width="1.2" stroke-linecap="round" opacity="0.5"/>
      <circle cx="7" cy="6" r="1" fill="#ebcb8b" opacity="0.8"/>
      <circle cx="17" cy="5" r="0.7" fill="#ebcb8b" opacity="0.6"/>
      <circle cx="4" cy="9" r="0.5" fill="white" opacity="0.5"/>
      <circle cx="20" cy="8" r="0.5" fill="white" opacity="0.5"/>
    </svg>""",

    "theme_solarized": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="solg" cx="50%" cy="50%" r="70%">
        <stop offset="0%" stop-color="#fdf6e3"/>
        <stop offset="100%" stop-color="#eee8d5"/>
      </radialGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#solg)"/>
      <circle cx="12" cy="12" r="4.5" fill="#b58900"/>
      <g stroke="#b58900" stroke-width="2" stroke-linecap="round">
        <line x1="12" y1="3" x2="12" y2="5.5"/>
        <line x1="12" y1="18.5" x2="12" y2="21"/>
        <line x1="3" y1="12" x2="5.5" y2="12"/>
        <line x1="18.5" y1="12" x2="21" y2="12"/>
        <line x1="5.6" y1="5.6" x2="7.4" y2="7.4"/>
        <line x1="16.6" y1="16.6" x2="18.4" y2="18.4"/>
        <line x1="18.4" y1="5.6" x2="16.6" y2="7.4"/>
        <line x1="7.4" y1="16.6" x2="5.6" y2="18.4"/>
      </g>
      <circle cx="12" cy="12" r="2.5" fill="#cb4b16"/>
    </svg>""",

    "theme_sunset": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="sug" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#7c3aed"/>
        <stop offset="40%" stop-color="#db2777"/>
        <stop offset="100%" stop-color="#ea580c"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#sug)"/>
      <path d="M3 15 Q8 9 12 13 Q16 17 21 11" fill="none"
            stroke="#fbbf24" stroke-width="1.5" stroke-linecap="round" opacity="0.8"/>
      <circle cx="12" cy="9" r="3.5" fill="#fbbf24" opacity="0.6"/>
      <line x1="4" y1="18" x2="20" y2="18" stroke="#fbbf24" stroke-width="1.5"
            opacity="0.4" stroke-linecap="round"/>
    </svg>""",

    "theme_rose": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="rog" cx="45%" cy="40%" r="65%">
        <stop offset="0%" stop-color="#881337"/>
        <stop offset="100%" stop-color="#4c0519"/>
      </radialGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#rog)"/>
      <circle cx="12" cy="10.5" rx="4" ry="4" r="3.8" fill="#fb7185"/>
      <circle cx="9" cy="13.5" r="2.8" fill="#f43f5e" opacity="0.8"/>
      <circle cx="15" cy="13.5" r="2.8" fill="#f43f5e" opacity="0.8"/>
      <circle cx="12" cy="16" r="2.2" fill="#be123c" opacity="0.7"/>
      <circle cx="12" cy="10.5" r="1.2" fill="#fda4af" opacity="0.6"/>
    </svg>""",

    "theme_cyberpunk": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="cpg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#09090b"/>
        <stop offset="100%" stop-color="#18181b"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#cpg)"/>
      <path d="M12 3 L20 12 L12 21 L4 12 Z" fill="none"
            stroke="#facc15" stroke-width="1.5"/>
      <path d="M12 6 L18 12 L12 18 L6 12 Z" fill="#facc15" opacity="0.15"/>
      <line x1="3" y1="12" x2="21" y2="12" stroke="#e879f9"
            stroke-width="0.8" opacity="0.5"/>
      <line x1="12" y1="3" x2="12" y2="21" stroke="#e879f9"
            stroke-width="0.8" opacity="0.5"/>
      <circle cx="12" cy="12" r="2" fill="#facc15" opacity="0.8"/>
    </svg>""",

    "theme_gruvbox": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="gvg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#282828"/>
        <stop offset="100%" stop-color="#1d2021"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#gvg)"/>
      <rect x="5.5" y="7" width="3.5" height="11" rx="1.5" fill="#d79921" opacity="0.9"/>
      <rect x="10.5" y="4.5" width="3.5" height="13.5" rx="1.5" fill="#98971a" opacity="0.9"/>
      <rect x="15.5" y="9" width="3.5" height="9" rx="1.5" fill="#cc241d" opacity="0.9"/>
      <line x1="4" y1="20" x2="20" y2="20" stroke="#a89984" stroke-width="1" opacity="0.4"/>
    </svg>""",

    "theme_catppuccin": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="catg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1e1e2e"/>
        <stop offset="100%" stop-color="#181825"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#catg)"/>
      <circle cx="9" cy="10" r="2" fill="#cba6f7"/>
      <circle cx="15" cy="10" r="2" fill="#cba6f7"/>
      <circle cx="9" cy="10" r="0.8" fill="#1e1e2e"/>
      <circle cx="15" cy="10" r="0.8" fill="#1e1e2e"/>
      <path d="M8.5 14 Q12 18 15.5 14" fill="none" stroke="#f38ba8"
            stroke-width="1.8" stroke-linecap="round"/>
      <path d="M10 7 L12 4.5 L14 7" fill="none" stroke="#cba6f7"
            stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
      <ellipse cx="9.5" cy="13" rx="2" ry="0.6" fill="#fab387" opacity="0.6"/>
      <ellipse cx="14.5" cy="13" rx="2" ry="0.6" fill="#fab387" opacity="0.6"/>
    </svg>""",

    "theme_lavender": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="lvg" cx="50%" cy="40%" r="70%">
        <stop offset="0%" stop-color="#4c1d95"/>
        <stop offset="100%" stop-color="#2e1065"/>
      </radialGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#lvg)"/>
      <ellipse cx="12" cy="14" rx="5.5" ry="6.5" fill="#c084fc" opacity="0.35"/>
      <ellipse cx="9" cy="10.5" rx="2.2" ry="3.8" fill="#a855f7" opacity="0.6"
               transform="rotate(-20 9 10.5)"/>
      <ellipse cx="15" cy="10.5" rx="2.2" ry="3.8" fill="#a855f7" opacity="0.6"
               transform="rotate(20 15 10.5)"/>
      <ellipse cx="12" cy="9.5" rx="1.8" ry="3" fill="#c084fc" opacity="0.7"/>
      <line x1="12" y1="20.5" x2="12" y2="23" stroke="#7c3aed" stroke-width="1.5"
            stroke-linecap="round"/>
    </svg>""",

    "theme_monokai": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="mog" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#272822"/>
        <stop offset="100%" stop-color="#1e1f1a"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#mog)"/>
      <!-- Kod linije u stilu Monokai -->
      <rect x="4" y="7" width="5" height="1.5" rx="0.7" fill="#f92672"/>
      <rect x="10.5" y="7" width="8" height="1.5" rx="0.7" fill="#a6e22e"/>
      <rect x="4" y="10.5" width="3" height="1.5" rx="0.7" fill="#66d9e8"/>
      <rect x="8.5" y="10.5" width="6" height="1.5" rx="0.7" fill="#fd971f"/>
      <rect x="16" y="10.5" width="3" height="1.5" rx="0.7" fill="#a6e22e"/>
      <rect x="4" y="14" width="7" height="1.5" rx="0.7" fill="#ae81ff"/>
      <rect x="12.5" y="14" width="4" height="1.5" rx="0.7" fill="#f92672"/>
      <rect x="4" y="17.5" width="4" height="1.5" rx="0.7" fill="#66d9e8"/>
      <rect x="9.5" y="17.5" width="9" height="1.5" rx="0.7" fill="#f8f8f2" opacity="0.5"/>
    </svg>""",

    "theme_material": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="matg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#263238"/>
        <stop offset="100%" stop-color="#1a2529"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#matg)"/>
      <rect x="4.5" y="4.5" width="6" height="6" rx="1.5" fill="#80cbc4"/>
      <rect x="13.5" y="4.5" width="6" height="6" rx="1.5" fill="#f48fb1"/>
      <rect x="4.5" y="13.5" width="6" height="6" rx="1.5" fill="#ffcc02"/>
      <rect x="13.5" y="13.5" width="6" height="6" rx="1.5" fill="#80deea"/>
      <circle cx="12" cy="12" r="2" fill="#263238"/>
    </svg>""",

    "theme_tokyo": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="tyg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1a1b26"/>
        <stop offset="100%" stop-color="#13131e"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#tyg)"/>
      <!-- Neon znakovi Tokija -->
      <circle cx="7" cy="9" r="1.3" fill="#7aa2f7" opacity="0.9"/>
      <circle cx="14" cy="6.5" r="0.9" fill="#bb9af7" opacity="0.8"/>
      <circle cx="18" cy="10" r="1.1" fill="#7dcfff" opacity="0.8"/>
      <circle cx="5" cy="14" r="0.8" fill="#e0af68" opacity="0.7"/>
      <circle cx="20" cy="15" r="0.7" fill="#9ece6a" opacity="0.7"/>
      <!-- Neon linija horizonta -->
      <path d="M2 16 Q5 12 8 15 Q11 18 14 14 Q17 10 20 13 Q21.5 14 22 15"
            stroke="#7aa2f7" stroke-width="1.5" fill="none" stroke-linecap="round"/>
      <!-- Odsjaj u vodi -->
      <path d="M4 18 Q8 16 12 17.5 Q16 19 20 18" stroke="#7aa2f7"
            stroke-width="0.8" fill="none" opacity="0.3"/>
    </svg>""",

    "theme_macos": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><radialGradient id="macg" cx="40%" cy="35%" r="65%">
        <stop offset="0%" stop-color="#f8f8f8"/>
        <stop offset="100%" stop-color="#e5e5ea"/>
      </radialGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#macg)"/>
      <!-- macOS traffic lights -->
      <circle cx="7.5" cy="10" r="2.5" fill="#ff5f56"/>
      <circle cx="7.5" cy="10" r="1.2" fill="#ff3b30" opacity="0.4"/>
      <circle cx="13.5" cy="10" r="2.5" fill="#ffbd2e"/>
      <circle cx="13.5" cy="10" r="1.2" fill="#ff9500" opacity="0.4"/>
      <circle cx="19.5" cy="10" r="2.5" fill="#27c93f"/>
      <circle cx="19.5" cy="10" r="1.2" fill="#28cd41" opacity="0.4"/>
      <!-- Dock -->
      <rect x="5" y="15" width="14" height="5" rx="2.5" fill="white" opacity="0.6"/>
      <circle cx="8.5" cy="17.5" r="1.5" fill="#007aff"/>
      <circle cx="12" cy="17.5" r="1.5" fill="#ff2d55"/>
      <circle cx="15.5" cy="17.5" r="1.5" fill="#34c759"/>
    </svg>""",

    "theme_windows": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="wing" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0067c0"/>
        <stop offset="100%" stop-color="#0078d4"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#wing)"/>
      <!-- Windows 11 logo - 4 kvadrata -->
      <rect x="4.5" y="4.5" width="6.5" height="6.5" rx="1.2" fill="white" opacity="0.92"/>
      <rect x="13" y="4.5" width="6.5" height="6.5" rx="1.2" fill="white" opacity="0.75"/>
      <rect x="4.5" y="13" width="6.5" height="6.5" rx="1.2" fill="white" opacity="0.75"/>
      <rect x="13" y="13" width="6.5" height="6.5" rx="1.2" fill="white" opacity="0.6"/>
    </svg>""",

    "theme_minimal": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
      <defs><linearGradient id="ming" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#27272a"/>
        <stop offset="100%" stop-color="#18181b"/>
      </linearGradient></defs>
      <circle cx="12" cy="12" r="11" fill="url(#ming)"/>
      <circle cx="12" cy="12" r="5" fill="none" stroke="#52525b" stroke-width="1.2"/>
      <circle cx="12" cy="12" r="2.5" fill="none" stroke="#71717a" stroke-width="1"/>
      <circle cx="12" cy="12" r="1" fill="#a1a1aa"/>
      <line x1="12" y1="2" x2="12" y2="4" stroke="#52525b" stroke-width="1.2"
            stroke-linecap="round"/>
      <line x1="12" y1="20" x2="12" y2="22" stroke="#52525b" stroke-width="1.2"
            stroke-linecap="round"/>
      <line x1="2" y1="12" x2="4" y2="12" stroke="#52525b" stroke-width="1.2"
            stroke-linecap="round"/>
      <line x1="20" y1="12" x2="22" y2="12" stroke="#52525b" stroke-width="1.2"
            stroke-linecap="round"/>
    </svg>""",

}

# ───────────────────────────────────────────────────────────────────────────
# MAPIRANJA
# ───────────────────────────────────────────────────────────────────────────

CATEGORY_ICON_MAP = {
    "🇷🇸 EX-YU":        "category_exyu",
    "🎸 Rock":           "category_rock",
    "🎵 Pop":            "category_pop",
    "🎤 Hip Hop & R&B": "category_hiphop",
    "🎹 Jazz":           "category_jazz",
    "🎻 Classical":      "category_classical",
    "💃 Dance":          "category_dance",
    "🌀 Trance":         "category_trance",
    "🛸 Electronic":     "category_electronic",
    "❄️ Chillout":       "category_chillout",
    "🌍 World Music":    "category_world",
    "🤠 Country":        "category_country",
    "🎷 Blues":          "category_blues",
    "🤘 Metal":          "category_metal",
    "🎺 Reggae":         "category_reggae",
    "📰 News & Talk":    "category_news",
    "🎬 Soundtracks":    "category_soundtracks",
    "🕺 House":          "category_house",
    "🌿 Ambient":        "category_ambient",
    "🎙️ Podcasts":       "category_podcasts",
    "🏆 Top 40":         "category_top40",
}

THEME_ICON_MAP = {
    "teal":       "theme_teal",
    "midnight":   "theme_midnight",
    "ocean":      "theme_ocean",
    "forest":     "theme_forest",
    "dracula":    "theme_dracula",
    "nord":       "theme_nord",
    "solarized":  "theme_solarized",
    "sunset":     "theme_sunset",
    "rose":       "theme_rose",
    "cyberpunk":  "theme_cyberpunk",
    "gruvbox":    "theme_gruvbox",
    "catppuccin": "theme_catppuccin",
    "lavender":   "theme_lavender",
    "monokai":    "theme_monokai",
    "material":   "theme_material",
    "tokyo":      "theme_tokyo",
    "macos":      "theme_macos",
    "windows":    "theme_windows",
    "minimal":    "theme_minimal",
}

# ───────────────────────────────────────────────────────────────────────────
# RENDERER
# ───────────────────────────────────────────────────────────────────────────

_icon_cache: dict = {}


def _render_svg(svg_string: str, size: int = 20) -> QPixmap:
    cache_key = (id(svg_string), size)
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]
    renderer = QSvgRenderer(QByteArray(svg_string.encode("utf-8")))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()
    _icon_cache[cache_key] = pixmap
    return pixmap


def get_icon(name: str, size: int = 20) -> QIcon:
    svg = _SVG.get(name)
    if not svg:
        logger.debug(f"Icon '{name}' not in registry")
        return QIcon()
    return QIcon(_render_svg(svg, size))


def get_pixmap(name: str, size: int = 20) -> QPixmap:
    svg = _SVG.get(name)
    if not svg:
        return QPixmap()
    return _render_svg(svg, size)


def _strip_emoji(text: str) -> str:
    return _re.sub(
        r'^[\U0001F000-\U0001FFFF\U00002600-\U000027FF\U00002B00-\U00002BFF'
        r'\U0001F1E0-\U0001F1FF\uFE0F\u20E3\u200D\s]+',
        '', text
    ).strip()


_CATEGORY_BARE_MAP: dict = {}


def _ensure_bare_map():
    if _CATEGORY_BARE_MAP:
        return
    for full_name, key in CATEGORY_ICON_MAP.items():
        _CATEGORY_BARE_MAP[_strip_emoji(full_name).lower()] = key


def get_category_icon(category_name: str, size: int = 18) -> QIcon:
    icon_key = CATEGORY_ICON_MAP.get(category_name)
    if not icon_key:
        _ensure_bare_map()
        q = _strip_emoji(category_name).lower()
        icon_key = _CATEGORY_BARE_MAP.get(q)
    if not icon_key:
        q_words = set(_strip_emoji(category_name).lower().split())
        best_key, best_score = None, 0
        for bare, key in _CATEGORY_BARE_MAP.items():
            bw = set(bare.split())
            overlap = len(bw & q_words)
            if overlap > 0 and overlap == len(bw) and overlap > best_score:
                best_score, best_key = overlap, key
        icon_key = best_key or "radio"
    return get_icon(icon_key, size)


def get_theme_icon(theme_name: str, size: int = 18) -> QIcon:
    icon_key = THEME_ICON_MAP.get(theme_name.lower(), "palette")
    return get_icon(icon_key, size)


def clear_cache():
    _icon_cache.clear()