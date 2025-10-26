burgerqueen/
├── .venv/
├── .gitignore
├── requirements.txt
├── burgerqueen.db
├── schema.sql                   # database creation + dummy data
├── main.py                      # entry point (main loop)
│
├── modules/                     # Python modules (logic split)
│   ├── database.py              # handles DB connections and queries
│   ├── user.py                  # handles user registration/login
│   ├── order.py                 # handles order logic
│   ├── inventory.py             # handles ingredient tracking
│   └── auth.py                  # handles password hashing and verification
│
└── utils/
    ├── menu.py                  # text-based user interface
    └── helpers.py               # input validation, small utility functions