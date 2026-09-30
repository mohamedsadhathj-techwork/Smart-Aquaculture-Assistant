import streamlit as st
import serial
import time

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Smart Aquaculture Assistant",
    page_icon="🐟",
    layout="wide"
)

st.title("Smart Aquaculture Assistant")
st.subheader("Live ESP32 Sensor Monitoring & Fish Health Prediction")


# =========================================================
# ESP32 CONNECTION
# =========================================================

try:
    ser = serial.Serial(
        "COM5",
        115200,
        timeout=1
    )

    time.sleep(2)

    st.success("🟢 ESP32 Connected Successfully — COM5")

except Exception:
    st.error("🔴 ESP32 Not Connected")
    st.warning("Please connect ESP32 and check COM5.")
    st.stop()


# =========================================================
# WATER SENSOR CALIBRATION
# =========================================================
# Change this value after checking your water sensor readings.
# Example: if water-filled value is above 1000, use 1000.

WATER_NORMAL_THRESHOLD = 1000


# =========================================================
# LIVE DISPLAY AREAS
# =========================================================

st.divider()

st.subheader("📊 Live Sensor Values")

col1, col2, col3, col4 = st.columns(4)

temperature_box = col1.empty()
ph_box = col2.empty()
tds_box = col3.empty()
water_box = col4.empty()


st.divider()

st.subheader("🐟 Fish Health Prediction")

prediction_box = st.empty()
prediction_message = st.empty()


st.divider()

st.subheader("📋 Sensor Status")

status_col1, status_col2, status_col3, status_col4 = st.columns(4)

temperature_status_box = status_col1.empty()
ph_status_box = status_col2.empty()
tds_status_box = status_col3.empty()
water_status_box = status_col4.empty()


# =========================================================
# SENSOR VARIABLES
# =========================================================

temperature = None
ph_value = None
tds_voltage = None
water_value = None


# =========================================================
# FUNCTIONS
# =========================================================

def temperature_status(value):

    if 25 <= value <= 30:
        return "Normal"

    elif 23 <= value < 25 or 30 < value <= 32:
        return "At Risk"

    else:
        return "High Risk"


def ph_status(value):

    if 6.5 <= value <= 8.5:
        return "Normal"

    elif 6.0 <= value < 6.5 or 8.5 < value <= 9.0:
        return "At Risk"

    else:
        return "High Risk"


def tds_status(value):

    # This is a prototype voltage range.
    # Proper TDS ppm calibration should be done later.

    if 0.30 <= value <= 1.50:
        return "Normal"

    elif 0.20 <= value < 0.30 or 1.50 < value <= 1.80:
        return "At Risk"

    else:
        return "High Risk"


def water_status(value):

    if value >= WATER_NORMAL_THRESHOLD:
        return "Normal"

    elif value >= WATER_NORMAL_THRESHOLD * 0.5:
        return "Low"

    else:
        return "Very Low"


# =========================================================
# LIVE ESP32 LOOP
# =========================================================

while True:

    if ser.in_waiting:

        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()


        # -------------------------------------------------
        # TEMPERATURE
        # -------------------------------------------------

        if line.startswith("Temperature:"):

            try:

                temperature = float(
                    line
                    .replace("Temperature:", "")
                    .replace("C", "")
                    .strip()
                )

            except:
                pass


        # -------------------------------------------------
        # WATER SENSOR
        # -------------------------------------------------

        elif line.startswith("Water Sensor:"):

            try:

                water_value = int(
                    line
                    .replace("Water Sensor:", "")
                    .strip()
                )

            except:
                pass


        # -------------------------------------------------
        # TDS
        # -------------------------------------------------

        elif line.startswith("TDS Voltage:"):

            try:

                tds_voltage = float(
                    line
                    .replace("TDS Voltage:", "")
                    .replace("V", "")
                    .strip()
                )

            except:
                pass


        # -------------------------------------------------
        # pH
        # -------------------------------------------------

        elif line.startswith("pH:"):

            try:

                ph_value = float(
                    line
                    .replace("pH:", "")
                    .strip()
                )

            except:
                pass


        # =================================================
        # DISPLAY LIVE VALUES
        # =================================================

        if temperature is not None:

            temperature_box.metric(
                "🌡️ Temperature",
                f"{temperature:.2f} °C"
            )


        if ph_value is not None:

            ph_box.metric(
                "🧫 pH",
                f"{ph_value:.2f}"
            )


        if tds_voltage is not None:

            tds_box.metric(
                "🧪 TDS Voltage",
                f"{tds_voltage:.2f} V"
            )


        if water_value is not None:

            water_box.metric(
                "💧 Water Level",
                str(water_value)
            )


        # =================================================
        # CHECK ALL FOUR SENSOR CONDITIONS
        # =================================================

        if (
            temperature is not None
            and ph_value is not None
            and tds_voltage is not None
            and water_value is not None
        ):

            temp_result = temperature_status(
                temperature
            )

            ph_result = ph_status(
                ph_value
            )

            tds_result = tds_status(
                tds_voltage
            )

            water_result = water_status(
                water_value
            )


            # =================================================
            # SENSOR STATUS DISPLAY
            # =================================================

            if temp_result == "Normal":

                temperature_status_box.success(
                    "🌡️ Normal"
                )

            elif temp_result == "At Risk":

                temperature_status_box.warning(
                    "🌡️ At Risk"
                )

            else:

                temperature_status_box.error(
                    "🌡️ High Risk"
                )


            if ph_result == "Normal":

                ph_status_box.success(
                    "🧫 Normal"
                )

            elif ph_result == "At Risk":

                ph_status_box.warning(
                    "🧫 At Risk"
                )

            else:

                ph_status_box.error(
                    "🧫 High Risk"
                )


            if tds_result == "Normal":

                tds_status_box.success(
                    "🧪 Normal"
                )

            elif tds_result == "At Risk":

                tds_status_box.warning(
                    "🧪 At Risk"
                )

            else:

                tds_status_box.error(
                    "🧪 High Risk"
                )


            # WATER STATUS

            if water_result == "Normal":

                water_status_box.success(
                    "💧 Normal"
                )

            elif water_result == "Low":

                water_status_box.warning(
                    "💧 Low"
                )

            else:

                water_status_box.error(
                    "💧 Very Low"
                )


            # =================================================
            # FISH HEALTH SCORE
            # =================================================

            score = 0

            if temp_result == "Normal":
                score += 1

            if ph_result == "Normal":
                score += 1

            if tds_result == "Normal":
                score += 1

            if water_result == "Normal":
                score += 1


            # =================================================
            # FISH HEALTH PREDICTION
            # =================================================

            if score == 4:

                prediction_box.success(
                    "🐟 FISH HEALTH STATUS: STABLE"
                )

                prediction_message.info(
                    "✅ All four live sensor conditions "
                    "are currently normal."
                )


            elif score >= 2:

                prediction_box.warning(
                    "⚠️ FISH HEALTH STATUS: AT RISK"
                )

                prediction_message.warning(
                    "⚠️ Some sensor conditions require attention."
                )


            else:

                prediction_box.error(
                    "🚨 FISH HEALTH STATUS: HIGH RISK"
                )

                prediction_message.error(
                    "🚨 Multiple sensor conditions "
                    "require immediate attention."
                )


        # Small delay
        time.sleep(0.1)