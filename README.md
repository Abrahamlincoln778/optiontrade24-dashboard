# OptionTrade24 💹

OptionTrade24 is a secure, client-facing crypto profit dashboard that allows users to log in, view their daily profit (e.g. +$500/day), and track performance. Built with FastAPI, Jinja2, and SQLAlchemy, it includes a full admin panel to manually update client balances and manage user activity.

---

## 🔧 Features

- 🔐 Secure user authentication (bcrypt + session-based)
- 📈 Client dashboard with real-time profit updates
- ⚙️ Admin panel for managing client balances and messages
- 📬 Email notifications for user registration and support
- 🗂️ Contact support form with admin-side message review
- 📦 Clean project structure and scalable backend

---

## 🚀 Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Uvicorn
- **Frontend:** Jinja2 (HTML templating)
- **Database:** SQLite (can scale to PostgreSQL)
- **Auth:** Session-based login, bcrypt hashing
- **Misc:** dotenv, SMTP email support, python-multipart

---

## 🛠 Environment Variables

Make sure to create a `.env` file in the root directory with the following:

```env
SECRET_KEY=supersecurefallbackkey123
SMTP_USER=optiontrade24.online@gmail.com
SMTP_PASSWORD=your_app_password_here
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587