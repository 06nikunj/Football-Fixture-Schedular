# ⚽ Football Fixture Scheduler

A smart and interactive web-based application that generates football match schedules using a **Backtracking Algorithm** while satisfying real-world constraints.

---

## 🚀 Live Demo

👉 https://github.com/06nikunj/Football-Fixture-Schedular

---

## 📌 Project Overview

This project simulates how real football leagues generate fixtures. It ensures that all matches are scheduled fairly while following strict constraints like rest periods and balanced home/away matches.

---

## 🧠 Algorithm Used

**Backtracking Algorithm (Constraint Satisfaction Problem)**

* Tries different match combinations
* Checks constraints at every step
* If a constraint fails → backtracks and tries another possibility

---

## ⚙️ Features

✅ No team plays on consecutive days
✅ Each team plays at most one match per day
✅ Balanced home and away matches
✅ Dynamic fixture generation
✅ Interactive UI with analytics
✅ Match schedule visualization

---

## 📊 Constraints Applied

1. **No Consecutive Matches**
   Ensures teams get rest between matches

2. **One Match Per Day**
   Prevents overloading any team

3. **Home/Away Balance**
   Each team plays once at home and once away against every opponent

---

## 📅 Example Output

```
Day 1:
Manchester vs Arsenal  
Liverpool vs Chelsea  

Day 3:
Arsenal vs Manchester  
Chelsea vs Liverpool  
```

---

## 🛠️ Tech Stack

* HTML
* CSS
* JavaScript
* Backtracking Algorithm

---

## 🌍 Real-World Applications

* Sports league scheduling (IPL, FIFA, etc.)
* Tournament planning systems
* Employee shift scheduling
* Cloud resource allocation systems

---

## 📁 Project Structure

```
football-fixture-scheduler/
│
├── index.html
├── style.css
├── script.js
├── assets/
└── README.md
```

---

## 🧑‍💻 How to Run Locally

1. Clone the repository:

```
git clone https://github.com/yourusername/football-fixture-scheduler.git
```

2. Open the project folder

3. Run `index.html` in your browser

---

## 🔥 Future Improvements

* Add minimum gap between same team matches
* Export fixtures as PDF/CSV
* Add user authentication
* Integrate real team data API

---

## 👨‍🎓 Author

**Nikunj**


---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share it!
