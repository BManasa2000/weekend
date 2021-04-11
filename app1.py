@app.route('/')
def dashboard():
    username = "Monkey"
    userTier = "123"
    return render_template("dashboard.html", username = username, userTier = userTier)