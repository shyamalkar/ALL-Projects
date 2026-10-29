import requests
import pandas as pd
import streamlit as st
import plotly.express as px

from datetime import datetime, timezone, timedelta


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Weather Intelligence",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# API CONFIGURATION
# ============================================================

API_KEY = "7d5cbd5f5aa0bc3e1c07c44859a5cbdc"

BASE_URL = "https://api.openweathermap.org/data/2.5"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 45px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 25px;
    }

    .weather-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 15px;
    }

    .temperature {
        font-size: 55px;
        font-weight: 800;
    }

    .condition {
        font-size: 22px;
        font-weight: 600;
    }

    .alert-box {
        padding: 15px;
        border-radius: 12px;
        background-color: rgba(255, 165, 0, 0.12);
        border: 1px solid rgba(255, 165, 0, 0.4);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API FUNCTIONS
# ============================================================

def get_current_weather(city, units="metric"):

    url = f"{BASE_URL}/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()


def get_forecast(city, units="metric"):

    url = f"{BASE_URL}/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_time(timestamp, timezone_offset):

    local_time = datetime.fromtimestamp(
        timestamp,
        timezone.utc
    ) + timedelta(
        seconds=timezone_offset
    )

    return local_time.strftime(
        "%I:%M %p"
    )


def get_weather_icon(icon_code):

    return (
        f"https://openweathermap.org/"
        f"img/wn/{icon_code}@2x.png"
    )


def get_alerts(weather):

    alerts = []

    temperature = weather["main"]["temp"]
    humidity = weather["main"]["humidity"]
    wind_speed = weather["wind"]["speed"]

    condition = weather["weather"][0]["main"]

    if temperature >= 40:
        alerts.append(
            "🔥 Extreme heat: temperature is very high."
        )

    elif temperature >= 35:
        alerts.append(
            "🌡️ High temperature: stay hydrated."
        )

    if temperature <= 5:
        alerts.append(
            "🥶 Very cold conditions detected."
        )

    if humidity >= 85:
        alerts.append(
            "💧 Very high humidity."
        )

    if wind_speed >= 15:
        alerts.append(
            "💨 Strong wind conditions."
        )

    if condition in [
        "Thunderstorm"
    ]:
        alerts.append(
            "⛈️ Thunderstorm conditions detected."
        )

    if condition in [
        "Rain",
        "Drizzle"
    ]:
        alerts.append(
            "🌧️ Rain is currently occurring."
        )

    if condition in [
        "Snow"
    ]:
        alerts.append(
            "❄️ Snow conditions detected."
        )

    return alerts


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🌦️ Weather Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Real-time weather monitoring and forecast analytics'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🌍 Weather Control"
)

city = st.sidebar.text_input(
    "📍 Enter City",
    value="Kolkata"
)

unit_option = st.sidebar.selectbox(
    "🌡️ Temperature Unit",
    [
        "Celsius (°C)",
        "Fahrenheit (°F)"
    ]
)

if unit_option == "Celsius (°C)":

    units = "metric"
    temperature_symbol = "°C"
    wind_symbol = "m/s"

else:

    units = "imperial"
    temperature_symbol = "°F"
    wind_symbol = "mph"


search = st.sidebar.button(
    "🔍 Get Weather",
    use_container_width=True
)


# ============================================================
# LOAD WEATHER
# ============================================================

if search:

    if not city.strip():

        st.error(
            "Please enter a city name."
        )

        st.stop()

    with st.spinner(
        "🌍 Fetching weather data..."
    ):

        try:

            current_data = get_current_weather(
                city,
                units
            )

            forecast_data = get_forecast(
                city,
                units
            )

            st.session_state[
                "current_weather"
            ] = current_data

            st.session_state[
                "forecast_weather"
            ] = forecast_data

        except requests.exceptions.HTTPError:

            st.error(
                """
                ❌ Could not find this location.

                Please check the city name and try again.
                """
            )

            st.stop()

        except Exception as error:

            st.error(
                f"❌ API Error: {error}"
            )

            st.stop()


# ============================================================
# DEFAULT LOAD
# ============================================================

if (
    "current_weather"
    not in st.session_state
):

    with st.spinner(
        "Loading weather..."
    ):

        try:

            st.session_state[
                "current_weather"
            ] = get_current_weather(
                "Kolkata",
                "metric"
            )

            st.session_state[
                "forecast_weather"
            ] = get_forecast(
                "Kolkata",
                "metric"
            )

            units = "metric"
            temperature_symbol = "°C"
            wind_symbol = "m/s"

        except Exception as error:

            st.error(
                f"Could not load weather: {error}"
            )

            st.stop()


# ============================================================
# GET DATA
# ============================================================

weather = st.session_state[
    "current_weather"
]

forecast = st.session_state[
    "forecast_weather"
]


# ============================================================
# LOCATION HEADER
# ============================================================

city_name = weather.get(
    "name",
    "Unknown"
)

