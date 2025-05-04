from booking.booking import Booking
import time

try:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency(currency="USD")
        bot.select_place_to_go('New York')
        bot.select_dates(check_in_date="2025-05-19", check_out_date="2025-05-30")
        bot.travellers(adults=3)
        bot.submit()
        bot.apply_filtrations()
        bot.report_results()

    time.sleep(30)

except Exception as e:
    if 'in PATH' in str(e):
        print(
            "You're trying to rn the bot from command line\n"
            "Please add to PATH your Selenium Drivers\n"
            "Windows:\n"
            "       set PATH=%PATH%;C:path-to-your-driver-folder\n\n"
            "Linux: \n"
            "       PATH=$PATH:/path/toyour/driverFolder/ \n"
        )
    else:
        raise