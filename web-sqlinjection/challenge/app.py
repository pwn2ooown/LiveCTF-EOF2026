from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_PATH = '/tmp/database.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email) VALUES (1, 'admin', 'super_secret_password', 'admin@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email) VALUES (2, 'user', 'user123', 'user@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email) VALUES (3, 'guest', 'guest', 'guest@example.com')")
    conn.commit()
    conn.close()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQL Injection Demo</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: rgba(148, 163, 184, 0.1);
            --code-bg: #1e1e1e;
            --error-bg: rgba(239, 68, 68, 0.1);
            --error-text: #f87171;
            --success-bg: rgba(34, 197, 94, 0.1);
            --success-text: #4ade80;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem;
            line-height: 1.6;
        }

        .container {
            width: 100%;
            max-width: 900px;
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 2.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: fadeIn 0.6s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        header {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        h1 {
            font-size: 2.25rem;
            font-weight: 700;
            background: linear-gradient(to right, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            letter-spacing: -0.025em;
        }

        .tagline {
            color: var(--text-muted);
            font-size: 1rem;
        }

        .alert-box {
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 0.95rem;
        }

        .alert-box code {
            background: rgba(0, 0, 0, 0.3);
            padding: 0.2rem 0.4rem;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            color: #c7d2fe;
            font-size: 0.85em;
        }

        .search-container {
            position: relative;
            margin-bottom: 2rem;
        }

        form {
            display: flex;
            gap: 1rem;
            background: rgba(0,0,0,0.2);
            padding: 0.5rem;
            border-radius: 16px;
            border: 1px solid var(--border);
            transition: border-color 0.3s ease;
        }

        form:focus-within {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }

        input[type="text"] {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-main);
            padding: 0.75rem 1rem;
            font-size: 1rem;
            font-family: 'Inter', sans-serif;
            outline: none;
        }

        input[type="text"]::placeholder {
            color: var(--text-muted);
        }

        button {
            background: var(--primary);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.95rem;
        }

        button:hover {
            background: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }
        
        button:active {
            transform: translateY(0);
        }

        .section-title {
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .code-block {
            background: var(--code-bg);
            border-radius: 12px;
            padding: 1.25rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #e2e8f0;
            overflow-x: auto;
            border: 1px solid var(--border);
            margin-bottom: 2rem;
            position: relative;
        }
        
        .code-block::before {
            content: "SQL";
            position: absolute;
            top: 0;
            right: 0;
            background: rgba(255,255,255,0.05);
            padding: 0.25rem 0.5rem;
            font-size: 0.7rem;
            border-bottom-left-radius: 8px;
            color: var(--text-muted);
        }

        .error-message {
            background: var(--error-bg);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: var(--error-text);
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            font-size: 0.95rem;
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
        }

        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 1rem;
        }

        th {
            text-align: left;
            padding: 1rem;
            color: var(--text-muted);
            font-weight: 500;
            font-size: 0.875rem;
            border-bottom: 1px solid var(--border);
        }

        td {
            padding: 1rem;
            color: var(--text-main);
            border-bottom: 1px solid var(--border);
            transition: background-color 0.2s;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background-color: rgba(255,255,255,0.03);
        }
        
        .empty-state {
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-style: italic;
        }
        
        .badge {
            display: inline-block;
            padding: 0.25em 0.6em;
            font-size: 0.75em;
            font-weight: 700;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 0.375rem;
            color: #fff;
            background-color: rgba(255,255,255,0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>SQL Injection Demo</h1>
            <p class="tagline">Explore vulnerabilities in a safe environment</p>
        </header>
        
        <div class="search-container">
            <form method="POST">
                <input type="text" id="searchInput" name="search" placeholder="Search by username (try ' OR '1'='1)..." value="{{ search_term }}" autocomplete="off">
                <button type="submit">Execute Query</button>
            </form>
        </div>

        <div class="code-block" id="liveQueryBlock">
            <span style="color: #c7d2fe;">SELECT</span> id, username, email <span style="color: #c7d2fe;">FROM</span> users <span style="color: #c7d2fe;">WHERE</span> username = '<span id="dynamicInput" style="color: #f472b6; font-weight: bold; text-shadow: 0 0 10px rgba(244, 114, 182, 0.5);"></span>'
        </div>
        
        <script>
            const searchInput = document.getElementById('searchInput');
            const dynamicInput = document.getElementById('dynamicInput');
            
            // Initialize with current value if any
            dynamicInput.textContent = searchInput.value;
            
            searchInput.addEventListener('input', (e) => {
                dynamicInput.textContent = e.target.value;
            });
        </script>
        
        {% if query %}
        <div class="section-title">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"></polyline><line x1="12" y1="19" x2="20" y2="19"></line></svg>
            Executed Query
        </div>
        <div class="code-block" style="opacity: 0.7;">{{ query }}</div>
        {% endif %}
        
        {% if error %}
        <div class="error-message">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
            <div>
                <strong>SQL Error:</strong> {{ error }}
            </div>
        </div>
        {% endif %}
        
        {% if results is not none %}
            <div class="section-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
                Results <span class="badge" style="margin-left: 8px">{{ results|length }}</span>
            </div>
            
            {% if results %}
            <table>
                <thead>
                    <tr>
                        <th width="10%">ID</th>
                        <th width="40%">Username</th>
                        <th width="50%">Email</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in results %}
                    <tr>
                        <td><span style="color: var(--text-muted)">#</span>{{ row[0] }}</td>
                        <td style="font-weight: 500; color: #fff">{{ row[1] }}</td>
                        <td>{{ row[2] if row[2] else '<span style="color: var(--text-muted)">N/A</span>'|safe }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">
                No users found matching your query.
            </div>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    search_term = ''
    query = ''
    results = None
    error = None
    
    if request.method == 'POST':
        search_term = request.form.get('search', '')
        
        # Vulnerable SQL query - intentionally using string concatenation
        query = f"SELECT id, username, email FROM users WHERE username = '{search_term}'"
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.executescript(query)
            results = cursor.fetchall()
            conn.close()
        except Exception as e:
            error = str(e)
    
    return render_template_string(HTML_TEMPLATE, 
                                 search_term=search_term,
                                 query=query,
                                 results=results,
                                 error=error)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
