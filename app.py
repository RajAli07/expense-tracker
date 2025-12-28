from flask import Flask, request, send_file, jsonify
import csv
import io
import json
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
expenses = []

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        data = request.form
        expense = {
            'id': len(expenses) + 1,
            'item': data['item'],
            'amount': float(data['amount']),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'category': data.get('category', 'Other')
        }
        expenses.append(expense)
        message = f" {expense['item']} added!"

    # Analytics
    total = sum(e['amount'] for e in expenses)
    categories = defaultdict(float)
    for e in expenses:
        categories[e['category']] += e['amount']
    recent = sorted(expenses[-5:], key=lambda x: x['date'], reverse=True)

    return f'''<!DOCTYPE html>
<html class="dark">
<head>
    <title>Expense Tracker Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-gray-900 dark:to-gray-800 min-h-screen py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="text-center mb-12">
            <h1 class="text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-4">
                <i class="fas fa-wallet mr-4"></i>Expense Tracker Pro
            </h1>
            <p class="text-xl text-gray-600 dark:text-gray-300">Modern dashboard for smart spending</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-white/70 dark:bg-gray-800/70 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/20 hover:scale-105 transition-all duration-300">
                <div class="text-3xl font-bold text-indigo-600 dark:text-indigo-400">₹{total:.0f}</div>
                <div class="text-gray-500 dark:text-gray-400">Total Spent</div>
            </div>
            <div class="bg-white/70 dark:bg-gray-800/70 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/20 hover:scale-105 transition-all duration-300">
                <div class="text-3xl font-bold text-green-600 dark:text-green-400">{len(expenses)}</div>
                <div class="text-gray-500 dark:text-gray-400">Transactions</div>
            </div>
            <div class="bg-white/70 dark:bg-gray-800/70 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/20 hover:scale-105 transition-all duration-300">
                <div class="text-3xl font-bold text-purple-600 dark:text-purple-400">{len(categories)}</div>
                <div class="text-gray-500 dark:text-gray-400">Categories</div>
            </div>
        </div>

        <!-- Add Expense Form -->
        <div class="bg-white/60 dark:bg-gray-800/60 backdrop-blur-xl rounded-3xl p-8 mb-8 shadow-2xl border border-white/30">
            <h2 class="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
                <i class="fas fa-plus-circle mr-2 text-green-500"></i>Add Expense
            </h2>
            <form method="post" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input name="item" placeholder="Item name" class="p-4 rounded-2xl border-2 border-gray-200 dark:border-gray-600 focus:border-indigo-400 focus:ring-4 focus:ring-indigo-100 dark:focus:ring-indigo-900 bg-white/50 dark:bg-gray-700/50 backdrop-blur-sm text-lg" required>
                <input name="amount" type="number" step="0.01" placeholder="Amount" class="p-4 rounded-2xl border-2 border-gray-200 dark:border-gray-600 focus:border-green-400 focus:ring-4 focus:ring-green-100 dark:focus:ring-green-900 bg-white/50 dark:bg-gray-700/50 backdrop-blur-sm text-lg" required>
                <select name="category" class="p-4 rounded-2xl border-2 border-gray-200 dark:border-gray-600 focus:border-purple-400 focus:ring-4 focus:ring-purple-100 dark:focus:ring-purple-900 bg-white/50 dark:bg-gray-700/50 backdrop-blur-sm text-lg">
                    <option value="Food">🍔 Food</option>
                    <option value="Transport">🚗 Transport</option>
                    <option value="Shopping">🛒 Shopping</option>
                    <option value="Entertainment">🎬 Entertainment</option>
                    <option value="Bills">💡 Bills</option>
                    <option value="Other">📋 Other</option>
                </select>
                <button type="submit" class="md:col-span-3 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-2xl text-xl shadow-2xl hover:shadow-3xl transform hover:-translate-y-1 transition-all duration-300">
                    <i class="fas fa-plus mr-2"></i>Add Expense
                </button>
            </form>
            {message if 'message' in locals() else ''}
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Chart -->
            <div class="bg-white/60 dark:bg-gray-800/60 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/30">
                <h3 class="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
                    <i class="fas fa-chart-pie mr-2 text-purple-500"></i>Spending Breakdown
                </h3>
                <canvas id="expenseChart" height="300"></canvas>
            </div>

            <!-- Recent Expenses -->
            <div class="bg-white/60 dark:bg-gray-800/60 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/30">
                <h3 class="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
                    <i class="fas fa-clock mr-2 text-blue-500"></i>Recent Expenses
                </h3>
                <div class="space-y-4 max-h-96 overflow-y-auto">
                    {''.join([f'''
                    <div class="flex justify-between items-center p-4 bg-white/50 dark:bg-gray-700/50 rounded-2xl hover:bg-white/70 dark:hover:bg-gray-600/70 transition-all duration-200">
                        <div>
                            <div class="font-semibold text-lg text-gray-800 dark:text-white">{e['item']}</div>
                            <div class="text-sm text-gray-500 dark:text-gray-400">{e['category']} • {e['date']}</div>
                        </div>
                        <div class="text-right">
                            <div class="text-2xl font-bold text-red-500">₹{e['amount']:.0f}</div>
                        </div>
                    </div>
                    ''' for e in recent]) or '<p class="text-gray-500 dark:text-gray-400 text-center py-8">No expenses yet</p>'}
                </div>
            </div>
        </div>

        <!-- Action Buttons -->
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mt-12">
            <a href="/view" class="group bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-bold py-4 px-6 rounded-2xl text-center shadow-2xl hover:shadow-3xl transform hover:-translate-y-2 transition-all duration-300 flex items-center justify-center space-x-2">
                <i class="fas fa-list text-xl group-hover:rotate-12"></i>
                <span>View All</span>
            </a>
            <a href="/summary" class="group bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold py-4 px-6 rounded-2xl text-center shadow-2xl hover:shadow-3xl transform hover:-translate-y-2 transition-all duration-300 flex items-center justify-center space-x-2">
                <i class="fas fa-chart-bar text-xl"></i>
                <span>Summary</span>
            </a>
            <a href="/download" class="group bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white font-bold py-4 px-6 rounded-2xl text-center shadow-2xl hover:shadow-3xl transform hover:-translate-y-2 transition-all duration-300 flex items-center justify-center space-x-2">
                <i class="fas fa-download text-xl"></i>
                <span>Export CSV</span>
            </a>
            <a href="/clear" class="group bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-bold py-4 px-6 rounded-2xl text-center shadow-2xl hover:shadow-3xl transform hover:-translate-y-2 transition-all duration-300 flex items-center justify-center space-x-2" onclick="return confirm('Clear all expenses?')">
                <i class="fas fa-trash text-xl"></i>
                <span>Clear All</span>
            </a>
            <label for="dark-toggle" class="group bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white font-bold py-4 px-6 rounded-2xl text-center shadow-2xl hover:shadow-3xl transform hover:-translate-y-2 transition-all duration-300 flex items-center justify-center space-x-2 cursor-pointer">
                <i class="fas fa-moon text-xl"></i>
                <span>Dark Mode</span>
                <input type="checkbox" id="dark-toggle" class="hidden" onclick="toggleDarkMode()">
            </label>
        </div><div class="grid grid-cols-2 md:grid-cols-5 gap-4 mt-12">
    <!-- ... your 5 buttons ... -->
</div>

<!--  COPYRIGHT YE ADD KARO  -->
<div class="text-center mt-12 pt-8 border-t border-gray-200 dark:border-gray-600">
    <p class="text-sm text-gray-500 dark:text-gray-400">
        © 2025 Rajali. All rights reserved. | Made in India ❤️
    </p>
</div>
    </div>

    <script>
        // Chart.js
        const ctx = document.getElementById('expenseChart').getContext('2d');
        const chartData = {{
            labels: {json.dumps(list(categories.keys()))},
            datasets: [{{
                data: {json.dumps(list(categories.values()))},
                backgroundColor: ['#EF4444','#F59E0B','#10B981','#3B82F6','#8B5CF6','#EC4899'],
                borderWidth: 0,
                offset: true
            }}]
        }};
        new Chart(ctx, {{
            type: 'doughnut',
            data: chartData,
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});

        function toggleDarkMode() {{
            document.documentElement.classList.toggle('dark');
            localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
        }}
        if (localStorage.getItem('darkMode') === 'true') {{
            document.documentElement.classList.add('dark');
        }}
    </script>
</body>
</html>'''

