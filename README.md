# DoWH Staff Intranet Portal

> Custom Frappe app powering the Department of Works & Highways (PNG) staff intranet portal at [erpnext.kumi-tech.com](https://erpnext.kumi-tech.com).

## Features

### 📢 Staff Circulars & Announcements (`/announcements`)
- Government bulletin-style layout with masthead
- Circular number assignments (auto-generated)
- Classification system: For Information, For Action, Urgent
- Wing and classification filtering
- Tag cloud with clickable filters
- Quick statistics widget (total, urgent, action required)
- Recent documents integration with Frappe Wiki

### 👥 Staff Directory (`/directory`)
- Search by name, department, or title
- Wing-level filter tabs
- Per-wing staff counts
- Employee cards with avatar, contact links
- Grid layout (responsive)

### 📁 Document Library (`/wiki`)
- Powered by Frappe Wiki 3.0
- Wing-specific Wiki Spaces

### 🔐 Authentication
- All portal pages are login-gated
- Guest users redirected to branded DoWH login page
- Custom DoWH login template

## Tech Stack

- **Framework:** Frappe 16.x
- **Platform:** ERPNext 16.x
- **Database:** MariaDB
- **Runtime:** Docker (erpnext docker compose)
- **Deployment:** VPS + Cloudflare Tunnel

## App Structure

```
dohw_intranet/
├── dohw_intranet/
│   ├── hooks.py              # App config, home_page, auth hooks
│   ├── modules.txt
│   ├── doctype/
│   │   └── announcement/     # Announcement DocType (JSON + Python)
│   ├── templates/
│   │   └── dohw_base.html    # Branded base template (navbar, sidebar, footer)
│   └── www/
│       ├── announcements.py  # Announcements controller + context
│       ├── announcements.html
│       ├── directory.py      # Staff directory controller
│       └── directory.html
├── pyproject.toml
└── license.txt
```

## Branding

- **Primary:** DoWH Gold (#FFBF00)
- **Dark:** #1A1A1A
- **Font:** Inter
- **Logo:** DoWH official seal (SVG)
- **Style:** Government bulletin — formal, numbered circulars, classification badges

## Getting Started

```bash
# Install on existing ERPNext site
bench get-app https://github.com/Amesi/dohw-intranet.git
bench --site your-site install-app dohw_intranet
bench --site your-site migrate
bench build
bench restart
```

## Deployment

Deployed at: `https://erpnext.kumi-tech.com`

```bash
# Restart after code changes
ssh root@76.13.197.207 "docker exec erpnext-backend-1 bench --site erpnext.kumi-tech.com clear-cache"
ssh root@76.13.197.207 "docker restart erpnext-backend-1"
```

## License

MIT — Department of Works & Highways, Papua New Guinea