country = weather.get(
    "sys",
    {}
).get(
    "country",
    ""
)

timezone_offset = weather.get(
    "timezone",
    0
)

st.header(
    f"📍 {city_name}, {country}"
)

st.caption(
    f"Coordinates: "
    f"{weather['coord']['lat']:.4f}, "
    f"{weather['coord']['lon']:.4f}"
)


# ============================================================
# CURRENT WEATHER
# ============================================================

st.subheader(
    "🌤️ Current Weather"
)

col1, col2, col3, col4 = st.columns(4)


# Temperature
with col1:

    temperature = weather[
        "main"
    ]["temp"]

    st.metric(
        "🌡️ Temperature",
        f"{temperature:.1f}{temperature_symbol}"
    )


# Feels Like
with col2:

    feels_like = weather[
        "main"
    ]["feels_like"]

    st.metric(
        "🤒 Feels Like",
        f"{feels_like:.1f}{temperature_symbol}"
    )


# Humidity
with col3:

    humidity = weather[
        "main"
    ]["humidity"]

    st.metric(
        "💧 Humidity",
        f"{humidity}%"
    )


# Wind
with col4:

    wind_speed = weather[
        "wind"
    ]["speed"]

    st.metric(
        "💨 Wind",
        f"{wind_speed:.1f} {wind_symbol}"
    )


# ============================================================
# WEATHER DESCRIPTION
# ============================================================

st.divider()

col1, col2 = st.columns(
    [1, 3]
)

with col1:

    icon = weather[
        "weather"
    ][0]["icon"]

    st.image(
        get_weather_icon(icon),
        width=120
    )


with col2:

    condition = weather[
        "weather"
    ][0]["main"]

    description = weather[
        "weather"
    ][0]["description"]

    st.markdown(
        f"""
        ### {condition}

        **{description.title()}**

        Atmospheric pressure:
        **{weather['main']['pressure']} hPa**
        """
    )


# ============================================================
# WEATHER DETAILS
# ============================================================

st.divider()