@app.route('/view')
def view():
    if not expenses:
        return '<h1 class="text-4xl text-center mt-20 text-gray-500">No expenses yet! <a href="/" class="text-indigo-600 hover:underline">← Add some</a></h1>'
    
    table = ''.join([f'<tr class="hover:bg-gray-50"><td class="p-4 font-medium">{e["id"]}</td><td class="p-4">{e["item"]}</td><td class="p-4 font-bold text-red-500">₹{e["amount"]:.0f}</td><td class="p-4">{e["category"]}</td><td class="p-4">{e["date"]}</td></tr>' for e in expenses])
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>All Expenses</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen py-12">
    <div class="max-w-6xl mx-auto px-4">
        <h1 class="text-4xl font-bold text-gray-800 mb-8">📋 All Expenses ({len(expenses)})</h1>
        <div class="bg-white rounded-3xl shadow-2xl overflow-hidden">
            <table class="w-full">
                <thead class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white">
                    <tr><th>ID</th><th>Item</th><th>Amount</th><th>Category</th><th>Date</th></tr>
                </thead>
                <tbody>{table}</tbody>
            </table>
        </div>
        <a href="/" class="mt-8 inline-block bg-indigo-600 text-white px-8 py-4 rounded-2xl font-bold hover:bg-indigo-700">← Dashboard</a>
    </div>
