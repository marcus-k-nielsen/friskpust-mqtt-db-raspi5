# MQTT Data to Supabase on Raspberry Pi 5

A Python application running on a **Raspberry Pi 5** that receives sensor data from a local **MQTT broker** and sends the data to **Supabase** for storage.

The Raspberry Pi acts as the MQTT broker, allowing connected devices to publish sensor measurements locally. A Python application running on the same Raspberry Pi subscribes to the relevant MQTT topic, processes the incoming data and sends it to Supabase.

## Overview

The project creates a simple connection between local IoT devices and a cloud database.

```text
IoT Sensor / Device
        │
        │ MQTT
        ▼
┌────────────────────┐
│   Raspberry Pi 5   │
│                    │
│    MQTT Broker     │
│         │          │
│         ▼          │
│    Python App      │
│         │          │
└─────────┼──────────┘
          │
          │ Supabase API
          ▼
     ┌──────────┐
     │ Supabase │
     │ Database │
     └──────────┘
```

The Raspberry Pi hosts the MQTT broker. Devices publish sensor data to the broker, while the Python application subscribes to the MQTT topic and forwards the received measurements to Supabase.

## Data

The application currently handles the following values:

| Value         | Description                               |
| ------------- | ----------------------------------------- |
| `temperature` | Temperature measurement                   |
| `humidity`    | Humidity measurement                      |
| `co2`         | CO₂ measurement                           |
| `device_id`   | Identifier of the device sending the data |

The received values are stored in the `measurements` table in Supabase.

### Example MQTT Payload

```json
{
    "temperature": 21.5,
    "humidity": 45.2,
    "co2": 620,
    "device_id": "sensor-01"
}
```

## Technologies

* **Python**
* **Raspberry Pi 5**
* * **MQTT**
* **Paho MQTT**
* **Supabase**
* **JSON**
* **Linux**

## Project Structure

```text
MQTTData-To-Database-On-Ras5/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── handlers.py
│   └── mqtt_client.py
│
├── requirements.txt
├── run.py
└── .gitignore
```

### `mqtt_client.py`

Handles the MQTT client connection and subscribes to the configured MQTT topic to receive incoming messages.

### `handlers.py`

Processes incoming MQTT messages and converts the received JSON payload into data that can be stored in the database.

### `database.py`

Handles the connection to Supabase and stores the received measurements in the `measurements` table.

### `config.py`

Contains the configuration used by the application, including the MQTT and Supabase settings.

### `run.py`

The entry point for the Python application.

## Data Flow

When a sensor sends a measurement:

1. The sensor publishes a JSON message to an MQTT topic.
2. The MQTT broker running on the Raspberry Pi receives the message.
3. The Python application subscribes to the topic and receives the message.
4. The application processes the JSON payload.
5. The processed data is sent to Supabase.
6. Supabase stores the measurement in the `measurements` table.


## Configuration

The application requires configuration for both the MQTT broker and Supabase.

Typical configuration includes:

### MQTT

* MQTT broker address
* MQTT port
* MQTT username
* MQTT password
* MQTT topic

### Supabase

* Supabase URL
* Supabase key

## Running

Start the application with:

```bash
python run.py
```

Once running, the Python application subscribes to the configured MQTT topic and processes incoming sensor data.

The Raspberry Pi therefore acts as both:

* The **MQTT broker**
* The **host for the Python data-processing application**

The processed measurements are then sent to Supabase for storage.

## What I Learned

This project gave me practical experience with:

* MQTT communication
* Running an MQTT broker on a Raspberry Pi
* Raspberry Pi and Linux
* Python
* JSON data processing
* Supabase
* Sending data from a local system to a cloud database
* Working with MQTT publishers and subscribers
* Separating MQTT handling, data processing and database operations

## Project Status

This is a personal learning project demonstrating a simple IoT data pipeline.

The project focuses on receiving sensor measurements through an MQTT broker running on a Raspberry Pi 5 and forwarding the data to Supabase for storage.
