# Printer Exerciser Script

This script generates a PDF with four vertical CMYK color bars at a random position on a page and sends it to a printer via CUPS. The purpose is to exercise all print nozzles and prevent clogging by printing a test page daily.

## Features
- Generates a test page with four vertical CMYK bars (configurable size and position)
- Sends the page to a specified printer using the CUPS spooler
- All parameters are configurable (printer name, page size, bar size)
- Debug mode to only generate and save the PDF for testing
- Cleans up temporary files after printing (unless in debug mode)
- Can be automated to run daily (see below)

## Requirements
- Python 3
- `reportlab` Python package (`pip install reportlab` or `sudo apt install python3-reportlab`)
- CUPS and the `lp` command (standard on most Linux systems with printing support)

## Usage Example

```
python3 printer_exerciser.py \
  --printer "EPSON_ET_1810_Series" \
  --page-size A4 \
  --bar-width 4 \
  --bar-height 40
```

- `--printer`: Name of your printer as known to CUPS (see `lpstat -p`)
- `--page-size`: Page size (A4 or letter)
- `--bar-width`: Width of each color bar in mm
- `--bar-height`: Height of each color bar in mm

### Debug Mode
To only generate and save the PDF (for testing):

```
python3 printer_exerciser.py --printer "EPSON_ET_1810_Series" --bar-width 4 --bar-height 40 --debug --output test_page.pdf
```

## Automation (Run Daily at Midnight)

### Using systemd (Recommended for modern Linux)

1. Create a systemd service file (e.g. `/etc/systemd/system/printer-exerciser.service`):

```
[Unit]
Description=Daily Printer Exerciser

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/carl/Desktop/printer_exerciser_script/printer_exerciser.py --printer "EPSON_ET_1810_Series" --page-size A4 --bar-width 4 --bar-height 40
```

2. Create a systemd timer file (e.g. `/etc/systemd/system/printer-exerciser.timer`):

```
[Unit]
Description=Run Printer Exerciser at Midnight

[Timer]
# Every day at midnight
OnCalendar=*-*-* 00:00:00
# Every second day at midnight:
# OnCalendar=*-*-2/2 00:00:00
# Every third day at midnight:
# OnCalendar=*-*-3/3 00:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

3. Enable and start the timer:

```
sudo systemctl daemon-reload
sudo systemctl enable --now printer-exerciser.timer
```

### Using cron (Alternative)

Add this line to your crontab (`crontab -e`):

```
0 0 * * * /usr/bin/python3 /home/carl/Desktop/printer_exerciser_script/printer_exerciser.py --printer "EPSON_ET_1810_Series" --page-size A4 --bar-width 4 --bar-height 40
# Every second day at midnight:
# 0 0 */2 * * /usr/bin/python3 /home/carl/Desktop/printer_exerciser_script/printer_exerciser.py --printer "EPSON_ET_1810_Series" --page-size A4 --bar-width 4 --bar-height 40
# Every third day at midnight:
# 0 0 */3 * * /usr/bin/python3 /home/carl/Desktop/printer_exerciser_script/printer_exerciser.py --printer "EPSON_ET_1810_Series" --page-size A4 --bar-width 4 --bar-height 40
```

## License
MIT
