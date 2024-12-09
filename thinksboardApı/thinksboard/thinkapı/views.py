import requests
import json
import io
import os
import tempfile
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from .forms import UserLogInForm, DevicesListForm
from datetime import datetime
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

BASEURL = "https://thingsboard.cloud/api"
LOGIN_URL = f"{BASEURL}/auth/login"
USER_URL = f"{BASEURL}/auth/user"


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


def devicePrefer(request):
    token = request.session.get('token')
    if not token:
        return redirect('login')

    if request.method == "POST":
        deviceform = DevicesListForm(request.POST)
        if deviceform.is_valid():
            device_key = deviceform.cleaned_data["device"]
            device_data = DEVICE_TELEMETRY.get(device_key)
            if not device_data:
                return render(request, "deviceInfo.html", {"error": "Invalid device selected!"})

            device_uuid = device_data["uuid"]
            telemetry_url = device_data["telemetry"]
            headers = {'Authorization': f'Bearer {token}'}

            # Cihaz bilgilerini al
            device_url = f"{BASEURL}/device/{device_uuid}"
            device_response = requests.get(device_url, headers=headers)

            # Telemetri bilgilerini al
            full_telemetry_url = f"{BASEURL}/plugins/telemetry/DEVICE/{device_uuid}/{telemetry_url}"
            telemetry_response = requests.get(full_telemetry_url, headers=headers)

            if device_response.status_code != 200 or telemetry_response.status_code != 200:
                return render(request, "deviceInfo.html", {
                    "error": f"Error fetching data! Device: {device_response.status_code}, "
                             f"Telemetry: {telemetry_response.status_code}"
                })

            device_info = device_response.json()
            telemetry_info = telemetry_response.json()

            # Telemetri geçmişini saklama
            telemetry_history = request.session.get('telemetry_history', {})

            # Her cihazın telemetri geçmişini ayrı bir anahtar altında sakla
            if device_uuid not in telemetry_history:
                telemetry_history[device_uuid] = {}
            request.session['device_uuid'] = device_uuid
            for key, entries in telemetry_info.items():
                if key not in telemetry_history[device_uuid]:
                    telemetry_history[device_uuid][key] = []

                for entry in entries:
                    # Format timestamp to human-readable time
                    timestamp = datetime.utcfromtimestamp(entry['ts'] / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
                    entry['formatted_ts'] = timestamp

                    # Eğer giriş zaten geçmişte yoksa ekle
                    if entry not in telemetry_history[device_uuid][key]:
                        telemetry_history[device_uuid][key].append(entry)

            # Telemetri geçmişini oturumda güncelle
            request.session['telemetry_history'] = telemetry_history

            # Grafik verilerini hazırlama
            charts_data = {}
            for key, entries in telemetry_history[device_uuid].items():
                chart_labels = [entry['formatted_ts'] for entry in entries]
                chart_data = [entry['value'] for entry in entries]
                charts_data[key] = {
                    "labels": chart_labels,
                    "data": chart_data
                }

            # charts_data'yı oturumda saklama
            request.session['charts_data'] = charts_data

            # Cihaz ve telemetri bilgisini gönder
            return render(request, "deviceİnformation.html", {
                "device_info": device_info,
                "telemetry_info": telemetry_info,
                "telemetry_history": telemetry_history[device_uuid],
                "charts_data": charts_data,
            })
        else:
            return render(request, "deviceInfo.html", {"error": "Invalid form submission!"})
    else:
        deviceform = DevicesListForm()
        return render(request, "deviceInfo.html", {"deviceform": deviceform})


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
    }
}

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
            # Sort entries by timestamp and value
            sorted_entries = sorted(entries, key=lambda x: (x['formatted_ts'], x['value']))
            for entry in sorted_entries:
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
            # Sort entries by timestamp and value
            sorted_entries = sorted(entries, key=lambda x: (x['formatted_ts'], x['value']))

            # Write sorted data to the PDF
            pdf.drawString(50, y, f"Key: {key}")
            y -= 20
            for entry in sorted_entries:
                pdf.drawString(70, y, f"Timestamp: {entry['formatted_ts']}, Value: {entry['value']}")
                y -= 20
                if y < 100:
                    pdf.showPage()
                    y = 750

            # Create a plot for each key in the telemetry data
            fig, ax = plt.subplots(figsize=(8, 6))

            # Extract sorted timestamps and values
            timestamps = [entry['formatted_ts'] for entry in sorted_entries]
            values = [entry['value'] for entry in sorted_entries]

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
