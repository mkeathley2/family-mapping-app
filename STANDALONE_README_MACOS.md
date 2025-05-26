# Family Mapping App - Standalone Version for macOS 🍎🗺️

## ✨ No Installation Required!

This is a **standalone version** of the Family Mapping App that runs without needing Docker, Python, or any other software installed on your Mac.

## 🚀 How to Use (Super Simple!)

### Step 1: Run the App
- **Double-click** `START_HERE.sh` (or open Terminal and run `./START_HERE.sh`)
- If macOS asks about security, go to **System Preferences > Security & Privacy** and click "Open Anyway"
- Wait a moment for the app to start
- Your web browser will open automatically to the app

### Step 2: Prepare Your Data
Create a CSV file (like in Excel or Numbers) with your family addresses:
```
name,address
John Smith,123 Main St New York NY
Jane Doe,456 Oak Ave Los Angeles CA
Bob Johnson,789 Pine Rd Chicago IL
```

### Step 3: Upload and Map
1. Click "Choose CSV File" and select your file
2. Click "Upload & Process"
3. Wait for the addresses to be geocoded (this may take a few minutes)
4. See your family locations on the interactive map!
5. Download the results with coordinates included

## 📋 What You Need

- **macOS** (macOS 10.14 Mojave or newer recommended)
- **Internet Connection** (for geocoding addresses and map tiles)
- **CSV file** with your family addresses

## 📁 Your Data

- All your uploaded files are saved in a `datasets` folder
- This folder is created automatically next to the app
- Your data stays on your computer - nothing is sent to external servers except for address geocoding

## 🛠️ Troubleshooting

**App won't start?**
- Make sure you're running macOS 10.14 or newer
- Right-click `START_HERE.sh` and select "Open" to bypass security warnings
- Try opening Terminal and running: `chmod +x START_HERE.sh && ./START_HERE.sh`

**Security warning appears?**
- Go to **System Preferences > Security & Privacy > General**
- Click "Open Anyway" next to the blocked app message
- Or try: Right-click the app → "Open" → "Open" in the dialog

**Browser doesn't open?**
- Manually open your web browser
- Go to: http://localhost:8765

**Geocoding fails?**
- Make sure you have an internet connection
- Check that your CSV has an "address" column
- Try with fewer addresses first (the service has rate limits)

**Port already in use?**
- Close any other instances of the app
- Restart your Mac if needed

## 🔒 Privacy & Security

- **Your data stays local** - files are only processed on your computer
- **Address geocoding** uses OpenStreetMap's free service
- **No account required** - no sign-ups or personal information needed
- **No data collection** - we don't track or store anything about you

## 📞 Need Help?

If you have issues:
1. Check the troubleshooting section above
2. Make sure your CSV file has the right format
3. Try restarting the app
4. Contact the developer with specific error messages

## 🍎 macOS Tips

- **First time running**: You may need to approve the app in Security & Privacy settings
- **Terminal method**: If double-clicking doesn't work, open Terminal and run `./START_HERE.sh`
- **Permissions**: The script will automatically make the app executable

---

**Made with ❤️ for families who want to visualize their connections across the map**

*This standalone version is perfect for Mac users who just want to map their family addresses without any complex setup!* 