st.subheader(
    "📊 Weather Details"
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    visibility = weather.get(
        "visibility",
        0
    )

    st.metric(
        "👁️ Visibility",
        f"{visibility / 1000:.1f} km"
    )


with col2:

    pressure = weather[
        "main"
    ]["pressure"]

    st.metric(
        "🔵 Pressure",
        f"{pressure} hPa"
    )


with col3:

    wind_direction = weather[
        "wind"
    ].get(
        "deg",
        0
    )

    st.metric(
        "🧭 Wind Direction",
        f"{wind_direction}°"
    )


with col4:

    cloudiness = weather[
        "clouds"
    ]["all"]

    st.metric(
        "☁️ Cloudiness",
        f"{cloudiness}%"
    )


# ============================================================
# SUNRISE / SUNSET
# ============================================================

st.divider()

st.subheader(
    "🌅 Sun Information"
)

col1, col2 = st.columns(2)

with col1:

    sunrise = format_time(
        weather["sys"]["sunrise"],
        timezone_offset
    )

    st.metric(
        "🌅 Sunrise",
        sunrise
    )

with col2:

    sunset = format_time(
        weather["sys"]["sunset"],
        timezone_offset
    )

    st.metric(
        "🌇 Sunset",
        sunset
    )


# ============================================================
# WEATHER ALERTS
# ============================================================

alerts = get_alerts(
    weather
)

st.divider()

st.subheader(
    "⚠️ Weather Monitor"
)

if alerts:

    for alert in alerts:

        st.warning(
            alert
        )

else:

    st.success(
        "✅ No major weather conditions detected."
    )


# ============================================================
# PREPARE FORECAST DATA
# ============================================================

forecast_rows = []

for item in forecast["list"]:

    forecast_rows.append(
        {
            "Datetime":
                item["dt_txt"],

            "Temperature":
                item["main"]["temp"],

            "Feels Like":
                item["main"]["feels_like"],

            "Min Temperature":
                item["main"]["temp_min"],

            "Max Temperature":
                item["main"]["temp_max"],

            "Humidity":
                item["main"]["humidity"],

            "Pressure":
                item["main"]["pressure"],

            "Wind Speed":
                item["wind"]["speed"],

            "Clouds":
                item["clouds"]["all"],

            "Rain Probability":
                item.get(
                    "pop",
                    0
                ) * 100,

            "Weather":
                item["weather"][0]["main"],

            "Description":
                item["weather"][0]["description"]
        }
    )


forecast_df = pd.DataFrame(
    forecast_rows
)

forecast_df["Datetime"] = pd.to_datetime(
    forecast_df["Datetime"]
)


# ============================================================
# FORECAST HEADER
# ============================================================

st.divider()

st.header(
    "📅 5-Day Forecast"
)

st.caption(
    "Forecast data is provided at approximately "
    "3-hour intervals."
)


# ============================================================
# FORECAST SUMMARY
# ============================================================

forecast_df["Date"] = (
    forecast_df["Datetime"]
    .dt.date
)

daily_summary = (
    forecast_df
    .groupby("Date")
    .agg(
        Min_Temperature=(
            "Min Temperature",
            "min"
        ),

        Max_Temperature=(
            "Max Temperature",
            "max"
        ),

        Average_Temperature=(
            "Temperature",
            "mean"
        ),

        Average_Humidity=(
            "Humidity",
            "mean"
        ),

        Max_Rain_Probability=(
            "Rain Probability",
            "max"
        ),

        Max_Wind=(
            "Wind Speed",
            "max"
        )
    )
    .reset_index()
)


# ============================================================
# DAILY FORECAST CARDS
# ============================================================

for _, row in daily_summary.iterrows():

    forecast_date = row["Date"]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.write(
            f"📅 **{forecast_date}**"
        )

    with col2:

        st.metric(
            "🌡️ Min",
            f"{row['Min_Temperature']:.1f}"
            f"{temperature_symbol}"
        )

    with col3:

        st.metric(
            "🔥 Max",
            f"{row['Max_Temperature']:.1f}"
            f"{temperature_symbol}"
        )

    with col4:

        st.metric(
            "🌧️ Rain",
            f"{row['Max_Rain_Probability']:.0f}%"
        )

    with col5:

        st.metric(
            "💨 Wind",
            f"{row['Max_Wind']:.1f}"
            f" {wind_symbol}"
        )


# ============================================================
# TEMPERATURE CHART
# ============================================================

st.divider()

st.subheader(
    "🌡️ Temperature Forecast"
)

fig_temperature = px.line(
    forecast_df,
    x="Datetime",
    y=[
        "Temperature",
        "Feels Like"
    ],
    markers=True,
    title="Temperature vs Feels Like"
)

fig_temperature.update_layout(
    xaxis_title="Time",
    yaxis_title=f"Temperature ({temperature_symbol})",
    legend_title="Metric"
)

st.plotly_chart(
    fig_temperature,
    use_container_width=True
)


# ============================================================
# HUMIDITY CHART
# ============================================================

st.subheader(
    "💧 Humidity Forecast"
)

fig_humidity = px.line(
    forecast_df,
    x="Datetime",
    y="Humidity",
    markers=True,
    title="Humidity Forecast"
)

fig_humidity.update_layout(
    xaxis_title="Time",
    yaxis_title="Humidity (%)"
)

st.plotly_chart(
    fig_humidity,
    use_container_width=True
)


# ============================================================
# RAIN PROBABILITY
# ============================================================

st.subheader(
    "🌧️ Rain Probability"
)

fig_rain = px.bar(
    forecast_df,
    x="Datetime",
    y="Rain Probability",
    title="Probability of Precipitation"
)

fig_rain.update_layout(
    xaxis_title="Time",
    yaxis_title="Probability (%)"
)

st.plotly_chart(
    fig_rain,
    use_container_width=True
)


# ============================================================
# WIND FORECAST
# ============================================================

st.subheader(
    "💨 Wind Forecast"
)

fig_wind = px.line(
    forecast_df,
    x="Datetime",
    y="Wind Speed",
    markers=True,
    title="Wind Speed Forecast"
)

fig_wind.update_layout(
    xaxis_title="Time",
    yaxis_title=f"Wind Speed ({wind_symbol})"
)

st.plotly_chart(
    fig_wind,
    use_container_width=True
)


# ============================================================
# CLOUD COVER
# ============================================================

st.subheader(
    "☁️ Cloud Coverage"
)

fig_clouds = px.area(
    forecast_df,
    x="Datetime",
    y="Clouds",
    title="Cloud Coverage Forecast"
)

fig_clouds.update_layout(
    xaxis_title="Time",
    yaxis_title="Cloud Coverage (%)"
)

st.plotly_chart(
    fig_clouds,
    use_container_width=True
)


# ============================================================
# FORECAST DATA TABLE
# ============================================================

st.divider()

st.subheader(
    "📊 Complete Forecast Data"
)

display_df = forecast_df.copy()

display_df["Datetime"] = (
    display_df["Datetime"]
    .dt.strftime(
        "%Y-%m-%d %H:%M"
    )
)

display_df = display_df.rename(
    columns={
        "Temperature":
            f"Temperature ({temperature_symbol})",

        "Feels Like":
            f"Feels Like ({temperature_symbol})",

        "Min Temperature":
            f"Min ({temperature_symbol})",

        "Max Temperature":
            f"Max ({temperature_symbol})",

        "Wind Speed":
            f"Wind ({wind_symbol})",

        "Rain Probability":
            "Rain Probability (%)"
    }
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD DATA
# ============================================================

st.divider()

st.subheader(
    "💾 Export Forecast"
)

csv_data = display_df.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Forecast CSV",
    data=csv_data,
    file_name="weather_forecast.csv",
    mime="text/csv",
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌦️ Weather Intelligence | "
    "Python + Streamlit + Requests + Pandas + Plotly | "
    "Powered by OpenWeather"
)