</body>
</html>'''

@app.route('/summary')
def summary():
    if not expenses:
        return '<h1 class="text-4xl text-center mt-20 text-gray-500">No data for summary! <a href="/" class="text-indigo-600 hover:underline">← Add expenses</a></h1>'
    
    total = sum(e['amount'] for e in expenses)
    avg = total / len(expenses)
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>Summary</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-50 min-h-screen py-12">
    <div class="max-w-4xl mx-auto px-4 text-center">
        <h1 class="text-4xl font-bold text-center mt-20 text-gray-800">📊 Summary</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
            <div class="bg-gradient-to-br from-blue-500 to-indigo-600 text-white p-12 rounded-3xl shadow-2xl">
                <div class="text-4xl font-bold">₹{total:.0f}</div>
                <div>Total Spent</div>
            </div>
            <div class="bg-gradient-to-br from-green-500 to-emerald-600 text-white p-12 rounded-3xl shadow-2xl">
                <div class="text-4xl font-bold">₹{avg:.0f}</div>
                <div>Average</div>
            </div>
            <div class="bg-gradient-to-br from-purple-500 to-pink-600 text-white p-12 rounded-3xl shadow-2xl">
                <div class="text-4xl font-bold">{len(expenses)}</div>
                <div>Transactions</div>
            </div>
        </div>
        <a href="/" class="mt-12 inline-block bg-indigo-600 text-white px-8 py-4 rounded-2xl font-bold hover:bg-indigo-700">← Dashboard</a>
    </div>
</body>
</html>'''

@app.route('/download')
def download():
    if not expenses:
        return "No data", 404
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['id', 'item', 'amount', 'category', 'date'])
    writer.writeheader()
    writer.writerows(expenses)
    return send_file(
        io.BytesIO(output.getvalue().encode()), 
        mimetype='text/csv', 
        as_attachment=True, 
        download_name='expenses.csv'
    )

@app.route('/clear')
def clear():
    expenses.clear()
    return '''<!DOCTYPE html>
<html>
<head>
    <title>Cleared</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body style="text-align:center;padding:100px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;min-height:100vh;display:flex;align-items:center;justify-content:center">
    <div>
        <h1 style="font-size:4rem;font-weight:900;margin:0">🗑️ All Cleared!</h1>
        <a href="/" style="display:inline-block;background:white;color:#667eea;padding:20px 40px;margin-top:30px;border-radius:50px;font-weight:700;text-decoration:none">← Back to Dashboard</a>
    </div>
</body>
</html>'''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
