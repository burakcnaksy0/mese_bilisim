import requests
import json
from django.shortcuts import render, redirect
from .forms import UserLogInForm, DevicesListForm
from datetime import datetime
import threading
import random
from .utils import send_random_telemetry
import io
import os
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
from channels.layers import get_channel_layer

matplotlib.use('Agg')
from django.http import HttpResponse, JsonResponse
from openpyxl import Workbook

BASEURL = "https://thingsboard.cloud/api"
LOGIN_URL = f"{BASEURL}/auth/login"
USER_URL = f"{BASEURL}/auth/user"

DEVICE_ACCESS = {
    "1": {"Erişim şifresi": "pDjy7eYL9BxweVinPuBY", "telemetry": "temperature,state,rez"},
    "2": {"Erişim şifresi": "aqBEbTWN7rHlhufbRyND", "telemetry": "temperature,temp"},
    "3": {"Erişim şifresi": "5Dmo4qa8vJfkUNcP4TCy", "telemetry": "temperature,machineState"},
    "4": {"Erişim şifresi": "0oIGlBuB5Rr5rtGKJGwX", "telemetry": "temperature,clock"},
    "5": {"Erişim şifresi": "NpMnH8RUsyXZkE8LsCKx", "telemetry": "temperature,quality"},
    "6": {"Erişim şifresi": "PKZIzE6ohmtw4MlgWilz", "telemetry": "temp,key"},
}
DEVICE_TELEMETRY = {
    "1": {
        "uuid": "95cf0970-a5b2-11ef-af8e-935e87032cca",
        "telemetry": "values/timeseries?keys=temperature,state,rez"
    },
    "2": {
        "uuid": "cd3c12f0-a69c-11ef-9126-e7e15310409e",
        "telemetry": "values/timeseries?keys=temp,temperature"
    },
    "3": {
        "uuid": "ea345690-a6fd-11ef-8300-7376affecafe",
        "telemetry": "values/timeseries?keys=temperature,machineState"
    },
    "4": {
        "uuid": "e03eb710-a730-11ef-af8e-935e87032cca",
        "telemetry": "values/timeseries?keys=clock,temperature"
    },
    "5": {
        "uuid": "87a23920-abe9-11ef-ba27-0bc777b49120",
        "telemetry": "values/timeseries?keys=quality,temperature"
    },
    "6": {
        "uuid": "dab4ae41-b3c8-11ef-8d27-31960e941324",
        "telemetry": "values/timeseries?keys=key,temp"
    }
}

THINGSBOARD_BASE_URL = "http://thingsboard.cloud/api/v1"


def userlogın(request):
    if request.method == 'POST':
        form = UserLogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            payload = json.dumps({"username": username, "password": password})
            headers = {'Content-Type': 'application/json'}
            response = requests.post(LOGIN_URL, headers=headers, data=payload)
            if response.status_code != 200:
                return render(request, "login.html", {"error": "login failed !!"})
            response_json = response.json()
            token = response_json.get("token")
            refresh_token = response_json.get("refreshToken")
            request.session['token'] = token
            request.session['refresh_token'] = refresh_token
            context = {
                "token": token,
                "refresh_token": refresh_token
            }
            return render(request, "token.html", context)
        else:
            return render(request, "login.html", {"error": "form is not valid !"})
    else:
        form = UserLogInForm()
        return render(request, "login.html", {"form": form})


def get_device_telemetry(request):
    device_uuid = request.session.get("device_uuid")
    telemetry_history = request.session.get("telemetry_history", {})

    if not device_uuid or device_uuid not in telemetry_history:
        return JsonResponse({"error": "No data found."}, status=404)

    # Return telemetry data for the device in session
    return JsonResponse({"telemetry_history": telemetry_history[device_uuid]})


