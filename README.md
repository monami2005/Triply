# TripSplit Pro v2.2 - Expense Splitting for Travel Groups

TripSplit Pro v2.2 is a premium SaaS-style web application for managing and splitting trip expenses among travel groups. Built with a modern UI and a Flask backend, it is fully compatible with Vercel deployment.

## Features

- **Premium Dashboard**: Real-time expense summaries, balance sheets, and date-wise filtering.
- **Member Management**: Add/Edit/Delete members with photo upload and WhatsApp integration.
- **Expense Splitting**: Advanced split calculation engine with multi-select participant support.
- **WhatsApp Integration**: Bulk send expense summaries to members with one click.
- **Message Templates**: Fully customizable message templates for WhatsApp notifications.
- **Modern UI/UX**: Responsive sidebar navigation, dark/light mode, and smooth animations.

## Tech Stack

- **Frontend**: HTML5, CSS3 (Modern Premium UI), Vanilla JavaScript.
- **Backend**: Python (Flask) in Vercel Serverless environment.
- **Database**: SQLite (Local) / Compatible with PostgreSQL/Supabase (Production).

## Vercel Deployment

1. **Install Vercel CLI**: `npm i -g vercel`
2. **Connect to Vercel**: `vercel login`
3. **Deploy**: `vercel`

## Setup Instructions

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run locally: `python api/index.py` (for direct Flask testing) or `vercel dev`.

## Changelog v2.2

- Premium Dashboard UI redesign.
- Member Photo Upload logic.
- Date-wise Expense Filtering.
- WhatsApp Bulk Messaging integration.
- Message Template Manager.
- Theme + Timezone Settings.
- Improved Split Calculation Engine.