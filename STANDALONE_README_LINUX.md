# Family Mapping App - Standalone Version for Linux 🐧🗺️

## ✨ No Installation Required!

This is a **standalone version** of the Family Mapping App that runs without needing Docker, Python, or any other software installed on your Linux system.

## 🚀 How to Use (Super Simple!)

### Step 1: Run the App
- **Open Terminal** in the folder containing the app
- Run: `./START_HERE.sh` (or double-click if your file manager supports it)
- Wait a moment for the app to start
- Your web browser will open automatically to the app

### Step 2: Prepare Your Data
Create a CSV file (like in LibreOffice Calc) with your family addresses:
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

- **Linux** (Most modern distributions - Ubuntu 18.04+, Fedora 30+, etc.)
- **Internet Connection** (for geocoding addresses and map tiles)
- **CSV file** with your family addresses

## 📁 Your Data

- All your uploaded files are saved in a `datasets` folder
- This folder is created automatically next to the app
- Your data stays on your computer - nothing is sent to external servers except for address geocoding

## 🛠️ Troubleshooting

**App won't start?**
- Make sure the script is executable: `chmod +x START_HERE.sh`
- Try running directly: `./FamilyMappingApp`
- Check if you have the required libraries: `ldd FamilyMappingApp`

**Permission denied?**
- Make the files executable: `chmod +x START_HERE.sh FamilyMappingApp`
- Make sure you're in the correct directory

**Browser doesn't open?**
- Manually open your web browser
- Go to: http://localhost:8765
- Or try: `xdg-open http://localhost:8765`

**Missing libraries error?**
- Most modern Linux distributions should work out of the box
- If you get library errors, try installing: `sudo apt install libc6 libgcc1` (Ubuntu/Debian)
- Or: `sudo dnf install glibc libgcc` (Fedora/RHEL)

**Geocoding fails?**
- Make sure you have an internet connection
- Check that your CSV has an "address" column
- Try with fewer addresses first (the service has rate limits)

**Port already in use?**
- Close any other instances of the app: `pkill -f FamilyMappingApp`
- Or restart your system if needed

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

## 🐧 Linux Tips

- **Command line**: You can run the app directly with `./FamilyMappingApp`
- **Desktop integration**: You can create a desktop shortcut to `START_HERE.sh`
- **Permissions**: The script will automatically make the app executable
- **Distributions**: Tested on Ubuntu, Fedora, and Debian-based systems

## 🔧 Advanced Users

- **Port configuration**: The app runs on port 8765 by default
- **Data location**: Files are stored in `./datasets/` relative to the app
- **Logs**: Check the terminal output for any error messages

---

**Made with ❤️ for families who want to visualize their connections across the map**

*This standalone version is perfect for Linux users who just want to map their family addresses without any complex setup!* 