# View for handling device preferences and telemetry data
def devicePrefer(request):
    if request.method == "POST":
        deviceform = DevicesListForm(request.POST)

        if deviceform.is_valid():
            device_key = deviceform.cleaned_data["device"]
            device_data = DEVICE_ACCESS.get(device_key)

            if not device_data:
                return render(request, "deviceInfo.html", {"error": "Invalid device selected!"})

            # Create random telemetry data for the device
            telemetry_keys = device_data["telemetry"].split(",")
            telemetry_history = {}
            charts_data = {}

            # Generate random telemetry data
            for key in telemetry_keys:
                entries = []
                timestamps = []
                values = []
                for i in range(10):  # Generate 10 random data points
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    value = round(random.uniform(10, 100), 2)  # Random value between 10 and 100
                    entries.append({"formatted_ts": ts, "value": value})
                    timestamps.append(ts)
                    values.append(value)

                telemetry_history[key] = entries
                charts_data[key] = {"labels": timestamps, "data": values}

            # Create device information (UUID, status, etc.)
            device_info = {
                "id": device_key,
                "name": device_data.get("name", f"Device {device_key}"),  # Fetch the device name from device_data
                "status": "active" if random.choice([True, False]) else "inactive",
                "uuid": f"uuid-{device_key}",
            }

            # Save telemetry_history and charts_data in session
            session_data = request.session.get('telemetry_history', {})
            session_data[device_info["uuid"]] = telemetry_history
            request.session['telemetry_history'] = session_data
            request.session['device_uuid'] = device_info["uuid"]
            request.session['charts_data'] = charts_data  # Save charts_data (not just the uuid)

            # Start a new thread to send random telemetry data
            telemetry_thread = threading.Thread(target=send_random_telemetry, args=(device_key, device_data))
            telemetry_thread.daemon = True  # Thread will stop when Django stops
            telemetry_thread.start()

            context = {
                "device_info": device_info,
                "telemetry_history": telemetry_history,
                "charts_data": charts_data,
                "message": f"Telemetry started for device {device_key}!",
            }

            return render(request, "deviceİnformation.html", context)  # 'deviceInformation.html' olduğunu varsayıyorum

        else:
            return render(request, "deviceInfo.html", {"error": "Invalid form submission!"})

    else:
        deviceform = DevicesListForm()
        return render(request, "deviceInfo.html", {"deviceform": deviceform})


def export_data(request):
    # Retrieve telemetry history and charts data from the session
    telemetry_history = request.session.get('telemetry_history', {})
    device_uuid = request.POST.get('device_uuid') or request.session.get('device_uuid')

    # Debugging: Output UUID and telemetry data for inspection
    print("POST device_uuid:", request.POST.get('device_uuid'))
    print("Session device_uuid:", request.session.get('device_uuid'))
    print("Telemetry History:", telemetry_history)

    # Check if telemetry history exists
    if not telemetry_history:
        return HttpResponse("No telemetry data found in session.", status=400)

    # Check if device_uuid is provided
    if not device_uuid:
        return HttpResponse("Device UUID is missing.", status=400)

    # Check if device_uuid exists in the telemetry history
    if device_uuid not in telemetry_history:
        return HttpResponse("Invalid device UUID or no data available for this device.", status=400)

    # Retrieve export format (Excel or PDF)
    export_format = request.POST.get("format")
    device_data = telemetry_history[device_uuid]

    # Excel Export
    if export_format == "excel":
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Telemetry Data"
        sheet.append(["Key", "Timestamp", "Value"])

        # Add telemetry data to the Excel sheet
        for key, entries in device_data.items():
            for entry in entries:  # Use entries as is to maintain the original order
                sheet.append([key, entry['formatted_ts'], entry['value']])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename=telemetry_data.xlsx'
        workbook.save(response)
        return response

    # PDF Export
    elif export_format == "pdf":
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("Telemetry Data")

        y = 750
        pdf.drawString(50, y, "Telemetry Data")
        y -= 30

        # Write data and plot for each key in the telemetry data
        for key, entries in device_data.items():
            # Write data to the PDF
            pdf.drawString(50, y, f"Key: {key}")
            y -= 20
            for entry in entries:  # Use entries as is to maintain the original order
                pdf.drawString(70, y, f"Timestamp: {entry['formatted_ts']}, Value: {entry['value']}")
                y -= 20
                if y < 100:
                    pdf.showPage()
                    y = 750

            # Create a plot for each key in the telemetry data
            fig, ax = plt.subplots(figsize=(8, 6))

            # Extract timestamps and values as is
            timestamps = [entry['formatted_ts'] for entry in entries]
            values = [entry['value'] for entry in entries]

            ax.plot(timestamps, values, label=key)

            ax.set_title(f'Telemetry Data for {key}')
            ax.set_xlabel('Timestamp')
            ax.set_ylabel('Value')
            plt.xticks(rotation=45, ha='right')
            ax.legend()
            plt.tight_layout()

            # Save the plot to a byte buffer
            img_buffer = io.BytesIO()
            FigureCanvas(fig).print_png(img_buffer)
            img_buffer.seek(0)

            # Create a temporary file to save the image
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(img_buffer.getvalue())
                temp_file_path = temp_file.name

            # Add the image to the PDF
            if y < 400:  # Check if there is enough space for the image
                pdf.showPage()
                y = 750
            pdf.drawImage(temp_file_path, 50, y - 300, width=500, height=300)
            y -= 350  # Adjust y position for the next plot

            # Clean up the temporary file after use
            os.remove(temp_file_path)

            if y < 100:
                pdf.showPage()
                y = 750

        # Save the PDF
        pdf.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=telemetry_data.pdf'
        return response

    else:
        return HttpResponse("Unsupported export format.", status=400)
